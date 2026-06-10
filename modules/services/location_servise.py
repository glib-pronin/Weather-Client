class LocationService:
    def __init__(self, api):
        self.api = api
        self.countries = []
        self.selected_country = None
        self.selected_country_code = None
        self.selected_city = None

    def set_location(self, country, country_code, city):
        self.selected_country = country
        self.selected_country_code = country_code
        self.selected_city = city

    async def load_countries(self):
        if not self.countries:
            res = await self.api.request(
                method='GET',
                url='countries/'
            )
            if res.status_code == 200:
                self.countries = res.json()

    async def save_selection(self):
        res = await self.api.auth_request(
            method='PATCH',
            url='me/',
            json={
                'country': self.selected_country,
                'country_code': self.selected_country_code,
                'city': self.selected_city
            }
        )
        if res.status_code == 200:
            return res.json()
        return None

    async def clear_location(self):
        self.set_location(None, None, None)
        res = await self.save_selection()
        return res
    
    def filter_countries(self, query):
        query = query.strip().lower()
        return [
            country for country in self.countries
            if query in country['name'].lower()
        ]