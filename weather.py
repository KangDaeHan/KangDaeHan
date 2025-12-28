import os
import requests
import re
from datetime import datetime

# 1. 공릉 2동 좌표
LAT = "37.6211" 
LON = "127.0834"
API_KEY = os.environ.get('b9af838d88199f8830657cf1b17217e2')

# 'weather' 대신 'forecast' 엔드포인트 사용 (5일/3시간 예보)
URL = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric&lang=kr"

def get_weather_emoji(icon_code):
    icon_map = {
        "01d": "☀️", "01n": "🌙", "02d": "⛅", "02n": "⛅",
        "03d": "☁️", "03n": "☁️", "04d": "☁️", "04n": "☁️",
        "09d": "🌧️", "09n": "🌧️", "10d": "☔", "10n": "☔",
        "11d": "⚡", "11n": "⚡", "13d": "❄️", "13n": "❄️",
        "50d": "🌫️", "50n": "🌫️"
    }
    return icon_map.get(icon_code, "🌡️")

try:
    response = requests.get(URL)
    data = response.json()

    # forecast 데이터는 'list' 안에 3시간 간격으로 들어있습니다.
    # index 0: 가장 가까운 시간 (현재~3시간 이내)
    # index 1: +3시간 뒤
    # index 2: +6시간 뒤
    
    forecasts = []
    
    # 3개 구간만 뽑아서 표시 (현재 -> 3시간후 -> 6시간후)
    for i in range(3):
        item = data['list'][i]
        dt_txt = item['dt_txt'] # 예: 2024-05-20 15:00:00
        temp = round(item['main']['temp'], 1)
        desc = item['weather'][0]['description']
        icon = item['weather'][0]['icon']
        emoji = get_weather_emoji(icon)
        
        # 시간만 추출 (예: 15:00)
        time_only = dt_txt.split(" ")[1][:5]
        
        forecasts.append(f"{time_only} {emoji} {temp}°C")

    # 출력 형식 만들기
    # 예: 서울 예보: 12:00 ☀️ 24°C → 15:00 ⛅ 23°C → 18:00 ☁️ 21°C
    weather_text = f"서울 공릉2동 예보: {' → '.join(forecasts)}"
    print(weather_text)

    # 2. README 업데이트
    readme_path = 'README.md'
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = re.sub(
        r'.*',
        f'\n{weather_text}\n',
        content,
        flags=re.DOTALL
    )

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

except Exception as e:
    print(f"에러 발생: {e}")