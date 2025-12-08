from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventCreationForm, EventUpdateForm, EventSearchForm
from django.core.paginator import Paginator
from datetime import datetime, time

def event_list_view(request):
    form = EventSearchForm(request.GET or None)
    events = Event.objects.all().order_by('-created_at')

    if form.is_valid():
        search = form.cleaned_data.get('search')
        category = form.cleaned_data.get('category')
        status = form.cleaned_data.get('status')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')

        if search:
            events = events.filter(title__icontains=search)

        if category:
            events = events.filter(category=category)

        if status:
            events = events.filter(status=status)
            
        if date_from:
            # Solució per a Djongo: la cerca per __date no està suportada
            start_dt = datetime.combine(date_from, time.min)
            events = events.filter(scheduled_date__gte=start_dt)
            
        if date_to:
            # Solució per a Djongo: la cerca per __date no està suportada
            end_dt = datetime.combine(date_to, time.max)
            events = events.filter(scheduled_date__lte=end_dt)

    # Paginación
    paginator = Paginator(events, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'events': page_obj
    }
    return render(request, 'events/event_list.html', context)

def event_detail_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request,'events/event_detail.html',{'event':event})

@login_required
def event_create_view(request):
    """
    Vista per crear un NO UN esdeveniment.
    Requereix que l'usuari estigui autenticat (@login_required).
    
    Funcionament:
    1. Si la petició és POST (enviar formulari):
       - Es valida el formulari amb les dades i fitxers enviats.
       - Si és vàlid, es guarda l'esdeveniment assignant l'usuari actual com a creador.
       - Es redirigeix a la pàgina de detall de l'esdeveniment creat.
    2. Si la petició és GET (veure pàgina):
       - Es mostra un formulari buit.
    """
    if request.method=='POST':
        form = EventCreationForm(request.POST,request.FILES)
        if form.is_valid():
            e=form.save(commit=False)
            e.creator=request.user
            e.save()
            return redirect(e.get_absolute_url())
    else:
        form = EventCreationForm()
    return render(request,'events/event_form.html',{'form':form})

@login_required
def event_update_view(request, pk):
    """
    Vista per editar un esdeveniment existent.
    - Només permet editar si l'usuari actual és el creador (filtre creator=request.user).
    - utilitza get_object_or_404 per llançar un error 404 si l'esdeveniment no existeix o no és seu.
    """
    event = get_object_or_404(Event, pk=pk, creator=request.user)
    form = EventUpdateForm(request.POST or None, request.FILES or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect(event.get_absolute_url())
    return render(request,'events/event_form.html',{'form':form})

@login_required
def event_delete_view(request, pk):
    """
    Vista per eliminar un esdeveniment.
    - També protegeix que només el creador pugui eliminar-lo.
    - Si la petició és POST (confirmació), elimina l'esdeveniment.
    - Si és GET, mostra la pàgina de confirmació.
    """
    event = get_object_or_404(Event, pk=pk, creator=request.user)
    if request.method=='POST':
        event.delete()
        return redirect('events:event_list')
    return render(request,'events/event_confirm_delete.html',{'event':event})

@login_required
def my_events_view(request):
    """
    Vista que mostra només els esdeveniments creats per l'usuari actual.
    Ideal per al 'Tauler de Control' de l'usuari.
    """
    events = Event.objects.filter(creator=request.user)
    return render(request,'events/my_events.html',{'events':events})

def events_by_category_view(request, category):
    """
    Vista per filtrar esdeveniments per una categoria específica directament des de la URL.
    Exemple: /events/category/gaming/
    """
    events = Event.objects.filter(category=category)
    return render(request,'events/event_list.html',{'events':events})
