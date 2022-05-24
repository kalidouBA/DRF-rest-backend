
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from dataApi import views


urlpatterns = [
    

#********************** Url POS GET PUT DELETE **********************

#--------------------------- api Personne CREATE GET PUT DELETE  -----------  
    path('api_personne/', views.personneList.as_view() , name='Création d\'une personne suivie'),
    path('api_personne/<int:pk>/', views.personneDetail.as_view() , name='Information détaillées d\'une personne suivies'),


# ---------------- api CALL CREATE GET PUT DELETE ---------------------------

    path('appel/', views.appelSetList),
    path('appel/<int:pk>/', views.appelSetDetail),


# ---------------- api CATALOG CALL CREATE GET PUT ---------------------------

    path('journalAppel/', views.journalAppelPersonListCreate),
    path('journalAppel/<int:pk>/', views.journalAppelPersonDetail),


# ---------------- api SMS CREATE GET PUT ---------------------------
    
    path('sms/', views.smsSetList),
    path('sms/<int:pk>/', views.smsSetDetail),


# ---------------- api CATALOG SMS CREATE GET PUT ---------------------------
    path('journalSMS/', views.journalSMSPersonListCreate),
    path('journalSMS/<int:pk>/', views.journalSMSPersonDetail),



# ---------------- api RESPONSE CREATE GET PUT ---------------------------
    path('reponsesQuestionnaire/', views.reponseSetList),
    path('reponseQuestionnaire/<str:username>/', views.reponseSetDetail),


# ---------------- api AIRQUALITY POST ---------------------------
    path('qualityAir/', views.qualityAirPersonListCreate),

]

urlpatterns = format_suffix_patterns(urlpatterns)
