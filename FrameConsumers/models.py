from django.db import models


# Create your models here.
class ProcessCategory(models.Model):
    # id->category (string)
    # automatically incremented ID added by default.
    # Category name (games | office | programming | work etc.
    category_name = models.CharField(max_length=128, unique=True)


class ProcessExecutable(models.Model):
    # id | executable name | category | path to executable
    # PK, id just in case we need to store LOTS of executables.
    id = models.BigAutoField(primary_key=True)
    # short version, something like wow.exe or clion.exe
    executable_name = models.CharField(max_length=128, unique=True)
    # full path to executable.
    executable_path = models.CharField(max_length=512)
    executable_category = models.ForeignKey(ProcessCategory, on_delete=models.SET_NULL)


class ProcessWindow(models.Model):
    # executable id | name | utc since | utc to
    id = models.BigAutoField(primary_key=True)
    process_window_title = models.CharField(max_length=512, unique=True)
    executable = models.ForeignKey(ProcessExecutable, on_delete=models.CASCADE)
    utc_since = models.DateTimeField()
    utc_to = models.DateTimeField()


class KnownHost(models.Model):
    # host
    # port
    # actively_monitored
    host = models.CharField(max_length=64)
    port = models.PositiveSmallIntegerField()
    is_monitored = models.BooleanField()
