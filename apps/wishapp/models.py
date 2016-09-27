from __future__ import unicode_literals
from ..mylogin.models import Users
from django.db import models

# Create your models here.

class WishManager(models.Manager):
      
    def yourwisheditems(self, userid):
        you = Users.objects.get(id = userid)
        youritems = Item.objects.filter(FK_addedby = you)
        yourwisheditems = Item.objects.filter(wish_item__FK_user = you)
        for youritem in youritems:
            yourwisheditems = yourwisheditems.exclude(id = youritem.id)
        return yourwisheditems
    
    def othersitems(self, userid):
        you = Users.objects.get(id = userid)
        otherswisheditems = Item.objects.exclude(FK_addedby = you).exclude(wish_item__FK_user = you)
        return otherswisheditems
    
    def makewish(self, postdata):
        you = Users.objects.get(id = postdata['userid'])
        item = Item.objects.get(id = postdata['itemid'])
        wish = Wish.objects.filter(FK_user = you, FK_item = item)
        if wish:
            return wish[0]
        else:
            wish = Wish.objects.create(FK_user = you, FK_item = item)
            return wish 
    
    def deletewish(self, postdata):
        targetuser = Users.objects.get(id = postdata['userid'])
        item = Item.objects.get(id = postdata['itemid'])
        wish = Wish.objects.filter(FK_user = targetuser, FK_item = item)
        wish.delete()
        return 
    
    def makeitem(self, postdata):
        response = {}
        response['errors'] = []
        response['success'] = []
        if not postdata['itemname']:
            response['errors'].append('Item Name can not be empty')
        elif len(postdata['itemname'])<4:
            response['errors'].append('Item name must be longer than 3 characters')
        you = Users.objects.get(id = postdata['userid'])
        if not response['errors']:
            item = Item.objects.create(FK_addedby = you, name = postdata['itemname'])
            response['success'].append('Item added to the database')
            Wish.objects.create(FK_item = item, FK_user = you)
            response['success'].append('Item added to the wishlist')
            return response
        else:
            return response
    
    def deleteitem(self, postdata):
        you = Users.objects.get(id = postdata['userid'])
        item = Item.objects.get(id = postdata['itemid'])
        try: 
            Wish.objects.get(FK_item = item, FK_user = you).delete()
        except:
            print 'no wish associated with item'
        item.delete()
        return 
    

class Item(models.Model):
    name = models.CharField(max_length=255)
    FK_addedby = models.ForeignKey(Users, related_name='item_adedby')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = WishManager()
    
class Wish(models.Model):
    FK_item = models.ForeignKey(Item, related_name='wish_item')
    FK_user = models.ForeignKey(Users, related_name='wish_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = WishManager()
