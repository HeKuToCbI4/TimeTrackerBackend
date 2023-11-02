from django.db import models


# Create your models here.
class ProcessCategory(models.Model):
    # id->category (string)
    # automatically incremented ID added by default.
    # Category name (games | office | programming | work etc.
    category_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f"{self.category_name}"


class KnownHost(models.Model):
    # remote_host
    # port
    # actively_monitored
    address = models.CharField(max_length=64)
    port = models.PositiveSmallIntegerField()
    consumer_id = models.CharField(max_length=64)
    is_monitored = models.BooleanField(default=False)
    status = models.CharField(max_length=128, default="Unknown")
    auto_start_monitor = models.BooleanField(default=False)

    class Meta(object):
        unique_together = ("address", "port")
        constraints = [
            models.UniqueConstraint(
                fields=["address", "port"], name="Host|Port unique check."
            )
        ]

    def __str__(self):
        return (
            f"{self.address}:{self.port}\n"
            f"consumer_id:{self.consumer_id}\n"
            f"automatic {self.auto_start_monitor}\n"
            f"monitored: {self.is_monitored}\n"
            f"status: {self.status}"
        )


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
    host = models.ForeignKey(KnownHost, on_delete=models.CASCADE)

    class Meta(object):
        unique_together = ("executable_name", "executable_path")
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
    process_window_title = models.CharField(max_length=512, unique=False)
    utc_from = models.DateTimeField()
    utc_to = models.DateTimeField()
    executable = models.ForeignKey(ProcessExecutable, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.process_window_title} | {self.executable} | {self.utc_from} - {self.utc_to}"
