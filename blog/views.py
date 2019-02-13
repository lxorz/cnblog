from django.shortcuts import render,HttpResponse,redirect
from PIL import Image,ImageDraw,ImageFont
import random

from django.http import JsonResponse
from io import BytesIO
from django.contrib import auth
from django import forms
from django.forms import widgets

# Create your views here.

def login(request):
    
    if request.method=="POST":
        response={"user":None,"msg":None}
        user=request.POST.get("user")
        pwd=request.POST.get("pwd")
        valid_code=request.POST.get("valid_code")
        valid_code_str=request.session.get("valid_code_str")
        if valid_code.upper()==valid_code_str.upper():
            user=auth.authenticate(username=user,password=pwd)
            if user:
                auth.login(request,user)  #request.user=当前登录对象
                response["user"]=user.username
            else:
                response["msg"]="username or password error!"

        else:
            response["msg"]="valid code error!"
        return JsonResponse(response)


    return render(request,"login.html")

def get_validCode_img(request):
    
    def get_random_color():
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    img=Image.new("RGB",(262,34),color="black")
    draw=ImageDraw.Draw(img)
    kumo_font=ImageFont.truetype("static/font/kumo.ttf",size=32)

    valid_code_str=""
    for i in range(5):
        random_num=str(random.randint(0,9))
        random_low_alpha=chr(random.randint(95,133))
        random_upper_alpha=chr(random.randint(66,90))
        random_char=random.choice([random_num,random_low_alpha,random_upper_alpha])
        valid_code_str+=random_char

        draw.text((i*50+20,5),random_char,"white",font=kumo_font)

    #生成验证图片方式1
    # with open("validCode.png","wb") as f:
    #     img.save(f,"png")
    #
    # with open("validCode.png","rb") as f:
    #     data = f.read()


    request.session["valid_code_str"]=valid_code_str
    # 生成验证图片方式2


    f=BytesIO()
    img.save(f,"png")
    data=f.getvalue()
    return HttpResponse(data)



def index(request):
    return render(request,"index.html")


class UserForm(forms.Form):
    user=forms.CharField(max_length=32,label="用户名",
                         widget=widgets.TextInput(attrs={"class":"form-control"}))
    pwd=forms.CharField(max_length=32,label="密码",
                        widget=widgets.PasswordInput(attrs={"class":"form-control"}))
    re_pwd=forms.CharField(max_length=32,label="确认密码",
                           widget=widgets.PasswordInput(attrs={"class":"form-control"}))
    email=forms.EmailField(max_length=32,label="邮箱",
                           widget=widgets.EmailInput(attrs={"class":"form-control"}))


def register(request):
    if request.is_ajax():
        form = UserForm(request.POST)
        response={"user":None,"msg":None}
        if form.is_valid():
            response["user"]=form.cleaned_data.get("user")
        else:
            response["msg"]=form.errors
        return JsonResponse(response)
    form=UserForm()
    return render(request,"register.html",{"form":form})