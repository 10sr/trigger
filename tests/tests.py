import unittest

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from trigger import models


class TestFailure(TestCase):
    @unittest.skip("demonstrating failing and skipping")
    def test_failure(self):
        self.assertEqual(True, False)
        return
