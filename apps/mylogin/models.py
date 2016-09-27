from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
import datetime

# Create your models here.

class UserManager(models.Manager):
    def register(self, postdata):
        response = {}
        response['errors'] = []
        response['success'] = []
        try:
            datehired = datetime.datetime.strptime(postdata['datehired'], "%Y-%m-%d")
        except:
            datehired = 0
        if not postdata['username']:
            response['errors'].append('Username is blank')
        if not postdata['name']:
            response['errors'].append('Name is blank')
        if datehired == 0:
            response['errors'].append('Please add a date hired')
        elif datehired > datetime.datetime.now():
            response['errors'].append('Date hired is in the future')
        if not postdata['password']:
            response['errors'].append('Password is blank')
        if postdata['password'] != postdata['confirmpw']:
            response['errors'].append('Password does not match')
        if not response['errors']:
            password = postdata['password']
            password = password.encode()
            hashedpw = bcrypt.hashpw(password, bcrypt.gensalt())
            try: 
                newuser = Users.objects.create(name = postdata['name'], username = postdata['username'],password = hashedpw, datehired=postdata['datehired'])
                response['success'].append('Registered User')
                print 'User Created'
                return response
            except:
                response['errors'].append('Unable to add to DB')
                return response
        else:
            return response

    def login(self, postdata):
        response = {}
        response['errors'] = []
        response['success'] = []
        try: 
            print 'trying get'
            user = Users.objects.get(username = postdata['username'])
            print 'try worked'
        except:
            response['errors'].append('username not found')
            return response
        password = postdata['password']
        password = password.encode()
        hashedpw = user.password
        hashedpw = hashedpw.encode()
        print 'password encoded'
        if bcrypt.hashpw(password, hashedpw) == hashedpw:
            response['success'].append('login successful')
            print 'matched hash'
            return response
        else:
            response['errors'].append('passwords do not match')
            return response
        
class Users(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    datehired = models.DateField()
    objects = UserManager()