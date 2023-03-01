from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tarefa
from django.contrib import messages
from django.contrib.messages import constants
from .forms import TarefaForm
from django.contrib.auth.models import User


def about(request):
    return render(request, 'index.html')

@login_required(login_url=('/auth/login/'))
def home(request):
    if request.method == 'GET': # Se o metodo por GET retorna a pagina com todas as tarefas
        tarefas = Tarefa.objects.all().order_by('-created_at').filter(user=request.user)

        get_filter = request.GET.get('filter')

        if get_filter:
            tarefas = tarefas.filter(status=get_filter)

        user = request.user

        return render(request, 'home.html', {'tarefas': tarefas, 'user': user})

    elif request.method == 'POST': # se for post

        get_search = request.POST['search'] # pega o input que o usuario digitou
        
        if get_search == "" : # se o usuario não digitou nada mostre todas as tarefas

            tarefas = Tarefa.objects.all().order_by('-created_at').filter(user=request.user)

            return render(request, 'home.html', {'tarefas': tarefas})
        
        else: # se não, vai no banco e filtra pelo resultado e devolve pra ele!
            search_bd = Tarefa.objects.filter(titulo__icontains=get_search).filter(user=request.user)

            return render(request, 'home.html', {'tarefas':search_bd})

@login_required(login_url=('/auth/login/'))
def criar_tarefa(request):
    if request.method == 'GET':
        return render(request, 'criar_tarefa.html')
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')

        if len(titulo.strip()) == 0 or len(descricao.strip()) == 0:
            messages.info(request, 'Campos inválidos.')
            return redirect('/criar_tarefa/')

        try:
            tarefa = Tarefa(
                user=request.user,
                titulo=titulo,
                descricao=descricao,
            )

            tarefa.save()
        except:
            messages.info(request, 'Erro interno do sistema.')
            return redirect('/home/')

        messages.success(request, 'Tarefa criada com sucesso.')
        return redirect('/home/')


@login_required(login_url=('/auth/login'))
def ver_tarefa(request, id):
    ver_tarefa = get_object_or_404(Tarefa, pk=id)
    return render(request, 'ver_tarefa.html', {'ver_tarefa': ver_tarefa})


@login_required(login_url=('/auth/login'))
def editar_tarefa(request, id):
    tarefa = get_object_or_404(Tarefa, pk=id)
    editar_tarefa = TarefaForm(instance=tarefa)

    if request.method == 'POST':
        editar_tarefa = TarefaForm(request.POST, instance=tarefa)

        if editar_tarefa.is_valid():
            editar_tarefa.save()
            messages.info(request, 'Tarefa editada com sucesso')
            return redirect('/home/')

    context = {
        'tarefa': tarefa,
        'editar_tarefa': editar_tarefa
    }
    
    return render(request, 'editar_tarefa.html', context=context)


def concluir_tarefa(request, id):
    tarefa_concluida = get_object_or_404(Tarefa, pk=id)

    if(tarefa_concluida.status == 'doing'):
        tarefa_concluida.status = 'done'
        messages.info(request, f'{tarefa_concluida} concluida')
    else:
        tarefa_concluida.status = 'doing'
        messages.warning(request, f'{tarefa_concluida} não concluída')

    tarefa_concluida.save()

    return redirect('/home/')

@login_required(login_url=('/auth/login'))
def excluir_tarefa(request, id):
    excluir_tarefa = get_object_or_404(Tarefa, pk=id)
    
    if not excluir_tarefa.user == request.user:
        messages.info(request, 'Essa tarefa não é sua.')
        return redirect('/home/')

    excluir_tarefa.delete()

    messages.info(request, 'Tarefa deletada com sucesso.')

    return redirect('/home/')


def alterar_senha(request):

    if not request.user.is_authenticated:
        return redirect('/auth/login/?login_info=3')

    if request.method == 'POST':    

        senha_nova = request.POST.get('senha_nova')
        confirmar_senha = request.POST.get('confirmar_senha')


        if len(senha_nova.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Campos invalidos.')
            return redirect('/alterar_senha/')

        if len(senha_nova) < 8:
            messages.add_message(request, constants.ERROR, 'Senhas menor que 8 digitos')
            return redirect('/alterar_senha/')

        if senha_nova != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Senhas diferentes')
            return redirect('/alterar_senha/')

        try:
            user = User.objects.get(username__exact=request.user)
            user.set_password(senha_nova)
            user.save()

            messages.success(request, 'Senha alterada com sucesso.')
            return redirect('/home/')
        except:
            messages.error(request, 'Senha nao alterada. tente novamente mais tarde')
            return redirect('/alterar_senha/')
        
    else:
        return render(request, 'alterar_senha.html')
    

def alterar_senha_deslogado(request):

    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha_nova = request.POST.get('senha_nova')
        confirmar_senha = request.POST.get('confirmar_senha')


        if len(nome.strip()) == 0 or len(senha_nova.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            messages.error(request, 'Campos invalidos.')
            return redirect('/alterar_senha_deslogado/')

        if len(senha_nova) < 8:
            messages.error(request, 'Senha menor que 8 digitos.')
            return redirect('/alterar_senha_deslogado/')

        if senha_nova != confirmar_senha:
            messages.error(request, 'Senhas diferentes.')
            return redirect('/alterar_senha_deslogado/')

        try:
            user = User.objects.get(username=nome)
            user.set_password(senha_nova)
            user.save()

            messages.success(request, 'Senha alterada com sucesso.')
            return redirect('/auth/login/?login_info=5')
        except:
            messages.error(request, 'Senha nao alterada. tente novamente mais tarde')
            return redirect('/alterar_senha_deslogado/')

    return render(request, 'alterar_senha_deslogado.html')