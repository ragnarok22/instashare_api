import os

from config.celery import app

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import tasks
from .models import File, CompressedFile
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
        last_compress = (
            CompressedFile.objects.filter(creator=request.user)
            .order_by("-updated_at")
            .first()
        )

        # Make sure the user only have a compressed file
        if last_compress:
            if last_compress.is_finish:
                return Response(
                    {
                        "message": "Already has a compressed file",
                        "url": last_compress.file.url,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                {"message": "Processing the file"}, status=status.HTTP_400_BAD_REQUEST
            )

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
                last_compress.file = result.get()
                last_compress.save()
                return Response(
                    {"message": result.status, "url": last_compress.file.url},
                    status=status.HTTP_200_OK,
                )

            return Response({"message": result.status}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "The compressed file doesn't exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, url_path="compress/force")
    def force_compress(self, request, *args, **kwargs):
        last_compress = (
            CompressedFile.objects.filter(creator=request.user)
            .order_by("-updated_at")
            .first()
        )

        if last_compress:
            # remove the file
            if last_compress.is_finish:
                os.unlink(last_compress.file.path)
            else:
                # stop the process
                app.control.revoke(last_compress.task_id, terminate=True)
            last_compress.delete()

        result = tasks.compress_all_user_files.delay(request.user.id)
        CompressedFile(creator=request.user, task_id=result.id).save()
        return Response({"message": "start processing"}, status=status.HTTP_200_OK)
