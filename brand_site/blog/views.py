from django.views.generic import *


class Blog(TemplateView):
    template_name = "blog.html"
