

import streamlit as st
import requests
import uuid
from google import genai

def get_mac_address():
    id = uuid.getnode()
    mac = ':'.join(("%012X" % id)[i:i+2] for i in range(0, 12, 2))
    return mac

def auth(username, password):
    mac = get_mac_address()
    res = requests.post('https://tellurium.ejae8319.workers.dev/api/users/auth', json={
        "project": "네이버자동포스팅-신공간",
        "username": username,
        "password": password,
        "code": mac,
    })
    return res.ok

st.set_page_config(page_title="Naver Auto Posting", layout="wide")

st.title("네이버 자동 포스팅 프로그램")

# Gemini API 키 입력 및 인증


st.subheader("Gemini API 키 입력")
gemini_api_key = st.text_input("Gemini API 키를 입력하세요", type="password", key="gemini_api_key")
if st.button("Gemini 키 인증하기"):
    try:
        client = genai.Client(api_key=gemini_api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Hello",
        )
        st.success("Gemini API 키 인증 성공!")
        st.session_state["gemini_api_key_valid"] = True
    except Exception as e:
        st.error(f"유효하지 않은 키입니다: {e}")
        st.session_state["gemini_api_key_valid"] = False


# 네이버 아이디/패스워드 입력란 및 로그인 버튼
st.subheader("네이버 로그인 정보 입력")
naver_id = st.text_input("네이버 아이디를 입력하세요", key="naver_id")
naver_pw = st.text_input("네이버 패스워드를 입력하세요", type="password", key="naver_pw")
if st.button("네이버 로그인"):
    try:
        from web import webdriver, login
        # 기존 세션이 있으면 안전하게 종료
        if getattr(webdriver, 'driver', None) is not None:
            try:
                webdriver.driver.quit()
            except Exception:
                pass
            webdriver.driver = None
        webdriver.init_chrome()
        login.enter_naver_login()
        login.input_id_pw(naver_id, naver_pw)
        login.click_login_button()
        if login.check_login_done():
            st.success("네이버 로그인 성공!")
        else:
            st.error("네이버 로그인 실패 또는 오류 발생.")
    except Exception as e:
        st.error(f"네이버 로그인 중 오류: {e}")

# 인증 폼 (main.py의 AuthDialog 대체)
if "auth" not in st.session_state:
    st.session_state["auth"] = False



# 인증 여부와 관계없이 메인 화면 항상 표시
col1, col2, col3 = st.columns([1,2,1])
with col1:
    st.subheader("계정/키워드/블로그/카페 리스트")
    st.write("계정 리스트")
    st.table([['user1', 'pass1'], ['user2', 'pass2']])
    st.write("키워드 리스트")
    st.table([['키워드1'], ['키워드2']])
    st.write("블로그 리스트")
    st.table([['블로그1'], ['블로그2']])
    st.write("카페 리스트")
    st.table([['카페1'], ['카페2']])
    st.write("상태: 대기중")
    st.write("IP 정보: 192.168.0.1 (예시)")
    st.write("API 번호: 123456 (예시)")
    st.write("핸드폰 번호: 010-1234-5678 (예시)")
with col2:
    st.subheader("포스팅 입력 및 실행")
    with st.form("posting_form"):
        title_input = st.text_input("포스팅 제목 입력")
        content_input = st.text_area("포스팅 내용 입력")
        address = st.text_input("주소(치환용)")
        company = st.text_input("업체명(치환용)")
        waiting_min = st.number_input("최소 대기 시간(초)", min_value=0, value=5)
        waiting_max = st.number_input("최대 대기 시간(초)", min_value=0, value=10)
        submitted = st.form_submit_button("자동 포스팅 실행")
    if submitted:
        st.info("자동 포스팅 기능은 Selenium 등 외부 모듈과 연동 필요. 실제 동작은 별도 구현 필요.")
        st.success("작업이 실행되었습니다. (예시)")
with col3:
    st.subheader("로그 및 결과")
    st.write(f"[{st.session_state.get('log_start', '2025-10-27')}] 프로그램 시작")
    st.write(f"[{st.session_state.get('log_auth', '2025-10-27')}] 인증 성공")
    st.write(f"[{st.session_state.get('log_wait', '2025-10-27')}] 작업 대기중...")
    st.write(f"[{st.session_state.get('log_post', '2025-10-27')}] 로그 예시: 자동 포스팅 실행")
