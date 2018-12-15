from django.db import models
from django.conf import settings


class TipoAvaliacao(models.Model):
    # Nome do tipo de avaliação
    nome = models.CharField(
        primary_key=True, max_length=settings.MAX_LENGTH_TIPO_AVALIACAO,
        help_text='Por exemplo: "Prova", "Lista" ou "Testinho"',
        null=False, blank=False
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "tipo de avaliação"
        verbose_name_plural = "tipos de avaliações"
        ordering = ['nome']


class Periodo(models.Model):
    # Nome do período
    nome = models.CharField(
        primary_key=True, max_length=settings.MAX_LENGTH_PERIODO,
        help_text='Por exemplo: "Primeiro semestre" ou "Férias de verão"',
        null=False, blank=False
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "período"
        verbose_name_plural = "períodos"
        ordering = ['nome']


class Disciplina(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        codigos = []
        for codigo in CodigoDisciplina.objects.filter(disciplina=self).all():
            codigos.append(codigo.codigo)
        return 'Disciplina #{disciplina.id} <-- {codigos}'.format(disciplina=self, codigos=codigos)

    class Meta:
        verbose_name = "disciplina"
        verbose_name_plural = "disciplinas"
        # Pegamos as registradas mais recentemente
        ordering = ['-id']


class CodigoDisciplina(models.Model):
    # Disciplina à qual associamos esse código
    disciplina = models.ForeignKey('Disciplina', on_delete=models.CASCADE)
    # Código da disciplina
    codigo = models.CharField(
        primary_key=True, max_length=settings.MAX_LENGTH_CODIGO_DISCIPLINA,
        help_text='Por exemplo, "MC202", "F328"',
        null=False, blank=False
    )

    def __str__(self):
        return 'codigo={modelo.codigo} --> id={modelo.disciplina.id}'.format(modelo=self)

    class Meta:
        verbose_name = "código da disciplina"
        verbose_name_plural = "códigos de disciplinas"
        ordering = ['disciplina__id', 'codigo']


# Nome do arquivo da avaliação a ser salva
def determinar_nome_arquivo(instance, filename):
    # Começamos com a lista de atributos obrigatórios
    atributos = [
        str(instance.disciplina.id),
        instance.tipo_avaliacao.nome + str(instance.quantificador_avaliacao),
    ]

    # Incluímos com o número de opcionais
    if instance.docente is not None:
        atributos.append(instance.docente)
    if instance.periodo is not None:
        atributos.append(instance.periodo.nome)
    if instance.ano is not None:
        atributos.append(str(instance.ano))

    # Pegamos a extensão do nome do arquivo
    if len(filename) > 0:
        split = filename.split('.')
        extensao = '.' + split[len(split) - 1].replace(' ', '')
    else:
        extensao = '.extensao_desconhecida'

    return settings.PROVAS_PATH + '-'.join(atributos) + extensao


class Avaliacao(models.Model):
    # Disciplina associada à avaliação (criamos utilizando o nome do formulário
    # associado a alguma instância de disciplina que representará todos os
    # nomes)
    disciplina = models.ForeignKey('Disciplina', on_delete=models.PROTECT)

    # Docente que fez a avaliação (pode ser omitido)
    docente = models.CharField(
        max_length=settings.MAX_LENGTH_DOCENTE,
        help_text='Tente tornar o mais próximo do e-mail ou "código" do docente. Por exemplo, Sara Diaz Cardell do IMECC possui e-mail/site com "sdcardell", então usamos "sdcardell".',
        null=True, blank=True
    )

    #   Tipo da avaliação
    # Não podem ser omitidos -- quem está enviando deve saber o que está
    # enviando..
    # Por exemplo "Prova"
    tipo_avaliacao = models.ForeignKey('TipoAvaliacao', on_delete=models.PROTECT, null=False, blank=False)
    # Por exemplo 1, para formar "Prova 1". Pode ser dispensado
    quantificador_avaliacao = models.PositiveIntegerField(null=True, blank=True)

    #   Semestre da avaliação (pode ser omitido)
    # Período
    periodo = models.ForeignKey('Periodo', on_delete=models.PROTECT, null=True, blank=True)
    # Ano
    ano = models.PositiveIntegerField(null=True, blank=True)

    # Arquivo associado à avaliação
    arquivo = models.FileField(upload_to=determinar_nome_arquivo)

    # Se a avaliação está visível a tod*s
    visivel = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return ' - '.join([
            str(self.disciplina),
            self.docente,
            str(self.tipo_avaliacao),
            str(self.quantificador_avaliacao),
            str(self.periodo),
            str(self.ano),
            'visivel' if self.visivel else 'invisível'
        ])

    class Meta:
        verbose_name = "avaliação"
        verbose_name_plural = "avaliações"
        ordering = ['-ano', '-periodo', 'docente', 'disciplina__id']
