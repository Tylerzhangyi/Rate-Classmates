from django.apps import AppConfig
from django.db.backends.signals import connection_created


def _enable_sqlite_pragmas(sender, connection, **kwargs):
    if connection.vendor != "sqlite":
        return
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("PRAGMA journal_mode = WAL;")


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self) -> None:
        connection_created.connect(_enable_sqlite_pragmas, dispatch_uid="core.enable_sqlite_pragmas")

