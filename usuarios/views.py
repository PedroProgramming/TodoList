from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as logar, logout
from .forms import CaptchaForm




def cadastro(request):

    if request.user.is_authenticated:
        messages.add_message(request, constants.ERROR, 'Você já esta logado no sistema!')
        return redirect('/home/?verificacao_user=1')


    if request.method == 'GET':
        cadastro_info = request.GET.get('cadastro_info')
        captcha = CaptchaForm()

        context = {
            'cadastro_info': cadastro_info,
            'captcha': captcha
        }

        return render(request, 'cadastro.html', context=context)
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            return redirect('/auth/cadastro/?cadastro_info=1')

        if len(senha) < 8:
            return redirect('/auth/cadastro/?cadastro_info=2')

        if senha != confirmar_senha: 
            return redirect('/auth/cadastro/?cadastro_info=3')

        captcha = CaptchaForm(request.POST)

        if captcha.is_valid():

            try:
                user = User.objects.create_user(
                    username=nome,
                    email=email,
                    password=senha,
                )
                return redirect('/auth/cadastro/?cadastro_info=0')

            except:
                return redirect('/auth/cadastro/?cadastro_info=4')

        else:
            return redirect('/auth/cadastro/?cadastro_info=5')
        
def login(request):

    if request.user.is_authenticated:
        return redirect('/home/?verificacao_user=1')

    if request.method == 'GET':
        login_info = request.GET.get('login_info')

        context = {
            'login_info': login_info,
        }

        return render(request, 'login.html', context=context)
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')

        user = authenticate(username=nome,
                            password=senha,)

        if len(nome.strip()) == 0 or len(senha.strip()) == 0:
            return redirect('/auth/login/?login_info=1')

        

        if user is not None:
            logar(request, user)

            return redirect('/home/')
        else:
            return redirect('/auth/login/?login_info=4')
        
        
def sair(request):
    logout(request)
    return redirect('/auth/login/?login_info=2')