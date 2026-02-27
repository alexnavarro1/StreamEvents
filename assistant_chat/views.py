import json
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .services.retriever import retrieve_events
from .services.prompts import build_prompt
from .services.llm_ollama import generate_stream

def chat_page(request):
    return render(request, "assistant_chat/chat.html")

@csrf_exempt
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    message = (payload.get("message") or "").strip()
    only_future = bool(payload.get("only_future", True))

    if not message:
        return JsonResponse({"error": "Empty message"}, status=400)

    ranked = retrieve_events(message, only_future=only_future, k=8)

    candidates = []
    for e, score in ranked:
        candidates.append({
            "id": int(e.pk),
            "title": e.title,
            "scheduled_date": e.scheduled_date.isoformat() if e.scheduled_date else None,
            "category": e.category,
            "tags": e.tags or "",
            "url": e.get_absolute_url(),
            "score": round(float(score), 3),
        })

    prompt = build_prompt(message, candidates)

    def event_stream():
        yield f"data: {json.dumps({'type': 'metadata', 'events': candidates[:3]})}\n\n"
        
        try:
            for chunk in generate_stream(prompt):
                yield f"data: {json.dumps({'type': 'text', 'text': chunk})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'text', 'text': f' [Error de model IA: {str(e)}]'})}\n\n"
            
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
