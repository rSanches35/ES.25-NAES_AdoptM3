from django.views.generic import TemplateView

# Create your views here.
class IndexView(TemplateView):
    
    template_name = "pages/index.html"

class AboutView(TemplateView):
    
    template_name = "pages/about.html"