from django.urls import path,include
from . views import index,products,customers,updateOrder,createOrder,deleteOrder,createCustomer,updateCustomer,deleteCustomer,loginPage,register,logoutPage,userPage,profilePage
from django.contrib.auth import views as auth_views
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
    path('logout/',logoutPage,name="logout"),
    path('user/',userPage,name="user"),
    path('profile_page/',profilePage,name="profile_page"),   
    path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),
    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
]