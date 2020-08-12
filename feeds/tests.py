from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from io import StringIO

from .forms import ItemAdminForm


class GrabFeedsTests(TestCase):
    def test_command_output(self):
        with StringIO() as out:
            call_command(
                "grabfeeds", "https://www.feedforall.com/sample.xml", stdout=out)
            self.assertIn(
                "Successfully grab items with URL: "
                "https://www.feedforall.com/sample.xml", out.getvalue())

    def test_empty_url(self):
        with self.assertRaisesMessage(CommandError, "URL should not be empty"):
            call_command("grabfeeds", "")

    def test_invalid_url(self):
        with StringIO() as out:
            call_command("grabfeeds", "abc", stderr=out)
            self.assertIn("Invalid URL: abc", out.getvalue())

    def test_non_parsable_url(self):
        with StringIO() as out:
            call_command("grabfeeds", "https://example.com", stderr=out)
            self.assertIn(
                "Cannot parse the URL: https://example.com", out.getvalue())


class ItemAdminFormTests(TestCase):
    def test_valid_form(self):
        form_data = {"title": "Test title",
                     "description": "Test description",
                     "link": "https://www.example.com",
                     "comments": "https://www.example.com",
                     "guid": 0}
        form = ItemAdminForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form_data = {}
        form = ItemAdminForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_missing_required_value(self):
        form_data = {"description": "Test description"}
        form = ItemAdminForm(data=form_data)
        self.assertEqual(form.errors["title"], ["This field is required."])
