from django.db import models
from django.utils.translation import gettext_lazy as _


class District(models.Model):
    INDUSTRIAL = 'industrial'
    RESIDENTIAL = 'residential'
    MIXED = 'mixed'

    DISTRICT_TYPE = (
        (INDUSTRIAL, _('industrial')),
        (RESIDENTIAL, _('residential')),
        (MIXED, _('mixed'))
    )
    name = models.CharField(_('name'), max_length=64, unique=True)
    district_type = models.CharField(max_length=32, choices=DISTRICT_TYPE, verbose_name=_('type'))
    description = models.TextField(verbose_name=_('description'), blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.district_type}'


class Person(models.Model):
    first_name = models.CharField(_('first name'), max_length=32)
    last_name = models.CharField(_('last name'), max_length=128, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        if self.last_name:
            return f'{self._meta.verbose_name} - {self.first_name} {self.last_name}'
        return f'{self._meta.verbose_name} - {self.first_name}'


class Manager(Person):
    pass


class Worker(Person):
    pass


class Resident(Person):
    district = models.ForeignKey(District, verbose_name=_('district'), on_delete=models.CASCADE)

    def __str__(self):
        if self.last_name:
            return f'{self._meta.verbose_name} of {self.district} - {self.first_name} {self.last_name}'
        return f'{self._meta.verbose_name} of {self.district} - {self.first_name}'
class Consultation(models.Model):
    date = models.DateTimeField(verbose_name=_('date'))
    description = models.TextField(verbose_name=_('description'))
    district = models.ForeignKey(District, verbose_name=_('district'), on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, verbose_name=_('manager'), on_delete=models.CASCADE)
    residents = models.ManyToManyField(Resident, _('residents'), blank=True)

    def __str__(self):
        return f'{self._meta.verbose_name} #{self.id} - {self.district} {self.date}'


class Action(models.Model):
    description = models.TextField(verbose_name=_('description'))
    date = models.DateTimeField(verbose_name=_('date'))
    consultation = models.ForeignKey(Consultation, verbose_name=_('consultation'), on_delete=models.CASCADE)
    workers = models.ManyToManyField(Worker, verbose_name=_('workers'), blank=True)

    def __str__(self):
        return f'{self._meta.verbose_name} #{self.id} - {self.consultation.district} {self.date}'


class Tool(models.Model):
    name = models.CharField(_('name'), max_length=64)
    description = models.TextField(verbose_name=_('description'), blank=True, null=True)
    worker = models.ForeignKey(Worker, verbose_name=_('worker'), blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    name = models.CharField(_('name'), max_length=64)
    description = models.TextField(verbose_name=_('description'), blank=True, null=True)
    workers = models.ManyToManyField(Worker, verbose_name=_('workers'), blank=True)

    def __str__(self):
        return self.name
