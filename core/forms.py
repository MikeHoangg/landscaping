import django.forms as forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.models import Consultation


class ConsultationForm(forms.ModelForm):
    def clean_residents(self):
        residents = self.cleaned_data.get('residents', ())
        district = self.cleaned_data.get('district', None)

        invalid_residents = [resident for resident in residents if resident.district != district]
        if invalid_residents:
            raise ValidationError(
                _('Invalid values: %(values)s. Wrong district'),
                params={'values': ', '.join(invalid_residents)},
            )
        return residents

    class Meta:
        model = Consultation
        fields = '__all__'
