import streamlit as st
from datetime import datetime, date, time
import openai
import os

# 1. 페이지 설정 (가장 위에!)
st.set_page_config(page_title="전생과 사주팔자 알아보기", layout="centered")

# 2. OpenAI API 키 (Streamlit Cloud의 Secrets에 OPENAI_API_KEY로 등록 필요)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# 3. 전생 후보 데이터 (더 다양하게!)
PAST_LIVES = {
    'animals': [
        '호랑이', '사자', '늑대', '여우', '고양이', '개', '독수리', '부엉이', '올빼미', '펭귄', '코끼리', '기린', '하마', '고래', '돌고래',
        '상어', '거북이', '토끼', '다람쥐', '판다', '수달', '사슴', '양', '염소', '말', '황소', '돼지', '닭', '공작', '까치', '앵무새',
        '참새', '비둘기', '매', '두루미', '백조', '고슴도치', '너구리', '스컹크', '두더지', '두꺼비', '개구리', '뱀', '이구아나',
        '카멜레온', '악어', '문어', '오징어', '게', '가재', '해파리', '불가사리', '벌', '나비', '잠자리', '개미', '무당벌레', '풍뎅이'
    ],
    'jobs': [
        '왕', '여왕', '장군', '무사', '승려', '화가', '음악가', '상인', '농부', '학자', '의사', '요리사', '무용가', '연금술사', '마법사',
        '시인', '작가', '철학자', '천문학자', '점성가', '장인', '도공', '목수', '대장장이', '어부', '사냥꾼', '목동', '재봉사', '도예가',
        '조각가', '건축가', '정원사', '연주가', '무희', '서예가', '화공', '궁수', '기사', '해적', '상단주', '전령', '사서', '도서관장',
        '교사', '선생', '군주', '장수', '탐험가', '상단장', '연금술사', '연설가', '정치가', '외교관', '상감장인', '연예인', '연극배우'
    ],
    'myth': [
        '용', '천사', '도깨비', '요정', '구미호', '유니콘', '드래곤', '피닉스', '키메라', '스핑크스', '그리핀', '트롤', '엘프', '드워프',
        '마왕', '천왕', '신선', '선녀', '수호신', '바다의 신', '태양의 신', '달의 여신', '풍요의 신', '지하세계의 신', '거인', '요괴',
        '마녀', '마법사', '현자', '예언자', '사신', '천둥의 신', '바람의 신', '불의 신', '물의 정령', '숲의 정령', '바다의 정령'
    ]
}

# 4. 사주팔자 계산 함수
def calculate_saju(birth_date):
    year = birth_date.year
    month = birth_date.month
    day = birth_date.day
    hour = birth_date.hour
    saju = {
        'year': ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'][year % 10],
        'month': ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'][month - 1],
        'day': ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'][day % 10],
        'hour': ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'][hour % 12]
    }
    fortune_map = {
        '甲': '새로운 시작과 도전이 많은 인생',
        '乙': '성실하고 부드러운 성격, 인복이 많음',
        '丙': '밝고 활기찬 인생, 리더십이 뛰어남',
        '丁': '섬세하고 따뜻한 마음, 예술적 재능',
        '戊': '든든하고 신뢰받는 인생',
        '己': '현실적이고 실속있는 삶',
        '庚': '강인하고 추진력 있는 인생',
        '辛': '지혜롭고 신중한 성격',
        '壬': '유연하고 적응력이 뛰어남',
        '癸': '섬세하고 감수성이 풍부함'
    }
    saju['life_fortune'] = fortune_map.get(saju['year'], '다채로운 인생')
    import datetime as dt
    this_year = dt.datetime.now().year
    year_key = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'][this_year % 10]
    newyear_fortune_map = {
        '甲': '올해는 새로운 기회가 찾아옵니다!',
        '乙': '올해는 인간관계에 행운이 있습니다.',
        '丙': '올해는 에너지가 넘치고 활발합니다.',
        '丁': '올해는 예술적 영감이 가득합니다.',
        '戊': '올해는 재정적으로 안정적입니다.',
        '己': '올해는 실속을 챙기기 좋은 해입니다.',
        '庚': '올해는 도전이 많지만 성취도 큽니다.',
        '辛': '올해는 신중함이 필요합니다.',
        '壬': '올해는 변화에 잘 적응할 수 있습니다.',
        '癸': '올해는 감수성이 풍부해집니다.'
    }
    saju['newyear_fortune'] = newyear_fortune_map.get(year_key, '올해는 다양한 변화가 예상됩니다!')
    return saju

# 5. 전생 결정 함수
def decide_past_life(saju, gender):
    keys = [saju['year'], saju['month'], saju['day'], saju['hour'], gender]
    # 각 key의 모든 글자에 대해 ord()를 적용
    total = sum(ord(ch) for k in keys for ch in str(k))
    category = total % 3
    if category == 0:
        idx = total % len(PAST_LIVES['animals'])
        return PAST_LIVES['animals'][idx]
    elif category == 1:
        idx = total % len(PAST_LIVES['jobs'])
        return PAST_LIVES['jobs'][idx]
    else:
        idx = total % len(PAST_LIVES['myth'])
        return PAST_LIVES['myth'][idx]

# 6. AI 운세 해석 함수 (GPT)
def generate_long_fortune(saju, gender):
    prompt = f"""
    사주팔자 정보:
    년주: {saju['year']}, 월주: {saju['month']}, 일주: {saju['day']}, 시주: {saju['hour']}
    성별: {gender}
    이 사람의 인생총운을 1000자 내외로 아주 상세하게, 예시와 조언, 인생의 흐름, 성격, 인간관계, 재물, 건강, 직업, 사랑 등 다양한 측면을 포함해 설명해줘.
    그리고 올해의 신년운세도 1000자 내외로 아주 상세하게, 금전운, 승진운, 올해의 기회와 주의점, 월별 흐름, 조언을 포함해 설명해줘.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # 또는 "gpt-4" (유료)
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "AI 운세 해석을 불러오지 못했습니다."

# 7. 전생 그림 생성 함수 (DALL·E)
def generate_past_life_image(past_life):
    prompt = f"A {past_life} in Studio Ghibli style, plain background, highly detailed, cute, no background, focus on character"
    try:
        response = openai.images.generate(
            model="dall-e-2",  # 또는 "dall-e-2"
            prompt=prompt,
            n=1,
            size="512x512"
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        return None

# 8. Streamlit UI
st.title("전생과 사주팔자 알아보기")

birth_date = st.date_input("태어난 날짜를 입력하세요", min_value=date(1900,1,1), max_value=date.today())
birth_time = st.time_input("태어난 시간을 입력하세요", value=time(0,0))
calendar_type = st.radio("달력 종류", ("양력", "음력"))
gender = st.radio("성별", ("남자", "여자"))

if st.button("결과 보기"):
    # 날짜+시간 합치기
    birth_datetime = datetime.combine(birth_date, birth_time)
    with st.spinner("분석중..."):
        saju = calculate_saju(birth_datetime)
        past_life = decide_past_life(saju, gender)
        long_fortune = generate_long_fortune(saju, gender)
        image_url = generate_past_life_image(past_life)
    st.subheader("사주팔자 해석")
    st.write(f"**년주:** {saju['year']}  **월주:** {saju['month']}  **일주:** {saju['day']}  **시주:** {saju['hour']}")
    st.write(f"**인생총운:** {saju['life_fortune']}")
    st.write(f"**신년운세:** {saju['newyear_fortune']}")
    st.markdown("---")
    st.subheader("AI 운세 해석")
    st.write(long_fortune)
    st.markdown("---")
    st.subheader("당신의 전생")
    st.write(f"**전생:** {past_life}")
    if image_url:
        st.image(image_url, caption=f"{past_life}의 모습", use_container_width=True)
    else:
        st.info("전생 이미지를 불러오지 못했습니다.")


