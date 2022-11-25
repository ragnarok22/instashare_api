from django.contrib import admin

from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("title", "creator", "size")
    search_fields = ("title",)

    @admin.display(description="Size")
    def size(self, obj):
        return obj.size()
