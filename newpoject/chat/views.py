from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from . import forms
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from . import models
from django.http import HttpResponseRedirect
from django.shortcuts import render

class Home(View):
    # מחלקה המייצגת את הדף הסופי , דף הצ'אט
    def get(self,request,*args, **kwargs):
        # הפעולה מקבלת את נתוני הלקוח ואת בקשתו להתחבר למערכת
        # פעולה הבודקת האם המשתמש שהוזן במערכת תקין, אם כן תעביר אותו לדף הצ'אט
        # ואם לא תטען מחדש את דף ההתחברות בצירוף הודעה מתאימה
        if not request.user.is_authenticated:
            return redirect('/login/')
        username = models.UserProfile.objects.get(id = request.user.id)
        args = {
                "friends_list":username.friends.all()[::-1],
                "search_users":username.filter_friends_out()
            }
        return render(request,'localchat.html', args)
class Register(View):
    def get(self,request):
        # הפעולה מקבלת את נתוני הלקוח ואת הבקשה לעבור לדף ההתחברות
        # פעולה המציגה את דף ההתחברות
        return render(request,'login.html')
    def post(self,request):
        # הפעולה מקבלת את נתוני הלקוח ואת בקשתו להתחבר למערכת
        # במידה והמשתמש תקין המערכת תעביר אותו לדף הצ'אט המיועד לו
        # במידה והייתה שגיאת התחברות תחזיר המערכת הודעה מתאימה
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(**data)
            if not user is None:
                login(request,user)
                return redirect("/local_chat")
            else:
                messages.error(request,'username or password incorrect...')
                return redirect("/login/")

class SignUp(View):
    # מחלקה המייצגת את דף ההרשמה
    def get(self,request):
        # הפעולה מקבלת את נתוני הלקוח ואת הבקשה לעבור לדף ההרשמה
        # הפעולה מציגה את דף ההרשמה
        return render(request,"signup.html")
    
    def post(self,request):
        # הפעולה מקבלת את נתוני הלקוח ואת בקשתו להרשם למערכת
        # מידה והמשתמש תקין המערכת תרשום אותו כמשתמש תקין ותעביר אותו לדף הצ'אט
        # במידה והייתה שגיאת התחברות תחזיר המערכת הודעה מתאימה
        form = forms.SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            username,password = data['username'],data['password']
            re_password,image = data['re_password'],data['image']
            if password != re_password:
                messages.error(request,"passwords don't match...")
                return redirect("/signup")
            if not User.objects.filter(username=username).exists(): 
                user = User.objects.create_user(username = username,password = password)
                customuser = models.UserProfile(user = user,image = image,id = user.id)
                customuser.save()
                login(request,user)
                return redirect("/local_chat")
            else:
                messages.error(request,'The username already taken...')
        return redirect('/signup')


def logout_page(request):
    # הפעולה מקבלת את הבקשה להתנתק מהמערכת
    # הפעולה תחזיר את המשתמש לדף ההתחברות
    logout(request)
    return redirect('/login')
def add_friend(request,friend_id):    
    # פעולה המוסיפה חבר לרשימה
    print(friend_id)
    friend = models.UserProfile.objects.get(id = friend_id)
    my_user = models.UserProfile.objects.get(id = request.user.id)
    chat_id = f"{my_user.id}Q{friend_id}"
    chat = models.Chat.objects.create(id_chat = chat_id)

    chat.people.add(friend,my_user)
    friend.friends.add(my_user)
    my_user.friends.add(friend)

    return redirect('/local_chat')