from django.urls import path
from auth import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home, name='home'),
    path('signup',views.signup, name='signup'),
    path('signin',views.signin, name='signin'),
    path('signout',views.signout, name='signout'),
    path('activate/<uidb64>/<token>',views.activate, name='activate'),
    path('forgot',views.forgot_password, name='forgot'),
    path('reset/<uidb64>/<token>',views.password_reset, name='reset'),
    # path('password_reset',auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done',auth_views.PasswordResetDoneView.as_view(), name='password_reset_done' ),
    # path('password_reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm' ),
    # path('reset/done',auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete' ),

]