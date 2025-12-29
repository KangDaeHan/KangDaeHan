import os
import requests
import re
from datetime import datetime

# 1. 공릉 2동 좌표
LAT = "37.5665" 
LON = "126.9780"
API_KEY = os.environ.get('OPENWEATHER_API_KEY')

# 'weather' 엔드포인트 사용 (5일/3시간 예보)
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
    return f'<img src="{url}" width="25" height="25" align="bottom" />'

try:
    response = requests.get(URL)
    data = response.json()

    temp = round(data['main']['temp'], 1)
    desc = data['weather'][0]['description']
    icon = data['weather'][0]['icon']
    
    # 움직이는 이모지 태그 생성
    anim_emoji = get_anim_emoji(icon)
    
    # 출력 예시: 서울 날씨: 맑음 <움직이는해> 24.5°C
    weather_text = f'서울 날씨: {desc} {anim_emoji} {temp}°C'
    print(f"생성된 날씨 문구: {weather_text}")

    # README 업데이트
    readme_path = 'README.md'
    # 기존 파일 내용을 '읽기 모드(r)'로 전부 가져옵니다.
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 정규표현식 패턴: 주석 사이의 공백이나 줄바꿈이 변해도 찾을 수 있게 유연하게 설정
    # re.escape()를 사용하여 , : 같은 특수문자가 정규식 명령어로 오해받지 않게 함
    start_tag = "<!-- WEATHER:START -->"
    end_tag = "<!-- WEATHER:END -->"

    # find는 찾으면 위치(숫자)를 반환하고, 없으면 -1을 반환합니다.
    start_index = content.find(start_tag)
    end_index = content.find(end_tag)

    # 디버깅용 출력 (Actions 로그에서 확인 가능)
    print(f"🔍 위치 검색 결과: START위치={start_index}, END위치={end_index}")
    
    # 교체할 내용 (주석 태그는 유지하고 내용만 바꿈)
    replacement = f"{start_tag}\n{weather_text}\n{end_tag}"

    # 검색 및 교체 실행
    if start_index != -1 and end_index != -1:
        # 1. 두 태그가 모두 존재할 때 (정상)
        print("✅ 주석 태그를 발견했습니다. 해당 구간만 교체합니다.")
        
        # 앞부분: 처음부터 ~ 시작 태그가 끝나는 지점까지
        before_part = content[:start_index + len(start_tag)]
        
        # 뒷부분: 종료 태그 시작 지점부터 ~ 파일 끝까지
        after_part = content[end_index:]
        
        # 새 내용 조립: (앞부분) + (줄바꿈+날씨+줄바꿈) + (뒷부분)
        new_content = before_part + "\n" + weather_text + "\n" + after_part
        
    else:
        # 2. 태그를 못 찾았을 때 (비정상)
        print("⚠️ 태그를 찾을 수 없습니다. 파일 맨 뒤에 새로 추가합니다.")
        print(f"   (참조: 파일 내 실제 내용 일부 -> {content[:50]}...)")
        
        # 혹시 모르니 기존에 있을 수도 있는 태그들을 한번 더 정리하고 추가
        # (무한 증식 방지용 안전장치는 수동 청소가 제일 확실합니다)
        new_content = content + f"\n\n{start_tag}\n{weather_text}\n{end_tag}"

    # 수정된 전체 내용을 다시 씁니다.
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("✅ README.md 업데이트 완료!")

except Exception as e:
    print(f"에러 발생: {e}")
