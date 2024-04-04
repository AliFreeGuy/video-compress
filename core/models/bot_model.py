from django.db import models



class BotModel(models.Model):
    name = models.CharField(max_length = 128 , unique = True)
    username = models.CharField(max_length = 128 , unique = True)
    token = models.CharField(max_length= 128 , unique = True)
    api_hash = models.CharField(max_length = 225)
    api_id = models.CharField(max_length = 225)

    def __str__(self) -> str:
        return str(self.name)
    


    

    class Meta :

        verbose_name = "My Bots"
        verbose_name_plural = "My Bots"