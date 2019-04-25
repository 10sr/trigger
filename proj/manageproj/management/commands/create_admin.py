import os

from django.contrib.auth.management.commands import createsuperuser

# from django.core.management.base import BaseCommand, CommandError

# https://stackoverflow.com/questions/6244382/how-to-automate-createsuperuser-on-django
# https://jumpyoshim.hatenablog.com/entry/how-to-automate-createsuperuser-on-django


class Command(createsuperuser.Command):
    help = "Create admin user"

    # def add_arguments(self, parser):
    #     return

    def handle(self, *args, **kargs):
        # TODO: Take from kargs?
        username = "admin"
        password = os.environ.get("ADMIN_PASSWORD", "")
        email = kargs.get("email")
        database = kargs.get("database")

        assert password, "Aborting: ADMIN_PASSWORD is empty"

        mng = self.UserModel._default_manager.db_manager(database)
        try:
            user = mng.get(username=username)
            self.stdout.write(f"User {username} already exists.")
            self.stdout.write(f"Updating password")
            user.set_password(password)
            user.save()
        except mng.model.DoesNotExist:
            self.UserModel._default_manager.db_manager(database).create_superuser(
                username=username, password=password, email=email
            )

        return
