from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
     path('get_safaricom_token/', views.get_safaricom_token_view, name='get_safaricom_token'),
    path('initiate_mpesa_payment/', views.initiate_mpesa_payment_view, name='initiate_mpesa_payment'),
    

]