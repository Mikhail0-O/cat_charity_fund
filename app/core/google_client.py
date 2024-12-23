from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from settings import INFO, SCOPES


cred = ServiceAccountCreds(scopes=SCOPES, **INFO)


async def get_service():
    async with Aiogoogle(service_account_creds=cred) as aiogoogle:
        yield aiogoogle
