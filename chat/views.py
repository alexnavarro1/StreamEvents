from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from events.models import Event
from .models import ChatMessage
from .forms import ChatMessageForm

@login_required
@require_POST
@login_required
@require_POST
def chat_send_message(request, event_pk):
    """
    Guarda un missatge nou.
    Només si l'esdeveniment està en directe.
    """
    event = get_object_or_404(Event, pk=event_pk)
    
    # Si no està 'live', no deixem escriure
    if event.status != 'live':
        return JsonResponse({'success': False, 'errors': {'global': "L'esdeveniment no està en directe."}}, status=403)
    
    form = ChatMessageForm(request.POST)
    if form.is_valid():
        msg = form.save(commit=False)
        msg.event = event
        msg.user = request.user
        msg.save()
        
        # Enviem el nou missatge en JSON
        return JsonResponse({
            'success': True,
            'message': {
                'id': msg.id,
                'user': msg.user.username,
                'display_name': msg.get_user_display_name(),
                'message': msg.message,
                'created_at': msg.get_time_since(),
                'can_delete': msg.can_delete(request.user),
                'is_highlighted': msg.is_highlighted
            }
        })
    else:
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

def chat_load_messages(request, event_pk):
    """
    Carrega missatges nous (es crida cada 3 segons).
    """
    event = get_object_or_404(Event, pk=event_pk)
    
    # 1. Recuperem els últims 100
    recent_messages = event.messages.all().order_by('-created_at')[:100]
    
    # 2. Filtrem esborrats i ens quedem amb 50
    valid_messages = [m for m in recent_messages if not m.is_deleted]
    messages_list = valid_messages[:50][::-1]
    
    data = []
    user = request.user if request.user.is_authenticated else None
    
    for msg in messages_list:
        can_delete = False
        if request.user.is_authenticated:
            can_delete = msg.can_delete(request.user)

        data.append({
            'id': msg.id,
            'user': msg.user.username,
            'display_name': msg.get_user_display_name(),
            'message': msg.message,
            'created_at': msg.get_time_since(),
            'can_delete': can_delete,
            'is_highlighted': msg.is_highlighted
        })
        
    return JsonResponse({'messages': data})

@login_required
@require_POST
def chat_delete_message(request, message_pk):
    """
    Elimina un missatge (només propietari o admin).
    """
    msg = get_object_or_404(ChatMessage, pk=message_pk)
    
    if msg.can_delete(request.user):
        msg.is_deleted = True # Amagar missatge
        msg.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Sense permís'}, status=403)

@login_required
@require_POST
def chat_highlight_message(request, message_pk):
    """
    Destaca missatge (només creador event).
    """
    msg = get_object_or_404(ChatMessage, pk=message_pk)
    
    if request.user == msg.event.creator:
        msg.is_highlighted = not msg.is_highlighted
        msg.save()
        return JsonResponse({'success': True, 'is_highlighted': msg.is_highlighted})
    else:
        return JsonResponse({'success': False, 'error': 'Sense permís'}, status=403)
