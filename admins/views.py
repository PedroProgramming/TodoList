from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from .forms import UserForm


def home(request):

    adm = request.user
    return render(request, 'admin.html', {'adm': adm})

def user_system(request):
    
    if request.method == 'GET':
        all_users = User.objects.all()
        adm = request.user

        return render(request, 'usuarios.html', {'all_users': all_users, 'adm': adm})
    
    elif request.method == 'POST':
        adm = request.user
        search = request.POST['search']

        if search == "":
            all_users = User.objects.all()
            
            return render(request, 'usuarios.html', {'all_users': all_users, 'adm': adm})
        else:
            search_user = User.objects.filter(username__icontains=search)

            return render(request, 'usuarios.html', {'all_users': search_user, 'adm': adm})


def view_user(request, id_user):

    if request.method == 'GET':
        user_view = User.objects.get(pk=id_user)

        context = {
            'user_view': user_view
        }

        return render(request, 'view_user.html', context=context)


def delete_user(request, id):
    user = User.objects.get(pk=id)

    try:
        user.delete()
    except:
        messages.success(request, 'Usuario nao pode ser deletado.')
        return render(request, 'view_user.html')
    

    messages.success(request, 'Usuario deletado com sucesso')
    return redirect('/admin_sistema/usuarios/')


def edit_user(request, id):

    if request.method == 'GET':
        user = User.objects.get(pk=id)
        user_edit = UserForm(instance=user)

        context = {
            'user': user,
            'user_edit': user_edit,
        }

        return render(request, 'edit_user.html', context=context)
    
    elif request.method == 'POST':
        
        user = User.objects.get(pk=id)

        user_edit = UserForm(request.POST, instance=user)

        if user_edit.is_valid():
            user_edit.save()
            return redirect(f'/admin_sistema/usuarios/')
        else:
            messages.error(request, 'Dados nao salvos. tente novamente mais tarde')
            return redirect('/admin_sistema/usuarios/')