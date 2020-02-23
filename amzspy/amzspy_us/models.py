from django.db import models

# Create your models here.


class User(models.Model):
    amzurl = models.URLField(max_length=500)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.amzurl + ' | ' + str(self.email)


class Send(models.Model):
    sendurl = models.URLField(max_length=500)
    sendemail = models.EmailField(max_length=254)
    sendprice = models.FloatField(max_length=50)

    def __str__(self):
        return self.sendurl + ' | ' + str(self.sendemail) + ' | ' + self.sendprice
