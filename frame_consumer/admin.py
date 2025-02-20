from django.contrib import admin

from frame_consumer.models import (
    ProcessCategory,
    ProcessExecutable,
    ProcessWindow,
    KnownHost,
    ProcessCategoryMapping,
    ProcessSubCategory,
    WindowSubCategoryMapping,
    ProcessWindowSnapshot,
)


# Register your models here.


@admin.register(ProcessCategory)
class ProcessCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessExecutable)
class ProcessExecutableAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessWindow)
class ProcessWindowAdmin(admin.ModelAdmin):
    pass


@admin.register(KnownHost)
class KnownHostAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessCategoryMapping)
class ModelNameAdmin(admin.ModelAdmin):
    pass


@admin.register(WindowSubCategoryMapping)
class WindowCategoryMappingAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessSubCategory)
class ModelNameAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessWindowSnapshot)
class ProcessWindowSnapshotAdmin(admin.ModelAdmin):
    pass
