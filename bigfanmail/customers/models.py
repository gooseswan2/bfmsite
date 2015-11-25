from django.db import models
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser
from django_localflavor_us.models import USStateField


class BFCustomerManager(BaseUserManager):
    def create_user(self, username, email_address, first_name, last_name, password=None):
        if not email_address:
           raise ValueError('Users must have an email address')
    
        user = self.model(
            username=BFCustomerManager.normalize_email(username),
            email_address=BFCustomerManager.normalize_email(email_address),
            first_name=first_name,
            last_name=last_name,
        )
  
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email_address, first_name, last_name, password=None):
        user = self.create_user(username,
            email_address=email_address,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user_is_admin = True;
        user.save(using=self._db)
        return user

# Create your models here.
class BFCustomer(AbstractBaseUser):
    username =	        models.CharField(max_length=75,unique=True,db_index=True)
    email_address =	models.CharField(max_length=75)
    first_name =	models.CharField(max_length=30)
    last_name =		models.CharField(max_length=40)
    add1 =		models.CharField(verbose_name="Address1", max_length=50, null=True, blank=True)
    add2 =  		models.CharField(verbose_name="Address2", max_length=50,null=True,blank=True)
    city =  		models.CharField(max_length=40, null=True, blank=True)
    state = 		USStateField(null=True, blank=True)
    zipcode =		models.CharField(verbose_name= "Zip code", max_length=10, null=True,blank=True)
    signup_date = 	models.DateTimeField(auto_now_add=True)
    is_active =         models.BooleanField(default=True)
    is_admin =          models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email_address', 'first_name', 'last_name']
    objects = BFCustomerManager()

    def get_full_name(self):
        return self.username 

    def get_short_name(self):
        return self.username 

    def __unicode__(self):
        return self.username 

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
