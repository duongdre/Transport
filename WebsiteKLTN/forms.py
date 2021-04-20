from django import forms

class DateInput(forms.DateInput):
    input_type = "date"

class ExampleForm(forms.Form):
    my_date_field = forms.DateField()