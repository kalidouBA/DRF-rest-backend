from dataApi.models import Questionnaire, PersonSuivie, Reponse, JournalAppel, JournalSms,Question, Sms, Appel,AirQuality
from dataApi.serializers import (QuestionReponseSerializer,JournalAppelSerializer,QuestionnaireSerializer, 
                                ReponsePersonneSerializer,ReponseSerializer,PersonneAppelSerializer,
                                PersonneSmsSerializer,PersonSerializer, SmsSerializer, AppelSerializer,
                                JournalAppelPersonSerializer,JournalSMSPersonSerializer,AppelSerializerSet,
                                SMSSerializerSet,ReponseSerializerSet,PersonSerializerComplet,PersonneAirQualitySerializer,
                                PersonneAirQualitySetSerializer)
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from dataApi.permissions import IsOwnerOrReadOnly
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


# ----------------------------------- api Personne Liste ---------------------------------------
class personneList(APIView):
    #permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        personnes = PersonSuivie.objects.all()
        serializer = PersonSerializer(personnes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PersonSerializer(data=request.data)
        if PersonSuivie.objects.filter(username = request.data['username'] , numeroTel = request.data['numeroTel']).exists():
            print('no create')
        else:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class personneDetail(APIView):
    """
    Retrieve, update or delete a code personne.
    """
    #permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return PersonSuivie.objects.get(pk=pk)
        except PersonSuivie.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        personne = self.get_object(pk)
        serializer = PersonSerializerComplet(personne)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        personne = self.get_object(pk)
        serializer = PersonSerializerComplet(personne, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        personne = self.get_object(pk)
        personne.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ----------------------------------- api Question Repoonse Liste -------------------------------------
class questionReponse(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionReponseSerializer

class questionReponseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionReponseSerializer

# ----------------------------------- api Questionnaire Liste ---------------------------------------
class questionnaireList(generics.ListCreateAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer

class questionnaireDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer




# ----------------------------------- api Reponses Liste ---------------------------------------------
class reponsesList(APIView):
    def get(self, request, format=None):
        personnes = PersonSuivie.objects.all()
        serializer = ReponsePersonneSerializer(personnes, many=True)
        return Response(serializer.data)


class reponseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PersonSuivie.objects.all()
    serializer_class = ReponsePersonneSerializer

#************************************************


@api_view(['GET', 'POST'])
def reponseSetList(request):
    if request.method == 'GET':
        reponseSet = Reponse.objects.all()
        serializer = ReponseSerializerSet(reponseSet, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        pers = PersonSuivie.objects.get(email = request.data['email'],password = request.data['password'])
        question = Question.objects.get(columnQuest = request.data['columnQuest'],
                                        columnQuestionnaireType = request.data['columnType'])
        reponse_data = {
                    "question":question.id,
                    "personne":pers.id,
                    "columnTimeAnswer":request.data['columnTimeAnswer'],
                    "columnRep":request.data['columnRep'],
                    "columnType":request.data['columnType'],
                    "columnLong":request.data['columnLong'],
                    "columnLat":request.data['columnLat'],
                    "columnAdresse":request.data['columnAdresse'],
                    "columnDate":request.data['columnDate'],
                    "columnOrientation":request.data['columnOrientation']
                    }
        serializer = ReponseSerializerSet(data=reponse_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors , status= status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])

def reponseSetDetail(request, username):
    try:
        pers = PersonSuivie.objects.get(username = username)
        reponsedata = Reponse.objects.get(pk=pers.id)
    except Reponse.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReponseSerializerSet(reponsedata)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ReponseSerializerSet(reponsedata, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        reponsedata.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ----------------------------------- api Appel Liste ---------------------------------------
class appelList(generics.ListCreateAPIView):
    queryset = Appel.objects.all()
    serializer_class = AppelSerializer

class appelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appel.objects.all()
    serializer_class = AppelSerializer


#**********************************

@api_view(['GET', 'POST'])
def appelSetList(request):
    if request.method == 'GET':
        appelSet = Appel.objects.all()
        serializer = AppelSerializerSet(appelSet, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        pers = PersonSuivie.objects.get(email = request.data['email'],password = request.data['password'])
        jappel = JournalAppel.objects.filter(personneAppel = pers).order_by('-id')[0]
        appel_data = {
                    "journalAppel":jappel.id,
                    "IDcall":request.data['IDcall'],
                    "NUMERO":request.data['NUMERO'],
                    "DATE":request.data['DATE'],
                    "REPONSE":request.data['REPONSE'],
                    "DUREE":request.data['DUREE'],
                    "TYPE":request.data['TYPE']
                    }
        serializer = AppelSerializerSet(data=appel_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors , status= status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])

def appelSetDetail(request, pk):
    try:
        appeldata = Appel.objects.get(pk=pk)
    except Appel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AppelSerializerSet(appeldata)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AppelSerializerSet(appeldata, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        appeldata.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# ----------------------------------- api Appel Journal Liste ------------------------------------------------
class appelJournalList(generics.ListCreateAPIView):
    queryset = PersonSuivie.objects.all()
    serializer_class = PersonneAppelSerializer

class appelJournalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PersonSuivie.objects.all()
    serializer_class = PersonneAppelSerializer


#*******************

@api_view(['GET', 'POST'])
def journalAppelPersonListCreate(request):
    if request.method == 'GET':
        journalAppelPerson = JournalAppel.objects.all()
        serializer = JournalAppelPersonSerializer(journalAppelPerson, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        appelSet = Appel.objects.all()
        length = appelSet.count() 
        print(length)
        if(request.data['nombreAppel'] > length):
            pers = PersonSuivie.objects.get(email = request.data['email'],password = request.data['password'])
            journal_data = {"personneAppel":pers.id,"nombreAppel":request.data['nombreAppel']}
            serializer = JournalAppelPersonSerializer(data=journal_data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status = status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors , status= status.HTTP_400_BAD_REQUEST)
        else:
            return length
    


@api_view(['GET', 'PUT', 'DELETE'])

def journalAppelPersonDetail(request, pk):
    try:
        journalAppelPerson = JournalAppel.objects.get(pk=pk)
    except JournalAppel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JournalAppelPersonSerializer(journalAppelPerson)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = JournalAppelPersonSerializer(journalAppelPerson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        journalAppelPerson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ***************************************  api Sms Liste *************************************************************
class smsList(generics.ListCreateAPIView):
    queryset = Sms.objects.all()
    serializer_class = SmsSerializer

class smsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sms.objects.all()
    serializer_class = SmsSerializer


#**********************************

@api_view(['GET', 'POST'])
def smsSetList(request):

    if request.method == 'GET':
        smsSet = Sms.objects.all()
        serializer = SMSSerializerSet(smsSet, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        pers = PersonSuivie.objects.get(email = request.data['email'],password = request.data['password'])
        jsms = JournalSms.objects.filter(personneSms = pers).order_by('-id')[0]
        sms_data = {
                    "journalSms":jsms.id,
                    "displayName":request.data['displayName'],
                    "address":request.data['address'],
                    "threadId":request.data['threadId'],
                    "date":request.data['date'],
                    "typeSms":request.data['typeSms'],
                    "person":request.data['person'],
                    "protocol":request.data['protocol'],
                    "read":request.data['read'],
                    "status":request.data['status'],
                    "replayPath":request.data['replayPath'],
                    "subject":request.data['subject'],
                    "service":request.data['service'],
                    "locked":request.data['locked'],
                    "error":request.data['error'],
                    "seen":request.data['seen']
                    }
        serializer = SMSSerializerSet(data=sms_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors , status= status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])

def smsSetDetail(request, pk):

    try:
        smsdata = Sms.objects.get(pk=pk)
    except Sms.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SMSSerializerSet(smsdata)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SMSSerializerSet(smsdata, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        smsdata.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# ----------------------------------- api Journal Sms Liste --------------------------------------------------
class smsJournalList(generics.ListCreateAPIView):
    queryset = PersonSuivie.objects.all()
    serializer_class = PersonneSmsSerializer
    
class smsJournalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PersonSuivie.objects.all()
    serializer_class = PersonneSmsSerializer


#****************************

@api_view(['GET', 'POST'])
def journalSMSPersonListCreate(request):
    if request.method == 'GET':
        journalSmsPerson = JournalSms.objects.all()
        serializer = JournalSMSPersonSerializer(journalSmsPerson, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        smsSet = Sms.objects.all()
        length = smsSet.count() 
        print(length)
        if(request.data['nombreSms'] > length):
            pers = PersonSuivie.objects.get(email = request.data['email'],password = request.data['password'])
            journal_data = {"personneSms":pers.id,"nombreSms":request.data['nombreSms']}
            serializer = JournalSMSPersonSerializer(data=journal_data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status = status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors , status= status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(serializer.errors , status= status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])

def journalSMSPersonDetail(request, pk):

    try:
        journalSmsPerson = JournalSms.objects.get(pk=pk)
    except JournalSms.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JournalSMSPersonSerializer(journalSmsPerson)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = JournalSMSPersonSerializer(journalSmsPerson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        journalSmsPerson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# ----------------------------------- Serializer Qualité de l'air ------------------------------------------------
class qualityAirList(generics.ListCreateAPIView):
    queryset = PersonSuivie.objects.all()
    serializer_class = PersonneAirQualitySerializer

class qualityAirDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PersonSuivie.objects.all()
    serializer_class = PersonneAirQualitySerializer


#*******************



@api_view(['GET', 'POST'])
def qualityAirPersonListCreate(request):

    if request.method == 'GET':
        air_quality = AirQuality.objects.all()
        serializer = PersonneAirQualitySetSerializer(air_quality, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        pers = PersonSuivie.objects.get(username = request.data['username'])
        air_quality_data = {"_username"   :pers.id,
                        "aqi"         :request.data['aqi'],
                        "_lati"       :request.data['_lati'],
                        "_long"       :request.data['_long'],
                        "dominentpol" :request.data['dominentpol'],
                        "iaqi_h"      :request.data['iaqi_h'],
                        "iaqi_no2"    :request.data['iaqi_no2'],
                        "iaqi_o3"     :request.data['iaqi_o3'],
                        "iaqi_p"      :request.data['iaqi_p'],
                        "iaqi_pM10"   :request.data['iaqi_pM10'],
                        "iaqi_pM25"   :request.data['iaqi_pM25'],
                        "iaqi_so2"    :request.data['iaqi_so2'],
                        "iaqi_t"      :request.data['iaqi_t'],
                        "iaqi_w"      :request.data['iaqi_w'],
                        "iaqi_wg"     :request.data['iaqi_wg'],
                        "iaqi_time"   :request.data['iaqi_time']}

        serializer = PersonneAirQualitySetSerializer(data=air_quality_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors , status= status.HTTP_400_BAD_REQUEST)
