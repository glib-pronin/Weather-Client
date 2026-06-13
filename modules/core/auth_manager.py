class AuthManager:
    def __init__(self, auth_service, api_client, storage, on_logout):
        self.auth_service = auth_service 
        self.api_client = api_client 
        self.storage = storage 
        self.on_logout = on_logout 
        self.user = None
        self.pending_email = None
        self.api_client.auth_failed_handler = self.logout
        self.api_client.token_refreshed_handler = self.save_access

    async def set_tokens(self, access, refresh):
        await self.storage.set('access', access)
        await self.storage.set('refresh', refresh)
        self.api_client.set_access(access)
        self.api_client.set_refresh(refresh)

    async def load_tokens(self):
        access = await self.storage.get('access')
        refresh = await self.storage.get('refresh')
        if access:
            self.api_client.set_access(access)
            self.api_client.set_refresh(refresh)

    async def login(self, email, password):
        res = await self.auth_service.login(email, password)
        if res.status_code == 403:
            self.pending_email = email
            return False, 'need_verify'
        if res.status_code != 200:
            return False, 'error'
        data = res.json()
        await self.set_tokens(data['access'], data['refresh'])
        await self.me()
        return True, ''
    
    async def register(self, email, password, confirm_password):
        res = await self.auth_service.register(email, password, confirm_password)
        if res.status_code not in (200, 201):
            return False
        self.pending_email = email
        return True
    
    async def verify_email(self, code):
        res = await self.auth_service.verify_email(self.pending_email, code)
        if res.status_code != 200:
            return False
        data = res.json()
        self.pending_email = None
        await self.set_tokens(data['access'], data['refresh'])
        await self.me()
        return True

    async def me(self):
        res = await self.auth_service.me()
        if res.status_code != 200:
            return False
        self.user = res.json()
        return True

    async def logout(self):
        await self.storage.remove('access')
        await self.storage.remove('refresh')
        self.api_client.set_access(None)
        self.api_client.set_refresh(None)
        self.user = None
        self.on_logout()

    async def save_access(self, access):
        await self.storage.set('access', access)

    def set_user(self, new_user_data):
        self.user = new_user_data