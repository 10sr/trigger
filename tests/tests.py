import unittest

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from trigger import models


class TestFailure(TestCase):  # type: ignore   # disallow_subclassing_any
    @unittest.skip("demonstrating failing and skipping")
    def test_failure(self) -> None:
        self.assertEqual(True, False)
        return
