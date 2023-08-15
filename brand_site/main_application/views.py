from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = 'main_page.html'


class CatalogPageView(TemplateView):
    template_name = 'services.html'


class BlogPageView(TemplateView):
    template_name = 'cases.html'


class ContactsPageView(TemplateView):
    template_name = 'contacts.html'


class BrandsPageView(TemplateView):
    template_name = 'brands.html'


class CosmeticsPageView(TemplateView):
    template_name = 'cosmetics.html'


class DiscountsPageView(TemplateView):
    template_name = 'discounts.html'