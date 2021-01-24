#!/usr/bin/env python3

"""Trigger manage.py ."""

import os
import sys
from django.core.management import execute_from_command_line

os.environ["DJANGO_SETTINGS_MODULE"] = f"proj.settings"
execute_from_command_line(sys.argv)
