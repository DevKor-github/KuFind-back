from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    # path('signup/', views.CreateUserView.as_view(), name='create'),
    # path('login/', views.CreateTokenView.as_view(), name='token'),
    # path('me/', views.ManageUserView.as_view(), name='me'),

    path('signup/', views.Registration.as_view()),
    path('login/', views.Login.as_view()),
#
# # 회원가입
#     path('rest-auth/registration', RegisterView.as_view(), name='rest_register'),
#     #
#     path('accounts/', include('allauth.urls')),
# # 이메일 관련 필요
#     path('accounts/allauth/', include('allauth.urls')),
#     # 유효한 이메일이 유저에게 전달
#     re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
#     # 유저가 클릭한 이메일(=링크) 확인
#     re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
]