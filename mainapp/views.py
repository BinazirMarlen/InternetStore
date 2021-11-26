from django.db.models.base import Model
from django.shortcuts import render
from django .views.generic import DetailView
from mainapp.models import *
from django .views.generic import DeleteView

from mainapp.models import SmartPhone, Notebook

def test_view(request):
    return render(request,'base.html',{})


class ProductDetailView(DetailView):

    CT_MODEL_CLASS={
        'notebook': Notebook,
        'smartphone': SmartPhone
    }

    def dispatch(self, request, *args, **kwargs):
        self.model=self.CT_MODEL_CLASS[kwargs['ct_model']]
        self.queryset=self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)
    # model=Model
    # queryset=Model.objects.all()
    context_object_name='product'
    template_name='product_detail.html'
    slug_url_kwarg='slug'
