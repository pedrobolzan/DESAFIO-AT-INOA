from django.shortcuts import render, redirect, get_object_or_404
from .models import Ativo, TunelParametro, Cotacao
from .forms import FormAtivo, ParametroTunelForm
from .scheduler.monitorar_ativos import create_monitorar_ativos_scheduler, remove_monitoramento

def home(request):
    query = request.GET.get('busca_ativo')
    if query:
        ativos = Ativo.objects.filter(codigo__icontains=query)
    else:
        ativos = Ativo.objects.all()

    monitorados = Ativo.objects.filter(tunelparametro__isnull=False)

    return render(request, 'home.html', {'ativos': ativos, 'monitorados': monitorados})

def create_ativo(request):

    if request.method == 'POST':
        form = FormAtivo(request.POST)

        if form.is_valid():
            form.save()

    else:
        form = FormAtivo()

    return render(request, 'create_ativo.html', {'form': form})

def update_ativo(request, ativo_id):
    
    ativo = get_object_or_404(Ativo, pk=ativo_id)

    try:
        parametros = TunelParametro.objects.get(ativo=ativo)
    except TunelParametro.DoesNotExist:
        parametros = None

    if request.method == 'POST':
        form = ParametroTunelForm(request.POST, instance=parametros)
        if form.is_valid():

            if parametros:
                parametros.delete()
            
            parametros = form.save(commit=False)
            parametros.ativo = ativo
            parametros.save()
            
            create_monitorar_ativos_scheduler(ativo.id, parametros)
            
            return redirect('home')
    else:
        form = ParametroTunelForm(instance=parametros)

    return render(request, 'update_parametros.html', {'form': form, 'ativo': ativo})

def get_cotacoes(request, ativo_id):

    ativo = Ativo.objects.get(pk=ativo_id)

    cotacoes = Cotacao.objects.filter(ativo=ativo).order_by('-data_hora')

    return render(request, 'get_cotacoes.html', {'cotacoes': cotacoes, 'ativo': ativo})

def delete_ativo(request, ativo_id):
    ativo = get_object_or_404(Ativo, pk=ativo_id)

    try:
        parametros = TunelParametro.objects.get(ativo=ativo)
    except TunelParametro.DoesNotExist:
        return redirect('home')

    parametros.delete()
    remove_monitoramento(ativo_id)

    return redirect('home')
