from django import forms

from .models import Temp_chart, Komax, KomaxTask, Harness, HarnessAmount
from django_select2.forms import Select2MultipleWidget, Select2Widget
from django.utils.translation import gettext_lazy as _


from .models import Harness, HarnessChart, Komax, KomaxTask
from django_select2.forms import Select2MultipleWidget, Select2Widget
from django.utils.translation import gettext_lazy as _

class KomaxEditForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Komax.STATUS_CHOICES, widget=Select2Widget)
    marking = forms.ChoiceField(choices=Komax.MARKING_CHOICES, widget=Select2Widget)
    pairing = forms.ChoiceField(choices=Komax.PAIRING_CHOICES, widget=Select2Widget)

    class Meta:
        model = Komax
        fields = (
            'status',
            'marking',
            'pairing'
        )


class KomaxCreateForm(forms.ModelForm):
    number = forms.IntegerField()
    status = forms.ChoiceField(choices=Komax.STATUS_CHOICES, widget=Select2Widget)
    marking = forms.ChoiceField(choices=Komax.MARKING_CHOICES, widget=Select2Widget)
    pairing = forms.ChoiceField(choices=Komax.PAIRING_CHOICES, widget=Select2Widget)

    class Meta:
        model = Komax
        fields = (
            'number',
            'status',
            'marking',
            'pairing'
        )

class KomaxEditForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Komax.STATUS_CHOICES, widget=Select2Widget)
    marking = forms.ChoiceField(choices=Komax.MARKING_CHOICES, widget=Select2Widget)
    pairing = forms.ChoiceField(choices=Komax.PAIRING_CHOICES, widget=Select2Widget)

    class Meta:
        model = Komax
        fields = (
            'status',
            'marking',
            'pairing'
        )

class Amount_tasks_form(forms.ModelForm):
    class Meta:
        model = HarnessAmount
        fields = (
            'harness',
            'amount',
        )

class KomaxTaskSetupForm(forms.ModelForm):
    task_name = forms.IntegerField(
        label=_('Task name')
    )
    harnesses = forms.ModelMultipleChoiceField(queryset=Harness.objects.all(),
                                               required=True,
                                               widget=Select2MultipleWidget,
                                               label=_('Harnesses')
                                               )
    komaxes = forms.ModelMultipleChoiceField(queryset=Komax.objects.all(),
                                             required=True,
                                             widget=Select2MultipleWidget,
                                             label=_('Komaxes')
                                             )
    shift = forms.IntegerField(
        label=_('Shift')
    )

    class Meta:
        model = KomaxTask
        fields = (
            'task_name',
            'shift',
            'harnesses',
            'komaxes'
        )

