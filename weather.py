import os
import requests
import re
from datetime import datetime

# 1. 공릉 2동 좌표
LAT = "37.5665" 
LON = "126.9780"
API_KEY = os.environ.get('OPENWEATHER_API_KEY')

# 'weather' 대신 'forecast' 엔드포인트 사용 (5일/3시간 예보)
URL = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul,kr&APPID={API_KEY}"

emoji_gifs = {
    # 맑음 (낮/밤)
    "01d": "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Sun.png", 
    "01n": "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Crescent%20Moon.png",
    
    # 구름 (낮/밤 구분 없이 구름 사용하거나 구분 가능)
    "02d": "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Sun%20Behind%20Large%20Cloud.png",
    "02n": "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Crescent%20Moon.png", # 밤 구름 대체
    "03d": "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Cloud.png",
    "03n": "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Cloud.png",
    "04d": "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Cloud.png",
    "04n": "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Cloud.png",
    
    # 비
    "09d": "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Cloud%20with%20Rain.png",
    "09n": "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Cloud%20with%20Rain.png",
    "10d": "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Cloud%20with%20Rain.png",
    "10n": "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Cloud%20with%20Rain.png",
    
    # 천둥번개
    "11d": "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Cloud%20with%20Lightning%20and%20Rain.png",
    "11n": "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Cloud%20with%20Lightning%20and%20Rain.png",
    
    # 눈
    "13d": "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Snowflake.png",
    "13n": "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Snowflake.png",
    
    # 안개
    "50d": "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Fog.png",
    "50n": "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Fog.png",
}

# 기본 이미지 (매칭 안될 때)
DEFAULT_ICON = "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Thermometer.png"

def get_anim_emoji(icon_code):
    url = emoji_gifs.get(icon_code, DEFAULT_ICON)
    # HTML 이미지 태그를 사용하여 크기를 25px로 제한 (텍스트와 어울리게)
    return f'<img src="{url}" width="25" height="25" style="vertical-align:middle" />'

try:
    response = requests.get(URL)
    data = response.json()

    temp = round(data['main']['temp'], 1)
    desc = data['weather'][0]['description']
    icon = data['weather'][0]['icon']
    
    # 움직이는 이모지 태그 생성
    anim_emoji = get_anim_emoji(icon)
    
    # 출력 예시: 서울 날씨: 맑음 <움직이는해> 24.5°C
    weather_text = f"서울 날씨: {desc} {anim_emoji} {temp}°C"
    print(weather_text)

    # 3. README 업데이트
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
