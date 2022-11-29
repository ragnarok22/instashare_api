from django.contrib import admin

from .models import File, CompressedFile


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("title", "creator", "size")
    search_fields = ("title",)

    @admin.display(description="Size")
    def size(self, obj):
        return obj.size()


@admin.register(CompressedFile)
class CompressedFile(admin.ModelAdmin):
    list_display = ("task_id", "creator", "created_at", "updated_at")
    search_fields = ("task_id",)
