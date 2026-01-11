from django.db import models
from django.conf import settings
from django.utils.timesince import timesince

class ChatMessage(models.Model):
    """
    Model per guardar els missatges del xat.
    """
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='messages'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    
    # Text del missatge (màxim 500 lletres)
    message = models.TextField(max_length=500)
    
    # Data automàtica
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Si és True, el missatge no es veu (paperera)
    is_deleted = models.BooleanField(default=False)
    
    # Si és True, surt en groc
    is_highlighted = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Missatge de Xat'
        verbose_name_plural = 'Missatges de Xat'

    def __str__(self):
        return f"{self.user.username}: {self.message[:50]}"

    def can_delete(self, user):
        """
        Diu si l'usuari pot esborrar aquest missatge.
        (Autor, Creador de l'event o Admin).
        """
        if not user.is_authenticated:
            return False
        return (
            user == self.user or
            user == self.event.creator or
            user.is_staff
        )

    def get_user_display_name(self):
        """
        Retorna el nom que s'ha de mostrar al xat.
        """
        if hasattr(self.user, 'display_name') and self.user.display_name:
            return self.user.display_name
        return self.user.username

    def get_time_since(self):
        """
        Exemple: "fa 5 minuts"
        """
        return f"fa {timesince(self.created_at)}"
