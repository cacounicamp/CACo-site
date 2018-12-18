"""
Django settings for djangosite project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
from datetime import timedelta

import os
import json


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

configuracao_path = os.path.join(BASE_DIR, 'config.json')
if os.path.exists(configuracao_path):
    with open(configuracao_path) as arquivo:
        configuracao = json.load(arquivo)
else:
    raise ValueError('Arquivo de configuração "config.json" não existente!')


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = configuracao['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = configuracao['DEBUG']

ALLOWED_HOSTS = configuracao['ALLOWED_HOSTS']

# Application definition

INSTALLED_APPS = [
    # Padrão
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Para ediçao de páginas estáticas (requer o comando 'collectstatic' do
    # django)
    'ckeditor',
    'ckeditor_uploader',

    # Nossos aplicativos
    'paginas_estaticas',
    'ouvidoria',
    'noticias',
    'atas',
    'gestoes',
    'representantes_discentes',
    'membros',
    'banco_de_provas',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangosite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangosite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgresql',
        'USER': 'postgresql',
        'PASSWORD': 'postgresql',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

APPEND_SLASH = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = '/static/'

# Para o comando 'collectstatic'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Arquivos estáticos a serem servidos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "djangosite/static/"),
]

# Configurações do CKEditor
CKEDITOR_CONFIGS = {
    'default': {
        'extraPlugins': 'sourcedialog,',
        'removePlugins': 'sourcearea,',
        'toolbar': 'full',
    }
}

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'
# Para onde os arquivos de mídia serão enviados
CKEDITOR_UPLOAD_PATH = 'uploaded/'
# Para onde as provas serão enviadas (dentro de MEDIA_ROOT)
PROVAS_PATH = 'provas/'

# Dados para captcha (página de contatos e membros)
CAPTCHA_SITE_KEY = configuracao['CAPTCHA_SITE_KEY']
CAPTCHA_SECRET_KEY = configuracao['CAPTCHA_SECRET_KEY']

# Configurações de e-mail para página de contato
EMAIL_HOST = configuracao['EMAIL_HOST']
EMAIL_PORT = configuracao['EMAIL_PORT']
EMAIL_HOST_USER = configuracao['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = configuracao['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = configuracao['EMAIL_USE_TLS']
EMAIL_USE_SSL = configuracao['EMAIL_USE_SSL']
# Qual o e-mail que aparecerá como remetente
EMAIL_CONTATO_REMETENTE = configuracao['EMAIL_CONTATO_REMETENTE']
# Qual o(s) destinatário(s) para os e-mails da ouvidoria (página '/contato/')
EMAIL_CONTATO_DESTINATARIO = configuracao['EMAIL_CONTATO_DESTINATARIO']
# Qual o e-mail que aparecerá na página de contato em caso de falha
EMAIL_CONTATO_DISPLAY = configuracao['EMAIL_CONTATO_DISPLAY']

# Definimos o formato do assunto do e-mail
EMAIL_ASSUNTO_BASE = """[CACo] {assunto}"""


#
# PARAMETRIZAÇÃO DA EXIBIÇÃO DO SITE
#

# Notícias por página no site
NOTICIAS_POR_PAGINA = 5
NOTICIAS_POR_PAGINA_RAIZ = 3

# Atas por página no site
ATAS_BARRA_LATERAL = 3
ATAS_POR_PAGINA = 3
ATAS_REUNIAO_POR_PAGINA = 7
ATAS_ASSEMBLEIA_POR_PAGINA = 7

# Gestões por página no site
GESTOES_POR_PAGINA = 10

# Anos de representantes discentes no site
REPRESENTANTES_DISCENTES_ANOS_POR_PAGINA = 10

# Caminho até o estatuto (será utilizado na página de membros)
ESTATUTO_URL = '/media/estatuto.pdf'

# Tempo para confirmação dos membros (seja para vincular, seja para
# desvincular-se). Se ultrapassar esse tempo, será inválido.
TEMPO_CONFIRMACAO_MEMBROS = timedelta(days=1)


#
# PARAMETRIZAÇÃO DO BANCO DE DADOS
#

# MAX_LENGTH_* define o tamanho máximo em caracteres para cada item

# Nome de pessoas, comissões, gestões e instituições
MAX_LENGTH_NOME = 160
MAX_LENGTH_APELIDO = 32
MAX_LENGTH_CARGOS = 64
# Página de atas
MAX_LENGTH_HIGHLIGHT_ATAS = 320
# Página de notícias
MAX_LENGTH_TITULO_NOTICIAS = 64
MAX_LENGTH_RESUMO_NOTICIAS = 128
# Página de contato
MAX_LENGTH_EMAIL = 320
MAX_LENGTH_ASSUNTO_CONTATO = 160
MAX_LENGTH_MENSAGEM_CONTATO = 4096
# Páginas estáticas
MAX_LEGNTH_TITULO_PAGINA = 32
MAX_LEGNTH_ENDERECO_PAGINA = 192
# Menu do site
MAX_LENGTH_TITULO_ITEM_MENU = 32
MAX_LEGNTH_ENDERECO_MENU = 512
# Banco de provas
MAX_LENGTH_MAX_AVALIACOES = 100
MAX_LENGTH_TIPO_AVALIACAO = 64
MAX_LENGTH_PERIODO = 64
MAX_LENGTH_CODIGO_DISCIPLINA = 6
MAX_LENGTH_DOCENTE = 32             # Tão grande quanto um apelido

# Lista de cursos
CURSOS = (
    ('CC', 'Ciência da computação'),
    ('EC', 'Engenharia de computação'),
    ('Pós', 'Pós-graduação do IC'),
)
# Máximo caractere para a sigla do curso (automatizada pela tupla acima)
MAX_LENGTH_CURSOS = 0
for sigla, _ in CURSOS:
    tamanho_sigla = len(sigla)
    if tamanho_sigla >= MAX_LENGTH_CURSOS:
        MAX_LENGTH_CURSOS = tamanho_sigla + 1
