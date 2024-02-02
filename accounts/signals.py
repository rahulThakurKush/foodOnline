from .models import User, UserProfile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


# 2nd way: As per the documetation we should use the decorator to connect the receiver to the sender 
@receiver(post_save, sender=User)
# Django signals : (Model signal): post_save 
# First we have to create a signal receiver function   
# 'created' argument is a Flag i.e a boolean value  
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        # print('user profile is created')
    else:
        try:
            profile = UserProfile.objects.get(user=instance) 
            profile.save() 
            print('user is updated')  
        except:
            #we will create the user profile if not exist 
            UserProfile.objects.create(user=instance)
            # print('profile was not exisy, bit i created one')   
        # print('user is updated')    

#1st way: this is the one way to connect the receiver to the sender
# post_save.connect(post_save_create_profile_receiver, sender=User) 



@receiver(pre_save, sender=User)
def pre_save_create_profile_receiver(sender, instance, **kwargs):
    pass
    # print(instance.username, 'this user is being saved')