import datetime

from django import forms
from django.conf import settings
from django.core.validators import RegexValidator

from .models import TipoAvaliacao, Periodo


def exemplo_ano():
    hoje = datetime.datetime.now()
    return 'Por exemplo: "{ano}", "{ano_anterior}".'.format(ano=hoje.year, ano_anterior=(hoje.year - 2))

class FormAvaliacao(forms.Form):
    # Disciplina: obrigatória, iremos pesquisar o nome posteriormente
    # Exemplo mínimo: "F328", exemplo máximo: "MA311"
    codigo_disciplina = forms.CharField(
        required=True,
        validators=[
            RegexValidator(
                r'([A-Za-z]{1}[ ]?[0-9]{3})|([A-Za-z]{2}[0-9]{3})',
                'Código não respeita formato padrão de código de disciplinas.'
            )
        ],
        label='Código da disciplina*',
        help_text='Apenas letras e números, sem traços ou espaços. Por exemplo: "f328", "ma311", "MC404".',
    )

    # Docente que fez a prova: não obrigatória, precisaremos prestar atenção
    docente = forms.CharField(
        required=False,
        max_length=settings.MAX_LENGTH_DOCENTE,
        validators = [
            RegexValidator(
                r'[A-Za-z0-9_]*',
                'Utilize apenas caracteres alfanuméricos e underline.'
            )
        ],
        label='"Código" d* docente que fez a prova',
        help_text='Tente preencher com o nome no e-mail ou site d* docente. Por exemplo: Sara Diaz Cardell do IMECC possui e-mail e site com o código "sdcardell". Se não conhecer ou identificar, coloque apenas o sobrenome.',
    )

    # Tipo de avaliação: obrigatório
    tipo_avaliacao = forms.ModelChoiceField(
        required=True,
        label='Tipo de avaliação*',
        queryset=TipoAvaliacao.objects.all()
    )

    # Quantificador da avaliação: não obrigatório
    quantificador = forms.IntegerField(
        required=False,
        min_value=1,
        label='Número da avaliação',
        help_text='Seguindo as respostas do item anterior, formaríamos: "Prova 1", "Exame", "Lista de exercícios 4", "Testinho 3". Esse número distingue P1 da P2, da P3.'
    )

    # Período e ano da avaliação
    periodo = forms.ModelChoiceField(
        required=False,
        label='Período da avaliação',
        queryset=Periodo.objects.all(),
        empty_label='Não encontrei o período que procuro ou não sei'
    )
    ano = forms.IntegerField(
        required=False,
        min_value=1970,
        label='Ano da avaliação',
        help_text=exemplo_ano()
    )

    # Se a avaliação possui resolução
    possui_resolucao = forms.BooleanField(
        required=False,
        label='Avaliação possui resolução*',
        help_text='Deve dizer se o arquivo que está enviando possui resolução dos exercícios ou se é apenas os enunciados de questões (não possui resolução).'
    )

    #   Arquivo a ser enviado
    # Exige tratamento especial:
    # https://docs.djangoproject.com/en/2.1/ref/forms/api/#binding-uploaded-files
    arquivo = forms.FileField(
        required=True,
        allow_empty_file=False,
        label='Arquivo da avaliação*',
        help_text='Prefira o formato PDF! Há ferramentas que convertem fotos em PDF ou ainda vários PDF em um único PDF.'
    )


    def clean_codigo_disciplina(self):
        codigo_disciplina = self.cleaned_data['codigo_disciplina']
        return codigo_disciplina.replace(' ', '')


    def clean_docente(self):
        docente = self.cleaned_data['docente']
        return docente.lower()


    # Colocamos uma ordem mais natural
    field_order = [
        'codigo_disciplina',
        'tipo_avaliacao',
        'quantificador',
        'possui_resolucao',
        'periodo',
        'ano',
        'docente',
        'arquivo'
    ]
