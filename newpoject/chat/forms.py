from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class RegisterForm(forms.Form):
    # ממחלקה המייצגת את תכונות המשתמש בעת ההתחברות
    username = forms.CharField(max_length = 15)
    password = forms.CharField(max_length = 20)
class SignUpForm(forms.Form):
    # ממחלקה המייצגת את תכונות המשתמש בעת ההרשמה
    username = forms.CharField(max_length = 15)
    password = forms.CharField(max_length = 20)
    re_password = forms.CharField(max_length = 20)
    image = forms.ImageField()
