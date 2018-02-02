from __future__ import unicode_literals
from django.db import models
import re
LETTER_REGEX = re.compile(r"^[a-zA-Z]+$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
DIG_REGEX = re.compile(r".*[0-9].*")

class BeltManager(models.Manager):
    def regvalidator(self, postData, valid):
        errors = {}
        if len(postData["name"]) < 1:
            errors["name"] = "First name cannot be empty!"
        elif DIG_REGEX.match(postData["name"]):
            errors["name"] = "First name cannot contain numbers!"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email!"
        elif User.objects.filter(email=postData['email']):
            errors["email"] = "Email already exists!"
        if len(postData["email"]) < 1:
            errors["email"] = "Email cannot be empty!"
        elif len(postData['password']) < 8:
            errors["password"] = "Password must be more than 8 characters"
        if len(postData['password']) < 1:
            errors["password"] = "Password cannot be left blank!"
        elif (postData["password"]) != (postData["passwords"]):
            errors["password"] = "Password must match Confirm password!"
        if len(postData["alias"]) < 1:
            errors["alias"] = "Alias cannot be empty!"
        elif len(postData["dob"]) < 1:
            errors["dob"] = "Date of Birth cannot be empty!"        
        return errors

    def logvalidator(self, postData, valid):
        errors = {}
        if not User.objects.filter(email=postData["email"]):
            errors["login"] = "Email is not registered"
        elif not User.objects.filter(password=postData["password"]):
            errors["password"] = "Incorrect password"
        return errors
    def quotevalidator(self, postData, valid):
        errors = {}
        if len(postData["quoted"]) < 4:
            errors["quoted"] = "Quoted by must be at least three characters"
        elif len(postData["message"]) < 11:
            errors["message"] = "Quote too short!"
        return errors

        

class User(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BeltManager()
    def __str__(self):
        user_str = "id: " + str(self.id) + ", name: " + str(self.name) + ", alias: " + str(self.alias) + ", email: " + str(self.email) + ", password: " + str(self.password) + ", dob: " + str(self.dob) + ", created_at: " + str(self.created_at) + ", updated_at " + str(self.updated_at)
        return user_str    
class Quote(models.Model):
    quoteby = models.CharField(max_length=50)
    message = models.CharField(max_length=255, null=True)
    userfavorite = models.ManyToManyField(User, related_name= 'fav_quote')
    user = models.ForeignKey(User, related_name="quotes", null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BeltManager()
    def __str__(self):
        user_str = "id: " + str(self.id) + ", quoteby: " + str(self.quoteby) + ", message: " + str(self.message) + ", userfavorite: " + str(self.userfavorite) + ", user: " + str(self.user) + ", created_at: " + str(self.created_at) + ", updated_at " + str(self.updated_at)
        return user_str