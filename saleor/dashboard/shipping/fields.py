from django import forms
from django.conf import settings
from measurement.measures import Mass

from .widgets import WeightInput


class WeightField(forms.DecimalField):
    def __init__(
            self, unit_choice=settings.DEFAULT_WEIGHT_UNITS[0][0],
            widget=WeightInput, *args, **kwargs):
        self.unit_choice = unit_choice
        if isinstance(widget, type):
            widget = widget(
                unit_choice=self.unit_choice,
                attrs={'type': 'number', 'step': 'any'})
        super().__init__(*args, widget=widget, **kwargs)

    def to_python(self, value):
        value = super().to_python(value)
        if value is None:
            return value
        return Mass(**{self.unit_choice: value})

    def validate(self, mass):
        if mass in self.empty_values:
            super().validate(mass)
            return mass
        elif not isinstance(mass, Mass):
            raise Exception('%r is not a valid mass.' % (mass,))
        elif mass.unit != self.unit_choice:
            raise forms.ValidationError(
                'Invalid unit_choice: %r (expected %r).' % (
                    mass.unit, self.unit_choice))
        elif mass.value < 0:
            raise forms.ValidationError(
                'Weight should be larger or equal 0 %(unit)s.' % {
                    'unit': self.unit_choice})

    def clean(self, value):
        value = self.to_python(value)
        self.validate(value)
        return value
