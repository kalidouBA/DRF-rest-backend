from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter


        #---------------- PERSONNE SUIVIE TABLE---------------------#
class PersonSuivie(models.Model):
    username  = models.CharField(max_length=20)
    password  = models.CharField(blank=True, default='',max_length=100)
    email     = models.EmailField(help_text='email valid svp')
    numeroTel = models.CharField(blank=True, default='',max_length=100)
    
    def __str__(self):
        return self.username


        #---------------- AIR QUALITY TABLE---------------------#
class AirQuality(models.Model):
    aqi         = models.FloatField()
    _lati       = models.FloatField()
    _long       = models.FloatField()
    dominentpol = models.CharField(blank=True, default='',max_length=10)
    iaqi_h      = models.FloatField()
    iaqi_no2    = models.FloatField()
    iaqi_o3     = models.FloatField()
    iaqi_p      = models.FloatField()
    iaqi_pM10   = models.FloatField()
    iaqi_pM25   = models.FloatField()
    iaqi_so2    = models.FloatField()
    iaqi_t      = models.FloatField()
    iaqi_w      = models.FloatField()
    iaqi_wg     = models.FloatField()
    iaqi_time   = models.CharField(blank=True, default='',max_length=20)
    _username   = models.ForeignKey(PersonSuivie, related_name='airquality', on_delete=models.CASCADE)
    def __str__(self):
        return str(self._lati) +","+str(self._long) + "(" + str(self._username) + ")"


        #---------------- QUESTIONNAIRE TABLE---------------------#

QUEST_CHOICES = [
    ('MiniGDS', 'Mini-GDS'),
    ('GDS15', 'GDS 15 items'),
    ('GDS30', 'GDS 30 items'),
    ('SF12', 'SF-12'),
    ('ANXIETE', 'Anxiété'),
    ('SF36', 'SF-36'),
]

class Questionnaire(models.Model):
    columnTypeQuestionnaire = models.CharField(choices=QUEST_CHOICES,max_length=100)
    columnTitle             = models.CharField(max_length=100, blank=True, default='')
    columnNumberQuestion    = models.IntegerField()
    columnDateQuestionnaire = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super(Questionnaire, self).save(*args, **kwargs)
    class Meta:
        ordering = ['columnDateQuestionnaire']
    def __str__(self):
        return self.columnTypeQuestionnaire

        #---------------- QUESTION TABLE---------------------#

LABELQUEST_CHOICES = [

    # Mini GDS
    ('row', 'Vous sentez- vous découragé(e) et triste ?'),
    ('row1', 'Avez-vous le sentiment que votre vie est vide ?'),
    ('row2', 'Etes-vous heureux (se) la plupart du temps ?'),
    ('row4', 'Avez-vous l’impression que votre situation est désespérée ?'),
    ('row5', 'SCORE TOTAL MINIGDS: '),

    # GDS 30
    ('row6', 'Etes-vous satisfait(e) de votre vie ?'),
    ('row7', 'Avez-vous renoncé à un grand nombre de vos activités ?'),
    ('row8', 'Avez-vous l\'impression que votre vie est vide ?'),
    ('row9', 'Vous ennuyez-vous souvent ?'),
    ('row10', 'Envisagez-vous l\'avenir avec optimisme ?'),
    ('row11', 'Etes-vous souvent préoccupé(e) par des pensées qui reviennent sans cesse ?'),
    ('row12', 'Etes-vous de bonne humeur la plupart du temps ?'),
    ('row13', 'Craignez-vous un mauvais présage pour l\'avenir ?'),
    ('row14', 'Etes-vous heureux(se) la plupart du temps ?'),
    ('row15', 'Avez-vous souvent besoin d\'aide ?'),
    ('row16', 'Vous sentez-vous souvent nerveux(se) au point de ne pouvoir tenir en place ?'),
    ('row17', 'Préférez-vous rester seul(e) dans votre chambre plutôt que d\'en sortir ?'),
    ('row18', 'L\'avenir vous inquiète-t-il ?'),
    ('row19', 'Pensez-vous que votre mémoire est plus mauvaise que celle de la plupart des gens ?'),
    ('row20', 'Pensez-vous qu\'il est merveilleux de vivre à notre époque ?'),
    ('row21', 'Avez-vous souvent le cafard ?'),
    ('row22', 'Avez-vous le sentiment d\'être désormais inutile ?'),
    ('row23', 'Ressassez-vous beaucoup le passé ?'),
    ('row24', 'Trouvez-vous que la vie est passionnante ?'),
    ('row25', 'Avez-vous des difficultés à entreprendre de nouveaux projets ?'),
    ('row26', 'Avez-vous beaucoup d\'énergie ?'),
    ('row27', 'Désespérez-vous de votre situation présente ?'),
    ('row28', 'Pensez-vous que la situation des autres est meilleure que la votre ?'),
    ('row29', 'Etes-vous souvent irrité(e) par des détails ?'),
    ('row30', 'Eprouvez-vous souvent le besoin de pleurer ?'),
    ('row31', 'Avez-vous du mal à vous concentrer ?'),
    ('row32', 'Etes-vous content(e) de vous lever le matin ?'),
    ('row33', 'Refusez-vous souvent les activités proposées ?'),
    ('row34', 'Vous est-il facile de prendre des décisions ?'),
    ('row35', 'Avez-vous l\'esprit aussi clair qu\'autrefois ?'),
    ('row36', 'SCORE TOTAL GDS-30'),

    # GDS 15

    ('row37', 'Êtes-vous satisfait(e) de votre vie ?'),
    ('row38', 'Avez-vous renoncé à un grand nombre de vos activités ?'),
    ('row39', 'Avez-vous le sentiment que votre vie est vide ?'),
    ('row40', 'Vous ennuyez-vous souvent ?'),
    ('row41', 'Êtes-vous de bonne humeur la plupart du temps ?'),
    ('row42', 'Avez-vous peur que quelque chose de mauvais vous arrive ?'),
    ('row43', 'Êtes-vous heureux (se) la plupart du temps ?'),
    ('row43', 'Avez-vous le sentiment d’être désormais faible ?'),
    ('row44', 'Préférez-vous rester seul(e) dans votre chambre plutôt que de sortir ?'),
    ('row45', 'Pensez-vous que votre mémoire est plus mauvaise que celle de la plupart des gens ?'),
    ('row46', 'Pensez-vous qu’il est merveilleux de vivre à notre époque ?'),
    ('row47', 'Vous sentez-vous une personne sans valeur actuellement ?'),
    ('row48', 'Avez-vous beaucoup d’énergie ?'),
    ('row49', 'Pensez-vous que votre situation actuelle est désespérée ?'),
    ('row50', 'Pensez-vous que la situation des autres est meilleure que la vôtre ?'),
    ('row51', 'SCORE TOTAL GDS-15: '),

    # SF 12

    ('row52', 'Dans l’ensemble, pensez-vous que votre santé est :'),
    ('row53', 'En raison de votre état de santé actuel, êtes-vous limité pour des efforts physiques modérés (déplacer une table, passer l’aspirateur, jouer aux boules...) ?:'),
    ('row54', 'monter plusieurs étages par l’escalier ?:'),
    ('row55', 'avez-vous accompli moins de choses que vous auriez souhaité ?:'),
    ('row56', 'avez-vous été limité pour faire certaines choses ?:'),
    ('row57', 'avez-vous accompli moins de choses que vous auriez souhaité ?:'),
    ('row58', 'avez-vous eu des difficultés à faire ce que vous aviez à faire avec autant de soin et d’attention que d’habitude ?:'),
    ('row59', 'Au cours de ces 4 dernières semaines, dans quelle mesure vos douleurs physiques vous ont -elles limité dans votre travail ou vos activités domestiques ?'),
    ('row60', 'y a t-il eu des moments où vous vous êtes senti calme et détendu ?:'),
    ('row61', 'y a t-il eu des moments où vous vous êtes senti débordant d’énergie ?:'),
    ('row62', 'y a t-il eu des moments où vous vous êtes senti triste et abattu ?:'),
    ('row63', 'Au cours de ces 4 dernières semaines, y a t-il eu des moments où votre état de santé physique ou émotionnel vous a gêné dans votre vie sociale et vos relations avec les autres, votre famille, vos amis, vos connaissances ?'),
]

class Question(models.Model):
    columnQuest             = models.CharField(max_length=350, blank = True, default='')
    columnQuestionnaireType = models.CharField(choices=QUEST_CHOICES,max_length=100)
    questionnaire           = models.ForeignKey(Questionnaire, related_name='questions', on_delete=models.CASCADE)

    class Meta:
        ordering = ['questionnaire']

    def save(self, *args, **kwargs):
        super(Question, self).save(*args, **kwargs)
    

    def __str__(self):
        return self.columnQuest+" ("+self.columnQuestionnaireType+")"

        #---------------- REPONSE TABLE---------------------#

class Reponse(models.Model):
    columnTimeAnswer  = models.CharField(max_length = 50, blank= True, default = '')
    columnRep         = models.CharField(max_length = 350, blank= True, default = '')
    columnType        = models.CharField(max_length = 20, blank= True, default = '')
    columnLong        = models.CharField(max_length = 20, blank= True, default = '')
    columnLat         = models.CharField(max_length = 20, blank= True, default = '')
    columnAdresse     = models.CharField(max_length=200, blank = True, default='')
    columnDate        = models.CharField(max_length=200, blank = True, default='')
    columnOrientation = models.CharField(max_length=200, blank = True, default='')
    question          = models.ForeignKey(Question,related_name='reponsesAuQuest', on_delete=models.CASCADE)
    personne          = models.ForeignKey(PersonSuivie, related_name='reponses', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('personne','question','columnRep')

    def __str__(self):
        return self.columnRep+" ("+self.columnType+")"

        #---------------- Journal Appel TABLE---------------------#

class JournalAppel(models.Model):
    nombreAppel      = models.IntegerField()
    dateJournalAppel = models.DateTimeField(auto_now_add=True)
    personneAppel    = models.ForeignKey(PersonSuivie,related_name='journalAppels', on_delete=models.SET_NULL, null = True)
    def __str__(self):
        return str(self.id)+" "+str(self.personneAppel) 
        #---------------- Appel TABLE---------------------#


class Appel(models.Model):
    IDcall = models.IntegerField(primary_key=True)
    journalAppel = models.ForeignKey(JournalAppel, related_name='appels', on_delete=models.CASCADE)
    NUMERO       = models.CharField(blank=True, default='',max_length=100)
    DATE         = models.CharField(blank=True, default='',max_length=100)
    REPONSE      = models.IntegerField()
    DUREE        = models.CharField(blank=True, default='',max_length=100)
    TYPE         = models.CharField(blank=True, default='',max_length=100)

    def __str__(self):
        return str(self.IDcall)+" "+str(self.NUMERO) 

        #---------------- JOURNAL SMS TABLE---------------------#

class JournalSms(models.Model):
    nombreSms      = models.IntegerField()
    dateJournalSms = models.DateTimeField(auto_now_add=True)
    personneSms    = models.ForeignKey(PersonSuivie,related_name='journalSms', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+" "+str(self.personneSms)    
        #---------------- SMS TABLE---------------------#

SMS_CHOICES = [
    ('in', 'Inbox')
]
PROTOCOL_CHOICES = [
    ('ps', 'SMS received')
]

READ_CHOICES = [
    ('yes', 'Yes'),
    ('no', 'No')
]

STATUS_CHOICES = [
    ('-1', '-1'),
    ('1', '1')
]

REPLAY_CHOICES = [
    ('0', '0'),
    ('1', '1')
]

LOCKED_CHOICES = [
    ('0', '0'),
    ('1', '1')
]
ERROR_CHOICES = [
    ('0', '0'),
    ('1', '1')
]
SEEN_CHOICES = [
    ('0', '0'),
    ('1', '1')
]

class Sms(models.Model):
    displayName= models.IntegerField(primary_key=True)
    address    = models.CharField(blank=True, default='',max_length=100)
    threadId   = models.CharField(blank=True, default='',max_length=100)
    date       = models.CharField(blank=True, default='',max_length=100)
    typeSms    = models.CharField(blank=True, default='',max_length=100)

    person     = models.CharField(blank=True, default='',max_length=100)
    protocol   = models.CharField(blank=True, default='',max_length=100)
    read       = models.CharField(blank=True, default='',max_length=100)
    status     = models.CharField(blank=True, default='',max_length=100)
    replayPath = models.CharField(blank=True, default='',max_length=100)

    subject    = models.CharField(blank=True, default='',max_length=100)
    service    = models.CharField(blank=True, default='',max_length=100)
    locked     = models.CharField(blank=True, default='',max_length=100)
    error      = models.CharField(blank=True, default='',max_length=100)
    seen       = models.CharField(blank=True, default='',max_length=100)
    journalSms = models.ForeignKey(JournalSms, related_name='sms', on_delete=models.CASCADE)
    
