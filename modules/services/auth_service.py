class AuthService:
    def __init__(self, api):
        self.api = api

    async def login(self, email, password):
        return await self.api.request(
            method='POST',
            url='login/',
            json={'username': email, 'password': password}
        )
    
    async def register(self, email, password, confirm_password):
        return await self.api.request(
            method='POST',
            url='register/',
            json={'email': email, 'password': password, 'confirm_password': confirm_password}
        )

    async def me(self):
        return await self.api.auth_request('GET', 'me/')
