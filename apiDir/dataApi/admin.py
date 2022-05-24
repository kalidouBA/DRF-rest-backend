from django.contrib import admin
from dataApi.models import Questionnaire, Sms, Question, JournalSms, Reponse, PersonSuivie, Appel, JournalAppel, AirQuality
# Register your models here.


admin.site.register(Questionnaire)
admin.site.register(JournalSms)
admin.site.register(Sms)
admin.site.register(Question)
admin.site.register(Reponse)
admin.site.register(PersonSuivie)
admin.site.register(Appel)
admin.site.register(JournalAppel)
admin.site.register(AirQuality)