import django.forms as forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.models import Consultation, District


class ConsultationForm(forms.ModelForm):
    def clean_residents(self):
        residents = self.cleaned_data.get('residents', ())
        district = self.cleaned_data.get('district', None)

        invalid_residents = [str(resident) for resident in residents if resident.district != district]
        if invalid_residents:
            raise ValidationError(
                _('Invalid values: %(values)s. Wrong district'),
                params={'values': ', '.join(invalid_residents)},
            )
        return residents

    class Meta:
        model = Consultation
        fields = '__all__'


class ActionsBySeasonForm(forms.Form):
    SEASONS = (
        ([12, 1, 2], _('winter')),
        ([3, 4, 5], _('spring')),
        ([6, 7, 8], _('summer')),
        ([9, 10, 11], _('autumn')),
    )

    season = forms.MultipleChoiceField(choices=SEASONS, required=False, widget=forms.CheckboxSelectMultiple())
    district_type = forms.MultipleChoiceField(choices=District.DISTRICT_TYPE, required=False,
                                              widget=forms.CheckboxSelectMultiple())
