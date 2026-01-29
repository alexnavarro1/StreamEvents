from django.shortcuts import render
from django.utils import timezone

from events.models import Event
from .services.embeddings import embed_text, model_name
from .services.ranker import cosine_top_k

def _event_text(e: Event) -> str:
    parts = [
        e.title or "",
        e.description or "",
        e.category or "",
        e.tags or "",
    ]
    return " | ".join([p.strip() for p in parts if p and p.strip()])

def semantic_search(request):
    q = (request.GET.get("q") or "").strip()
    only_future = request.GET.get("future", "1") == "0"

    results = []
    if q:
        q_vec = embed_text(q)

        # Carreguem candidats de la DB de forma optimitzada
        qs = Event.objects.all().only('id', 'title', 'description', 'category', 'scheduled_date', 'embedding')
        if only_future:
            qs = qs.filter(scheduled_date__gte=timezone.now())

        items = []
        for e in qs:
            emb = getattr(e, "embedding", None)
            if emb:
                items.append((e, emb))

        ranked = cosine_top_k(q_vec, items, k=20)
        results = ranked

    context = {
        "query": q,
        "results": results,  # llista de tuples (Event, score)
        "only_future": only_future,
        "embedding_model": model_name(),
    }
    return render(request, "semantic_search/search.html", context)
