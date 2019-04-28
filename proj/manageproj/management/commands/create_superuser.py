import os

from typing import List, Mapping

from django.contrib.auth.management.commands import createsuperuser
from django.core.management.base import BaseCommand, CommandError

# https://stackoverflow.com/questions/6244382/how-to-automate-createsuperuser-on-django
# https://jumpyoshim.hatenablog.com/entry/how-to-automate-createsuperuser-on-django


class Command(createsuperuser.Command):  # type: ignore   # disallow_subclassing_any
    help = "Create admin user"

    # def add_arguments(self, parser):
    #     return

    def handle(self, *args: List[str], **kargs: Mapping[str, str]) -> None:
        username = kargs.get("username") or "admin"
        password = os.environ.get("SUPERUSER_PASSWORD", "")
        email = kargs.get("email")
        database = kargs.get("database")

        if not password:
            raise CommandError("Aborting: SUPERUSER_PASSWORD is empty")

        mgr = self.UserModel._default_manager.db_manager(database)
        user = mgr.filter(username=username).first()
        if user:
            self.stdout.write(f"User {username} already exists.")
            self.stdout.write(f"Updating password")
            user.set_password(password)
            user.save()
        else:
            self.stdout.write(f"Creating user {username}")
            mgr.create_superuser(username=username, password=password, email=email)

        return
