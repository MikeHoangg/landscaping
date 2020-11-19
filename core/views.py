import json

from django.views.generic import ListView, FormView

from core import forms, models


class ActionsBySeasonsView(ListView, FormView):
    form_class = forms.ActionsBySeasonForm
    template_name = 'actions_by_seasons.html'
    model = models.Action

    def get_queryset(self):
        queryset = super(ActionsBySeasonsView, self).get_queryset()
        if season := self.request.GET.getlist('season', []):
            queryset = queryset.filter(date__month__in={month for s in season for month in json.loads(s)})
        if district_type := self.request.GET.getlist('district_type', []):
            queryset = queryset.filter(consultation__district__district_type__in=district_type)
        return queryset

    def get_form_kwargs(self):
        kwargs = super(ActionsBySeasonsView, self).get_form_kwargs()
        kwargs.update({
            'data': self.request.GET
        })
        return kwargs
