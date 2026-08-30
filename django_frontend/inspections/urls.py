from django.urls import path
from . import views


urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    path('upload/', views.upload_product, name='upload_product'),

    path(
        'inspection/<int:inspection_id>/',
        views.inspection_detail,
        name='inspection_detail'
    ),

]