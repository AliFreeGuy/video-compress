from django.db import models



class BotModel(models.Model):
    name = models.CharField(max_length = 128 , unique = True)
    username = models.CharField(max_length = 128 , unique = True)
    token = models.CharField(max_length= 128 , unique = True)

    def __str__(self) -> str:
        return self.name
    


    
