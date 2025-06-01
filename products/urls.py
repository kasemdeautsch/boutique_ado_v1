
#from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'), # adding a trailing slash '/' in the end of the url here as that's just good practice and I've accidentally left it off.
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product')
               
]
# adding<int:> sprcifying it should be integer, 
# otherweise navigating to products/add will interpret the string 'add' as a <product_id> 
# which will cause that view to throw an error'
# This happens because django will always use the first URL it finds a matching pattern for.
# And in this case unless we specify that product id is an integer,
# django doesn't know the difference between a product number and a string like, add.