from django.urls import path
from . import views

urlpatterns = [
    path('', views.base),
    path('login_action/', views.login_action),
    path('home/', views.home),
    # path('home/upload_file/', views.upload_file),
    # path('home/upload_file/Analysis', views.after_up_analysis),
    path('Analysis/', views.Analysis),
    path('log_out/', views.log_out),
    path('feedback/', views.feedback),
    path('preference/', views.preference, name='preference'),
    path('product_analysis', views.product_analysis, name='product_analysis'),
    path('product_analysis/<str:name>/', views.product_analysis, name='product_analysis'),
    path('store_analysis',views.store_analysis,name='store_analysis'),
    path('store_analysis/<str:name>/', views.store_analysis, name='store_analysis'),
]
