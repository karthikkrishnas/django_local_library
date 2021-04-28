import datetime

from django.test import SimpleTestCase, TestCase #SimpleTestCase doesnt use database or test client.
from django.utils import timezone

from catalog.forms import RenewBookForm

# Create your tests here.

# The below code works perfectly even if SimpleTestCase is just changed to TestCase in the class inheritance
class RenewBookFormTest(SimpleTestCase):
    def test_renew_form_date_field_label(self):
        form = RenewBookForm()
        self.assertTrue(form.fields['renewal_date'].label is None or form.fields['renewal_date'].label == 'renewal date')

    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        self.assertEqual(form.fields['renewal_date'].help_text, 'Enter a date within the next 4 weeks (default 3 weeks).')

    def test_renew_form_date_in_past(self):
        yesterday = datetime.date.today() + datetime.timedelta(days=-1)
        form = RenewBookForm(data={'renewal_date': yesterday})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        late_date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': late_date})
        self.assertFalse(form.is_valid())
    
    def test_renew_form_date_today(self):
        today = datetime.date.today()
        form = RenewBookForm(data={'renewal_date':today})
        self.assertTrue(form.is_valid())
    
    def test_renew_form_date_max(self):
        max_date = datetime.date.today() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date':max_date})
        self.assertTrue(form.is_valid())



