from django.views.generic.base import TemplateView

"""На самом деле я просто забыл о том, что остался в этом скрипте мусор.
Все данные забиты в соответствующие страницы. Статичные страницы — они и
должны быть статичными. Спасибо)"""


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'
