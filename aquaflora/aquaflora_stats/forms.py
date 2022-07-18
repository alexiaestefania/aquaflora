from django import forms
from functools import partial

DateInput = partial(forms.DateInput, {'class': 'datepicker'}, format="%m/%d/%Y")

class DatepickerForm(forms.Form):
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())