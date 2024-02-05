from django.db import models 
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from accounts.managers import UserManager


class User(AbstractBaseUser , PermissionsMixin):
    chat_id = models.IntegerField(unique = True)
    full_name = models.CharField(max_length = 128 , null = True , blank = True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    creation= models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'chat_id'
    REQUIRED_FIELDS = [ 'full_name',]


    objects = UserManager()

    def __str__(self) -> str:
        return f'{self.chat_id} - {self.full_name}'
    

    

    @property
    def is_staff(self):
        return self.is_admin
    
    class Meta :

        verbose_name = "All Users"
        verbose_name_plural = "All Users"
    
# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
# from accounts.managers import UserManager
# from django.utils import timezone
# from django.contrib.auth.models import PermissionsMixin







# from core.models import AbstractBaseModel
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from django.db import models
# from ..managers import UserManager





# class User(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
#     email = models.EmailField(max_length=50, unique=True)
#     phone_number = models.CharField(max_length=11, unique=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     full_name = models.CharField(max_length=100)
#     image = models.ImageField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     USERNAME_FIELD = 'phone_number'
#     REQUIRED_FIELDS = ['email', 'full_name']

#     objects = UserManager()

#     def __str__(self):
#         return self.email

#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'

#     def has_perm(self, perm, obj=None):
#         return True

#     def has_module_perms(self, app_label):
#         return True

#     @property
#     def is_staff(self):
#         return self.is_admin

