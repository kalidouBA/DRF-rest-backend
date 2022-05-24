from rest_framework import serializers
from dataApi.models import (Questionnaire, Question, Reponse, PersonSuivie, 
                            Sms, JournalSms, Appel, JournalAppel, AirQuality)

from django.contrib.auth.models import User



class PersonSerializerComplet(serializers.ModelSerializer):
    class Meta:
        model = PersonSuivie
        fields = '__all__'


class ReponseQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reponse
        fields = ['columnTimeAnswer','columnRep','columnType','columnLong','columnLat','columnDate','columnAdresse','columnOrientation']

class QuestionReponseSerializer(serializers.ModelSerializer):
    reponsesAuQuest = ReponseQuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['columnQuest','columnQuestionnaireType','reponsesAuQuest']


class ReponseSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Reponse
        fields = ['question','columnTimeAnswer','columnRep','columnType','columnLong','columnLat','columnDate','columnAdresse','columnOrientation']

class ReponsePersonneSerializer(serializers.ModelSerializer):
    reponses = ReponseSerializer(many=True, read_only=True)
    class Meta:
        model = PersonSuivie
        fields = ['username','password','email','numeroTel','reponses']

class QuestionSerializer(serializers.ModelSerializer):
    reponse = ReponseSerializer()
    class Meta:
        model = Question
        fields = ['columnQuest','reponse']


class QuestionQuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['columnQuest','columnQuestionnaireType']

class ReponseSerializerSet(serializers.ModelSerializer):
    class Meta:
        model = Reponse
        fields =['question','personne','columnTimeAnswer','columnRep','columnType','columnLong','columnLat',
                'columnAdresse','columnDate','columnOrientation']

    def to_representation(self, instance):
        self.fields['question'] =  QuestionQuestionnaireSerializer(read_only=True)
        self.fields['personne'] =  PersonSerializer(read_only=True)
        return super(ReponseSerializerSet, self).to_representation(instance)




class QuestionnaireSerializer(serializers.ModelSerializer):
    #personneSuivie = PersonSuivieSerializer(source = person_suivi_set)
    questions = QuestionQuestionnaireSerializer(many=True)
    class Meta:
        model = Questionnaire
        depth = 3
        fields = ['columnTypeQuestionnaire', 'columnTitle', 'columnNumberQuestion', 'columnDateQuestionnaire','questions']
    
    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        questionnaire = Questionnaire.objects.create(**validated_data)
        for question_data in questions_data:
            Question.objects.create(questionnaire=questionnaire, **question_data)
        return questionnaire


class SmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sms
        fields =['displayName','date','address','threadId','typeSms','person','protocol','read','status','replayPath',
        'subject','service','locked','error','seen','journalSms']

class JournalSmsSerializer(serializers.ModelSerializer):
    sms = SmsSerializer(many=True)
    class Meta:
        model = JournalSms
        fields =['nombreSms','dateJournalSms','sms']

class JournalSMSPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalSms
        fields =['personneSms','nombreSms','dateJournalSms']
    def to_representation(self, instance):
        self.fields['personneSms'] =  PersonSerializer(read_only=True)
        return super(JournalSMSPersonSerializer, self).to_representation(instance)


class SMSSerializerSet(serializers.ModelSerializer):
    class Meta:
        model = Sms
        fields =['journalSms','displayName','address','threadId','date','typeSms','person','protocol','read','status',
                'replayPath','subject','service','locked','error','seen']
    def to_representation(self, instance):
        self.fields['journalSms'] =  JournalSMSPersonSerializer(read_only=True)
        return super(SMSSerializerSet, self).to_representation(instance)


class PersonneSmsSerializer(serializers.ModelSerializer):
    journalSms = JournalSmsSerializer(many=True)
    class Meta:
        model = PersonSuivie
        fields =['username','numeroTel','journalSms']

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonSuivie
        fields = ['username','password','email','numeroTel']
        
class AppelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appel
        fields = ['NUMERO','DATE','REPONSE','DUREE','TYPE']


class JournalAppelPersonSerializer(serializers.ModelSerializer):
    class Meta:
        #depth=1
        model = JournalAppel
        fields =['personneAppel','nombreAppel','dateJournalAppel']
    def to_representation(self, instance):
        self.fields['personneAppel'] =  PersonSerializer(read_only=True)
        return super(JournalAppelPersonSerializer, self).to_representation(instance)


class AppelSerializerSet(serializers.ModelSerializer):
    class Meta:
        model = Appel
        fields =['journalAppel','IDcall','NUMERO','DATE','REPONSE','DUREE','TYPE']
    def to_representation(self, instance):
        self.fields['journalAppel'] =  JournalAppelPersonSerializer(read_only=True)
        return super(AppelSerializerSet, self).to_representation(instance)



class JournalAppelSerializer(serializers.ModelSerializer):
    appels = AppelSerializer(many=True)
    class Meta:
        model = JournalAppel
        fields =['nombreAppel','dateJournalAppel','appels']

class PersonneAppelSerializer(serializers.ModelSerializer):
    journalAppels = JournalAppelSerializer(many=True)
    class Meta:
        model = PersonSuivie
        fields = ['username','numeroTel','journalAppels']


class AirQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AirQuality
        fields = ['aqi','_lati','_long','dominentpol','iaqi_h','iaqi_no2','iaqi_o3','iaqi_p','iaqi_pM10','iaqi_pM25',
                  'iaqi_so2','iaqi_t','iaqi_w','iaqi_wg','iaqi_time']

class PersonneAirQualitySerializer(serializers.ModelSerializer):
    airquality = AirQualitySerializer(many=True)
    class Meta:
        model = PersonSuivie
        fields = ['username','numeroTel','airquality']

class PersonneAirQualitySetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirQuality
        fields =['_username','aqi','_lati','_long','dominentpol','iaqi_h','iaqi_no2','iaqi_o3','iaqi_p','iaqi_pM10','iaqi_pM25',
                  'iaqi_so2','iaqi_t','iaqi_w','iaqi_wg','iaqi_time']
    def to_representation(self, instance):
        self.fields['_username'] =  PersonSerializer(read_only=True)
        return super(PersonneAirQualitySetSerializer, self).to_representation(instance)