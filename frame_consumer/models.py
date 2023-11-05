from django.db import models


# Create your models here.
class ProcessCategory(models.Model):
    # id->category (string)
    # automatically incremented ID added by default.
    # Category name (games | office | programming | work etc.
    category_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f"{self.category_name}"


class ProcessSubCategory(models.Model):
    # id->category (string)
    # automatically incremented ID added by default.
    # SubCategory name (games | office | programming | work etc.
    subcategory_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f"{self.subcategory_name}"


class ProcessCategoryMapping(models.Model):
    """
    Map between process executable name and category. Kind of static one.
    map clion.exe to development.
    """

    executable_name = models.CharField(max_length=128, unique=True)
    category = models.ManyToManyField(ProcessCategory, related_name="executable_names")


class WindowCategoryMapping(models.Model):
    """
    Map between window title part and subcategory. Kind of static one.
    for example map youtube to entertainment.
    """

    pattern = models.CharField(max_length=256, unique=True)
    category = models.ManyToManyField(ProcessSubCategory, related_name="title_patterns")


class KnownHost(models.Model):
    # remote_host
    # port
    # actively_monitored
    address = models.CharField(max_length=64)
    port = models.PositiveSmallIntegerField()
    consumer_id = models.CharField(max_length=64)
    is_monitored = models.BooleanField(default=False)
    status = models.CharField(max_length=128, default="Unknown", blank=True)
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
    executable_category = models.ManyToManyField(
        ProcessCategory, related_name="processes"
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


# Dispatch this thing.
# Make this separate window - window data. The window itself should refer executable, have title and subcategory.
# Save storage :)
class ProcessWindow(models.Model):
    # executable id | name | utc since | utc to
    id = models.BigAutoField(primary_key=True)
    process_window_title = models.CharField(max_length=512, unique=False)
    executable = models.ForeignKey(ProcessExecutable, on_delete=models.CASCADE)
    process_subcategory = models.ManyToManyField(
        ProcessSubCategory, related_name="process_windows"
    )

    class Meta(object):
        unique_together = ("process_window_title", "executable")
        constraints = [
            models.UniqueConstraint(
                fields=["process_window_title", "executable"],
                name="window_title-process unique constraint",
            )
        ]

    def __str__(self):
        return f"{self.process_window_title} | {self.executable}"


class ProcessWindowSnapshot(models.Model):
    id = models.BigAutoField(primary_key=True)
    utc_from = models.DateTimeField()
    utc_to = models.DateTimeField()
    process_window = models.ForeignKey(ProcessWindow, on_delete=models.CASCADE)

    def __str__(self):
        return f"Snapshot of {self.process_window} {self.utc_from} {self.utc_to}"
