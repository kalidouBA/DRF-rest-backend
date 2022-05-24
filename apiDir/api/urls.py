from django.contrib import admin
from django.conf.urls import include
from django.urls import path, include
from dataApi.views import *
from rest_framework import routers
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from dataApi import views
from rest_framework.authtoken.views import obtain_auth_token


schema_view = get_swagger_view(title='API REST Documentation')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dataApi.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('documentation/', schema_view),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth',),


#--------------------------- api Appel ----------------------------  
    path('api_appel/', views.appelList.as_view()),
    path('api_appel/<int:pk>/', views.appelDetail.as_view()),
  
  
# ---------------- api Question Reponse ---------------------------
    path('api_questionReponse/', views.questionReponse.as_view()),
    path('api_questionReponse/<int:pk>/', views.questionReponseDetail.as_view()),


#------------------------ api Questionnaire -----------------------
    path('api_questionnaire/', views.questionnaireList.as_view()),
    path('api_questionnaire/<int:pk>/', views.questionnaireDetail.as_view()),




#--------------------------- api Reponse --------------------------
    path('api_reponses/', views.reponsesList.as_view()),
    path('api_reponses/<int:pk>/', views.reponseDetail.as_view()),


#--------------------------- api Journal Appel ----------------------------  
    path('api_journalAppel/', views.appelJournalList.as_view()),
    path('api_journalAppel/<int:pk>/', views.appelJournalDetail.as_view()),
    
# -------------------------- api SMS -------------------------------
    path('api_sms/', views.smsList.as_view()),
    path('api_sms/<int:pk>/', views.smsDetail.as_view()),

# -------------------------- api Journal SMS -------------------------------
    path('api_journalSMS/', views.smsJournalList.as_view()),
    path('api_journalSMS/<int:pk>/', views.smsJournalDetail.as_view()),


# -------------------------- api Air Quality -------------------------------
    path('api_qualityAir/', views.qualityAirList.as_view()),
    path('api_qualityAir/<int:pk>/', views.qualityAirDetail.as_view()),


    #url(r'^$', schema_view),
]
