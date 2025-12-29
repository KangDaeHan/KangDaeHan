import os
import requests
import re
from datetime import datetime

# 1. 공릉 2동 좌표
LAT = "37.5665" 
LON = "126.9780"
API_KEY = os.environ.get('OPENWEATHER_API_KEY')

# 'weather' 대신 'forecast' 엔드포인트 사용 (5일/3시간 예보)
URL = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul,kr&APPID={API_KEY}&units=metric&lang=kr"

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
    weather_text = f'<div style="vertical-align:middle">서울 날씨: {desc} {anim_emoji} {temp}°C</div>'
    print(f"생성된 날씨 문구: {weather_text}")

    # README 업데이트
    readme_path = 'README.md'
    # 기존 파일 내용을 '읽기 모드(r)'로 전부 가져옵니다.
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 정규표현식 패턴: 주석 사이의 공백이나 줄바꿈이 변해도 찾을 수 있게 유연하게 설정
    # 와 사이의 모든 문자를 찾음
    pattern = r'[\s\S]*?'
    
    # 교체할 문자열 (주석 포함해서 전체를 갈아끼움)
    replacement = f'\n{weather_text}\n'

    if re.search(pattern, content):
        print("✅ 기존 날씨 블록을 찾았습니다. 내용을 교체합니다.")
        # 기존 블록을 찾아서 -> 새 블록으로 통째로 교체
        new_content = re.sub(pattern, replacement, content)
    else:
        print("⚠️ 기존 날씨 블록을 찾지 못했습니다. 파일 맨 끝에 추가합니다.")
        # 없으면 맨 뒤에 추가
        new_content = content + "\n" + replacement

    # 수정된 전체 내용을 다시 씁니다.
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("✅ README.md 업데이트 완료!")

except Exception as e:
    print(f"에러 발생: {e}")
