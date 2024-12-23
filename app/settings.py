from app.core.config import settings


MIN_LENGTH = 1
MAX_LENGTH = 100
TOKEN_LIFETIME_SECONDS = 3600
MIN_LENGTH_PASSWORD = 3
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

INFO = {
    'type': settings.type,
    'project_id': settings.project_id,
    'private_key_id': settings.private_key_id,
    'private_key': settings.private_key_2,
    'client_email': settings.client_email,
    'client_id': settings.client_id,
    'auth_uri': settings.auth_uri,
    'token_uri': settings.token_uri,
    'auth_provider_x509_cert_url': settings.auth_provider_x509_cert_url,
    'client_x509_cert_url': settings.client_x509_cert_url
}

FORMAT = "%Y/%m/%d %H:%M:%S"
