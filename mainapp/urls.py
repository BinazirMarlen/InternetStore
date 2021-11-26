
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ProductDetailView, test_view
urlpatterns = [
    path('', test_view, name='base'),
    path('product/<str:ct_model>/<str:slug>/', ProductDetailView.as_view() , name='product_detail')
]


