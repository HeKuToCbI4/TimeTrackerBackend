from django.db import models


# Create your models here.
class ProcessCategory(models.Model):
    # id->category (string)
    # automatically incremented ID added by default.
    # Category name (games | office | programming | work etc.
    category_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f"{self.category_name}"


class ProcessExecutable(models.Model):
    # id | executable name | category | path to executable
    # PK, id just in case we need to store LOTS of executables.
    id = models.BigAutoField(primary_key=True)
    # short version, something like wow.exe or clion.exe
    executable_name = models.CharField(max_length=128, unique=True)
    # full path to executable.
    executable_path = models.CharField(max_length=512)
    executable_category = models.ForeignKey(
        ProcessCategory, on_delete=models.SET_NULL, null=True
    )

    class Meta(object):
        constraints = [
            models.UniqueConstraint(
                fields=["executable_name", "executable_path"],
                name="executable name|path unique check.",
            )
        ]

    def __str__(self):
        return f"{self.executable_name} | {self.executable_category}"


class ProcessWindow(models.Model):
    # executable id | name | utc since | utc to
    id = models.BigAutoField(primary_key=True)
    process_window_title = models.CharField(max_length=512, unique=True)
    executable = models.ForeignKey(ProcessExecutable, on_delete=models.CASCADE)
    utc_from = models.DateTimeField()
    utc_to = models.DateTimeField()

    def __str__(self):
        return f"{self.process_window_title} | {self.executable} | {self.utc_from} - {self.utc_to}"


class KnownHost(models.Model):
    # remote_host
    # port
    # actively_monitored
    host = models.CharField(max_length=64)
    port = models.PositiveSmallIntegerField()
    is_monitored = models.BooleanField(default=False)
    status = models.CharField(max_length=128, default="Unknown")

    class Meta(object):
        constraints = [
            models.UniqueConstraint(
                fields=["host", "port"], name="Host|Port unique check."
            )
        ]

    def __str__(self):
        return f"{self.host}:{self.port} | state: {self.is_monitored}"
