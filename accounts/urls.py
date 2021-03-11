from django.urls import path,include
from . views import index,products,customers,updateOrder,createOrder,deleteOrder,createCustomer,updateCustomer,deleteCustomer,loginPage,register,logoutPage
urlpatterns = [
    path('',index,name="index"),
    path('products/',products,name="products"),
    path('customer/<int:id>/',customers,name="customer"),
    path('update_order/<int:id>',updateOrder,name="update_order"),
    path('create_order/<int:id>',createOrder,name="create_order"),
    path('delete_order/<int:id>',deleteOrder,name="delete_order"),
    path('create_customer/',createCustomer,name="create_customer"),
    path('update_customer/<int:id>',updateCustomer,name="update_customer"),
    path('delete_customer/<int:id>',deleteCustomer,name="delete_customer"),
    path('login/',loginPage,name="login"),
    path('register/',register,name="register"),
    path('logout/',logoutPage,name="logout")
    
]