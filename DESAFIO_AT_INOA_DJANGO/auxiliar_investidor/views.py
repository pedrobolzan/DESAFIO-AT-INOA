from django.shortcuts import render, redirect
from .models import Ativo, TunelParametro, Cotacao
from .forms import FormAtivo, ParametroTunelForm

def home(request):

    ativos_all = Ativo.objects.all()

    return render(request, 'home.html', {'ativos': ativos_all})

def create_ativo(request):

    if request.method == 'POST':
        form = FormAtivo(request.POST)

        if form.is_valid():
            form.save()

    else:
        form = FormAtivo()

    return render(request, 'create_ativo.html', {'form': form})

def update_ativo(request, ativo_id):

    ativo = Ativo.objects.get(pk=ativo_id)

    try:
        parametros = TunelParametro.objects.get(ativo=ativo)
    except TunelParametro.DoesNotExist:
        parametros = None

    if request.method == 'POST':
        form = ParametroTunelForm(request.POST, instance=parametros)
        if form.is_valid():
            parametros = form.save(commit=False)
            parametros.ativo = ativo
            parametros.save()
            return redirect('home')
    else:
        form = ParametroTunelForm(instance=parametros)

    return render(request, 'update_parametros.html', {'form': form, 'ativo': ativo})

def get_cotacoes(request, ativo_id):

    ativo = Ativo.objects.get(pk=ativo_id)

    cotacoes = Cotacao.objects.filter(ativo=ativo).order_by('-data_hora')

    return render(request, 'get_cotacoes.html', {'cotacoes': cotacoes, 'ativo': ativo})
