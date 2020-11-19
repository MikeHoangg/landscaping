from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()


def get_season(month):
    if month in [12, 1, 2]:
        return _('winter')
    if month in [3, 4, 5]:
        return _('spring')
    if month in [6, 7, 8]:
        return _('summer')
    if month in [9, 10, 11]:
        return _('autumn')


@register.filter
def workers_per_action(actions_list):
    res = dict()
    for action in actions_list:
        season = get_season(action.date.month)
        district_type = action.consultation.district.district_type

        season_data = res.get(season, {})
        district_data = season_data.get(district_type, {})
        action_data = district_data.get(action.description, {'min': 1, 'max': 0})

        workers = action.workers.count()
        if workers < action_data['min']:
            action_data['min'] = workers
        if workers > action_data['max']:
            action_data['max'] = workers

        district_data.update({
            action.description: action_data
        })
        season_data.update({
            district_type: district_data
        })
        res.update({
            season: season_data
        })
    return res
