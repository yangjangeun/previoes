import streamlit as st
from datetime import datetime, date, time
import openai
import os

st.set_page_config(page_title="전생과 사주팔자 알아보기", layout="centered")  # ← 반드시 가장 위에!

# 이하 코드 계속...

# 1. OpenAI API 키를 환경변수에서 읽어옵니다 (Streamlit Cloud의 Secrets에 등록 필요)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# 2. 전생 후보 데이터
PAST_LIVES = {
    'animals': ['호랑이', '사자', '독수리', '고래', '코끼리', '팬더', '늑대', '여우', '고양이', '돌고래', '토끼', '다람쥐', '부엉이', '거북이'],
    'jobs': ['왕', '장군', '무사', '승려', '화가', '음악가', '상인', '농부', '학자', '의사', '요리사', '무용가', '연금술사', '마법사'],
    'myth': ['용', '천사', '도깨비', '요정', '구미호', '유니콘', '드래곤', '피닉스']
}

# 3. 사주팔자 계산 함수
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

# 4. 전생 결정 함수
def decide_past_life(saju):
    keys = [saju['year'], saju['month'], saju['day'], saju['hour']]
    total = sum([ord(k) for k in keys])
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

# 5. AI 운세 해석 함수 (GPT-3.5/4 사용)
def generate_long_fortune(saju):
    prompt = f"""
    사주팔자 정보:
    년주: {saju['year']}, 월주: {saju['month']}, 일주: {saju['day']}, 시주: {saju['hour']}
    이 사람의 인생총운을 1000자 이상으로 아주 상세하게, 예시와 조언, 인생의 흐름, 성격, 인간관계, 재물, 건강, 직업, 사랑 등 다양한 측면을 포함해 설명해줘.
    그리고 올해의 신년운세도 1000자 이상으로 아주 상세하게, 올해의 기회와 주의점, 월별 흐름, 조언, 예상되는 사건 등도 포함해서 설명해줘.
    각각 [인생총운], [신년운세]로 구분해서 써줘.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # 또는 gpt-4
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            temperature=0.8
        )
        content = response.choices[0].message.content
        return content
    except Exception as e:
        return f"AI 해석 중 오류가 발생했습니다: {e}"

# 6. Streamlit UI
st.title("전생과 사주팔자 알아보기")

birth_date = st.date_input("태어난 날짜를 입력하세요", min_value=date(1900,1,1), max_value=date.today())
birth_time = st.time_input("태어난 시간을 입력하세요", value=time(0,0))
calendar_type = st.radio("달력 종류", ("양력", "음력"))
gender = st.radio("성별", ("남자", "여자"))

if st.button("결과 보기"):
    with st.spinner('분석중...'):
        birth_datetime = datetime.combine(birth_date, birth_time)
        saju = calculate_saju(birth_datetime)
        past_life = decide_past_life(saju)
        long_fortune = generate_long_fortune(saju)
    st.subheader("사주팔자")
    st.write(f"년주: {saju['year']}")
    st.write(f"월주: {saju['month']}")
    st.write(f"일주: {saju['day']}")
    st.write(f"시주: {saju['hour']}")
    st.markdown(long_fortune)
    st.subheader("당신의 전생")
    st.write(f"당신의 전생은 {past_life}이었습니다!")

