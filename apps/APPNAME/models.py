# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re, datetime, bcrypt
EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def register(self, data):
        errors = []
        if len(data['first_name'])<2:
            errors.append("First name must consist 2 or more characters.")
        if not data['first_name'].isalpha():
            errors.append("First name must be only letters.")
        if len(data['last_name'])<2:
            errors.append("Last name must consist 2 or more characters.")
        if not data['last_name'].isalpha():
            errors.append("Last name must be only letters.")
        if data['email']=="":
            errors.append("Email address may not be blank.")
        if data['question1']=="":
            errors.append("Security question 1 may not be blank.")
        if data['answer1']=="":
            errors.append("Answer for security question 1 may not be blank.")
        if data['question2']=="":
            errors.append("Security question 2 may not be blank.")
        if data['answer2']=="":
            errors.append("Answer for security question 2 may not be blank.")
        try:
            User.objects.get(email=data['email'])
            errors.append("Entered email already exists.")
        except:
            try:
                Business.objects.get(email=data['email'])
                errors.append("Entered email already exists.")
            except:
                pass
            pass
        if not EMAIL_REGEX.match(data['email']):
            errors.append("Please enter a valid email address.")
        if len(data['password'])<8:
            errors.append("Password must be at least 8 characters long")
        if data['password']!=data['confirm_password']:
            errors.append("Password and Confirm Password do not match.")

        if len(errors)>0:
            return{
            'new':None,
            'errors_list':errors,
            }
        else:
            data['password']=bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            new_user=User.objects.create(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=data['password'], question1=data['question1'], answer1=data['answer1'], question2=data['question2'], answer2=data['answer2'])
            return{
            'new':new_user,
            'errors_list':None,
            }

    def login(self, data):
        errors = []
        try:
            found_user = User.objects.get(email=data['email'])
            if bcrypt.hashpw(data['password'].encode('utf-8'), found_user.password.encode('utf-8')) != found_user.password.encode('utf-8'):
                errors.append("Incorrect password.")
        except:
            errors.append("Entered email does not exist. (email is case sensitive)")

        if len(errors)>0:
            return{
            'logged_user':None,
            'errors_list':errors,
            }
        else:
            return{
            'logged_user':found_user,
            'errors_list':None,
            }

    def changepassword(self, data):
        errors = []
        this_user = data['this_user']
        if bcrypt.hashpw(data['current_password'].encode('utf-8'), this_user.password.encode('utf-8')) != this_user.password.encode('utf-8'):
            errors.append("Current password and input do not match.")
        if data['new_password']!=data['confirm_password']:
            errors.append("New password and confirm password do not match")
        if len(data['new_password'])<8:
            errors.append("New password must be 8 characters or longer.")

        if len(errors)>0:
            return{
            'user':None,
            'errors_list':errors,
            }
        else:
            this_user.password = bcrypt.hashpw(data['new_password'].encode('utf-8'), bcrypt.gensalt())
            this_user.save()
            return{
            'user':this_user,
            'errors_list':None,
            }
    def reset_password(self, data):
        errors = []
        this_user = data['this_user']
        if len(data['password'])<8:
            errors.append("Password must be at least 8 characters long.")
        if data['password']!=data['confirm_password']:
            errors.append("New password and confirm password do not match.")

        if len(errors)>0:
            return {
            'user':None,
            'errors_list':errors,
            }
        else:
            this_user.password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            this_user.save()
            return {
            'user':this_user,
            'errors_list':None,
            }

class BusinessManager(models.Manager):
    def register(self, data):
        errors = []
        if data['name']=="":
            errors.append("Business name may not be blank.")
        if data['address']=="":
            errors.append("Address may not be blank.")
        if data['city']=="":
            errors.append("City may not be blank.")
        if data['state']=="":
            errors.append("State may not be blank.")
        if data['zipcode']=="":
            errors.append("Zip code may not be blank.")
        if data['email']=="":
            errors.append("Email address may not be blank.")
        if data['question1']=="":
            errors.append("Security question 1 may not be blank.")
        if data['answer1']=="":
            errors.append("Answer for security question 1 may not be blank.")
        if data['question2']=="":
            errors.append("Security question 2 may not be blank.")
        if data['answer2']=="":
            errors.append("Answer for security question 2 may not be blank.")
        try:
            User.objects.get(email=data['email'])
            errors.append("Entered email already exists.")
        except:
            try:
                Business.objects.get(email=data['email'])
                errors.append("Entered email already exists.")
            except:
                pass
            pass
        if not EMAIL_REGEX.match(data['email']):
            errors.append("Please enter a valid email address.")
        if len(data['password'])<8:
            errors.append("Password must be at least 8 characters long.")
        if data['password']!=data['confirm_password']:
            errors.append("Password and confirm Password do not match.")

        if len(errors)>0:
            return{
            'new':None,
            'errors_list':errors,
            }
        else:
            data['password']=bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            new_business=Business.objects.create(name=data['name'], address=data['address'], city=data['city'], state=data['state'], zipcode=data['zipcode'], email=data['email'], password=data['password'], question1=data['question1'], answer1=data['answer1'], question2=data['question2'], answer2=data['answer2'])
            return{
            'new':new_business,
            'errors_list':None,
            }

    def login(self,data):
        errors = []
        try:
            found_business = Business.objects.get(email=data['email'])
            if bcrypt.hashpw(data['password'].encode('utf-8'), found_business.password.encode('utf-8')) != found_business.password.encode('utf-8'):
                errors.append("Incorrect password.")
        except:
            errors.append("Entered email does not exist. (email is case sensitive)")

        if len(errors)>0:
            return{
            'logged_business':None,
            'errors_list':errors,
            }
        else:
            return{
            'logged_business':found_business,
            'errors_list':None,
            }

    def changepassword(self, data):
        errors = []
        this_business = data['this_business']
        if bcrypt.hashpw(data['current_password'].encode('utf-8'), this_business.password.encode('utf-8')) != this_business.password.encode('utf-8'):
            errors.append("Current password and input do not match.")
        if data['new_password']!=data['confirm_password']:
            errors.append("New password and confirm password do not match")
        if len(data['new_password'])<8:
            errors.append("New password must be 8 characters or longer.")
        if len(errors)>0:
            return{
            'business':None,
            'errors_list':errors,
            }
        else:
            this_business.password = bcrypt.hashpw(data['new_password'].encode('utf-8'), bcrypt.gensalt())
            this_business.save()
            return{
            'business':this_business,
            'errors_list':None,
            }
    def reset_password(self, data):
        errors = []
        this_business = data['this_business']
        if len(data['password'])<8:
            errors.append("Password must be at least 8 characters long.")
        if data['password']!=data['confirm_password']:
            errors.append("New password and confirm password do not match.")

        if len(errors)>0:
            return {
            'business':None,
            'errors_list':errors,
            }
        else:
            this_business.password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            this_business.save()
            return {
            'business':this_business,
            'errors_list':None,
            }


    def reset_password(self, data):
        errors = []
        this_business = data['this_business']
        if len(data['password'])<8:
            errors.append("Password must be at least 8 characters long.")
        if data['password']!=data['confirm_password']:
            errors.append("New password and confirm password do not match.")

        if len(errors)>0:
            return {
            'business':None,
            'errors_list':errors,
            }
        else:
            this_business.password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            this_business.save()
            return {
            'business':this_business,
            'errors_list':None,
            }

class DealManager(models.Manager):
    def creation(self,data):
        errors=[]
        if data['title']=="":
            errors.append("Title may not be blank")
        if len(data['address'])<3:
            errors.append("address must but more than 3 characters")
        if data['city'] == "":
            errors.append("city cannot be blank")
        if data['price'] == "":
            errors.append("price cannot be blank")
        if data['fine_print']=="":
            errors.append("Fine Print cannot be blank")
        if data['deal_type']=="":
            errors.append("Deal type cannot be blank")
        if data['contact_email']=="":
            errors.append("Contact email cannot be blank")
        if data['start_date']=="":
            errors.append("Start date cannot be blank")
        if data['end_date']=="":
            errors.append("End date cannot be blank")
        if datetime.datetime.strptime(data['end_date'], '%Y-%m-%d') < datetime.datetime.strptime(data['start_date'], '%Y-%m-%d'):
            errors.append("End date cannot be a date prior to the start date.")
        elif datetime.datetime.strptime(data['end_date'], '%Y-%m-%d') <= datetime.datetime.now():
            errors.append("The deal has already expired.")
        if len(data['details'])<5:
            errors.append("details cannot be less than 5 characters")

        if len(errors)>0:
            return{
            'new':None,
            'errors_list':errors,
            }
        else:
            new_deal=Deal.objects.create(business=data['business'], address=data['address'], city=data['city'], state=data['state'], deal_type=data['deal_type'], contact_email=data['contact_email'], title=data['title'], details=data['details'], fine_print=data['fine_print'], start_date=data['start_date'], price=data['price'], end_date=data['end_date'])
            return{
            'new':new_deal,
            'errors_list':None
            }

class MessageboardManager(models.Manager):
    def post(self, data):
        errors = []
        if data['title']=="":
            errors.append("Title may not be blank.")
        if data['message']=="":
            errors.append("Message may not be blank.")

        if len(errors)>0:
            return{
            'new':None,
            'errors_list':errors,
            }
        else:
            new_message=Messageboard_Message.objects.create(title=data['title'], message=data['message'], user=data['this_user'])
            return{
            'new':new_message,
            'errors_list':None,
            }
    def comment(self, data):
        errors = []
        if data['comment']=="":
            errors.append("Comment may not be blank.")

        if len(errors)>0:
            return{
            'new':None,
            'errors_list':errors,
            }
        else:
            try:
                if data['this_user']:
                    new_comment=Messageboard_Comment.objects.create(comment=data['comment'], messageboard_message=data['this_message'], user=data['this_user'])
            except:
                if data['this_business']:
                    new_comment=Messageboard_Comment.objects.create(comment=data['comment'], messageboard_message=data['this_message'], business=data['this_business'])
            return{
            'new':new_comment,
            'errors_list':None,
            }



class MeetupManager(models.Manager):
    def add(self, data):
        errors = []
        if len(data['eventname'])<3:
            errors.append("Eventname must be 3 or more characters.")
        if data['location']=="":
            errors.append("Location cannot be blank.")
        if data['description']=="":
            errors.append("Description cannot be blank.")
        if data['date']=="":
            errors.append("Meetup date cannot be blank.")
        elif datetime.datetime.strptime(data['date'], '%Y-%m-%d') <= datetime.datetime.now():
            errors.append("Meetup date must be in future.")
        if data['details']=="":
            errors.append("Details cannot be blank.")

        if len(errors)>0:
            return{
            'new':None,
            'errors_list':errors,
            }
        else:
            new_meetup=Meetup.objects.create(eventname=data['eventname'], description=data['description'], location=data['location'], date=data['date'], details=data['details'], user=data['this_user'])
            return{
            'new':new_meetup,
            'errors_list':None,
            }

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    question1=models.CharField(max_length=255)
    answer1=models.CharField(max_length=255)
    question2=models.CharField(max_length=255)
    answer2=models.CharField(max_length=255)
    image=models.FileField(upload_to="profile_picture", null=True, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

class Business(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    question1 = models.CharField(max_length=255)
    answer1 = models.CharField(max_length=255)
    question2 = models.CharField(max_length=255)
    answer2 = models.CharField(max_length=255)
    image=models.FileField(upload_to="business_picture", null=True, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=BusinessManager()




class Meetup(models.Model):
    eventname=models.CharField(max_length=255)
    description=models.CharField(max_length=55)
    details=models.CharField(max_length=255)
    location=models.CharField(max_length=255)
    date=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User, related_name="meetups")
    objects=MeetupManager()

class Meetup_Bookmark(models.Model):
    user=models.ForeignKey(User, related_name="meetup_bookmarks", null=True)
    business=models.ForeignKey(Business, related_name="meetup_bookmarks", null=True)
    meetup=models.ForeignKey(Meetup, related_name="meetup_bookmarks")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Meetup_Like(models.Model):
    user=models.ForeignKey(User, related_name="meetup_likes", null=True)
    business=models.ForeignKey(Business, related_name="meetup_likes", null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    meetup=models.ForeignKey(Meetup, related_name="meetup_likes")

class Meetup_Comment(models.Model):
    comment=models.CharField(max_length=255)
    user=models.ForeignKey(User)
    meetup=models.ForeignKey(Meetup, related_name="meetup_comments")

class Messageboard_Message(models.Model):
    title=models.CharField(max_length=255)
    message=models.CharField(max_length=255)
    image=models.FileField(upload_to="messageboard_message", null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User, related_name="messageboard_messages")
    objects=MessageboardManager()

class Messageboard_Message_Like(models.Model):
    user=models.ForeignKey(User, related_name="messageboard_message_likes", null=True)
    business=models.ForeignKey(Business, related_name="messageboard_message_likes", null=True)
    messageboard_message=models.ForeignKey(Messageboard_Message, related_name="messageboard_message_likes")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Messageboard_Message_Bookmark(models.Model):
    user=models.ForeignKey(User, related_name="messageboard_message_bookmarks", null=True)
    business=models.ForeignKey(Business, related_name="messageboard_message_bookmarks", null=True)
    messageboard_message=models.ForeignKey(Messageboard_Message, related_name="messageboard_message_bookmarks")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Messageboard_Comment(models.Model):
    user=models.ForeignKey(User, related_name="messageboard_comments", null=True)
    business=models.ForeignKey(Business, related_name="messageboard_comments", null=True)
    messageboard_message=models.ForeignKey(Messageboard_Message, related_name="messageboard_comments")
    comment=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=MessageboardManager()

class Messageboard_Message_View(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    messageboard_message=models.ForeignKey(Messageboard_Message, related_name="messageboard_message_views")



class Deal(models.Model):
    business=models.ForeignKey(Business, related_name="deals")
    address=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    state=models.CharField(max_length=255)
    deal_type=models.CharField(max_length=255)
    contact_email=models.CharField(max_length=255)
    title=models.CharField(max_length=255)
    details=models.CharField(max_length=255)
    fine_print=models.CharField(max_length=255)
    price=models.IntegerField(null=False)
    start_date=models.CharField(max_length=255)
    end_date=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=DealManager()




# class Deal(models.Model):
#     name=models.CharField(max_length=255)
#     description=models.CharField(max_length=255)
#     date_to=models.CharField(max_length=255)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)
#     user=models.ForeignKey(User, related_name="deals")









# NO LONGER BEING USED
# class MessageboardManager(models.Manager):
#     def message(self, data):
#         errors = []
#         if data['message']=="":
#             errors.append("Message may not be blank.")
#
#         if len(errors)>0:
#             return{
#             'new':None,
#             'errors_list':errors,
#             }
#         else:
#             new_message=Messageboard_Message.objects.create(message=data['message'], user=data['this_user'])
#             return{
#             'new':new_message,
#             'errors_list':None,
#             }
#
#     def comment(self, data):
#         errors = []
#         if data['comment']=="":
#             errors.append("Comment may not be blank.")
#
#         if len(errors)>0:
#             return{
#             'new':None,
#             'errors_list':errors,
#             }
#         else:
#             new_comment=Messageboard_Comment.objects.create(comment=data['comment'], user=data['this_user'], messageboard_message=data['this_message'])
#             return{
#             'new':new_comment,
#             'errors_list':None,
#             }
#
# class Messageboard_Message(models.Model):
#     message=models.CharField(max_length=255)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)
#     user=models.ForeignKey(User, related_name="messageboard_messages")
#     objects=MessageboardManager()
#
#
# class Messageboard_Comment(models.Model):
#     comment=models.CharField(max_length=255)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)
#     user=models.ForeignKey(User, related_name="messageboard_comments")
#     messageboard_message=models.ForeignKey(Messageboard_Message, related_name="messageboard_comments")
#     objects=MessageboardManager()
#
# class Messageboard_Comment_Like(models.Model):
#     user=models.ForeignKey(User, related_name="messageboard_comment_likes")
#     messageboard_comment=models.ForeignKey(Messageboard_Comment, related_name="messageboard_comment_likes")
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)
