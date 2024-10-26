from django.views import generic
from .models import Employ


class IndexView(generic.ListView):
    model = Employ