from django.shortcuts import render, redirect
from .models import Item, Wish
from ..mylogin.models import Users
from django.contrib import messages

# Create your views here.
def index(request):
    if not 'userid' in request.session:
        return redirect('/login')
    else:
        return redirect('/wish/dashboard')

def dashboard(request):
    if not 'userid' in request.session:
        return redirect('/login')
    you = Users.objects.get(id = request.session['userid'])
    userid = request.session['userid']
    context = {
        'yourwisheditems':Item.objects.yourwisheditems(userid),
        'youritems':Item.objects.filter(FK_addedby=you),
        'othersitems':Item.objects.othersitems(userid)
    }
    return render(request, 'wishapp/index.html', context)
    
def addwish(request):
    if request.method == 'POST':
        Wish.objects.makewish(request.POST)
    return redirect('/wish/dashboard')

def deletewish(request):
    if request.method == 'POST':
        Wish.objects.deletewish(request.POST)
    return redirect('/wish/dashboard')

def wishitem(request, itemid):
    if not 'userid' in request.session:
        return redirect('/login')
    else:
        targetitem = Item.objects.get(id = itemid)
        wishedusers = Users.objects.filter(wish_user__FK_item = targetitem)
        context = {
            'item':Item.objects.get(id=itemid),
            'users':wishedusers
        }
        return render(request, 'wishapp/wish_item.html', context)

def create(request):
    if not 'userid' in request.session:
        return redirect('/login')
    else:
        return render(request, 'wishapp/create_item.html')

def deleteitem(request):
    if request.method == 'POST':
        Item.objects.deleteitem(request.POST)
    return redirect('/wish/dashboard')

def createitem(request):
    if request.method == 'POST':
        res = Item.objects.makeitem(request.POST)
        if res['success']:
            for message in res['success']:
                messages.add_message(request, messages.SUCCESS, message)
            return redirect('/wish/dashboard')
        elif res['errors']:
            for message in res['errors']:
                messages.add_message(request, messages.ERROR, message)
            return redirect('/wish/create')
        else:
            return redirect('/wish/dashboard')
    else:
        return redirect('/wish/dashboard')

def allwishes(request):
    if request.method == 'POST':
        Item.objects.makeitem(request.POST)
        return redirect('/wish/dashboard')
    else:
        context = {
            'allwishes' : Wish.objects.all()
        }
        return render(request, 'wishapp/allwishes.html', context)

def allitems(request):
    if request.method == 'POST':
        Item.objects.makeitem(request.POST)
        return redirect('/wish/dashboard')
    else:
        context = {
            'allitems' : Item.objects.all()
        }
        return render(request, 'wishapp/allitems.html', context)