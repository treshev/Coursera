from django.db import models


# Create your models here.
class Setting(models.Model):
    SMART_HOME_API_URL = "http://smarthome2.t3st.ru/api/"
    SMART_HOME_ACCESS_TOKEN = "cd5547b376b51438221dcdc905b426cfd463d8735a5ab1509c137ceb2f66132a"
    MAIL_RECEPIENT = ['a.treshev@gmail.com']

    controller_name = models.CharField(max_length=40, unique=True)
    label = models.CharField(max_length=100)
    value = models.IntegerField(default=20)
