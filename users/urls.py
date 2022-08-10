
from django.contrib import admin
from django.urls import path,include
from .views import (register,
login,contact,profile,basic,regular,premium,standard,
depositplans,confirm_trade,WithdrawView,uploadEvidence,
transactions,history,settings,my_profile,game1
)

urlpatterns = [
 path('accounts/sign_up/', register,name ='register'),
 path('accounts/sign_up/<str:ref>/', register),
 path('accounts/login/', login,name ='login'),
 path('contact/us/', contact,name ='contact'),
 path('profile/me/', profile,name ='profile'),
 path('profile/me/plans/', depositplans,name ='deposit_plans'),
 path('profile/me/plans/regular/', regular,name ='regular'),
 path('profile/me/plans/standard/', standard,name ='standard'),
 path('profile/me/plans/basic/', basic,name ='basic'),
 path('profile/me/plans/premium/', premium,name ='premium'),
 path('profile/me/plans/<int:pk>trade/',confirm_trade, name = 'confirm'),
 #withdraw url
 path('profile/me/withdraw', WithdrawView.as_view(),name = 'withdraw'),
 path('profile/me/uploads/', uploadEvidence, name = 'upload_evidence'),
 path('profile/me/transactions/',transactions, name = 'txns'),
 path('profile/me/history/',history, name = 'history'),
 path('profile/me/settings/',settings, name = 'settings'),
 path('profile/me/settings/me/',my_profile, name = 'my_profile'),
 #games
 path('games/counter/racing/',game1,name = 'game1'),
]
