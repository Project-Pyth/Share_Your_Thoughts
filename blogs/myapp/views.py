from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from .forms import  EditProfileForm, PersonalEditForm
from django.contrib.auth.forms import PasswordChangeForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import UserProfile,Blog,BlogComment
import matplotlib.pyplot as plt
import numpy as np
from .templatetags import extras
# Create your views here.
def index(request):
    return render(request,'myapp/index.html')


def register(request):
    if request.method == 'POST':
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        em = request.POST['email']
        un = request.POST['uname']
        pass1 = request.POST['pass']
        pass2 = request.POST['pass2']
        if pass1 == pass2:
            if User.objects.filter(username=un).exists():
                messages.error(request,'Username already taken')
                return redirect('/register')
            elif User.objects.filter(email=em).exists():
                messages.error(request,'Email already taken')
                return redirect('/register')
            else:
                user = User.objects.create_user(username=un, email=em, password=pass1, first_name=fn, last_name=ln)
                user.save()
                messages.info(request, 'You are Registered successfully !')
                return redirect('/login')

        else:
            messages.error(request,'Password does not match')
            return redirect('register')

    else:
        return render(request,"myapp/Signin.html")

def login(request):
    if request.method == 'POST':
        un = request.POST['uname']
        pass1 = request.POST['pass']

        user = auth.authenticate(username=un,password=pass1)
        if user is not None:
            auth.login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid credentials')
            return redirect('/login')
    else:
        return render(request,'myapp/login.html')

@login_required
def dashboard(request):
    context = {}
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        pro = Blog.objects.filter(user_id=request.user.id)
        context['user'] = user
        if len(pro)!=0:
            pro1 = Blog.objects.values('category').distinct().order_by('category')
            pro2 = Blog.objects.filter(category='Historical',user_id=request.user.id).count()
            pro3 = Blog.objects.filter(category='Literature',user_id=request.user.id).count()
            pro4 = Blog.objects.filter(category='Technical',user_id=request.user.id).count()
            context['pro'] = pro
            context['pro1'] = pro1
            context['pro2'] = pro2
            context['pro3'] = pro3
            context['pro4'] = pro4
        return render(request,'myapp/template.html',context)


@login_required
def blog(request):
    if request.method=='POST':
        category = request.POST['category']
        title = request.POST['title']
        blog = request.POST['blog']
        bl = Blog(category=category,title=title,blog=blog,user_id=request.user)
        bl.save()
        messages.success(request,"Blog has been submitted successfully")
        return render(request,'myapp/blog.html')
    else:
        return render(request,'myapp/blog.html')


def logout(request):
    auth.logout(request)
    return redirect("/")

@login_required
def profile(request,pk=None):
    context = {}
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        pro = UserProfile.objects.get(user=request.user.id)

        context['user'] = user
        context['pro'] = pro
        return render(request,'myapp/profile/index.html',context)

@login_required
@transaction.atomic
def edit_profile(request):
        if request.method=='POST':
            user_form = EditProfileForm(request.POST, instance=request.user)
            profile_form = PersonalEditForm(request.POST, request.FILES or None, instance=request.user.userprofile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('profile')
            else:
                messages.info(request,"not updated ")
        else:
            user_form = EditProfileForm(instance=request.user)
            profile_form = PersonalEditForm(instance=request.user.userprofile)
        return render(request, 'myapp/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form})
@login_required
def change_password(request):
    if request.method == "POST":
        form=PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('profile')
    else:
        form=PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request,'myapp/change_password.html',args)

def view_blog(request):
    if request.method == "GET":
        b=Blog.objects.filter(user_id=request.user)
        return render(request,'myapp/view_blog.html',{'b':b})

@login_required
def blogpost(request,id):
    post=Blog.objects.filter(id=id).first()
    post.views = post.views+1
    post.save()
    pro = UserProfile.objects.get(user=request.user)
    comments=BlogComment.objects.filter(post=post,parent=None)
    replies=BlogComment.objects.filter(post=post).exclude(parent=None)
    replydict={}
    for reply in replies:
        if reply.parent.sno not in replydict.keys():
            replydict[reply.parent.sno]=[reply]
        else:
            replydict[reply.parent.sno].append(reply)
    context={'pro':pro,'post':post,'comments':comments,'user':request.user,'replydict':replydict}


    return render(request,'myapp/blogpost.html',context)

def postcomment(request):
    if request.method=='POST':
        comment=request.POST.get('comment')
        user=request.user
        postsno=request.POST.get('postsno')
        post=Blog.objects.get(id=postsno)
        parentsno=request.POST.get('parentsno')
        if parentsno=='':
            comment=BlogComment(comment=comment,user=user,post=post)
        else:
            parent=BlogComment.objects.get(sno=parentsno)
            comment=BlogComment(comment=comment,user=user,post=post,parent=parent)
        comment.save()
    return redirect(f'/blogpost/{post.id}')

def allblog(request):
    if request.method == "GET":
        b=Blog.objects.filter(status=True).order_by
        return render(request,'myapp/allblogs.html',{'b':b})


def search_blogs(request):
    if request.method == 'POST':
        search = request.POST['search']
        content = Blog.objects.filter(category = search,status=True)
        if len(content) == 0:
            return render(request,'myapp/Not_found.html')
        else:
            return render(request,'myapp/search_blogs.html',{'content':content})
    else:
        return render(request,'myapp/index.html')

def about_us(request):
    return render(request,'myapp/about_us.html')

def error_404_view(request,exception):
    return render(request,'myapp/404_error.html')

