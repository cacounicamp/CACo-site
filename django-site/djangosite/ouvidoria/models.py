from django.db import models
from django.conf import settings


# Modelo para página de contato caso o envio do e-mail falhe.
class FormularioContato(models.Model):
    contato = models.EmailField('E-mail para contato', blank=True, max_length=settings.MAX_LENGTH_EMAIL)
    assunto = models.CharField('Assunto*', max_length=settings.MAX_LENGTH_ASSUNTO_CONTATO, null=False, blank=False)
    mensagem = models.TextField('Mensagem*', max_length=settings.MAX_LENGTH_MENSAGEM_CONTATO, null=False, blank=False)
    email_enviado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "formulário de contato"
        verbose_name_plural = "formulários de contato"
