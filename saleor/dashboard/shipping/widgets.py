from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from measurement.measures import Mass


class WeightInput(forms.TextInput):
    template = 'dashboard/shipping/weight_widget.html'
    input_type = 'number'

    def __init__(
            self, unit_choice=settings.DEFAULT_WEIGHT_UNITS[0][0],
            *args, **kwargs):
        self.unit_choice = unit_choice
        super().__init__(*args, **kwargs)

    def format_value(self, value):
        if isinstance(value, Mass):
            return value.value
        return value

    def render(self, name, value, attrs=None):
        widget = super().render(name, value, attrs=attrs)
        return render_to_string(self.template, {
            'widget': widget, 'value': value, 'unit': self.unit_choice})
