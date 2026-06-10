from .api_client import ApiClient
from .router import resolve_route
from .auth_manager import AuthManager
from ..services import AuthService, LocationService

class AppContainer:
    def __init__(self, on_logout, storage):
        self._api_client = ApiClient()
        self.auth_manager = AuthManager(AuthService(self._api_client), self._api_client, storage, on_logout)
        self.resolve_route = resolve_route
        self.location_service = LocationService(self._api_client)
    
    async def on_close(self, e):
        await self._api_client.close()
        