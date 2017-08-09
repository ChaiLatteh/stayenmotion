# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from .models import User, UserManager, Business, BusinessManager, Messageboard_Message, Messageboard_Comment, Messageboard_Message_Like, Messageboard_Message_Bookmark, Messageboard_Message_View, MessageboardManager, Meetup, MeetupManager, Meetup_Bookmark
from .forms import UploadFileForm, Messageboard_MessageForm
import datetime, random, requests, json
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

# Create your views here.
def index(request):
    meetups_list=[]
    messages_list=[]

    for message in Messageboard_Message.objects.all().order_by('-created_at'):
        messages_list.append(message)
    for meetup in Meetup.objects.all():
        meetups_list.append(meetup)



    if 'user_id' in request.session:
        this_user = User.objects.get(id=request.session['user_id'])
        liked_messages_list=[]
        for like in Messageboard_Message_Like.objects.filter(user=this_user).order_by('-created_at'):
            liked_messages_list.append(Messageboard_Message.objects.get(id=like.messageboard_message.id))
        liked_messages_list=liked_messages_list[:3]
        data={
        "this_user":this_user,
        "messages_list":messages_list,
        "meetups_list":meetups_list,
        "liked_messages_list":liked_messages_list,
        }
        return render(request, 'APPNAME/home.html', data)

    elif 'business_id' in request.session:
        this_business = Business.objects.get(id=request.session['business_id'])
        data={
        "this_business":this_business,
        "messages_list":messages_list,
        "meetups_list":meetups_list,
        }
        return render(request, 'APPNAME/home.html', data)


        # random.shuffle(meetupname)
        # try:
        # this_user=User.objects.get(id=request.session['user_id'])

        # for like in Messageboard_Message_Like.objects.all():
        #     likes_list.append(like)


    else:
        return render(request, 'APPNAME/index.html')

def user_register(request):
    data = {
    'first_name':request.POST['user_reg_first_name'],
    'last_name':request.POST['user_reg_last_name'],
    'email':request.POST['user_reg_email'],
    'password':request.POST['user_reg_password'],
    'confirm_password':request.POST['user_reg_confirm_password'],
    }
    new_user = User.objects.register(data)
    if new_user['errors_list']:
        for error in new_user['errors_list']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')
    else:
        messages.add_message(request, messages.ERROR, "Successfully Registered!")
        return redirect('/')

def user_login(request):
    data = {
    'email':request.POST['user_login_email'],
    'password':request.POST['user_login_password'],
    }
    user = User.objects.login(data)
    if user['errors_list']:
        for error in user['errors_list']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')
    else:
        request.session['user_id']=user['logged_user'].id
        return redirect('/')

def business_register(request):
    data = {
    'name':request.POST['business_reg_name'],
    'address':request.POST['business_reg_address'],
    'city':request.POST['business_reg_city'],
    'state':request.POST['business_reg_state'],
    'zipcode':request.POST['business_reg_zipcode'],
    'email':request.POST['business_reg_email'],
    'password':request.POST['business_reg_password'],
    'confirm_password':request.POST['business_reg_confirm_password'],
    }
    new_business = Business.objects.register(data)
    if new_business['errors_list']:
        for error in new_business['errors_list']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')
    else:
        messages.add_message(request, messages.ERROR, "Successfully Registered!")
        return redirect('/')

def business_login(request):
    data = {
    'email':request.POST['business_login_email'],
    'password':request.POST['business_login_password'],
    }
    business = Business.objects.login(data)
    if business['errors_list']:
        for error in business['errors_list']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')
    else:
        request.session['business_id']=business['logged_business'].id
        return redirect('/')

def show_user(request, user_id):
    a_user = User.objects.get(id=user_id)
    if 'user_id' in request.session:
        data = {
        'this_user':User.objects.get(id=request.session['user_id']),
        'a_user':a_user,
        }
        return render(request, 'APPNAME/show_user.html', data)

    elif 'business_id' in request.session:
        data = {
        'this_business':Business.objects.get(id=request.session['business_id']),
        'a_user':a_user,
        }
        return render(request, 'APPNAME/show_user.html', data)
    else:
        return redirect('/')


def show_business(request, business_id):
    a_business = Business.objects.get(id=business_id)
    if 'user_id' in request.session:
        data = {
        'this_user':User.objects.get(id=request.session['user_id']),
        'a_business':a_business,
        }
        return render(request, 'APPNAME/show_business.html', data)

    elif 'business_id' in request.session:
        data = {
        'this_business':Business.objects.get(id=request.session['business_id']),
        'a_business':a_business,
        }
        return render(request, 'APPNAME/show_business.html', data)
    else:
        return redirect('/')

def upload_picture(request):
    form = UploadFileForm()
    data = {
    "form":form,
    }
    return render(request, 'APPNAME/upload_picture.html', data)

def upload_picture_process(request):
    if 'user_id' in request.session:
        this_user = User.objects.get(id=request.session['user_id'])
        if request.POST:
            form = UploadFileForm(request.POST, request.FILES, instance=this_user)
            if form.is_valid():
                this_user = form.save(commit=False)
                this_user.save()
            else:
                form = UploadFileForm()
        return redirect('/users/'+str(this_user.id))

    elif 'business_id' in request.session:
        this_business = Business.objects.get(id=request.session['business_id'])
        if request.POST:
            form = UploadFileForm(request.POST, request.FILES, instance=this_business)
            if form.is_valid():
                this_business = form.save(commit=False)
                this_business.save()
            else:
                form = UploadFileForm()
        return redirect('/businesses/'+str(this_business.id))

    else:
        return redirect('/')

def remove_picture_process(request):
    if 'user_id' in request.session:
        this_user = User.objects.get(id=request.session['user_id'])
        this_user.image=""
        this_user.save()
        return redirect('/users/'+str(this_user.id))

    elif 'business_id' in request.session:
        this_business = Business.objects.get(id=request.session['business_id'])
        this_business.image=""
        this_business.save()
        return redirect('/businesses/'+str(this_business.id))

    else:
        return redirect('/')

def updateprofile(request):
    if 'user_id' in request.session:
        data={
        'this_user':User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'APPNAME/updateprofile.html', data)

    elif 'business_id' in request.session:
        data={
        'this_business':Business.objects.get(id=request.session['business_id']),
        }
        return render(request, 'APPNAME/updateprofile.html', data)

    else:
        return redirect('/')

def updateprofile_process(request):
    if 'user_id' in request.session:
        this_user=User.objects.get(id=request.session['user_id'])
        # if form is valid
        if request.POST['user_first_name']!="" and request.POST['user_last_name']!="":
            this_user.first_name=request.POST['user_first_name']
            this_user.last_name=request.POST['user_last_name']
            this_user.save()
            return redirect('/users/'+str(request.session['user_id']))
        # if form is NOT valid
        else:
            messages.add_message(request, messages.ERROR, "ERROR")
            return redirect('/updateprofile')

    elif 'business_id' in request.session:
        this_business=Business.objects.get(id=request.session['business_id'])
        if request.POST['business_name']!="" and request.POST['business_address']!="" and request.POST['business_city']!="" and len(request.POST['business_state'])==2 and len(request.POST['business_zipcode'])==5:
            this_business.name=request.POST['business_name']
            this_business.address=request.POST['business_address']
            this_business.city=request.POST['business_city']
            this_business.state=request.POST['business_state']
            this_business.zipcode=request.POST['business_zipcode']
            this_business.save()
            return redirect('/businesses/'+str(request.session['business_id']))
        else:
            messages.add_message(request, messages.ERROR, "ERROR")
            return redirect('/updateprofile')

    else:
        return redirect('/')

def changepassword(request):
    return render(request, 'APPNAME/changepassword.html')

def changepassword_process(request):
    if 'user_id' in request.session:
        this_user = User.objects.get(id=request.session['user_id'])
        data = {
        'this_user':this_user,
        'current_password':request.POST['current_password'],
        'new_password':request.POST['new_password'],
        'confirm_password':request.POST['confirm_password'],
        }
        user = User.objects.changepassword(data)
        if user['errors_list']:
            for error in user['errors_list']:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/changepassword')
        else:
            messages.add_message(request,messages.ERROR, "Successfully changed password!")
            return redirect('/users/'+str(request.session['user_id']))


    elif 'business_id' in request.session:
        this_business = Business.objects.get(id=request.session['business_id'])
        data = {
        'this_business':this_business,
        'current_password':request.POST['current_password'],
        'new_password':request.POST['new_password'],
        'confirm_password':request.POST['confirm_password'],
        }
        business = Business.objects.changepassword(data)
        if business['errors_list']:
            for error in business['errors_list']:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/changepassword')
        else:
            messages.add_message(request,messages.ERROR, "Successfully changed password!")
            return redirect('/businesses/'+str(request.session['business_id']))
    else:
        return redirect('/')


def bookmarks(request):
    messages_list=[]
    meetups_list=[]
    this_user = User.objects.get(id=request.session['user_id'])
    for message in Messageboard_Message.objects.all():
        try:
            Messageboard_Message_Bookmark.objects.get(user=this_user, messageboard_message=message)
            messages_list.append(message)
        except:
            pass

    for meetup in Meetup.objects.all():
        try:
            Meetup_Bookmark.objects.get(user=this_user, meetup=meetup)
            meetups_list.append(meetup)
        except:
            pass

    data = {
    "messages_list":messages_list,
    "meetups_list":meetups_list,
    }

    return render(request, 'APPNAME/bookmarks.html', data)

def messageboard(request):
    messages_list=[]
    for message in Messageboard_Message.objects.all().order_by('-created_at'):
        messages_list.append(message)

    if 'user_id' in request.session:
        data={
        "this_user":User.objects.get(id=request.session['user_id']),
        "messages_list":messages_list,
        }
        return render(request, 'APPNAME/messageboard.html', data)

    elif 'business_id' in request.session:
        data={
        "this_business":Business.objects.get(id=request.session['business_id']),
        "messages_list":messages_list,
        }
        return render(request, 'APPNAME/messageboard.html', data)
    else:
        return redirect('/')

def new_message(request):
    if 'user_id' not in request.session:
        return redirect('/')

    form = Messageboard_MessageForm()
    data = {
        "form":form,
    }
    return render(request, 'APPNAME/new_message.html', data)

def new_message_process(request):
    if 'user_id' not in request.session:
        return redirect('/')

    this_user = User.objects.get(id=request.session['user_id'])
    if request.POST:
        form = Messageboard_MessageForm(request.POST, request.FILES)
        if form.is_valid():
            new_message = form.save(commit=False)
            print new_message.image
            new_message.user=this_user
            new_message.save()
            print new_message.image
            return redirect('/messageboard')
        else:
            print "FAIL"
            form = Messageboard_MessageForm()
            return redirect('/messageboard/new')

def show_message(request, message_id):
    if 'user_id' not in request.session:
        return redirect('/')

    this_message=Messageboard_Message.objects.get(id=message_id)
    Messageboard_Message_View.objects.create(messageboard_message=this_message)
    print this_message.image
    data={
    "this_message":this_message,
    }

    return render(request, 'APPNAME/show_message.html', data)

def new_comment_process(request, message_id):
    if 'user_id' not in request.session:
        return redirect('/')

    this_message = Messageboard_Message.objects.get(id=message_id)
    this_user = User.objects.get(id=request.session['user_id'])
    data={
    'comment':request.POST['comment'],
    'this_message':this_message,
    'this_user':this_user,
    }
    new_comment=Messageboard_Comment.objects.comment(data)
    return redirect('/messageboard/'+message_id)

def like_message_process(request, message_id):
    if 'user_id' not in request.session:
        return redirect('/')

    this_user=User.objects.get(id=request.session['user_id'])
    this_message=Messageboard_Message.objects.get(id=message_id)
    try:
        Messageboard_Message_Like.objects.get(messageboard_message=this_message, user=this_user)
        messages.add_message(request, messages.ERROR, "INVALID APPROACH")
    except:
        Messageboard_Message_Like.objects.create(messageboard_message=this_message, user=this_user)
    return redirect('/messageboard/'+message_id)

def unlike_message_process(request, message_id):
    if 'user_id' not in request.session:
        return redirect('/')

    this_user=User.objects.get(id=request.session['user_id'])
    this_message=Messageboard_Message.objects.get(id=message_id)
    try:
        Messageboard_Message_Like.objects.get(messageboard_message=this_message, user=this_user).delete()
    except:
        messages.add_message(request, messages.ERROR, "INVALID APPROACH")
    return redirect('/messageboard/'+message_id)

def bookmark_message_process(request, message_id):
    if 'user_id' not in request.session:
        return redirect('/')

    this_user=User.objects.get(id=request.session['user_id'])
    this_message=Messageboard_Message.objects.get(id=message_id)
    try:
        Messageboard_Message_Bookmark.objects.get(messageboard_message=this_message, user=this_user)
    except:
        Messageboard_Message_Bookmark.objects.create(messageboard_message=this_message, user=this_user)
    return redirect('/messageboard/'+message_id)

def unbookmark_message_process(request, message_id):
    if 'user_id' not in request.session:
        return redirect('/')

    this_user=User.objects.get(id=request.session['user_id'])
    this_message=Messageboard_Message.objects.get(id=message_id)
    try:
        Messageboard_Message_Bookmark.objects.get(messageboard_message=this_message, user=this_user).delete()
    except:
        messages.add_message(request, messages.ERROR, "INVALID APPROACH")
    return redirect('/messageboard/'+message_id)



def meetups(request):
    meetups_list=[]
    for meetup in Meetup.objects.all():
        meetups_list.append(meetup)

    if 'user_id' in request.session:
        data={
        "this_user":User.objects.get(id=request.session['user_id']),
        "meetups_list":meetups_list,
        }
        return render(request, 'APPNAME/meetups.html', data)
    elif 'business_id' in request.session:
        data={
        "this_business":Business.objects.get(id=request.session['business_id']),
        "meetups_list":meetups_list,
        }
        return render(request, 'APPNAME/meetups.html', data)
    else:
        return redirect('/')


def new_meetup(request):
    if 'user_id' not in request.session:
        return redirect('/')

    this_user=User.objects.get(id=request.session['user_id'])
    data={
    "this_user":this_user,
    }
    return render(request, 'APPNAME/new_meetup.html', data)

def new_meetup_process(request):
    if 'user_id' not in request.session:
        return redirect('/')

    this_user = User.objects.get(id=request.session['user_id'])
    data={
    'eventname':request.POST['eventname'],
    'location':request.POST['location'],
    'description':request.POST['description'],
    'date':request.POST['date'],
    'details':request.POST['details'],
    'this_user':this_user,
    }

    new_meetup=Meetup.objects.add(data)
    if new_meetup['errors_list']:
        for error in new_meetup['errors_list']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/meetups/new')
    else:
        messages.add_message(request, messages.ERROR, "Posted!")
        return redirect('/meetups')


def show_meetup(request, meetup_id):
    if 'user_id' not in request.session:
        return redirect('/')

    this_user=User.objects.get(id=request.session['user_id'])
    this_meetup = Meetup.objects.get(id=meetup_id)
    data={
    'this_meetup':this_meetup,
    "this_user":this_user,
    }
    return render(request, 'APPNAME/show_meetup.html', data)

def bookmark_meetup_process(request, meetup_id):
    if 'user_id' not in request.session:
        return redirect('/')

    this_user=User.objects.get(id=request.session['user_id'])
    this_meetup=Meetup.objects.get(id=meetup_id)
    try:
        Meetup_Bookmark.objects.get(meetup=this_meetup, user=this_user)
    except:
        Meetup_Bookmark.objects.create(meetup=this_meetup, user=this_user)
    return redirect('/meetups/'+meetup_id)

def unbookmark_meetup_process(request, meetup_id):
    if 'user_id' not in request.session:
        return redirect('/')

    this_user=User.objects.get(id=request.session['user_id'])
    this_meetup=Meetup.objects.get(id=meetup_id)
    try:
        Meetup_Bookmark.objects.get(meetup=this_meetup, user=this_user).delete()
    except:
        messages.add_message(request, messages.ERROR, "INVALID APPROACH")
    return redirect('/meetups/'+meetup_id)


def search_meetup(request):
    if 'user_id' not in request.session:
        return redirect('/')

    if request.method == 'GET':
        this_user=User.objects.get(id=request.session['user_id'])

        search_query = request.GET.get('search_box', None)
        print search_query
        search_list=[]
        for meetup in Meetup.objects.filter(eventname__contains=search_query):
            search_list.append(meetup)
        data={
        'search_list':search_list,
        "this_user":this_user,
        }
        return render(request, 'APPNAME/search_meetup.html', data)

def landing(request):
    return render(request, 'APPNAME/landing.html')


def deals(request):
    if 'user_id' in request.session:
        data={
        "this_user":User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'APPNAME/deals.html', data)

    elif 'business_id' in request.session:
        data={
        "this_business":Business.objects.get(id=request.session['business_id']),
        }
        return render(request, 'APPNAME/deals.html', data)

def createdeal(request):
    if 'business_id' not in request.session:
        return redirect('/')
    data={
    "this_business":Business.objects.get(id=request.session['business_id']),
    }
    return render(request, 'APPNAME/createdeal.html', data)


def getting(request):

    return render(request, 'APPNAME/createdeal.html', data)
def pickbusiness(request):
    r = requests.post('https://api.yelp.com/oauth2/token', data={'grant_type':"client_credentials", "client_id":"REPLACE","client_secret":"REPLACE"})

    tokendata = json.loads(r.text)
    print(tokendata, "**************")
    print (tokendata)
    accesstoken = tokendata["access_token"]
    accesstype = tokendata['token_type']
    expires = tokendata['expires_in']
    keyword = request.POST['keyword']
    location = request.POST['location']

    url_params={
    'term':keyword,
    "location":location
    }

    variable1 = requests.get('https://api.yelp.com/v3/businesses/search', headers={'Authorization': 'Bearer %s' % accesstoken}, params=url_params)
    # print type(variable1.text)
    response_data=json.loads(variable1.text)
    # print response_data
    # for business in response_data['businesses']:
    #     print business['name']
    data={
    "thedata":response_data
    }
    return render(request, 'APPNAME/pickbusiness.html', data)

def aboutus(request):
    return render(request, 'APPNAME/aboutus.html')

def contact(request):
    return render(request, 'APPNAME/contact.html')

def gyms(request):
    return render(request, 'APPNAME/gyms.html')

def careers(request):
    return render(request, 'APPNAME/careers.html')




def logout(request):
    request.session.clear()
    return redirect('/')

def form(request):
    data={
    'name':request.POST['name'],
    'address':request.POST['address1'],
    'city':request.POST['city'],
    'state':request.POST['state'],
    'theimage':request.POST['image']
    }
    return render(request, 'APPNAME/form.html', data)



#NO LONGER IN USE
# def messageboard(request):
#     this_user=User.objects.get(id=request.session['user_id'])
#     messages_list=[]
#     comments_list=[]
#     likes_list=[]
    # for message in Messageboard_Message.objects.all().order_by('-created_at'):
    #     messages_list.append(message)
#     for comment in Messageboard_Comment.objects.all():
#         comments_list.append(comment)
#     for like in Messageboard_Message_Like.objects.all():
#         likes_list.append(like)
#     data = {
#     "this_user":this_user,
#     "messages_list":messages_list,
#     "comments_list":comments_list,
#     "likes_list":likes_list,
#     }
#     return render(request, 'APPNAME/messageboard.html', data);
#
#
# def new_message_process(request):
#     this_user = User.objects.get(id=request.session['user_id'])
#     data = {
#     'message':request.POST['message'],
#     'this_user':this_user,
#     }
#     new_message=Messageboard_Message.objects.message(data)
#     if new_message['errors_list']:
#         for error in new_message['errors_list']:
#             messages.add_message(request, messages.ERROR, error)
#         return redirect('/messageboard')
#     else:
#         messages.add_message(request, messages.ERROR, "Posted!")
#         return redirect('/messageboard')
#
#
# def home_like_message(request, message_id):
#     this_user=User.objects.get(id=request.session['user_id'])
#     this_message=Messageboard_Message.objects.get(id=message_id)
#     try:
#         Messageboard_Message_Like.objects.get(messageboard_message=this_message, user=this_user)
#         messages.add_message(request, messages.ERROR, "INVALID APPROACH")
#     except:
#         Messageboard_Message_Like.objects.create(messageboard_message=this_message, user=this_user)
#     return redirect('/')
#
# def home_unlike_message(request, message_id):
#     this_user=User.objects.get(id=request.session['user_id'])
#     this_message=Messageboard_Message.objects.get(id=message_id)
#     try:
#         Messageboard_Message_Like.objects.get(messageboard_message=this_message, user=this_user).delete()
#     except:
#         messages.add_message(request, messages.ERROR, "INVALID APPROACH")
#     return redirect('/')
#
# def new_comment_process(request, message_id):
#     this_user = User.objects.get(id=request.session['user_id'])
#     this_message = Messageboard_Message.objects.get(id=message_id)
#     data = {
#     'comment':request.POST['comment'],
#     'this_user':this_user,
#     'this_message':this_message,
#     }
#     new_comment=Messageboard_Comment.objects.comment(data)
#     if new_comment['errors_list']:
#         for error in new_comment['errors_list']:
#             messages.add_message(request, messages.ERROR, error)
#         return redirect('/messageboard')
#     else:
#         messages.add_message(request, messages.ERROR, "Commented!")
#         return redirect('/messageboard')
