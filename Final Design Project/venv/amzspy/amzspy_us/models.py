from django.db import models

# Create your models here.


class User(models.Model):
    amzurl = models.URLField(max_length=500)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.amzurl + ' | ' + str(self.email)
