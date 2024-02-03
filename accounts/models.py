from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

# this usermanager class never contain any field, it will only contains methods
# 1st method: to create a user 
# 2nd method: to create a superUser
# BaseUserManager: this baseusermanager will allow us to edit the way how users and superusers are created,
# ..and it also gives the methods to normalize the email adresses 
class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have username')
        
        user = self.model(
            email = self.normalize_email(email), 
            username = username,
            first_name = first_name,
            last_name = last_name,

        )
        # set_password is a method which takes the password and encode the password and store it in the database
        user.set_password(password)
        # django by default using "using" parameter to define which database manager should use for the operations
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email = self.normalize_email(email), 
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        # create this user as a super user 
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



# and this user model contains a typical filed like(first name, last name ....etc)
# by extended(inheriting) this "AbstractBaseUser", we are taking the full control of editing the whole custom user model
#..including the Authontication functinallity of django
#"AbstractUser": we can also use this , but django will only allow us to use extra fields to our model not more than that
class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True,null=True)

    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()


    # string representation of this model:
    def __str__(self):
        return self.email
    
    # define has permition
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    # we return true if user is an active superuser or he is an admin
    def has_module_perms(self, app_label):
        return True
    
    def get_role(self):
        if self.role == 1:
            user_role = 'Vendor'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role 


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, blank=True, null=True)
    # make sure t0 install: pip install Pillow to use 'ImageField'
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    address_line_1 = models.CharField(max_length=50, blank=True, null=True)
    address_line_2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)


    # String representation of this model:
    def __str__(self):
        return self.user.email



 