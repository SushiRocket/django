from django.views import generic


class InexView(generic.TemplateView):
    template_name = 'notes/post_list.html'