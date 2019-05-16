#!/usr/bin/env python3

"""Trigger manage.py ."""

import os
import sys
from django.core.management import execute_from_command_line

# TODO: How to check if going to run tests?
if sys.argv[1] == "test":
    os.environ["TRIGGER_ENV"] = "test"
    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"
else:
    os.environ["DJANGO_SETTINGS_MODULE"] = f"proj.settings"

execute_from_command_line(sys.argv)
