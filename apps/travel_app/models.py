from django.db import models

# Create your models here.

class UserManager(models.Manager):
    def user_validation(self, postData):
        errors = []
        for key,val in postData.items():
            if len(val)<1:
                errors.append("{} is required!".format(" ".join(key.split('_')).title()))
            elif not postData['first_name'].isalpha() and key == 'first_name':
                errors.append('First Name cannot contain numbers')
            elif not postData['last_name'].isalpha() and key == 'last_name':
                errors.append('Last Name cannot contain numbers')
       
        if errors: 
            return {"errors": errors}
        else:
            return {"success": True}
        


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class ItineraryManager(models.Manager):
    def trip_validation(self, postData):
        errors = []
        for key,val in postData.items():
            if len(val)<1:
                errors.append("{} is required!".format(key))
        
        if errors: 
            return {"errors": errors}
        else:
            return {"success": True}

class Itinerary(models.Model):
    title = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    description = models.TextField()
    added_user = models.ForeignKey(User, related_name="added_trip")
    saved_user = models.ManyToManyField(User, related_name="saved_trip")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
