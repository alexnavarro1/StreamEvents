from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from urllib.parse import urlparse, parse_qs


User = get_user_model()

CATEGORY_CHOICES = [
    ('gaming','Gaming'),('music','Música'),('talk','Xerrades'),
    ('education','Educació'),('sports','Esports'),('entertainment','Entreteniment'),
    ('technology','Tecnologia'),('art','Art i Creativitat'),('other','Altres')
]

STATUS_CHOICES = [
    ('scheduled','Programat'),('live','En Directe'),
    ('finished','Finalitzat'),('cancelled','Cancel·lat')
]

class Event(models.Model):
    """
    Model que representa un esdeveniment en streaming.
    Conté tota la informació necessària per gestionar, programar i mostrar l'esdeveniment.
    Camps:
    - title: Títol de l'esdeveniment.
    - description: Explicació detallada de què tractarà l'esdeveniment.
    - creator: Usuari que ha creat l'esdeveniment (clau forana).
    - category: Temàtica de l'esdeveniment (Gaming, Música, etc.).
    - scheduled_date: Data i hora en què està previst l'inici.
    - status: Estat actual (Programat, En Directe, Finalitzat, Cancel·lat).
    - thumbnail: Imatge de portada (es redimensiona automàticament).
    - max_viewers: Límit o estimació d'espectadors.
    - tags: Paraules clau separades per comes.
    - stream_url: Enllaç directe a la plataforma de streaming (YouTube, Twitch).
    """
    title = models.CharField(max_length=200, verbose_name="Títol")
    description = models.TextField(verbose_name="Descripció")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Creador")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Categoria")
    scheduled_date = models.DateTimeField(verbose_name="Data programada")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Estat", default='scheduled')
    thumbnail = models.ImageField(upload_to='events/thumbnails/', blank=True, null=True, default='events/default_thumbnail.jpg', verbose_name="Imatge de portada")
    max_viewers = models.PositiveIntegerField(default=100, verbose_name="Màxim d'espectadors")
    is_featured = models.BooleanField(default=False, verbose_name="És destacat?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creat el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualitzat el")
    tags = models.CharField(max_length=500, blank=True, verbose_name="Etiquetes")
    stream_url = models.URLField(max_length=500, blank=True, verbose_name="URL del Streaming")

    def save(self, *args, **kwargs):
        """
        Sobreescriu el mètode save per processar la imatge abans de guardar-la.
        Si hi ha una imatge pujada, la redimensiona a 600x600 px màxim
        per optimitzar l'espai i la velocitat de càrrega.
        """
        super().save(*args, **kwargs)
        
        if self.thumbnail:
            try:
                from PIL import Image
                img = Image.open(self.thumbnail.path)
                
                # Comprovar si la imatge és més gran que 600px
                if img.height > 600 or img.width > 600:
                    output_size = (600, 600)
                    img.thumbnail(output_size)
                    img.save(self.thumbnail.path)
            except Exception as e:
                # Registra l'error si PIL falla (opcional)
                print(f"Error rescalant la imatge: {e}")

    def __str__(self):
        """Retorna el títol com a representació en text de l'objecte."""
        return self.title

    def get_absolute_url(self):
        """Retorna l'URL permanent per accedir al detall d'aquest esdeveniment."""
        return reverse('events:event_detail', args=[self.pk])

    @property
    def is_live(self):
        """Propietat booleana per saber ràpidament si l'esdeveniment està EN DIRECTE."""
        return self.status == 'live'

    @property
    def is_upcoming(self):
        """Propietat booleana per saber si l'esdeveniment està PROGRAMAT."""
        return self.status == 'scheduled'

    def get_tags_list(self):
        """
        Converteix la cadena de text 'tags' (separada per comes) en una llista de Python.
        Exemple: "gaming, fun" -> ['gaming', 'fun']
        Utilitzat a les plantilles per iterar sobre les etiquetes.
        """
        return [t.strip() for t in self.tags.split(',') if t]
    
    def get_stream_embed_url(self):
        """
        Genera i retorna l'URL formatada per ser incrustada en un <iframe>.
        Detecta automàticament si l'URL és de YouTube o Twitch i l'adapta.
        
        Mètode:
        1. Analitza l'URL original (stream_url).
        2. Si és YouTube: extreu l'ID del vídeo i construeix l'URL /embed/.
        3. Si és Twitch: extreu el nom del canal i afegeix els paràmetres 'parent'
           necessaris per evitar errors de seguretat (CSP).
        4. Si no és cap dels dos, retorna l'URL tal qual.
        """
        if not self.stream_url:
            return ''
        
        parsed = urlparse(self.stream_url)
        
        # Processament per a YouTube
        if 'youtube.com' in parsed.netloc or 'youtu.be' in parsed.netloc:
            # Cas: youtube.com/watch?v=xxxx
            if parsed.netloc == 'youtu.be':
                video_id = parsed.path[1:]
            else:
                query = parse_qs(parsed.query)
                video_id = query.get('v', [None])[0]
            if video_id:
                return f'https://www.youtube.com/embed/{video_id}'
        
        # Processament per a Twitch
        if 'twitch.tv' in parsed.netloc:
            path_parts = parsed.path.strip('/').split('/')
            if len(path_parts) >= 1:
                channel = path_parts[0]
                # Afegim parent=localhost i parent=127.0.0.1 per permetre l'execució en local
                return f'https://player.twitch.tv/?channel={channel}&parent=localhost&parent=127.0.0.1&autoplay=false'

        # Altres casos: retornar l'URL original
        return self.stream_url

    # Semantic Search Fields
    embedding = models.JSONField(blank=True, null=True)  # llista de floats
    embedding_model = models.CharField(max_length=200, blank=True, null=True)
    embedding_updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        """
        Opcions metadades del model.
        - ordering: Ordena per defecte els esdeveniments per data de creació (més nous primer).
        """
        ordering = ['-created_at']
        verbose_name = 'Esdeveniment'
        verbose_name_plural = 'Esdeveniments'
