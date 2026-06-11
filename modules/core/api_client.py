import httpx

class ApiClient:
    def __init__(self):
        self.access = None
        self.refresh = None

        self.base_url = 'http://127.0.0.1:8000/api/'
        self.client = None

        self.auth_failed_handler = None
        self.token_refreshed_handler = None

    def set_access(self, access):
        self.access = access

    def set_refresh(self, refresh):
        self.refresh = refresh

    def build_url(self, url):
        if url.startswith(('http://', 'https://')):
            return url
        return f'{self.base_url}{url}'

    def get_headers(self):
        headers = {'Content-Type': 'application/json'}
        if self.access:
            headers.update({'Authorization': f'Bearer {self.access}'})
        return headers
    
    async def request(self, method, url, json=None, headers=None, params=None):
        if self.client is None:
            self.client = httpx.AsyncClient()
        return await self.client.request(method=method, url=self.build_url(url), json=json, headers=headers, params=params)
    
    async def auth_request(self, method, url, json=None, params=None):
        res = await self.request(
            method=method,
            url=url, 
            json=json,
            headers=self.get_headers(),
            params=params
        )
        if res.status_code == 401:
            refreshed = await self.refresh_access_token(self.refresh)
            if not refreshed:
                await self.auth_failed_handler()
                return res
            res = await self.request(
                method=method,
                url=url, 
                json=json,
                headers=self.get_headers()
            )    
        return res       

    async def refresh_access_token(self, refresh):
        if not refresh:
            return False
        res = await self.request(method='POST', url='refresh/', json={'refresh': refresh})
        if res.status_code != 200:
            return False
        access = res.json().get('access')
        self.set_access(access)
        await self.token_refreshed_handler(access)
        return True

    async def close(self):
        if self.client is not None:
            await self.client.aclose() 