from django.urls import path
from customer import views
urlpatterns=[
    path("home",views.CustomerIndex.as_view(),name="custhome"),
    path('accounts/register',views.SignupView.as_view(),name="signup"),
    path('accounts/login',views.SignInView.as_view(),name='signin'),
    path('accounts/logout',views.signout,name='signout'),
    path('accounts/password/reset',views.PasswordResetView.as_view(),name='passwordreset'),
    path("carts/items/add/<int:id>",views.add_to_carts,name="addtocart"),
    path("carts/all",views.ViewMycart.as_view(),name='viewmycart'),
    path("carts/remove/<int:id>",views.remove_from_carts,name="removeitem"),
]