from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import File, CompressedFile
from . import tasks
from .serializers import FileSerializer


class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return File.objects.filter(creator=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=False)
    def compress(self, request, *args, **kwargs):
        result = tasks.compress_all_user_files.delay(request.user.id)
        CompressedFile(creator=request.user, task_id=result.id).save()
        return Response({"message": "start processing"}, status=status.HTTP_200_OK)

    @action(detail=False, url_path="compress/check")
    def check_compress(self, request, *args, **kwargs):
        last_compress = (
            CompressedFile.objects.filter(creator=request.user)
            .order_by("-updated_at")
            .first()
        )

        if last_compress:
            result = tasks.compress_all_user_files.AsyncResult(last_compress.task_id)

            if result.status == "SUCCESS":
                last_compress.is_finish = True
                last_compress.save()
            return Response({"message": result.status}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "The compressed file doesn't exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
