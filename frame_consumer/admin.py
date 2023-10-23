from django.contrib import admin
from models import ProcessCategory, ProcessExecutable, ProcessWindow, KnownHost
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