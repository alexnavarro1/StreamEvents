import json

def build_prompt(user_message: str, candidates: list[dict]) -> str:
    # candidates: [{id,title,scheduled_date,category,tags,url,score}, ...]
    context_json = json.dumps(candidates, ensure_ascii=False, indent=2)

    return f"""
Ets un assistent que recomana esdeveniments del lloc StreamEvents.
IMPORTANT:
- NOMÉS pots recomanar esdeveniments que apareguin en el CONTEXT.
- Sigues intel·ligent: relaciona conceptes de la cerca de l'usuari amb categories més àmplies (per exemple, relaciona 'futbol', 'bàsquet' o un equip esportiu amb la categoria 'sports', 'pòdcast' amb 'talk', etc.).
- No inventis esdeveniments, dates, ni URLs.
- Si realment creus que cap dels esdeveniments del context no encaixa ni mínimament, digues-ho i demana aclariments.

Respon en català i en format de text explicatiu de forma amable. No utilitzis JSON. Recomana els esdeveniments parlant d'ells i donant context.

CONTEXT (llista d'esdeveniments disponibles):
{context_json}

Petició de l'usuari: {user_message}
""".strip()
