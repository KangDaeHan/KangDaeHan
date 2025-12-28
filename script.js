// ==========================================
// 1. 설정 영역 (본인의 정보로 수정하세요)
// ==========================================
const API_KEY = "b9af838d88199f8830657cf1b17217e2"; 
const LAT = "37.5665"; // 서울 위도
const LON = "126.9780"; // 서울 경도

// 날씨 상태별 비디오 파일 경로 매핑
// OpenWeatherMap의 'main' 상태 또는 아이콘 코드를 기준으로 매핑합니다.
const videoMap = {
    'Clear': { // 맑음
        day: 'videos/clear-day.mp4',
        night: 'videos/clear-night.mp4'
    },
    'Clouds': 'videos/clouds.mp4', // 구름
    'Rain': 'videos/rain.mp4',     // 비
    'Drizzle': 'videos/rain.mp4',  // 이슬비
    'Thunderstorm': 'videos/rain.mp4', // 뇌우 (천둥번개 비디오가 있다면 교체)
    'Snow': 'videos/snow.mp4',     // 눈
    'Atmosphere': 'videos/clouds.mp4', // 안개, 황사 등 (Mist, Smoke, Haze...)
    'Default': 'videos/default.mp4' // 기본값
};

// ==========================================
// 2. DOM 요소 선택
// ==========================================
const videoElement = document.getElementById('bg-video');
const sourceElement = document.getElementById('bg-source');
const statusElement = document.getElementById('weather-status');


// ==========================================
// 3. 핵심 함수: 비디오 교체 기능
// ==========================================
function changeBackgroundVideo(weatherMain, iconCode) {
    let videoPath = videoMap['Default']; // 기본값 설정

    // 낮/밤 구분 (아이콘 코드에 'n'이 포함되면 밤)
    const isNight = iconCode.includes('n');

    // 날씨 상태에 따른 비디오 경로 결정
    if (videoMap[weatherMain]) {
        if (typeof videoMap[weatherMain] === 'object') {
            // Clear 처럼 낮/밤이 구분된 경우
            videoPath = isNight ? videoMap[weatherMain].night : videoMap[weatherMain].day;
        } else {
            // Rain, Snow 처럼 낮/밤 구분이 없는 경우
            videoPath = videoMap[weatherMain];
        }
    }

    console.log(`날씨: ${weatherMain}, 밤 여부: ${isNight}, 선택된 비디오: ${videoPath}`);

    // 현재 비디오와 다를 경우에만 교체 실행
    // (sourceElement.getAttribute('src')를 사용하여 상대 경로 비교)
    if (sourceElement.getAttribute('src') !== videoPath) {
        // 1. 소스 경로 변경
        sourceElement.src = videoPath;
        // 2. 중요: 비디오 요소를 반드시 reload 해줘야 새 소스를 읽어옵니다.
        videoElement.load();
        // 3. 재생 시작 (브라우저 정책상 muted 상태여야 자동 재생됨)
        videoElement.play().catch(e => console.error("비디오 재생 실패:", e));
    }
}


// ==========================================
// 4. 날씨 데이터 가져오기 및 실행
// ==========================================
async function fetchWeatherAndUpdateBg() {
    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${LAT}&lon=${LON}&appid=${API_KEY}&units=metric&lang=kr`;

    try {
        const response = await axios.get(url);
        const data = response.data;

        const weatherMain = data.weather[0].main; // 예: Clear, Rain, Clouds
        const weatherDesc = data.weather[0].description; // 예: 맑음, 실 비
        const iconCode = data.weather[0].icon; // 예: 01d (낮), 01n (밤)
        const temp = Math.round(data.main.temp);

        // 상태 메시지 업데이트
        statusElement.innerText = `${weatherDesc}, 기온: ${temp}°C`;

        // 배경 비디오 교체 함수 호출
        changeBackgroundVideo(weatherMain, iconCode);

    } catch (error) {
        console.error("날씨 데이터를 가져오는데 실패했습니다:", error);
        statusElement.innerText = "날씨 정보를 불러올 수 없습니다. (기본 배경 적용)";
        changeBackgroundVideo('Default', '01d'); // 에러 발생 시 기본 배경 적용
    }
}

// ==========================================
// 5. 초기화
// ==========================================

// 페이지 로드 시 최초 실행
fetchWeatherAndUpdateBg();

// 6시간(21,600,000ms)마다 날씨 갱신 및 배경 교체 실행
setInterval(fetchWeatherAndUpdateBg, 21600000);