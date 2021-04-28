import datetime
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from catalog.models import BookInstance, Author

#The below two forms are equivalent, with some difference regd how to refer to the input fields.

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text='Enter a date within the next 4 weeks (default 3 weeks).')

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date entered - renewal date cannot be in the past'))
        
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date entered - renewal date cannot be more than 4 weeks away.'))
        
        return data

class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['due_back']
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date entered - renewal date cannot be in the past'))
        
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date entered - renewal date cannot be more than 4 weeks away.'))

        return data
    
    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('Renewal date')}
        help_texts = {'due_back': _('Enter a date within the next 4 weeks (default 3 weeks).')}
 