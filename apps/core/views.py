from django.views import generic


class IndexView(generic.RedirectView):
    url = "/docs"
    permanent = False
