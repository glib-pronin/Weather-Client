from ..core.config import WEATHER_API_KEY, OPENWEATHER_API_KEY
from collections import defaultdict
from datetime import datetime, timezone
import asyncio

class WeatherService:
    def __init__(self, api):
        self.api = api
        self.cache = {}

        self.weather_code_map = {
            "1000": "01",
            "1003": "02",
            "1006": "03",
            "1009": "03",
            "1030": "04",
            "1063": "09",
            "1066": "13",
            "1069": "13",
            "1072": "13",
            "1114": "13",
            "1117": "13",
            "1087": "11",
            "1135": "04",
            "1147": "04",
            "1150": "09",
            "1153": "10",
            "1168": "03",
            "1171": "03",
            "1180": "09",
            "1183": "09",
            "1186": "09",
            "1189": "10",
            "1192": "10",
            "1195": "10",
            "1198": "09",
            "1201": "09",
            "1204": "09",
            "1207": "09",
            "1210": "13",
            "1213": "13",
            "1216": "13",
            "1219": "13",
            "1222": "13",
            "1225": "13",
            "1237": "13",
            "1240": "10",
            "1243": "10",
            "1246": "10",
            "1249": "10",
            "1252": "10",
            "1255": "13",
            "1258": "13",
            "1261": "13",
            "1264": "13",
            "1273": "11",
            "1276": "11",
            "1279": "11",
            "1282": "11",
        }

    async def get_weather(self, lat, lng, city_name, ttl=1800):
        now = int(datetime.now(timezone.utc).timestamp())
        key = f'{lat},{lng}'
        if key in self.cache:
            data = self.cache[key]
            if now - data['timestamp'] < ttl:
                return data['data']
        fetch_data = await self.fetch_weather(lat, lng, city_name)
        self.cache[key] = {'data': fetch_data, 'timestamp': now}
        return fetch_data

    async def fetch_weather(self, lat, lng, city_name):
        current_hourly_data, daily_data = await asyncio.gather(
            self.get_current_and_hourly_wetaher(lat, lng, city_name),
            self.get_daily_weather(lat, lng)
        )
        if daily_data and current_hourly_data.get('hourly'):
            daily_data[0]['main'] = current_hourly_data.get('hourly', {}).get('for_daily')
        return {
            'current': current_hourly_data.get('current', {}),
            'hourly': current_hourly_data.get('hourly', {}),
            'daily': daily_data
        }

    async def update_current_weather(self, lat, lng, city_name):
        key = f'{lat},{lng}'
        if not key in self.cache:
            return 
        current = await self.get_current_and_hourly_wetaher(lat, lng, city_name, include_hourly=False)
        if not current:
            return
        self.cache[key]['data']['current'] = current['current']
        return current['current']
        

    async def get_current_and_hourly_wetaher(self, lat, lng, city_name, include_hourly=True):
        print('current_hourly')
        try:
            res = await self.api.request(
                method='GET',
                url='http://api.weatherapi.com/v1/forecast.json',
                params={
                    'q': f'{lat},{lng}',
                    'lang': 'uk',
                    'aqi': 'no',
                    'alerts': 'no',
                    'days': 10,
                    'key': WEATHER_API_KEY
                }
            ) 
        except:
            return {}
        if res.status_code != 200:
            return {}
        data = res.json()
        result = {'current': self._form_current_data(data, city_name)}
        if include_hourly:
            result['hourly'] = self._form_hourly_data(data)
        return result
    
    def _form_current_data(self, api_data, city_name):
        return {
            'city_name': city_name,
            'icon_code': self.get_icon(str(api_data["current"]['condition']['code']), api_data["current"]['is_day']),
            'temp': f'{round(api_data["current"]["temp_c"])}°',
            'desc': api_data['current']['condition']['text'].capitalize(),
            'max_min': f'Макс.:{round(api_data["forecast"]["forecastday"][0]["day"]["maxtemp_c"])}°, мін.:{round(api_data["forecast"]["forecastday"][0]["day"]["mintemp_c"])}°',
        }
    
    def _form_hourly_data(self, api_data):
        return {
            'general': {
                'desc': api_data['forecast']['forecastday'][0]['day']['condition']['text'].capitalize(),
                'tz_id': api_data['location']['tz_id']
            },
            'for_daily': {
                'min': f'{round(api_data["forecast"]["forecastday"][0]["day"]["mintemp_c"])}°',
                'max': f'{round(api_data["forecast"]["forecastday"][0]["day"]["maxtemp_c"])}°',
                'icon': self.get_icon(str(api_data['forecast']['forecastday'][0]['day']['condition']['code']), 1)
            },
            'hours': [
                {
                    'hour': hour['time'].split()[1].split(':')[0],
                    'temp': f'{round(hour["temp_c"])}°',
                    'icon': self.get_icon(str(hour['condition']['code']), hour['is_day'])
                }
                for hour in api_data['forecast']['forecastday'][0]['hour']
            ]
        }
    
    async def get_daily_weather(self, lat, lng):
        print('daily')
        try:
            res = await self.api.request(
                method='GET',
                    url='https://api.openweathermap.org/data/2.5/forecast',
                    params={
                        'lat': lat,
                        'lon': lng,
                        'appid': OPENWEATHER_API_KEY,
                        'units': 'metric'
                    }
            )
        except:
            return []
        if res.status_code != 200:
            return []
        return self._form_daily_data(res.json())

    def _form_daily_data(self, api_data):
        days = defaultdict(list)
        for item in api_data['list']:
            date = item['dt_txt'].split()[0]
            days[date].append(item)
        
        result = []
        for date, items in days.items():
            temps = [i['main']['temp'] for i in items]
            min_temp = min(temps)
            max_temp = max(temps)

            icon = None
            for item in items:
                hour = int(item['dt_txt'].split()[1].split(':')[0])
                if 12 <= hour:
                    icon = item['weather'][0]['icon']
                    break

            result.append({
                'date': date,
                'main': {
                    'min': f'{round(min_temp)}°',
                    'max': f'{round(max_temp)}°',
                    'icon': icon
                }
            })
        return result[:5]
    
    def get_icon(self, code, is_day):
        return '01d' if not self.weather_code_map.get(code) else self.weather_code_map[code] + 'd' if is_day == 1 else self.weather_code_map[code] + 'n'
