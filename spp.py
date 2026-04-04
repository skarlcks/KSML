
import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정 (모바일 최적화)
st.set_page_config(page_title="직업 분석 대시보드", layout="wide")

st.title("📊 KSML 직업 분석 대시보드")

@st.cache_data
def load_data():
    # 실제 파일명을 확인하세요. (리포지토리에 올린 파일명과 똑같아야 합니다)
    file_name = "KSML_fully_linked_experimental.xlsx"
    
    # 여러 인코딩 방식을 순차적으로 시도 (한글 깨짐 방지)
    encodings = ['utf-8-sig', 'cp949', 'euc-kr', 'latin1']
    for enc in encodings:
        try:
            return pd.read_csv(file_name, encoding=enc)
        except:
            continue
    return None

try:
    df = load_data()

    if df is not None:
        # 데이터가 정상일 때 화면 구성
        st.success("데이터를 성공적으로 불러왔습니다!")
        
        # 4분면 산점도 그래프
        fig = px.scatter(
            df, x="SML_score", y="Physical_score", 
            color="Quadrant", hover_name="KSCO_title",
            title="SML vs Physical 분포"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 직업 검색 창
        search = st.text_input("검색할 직업명을 입력하세요")
        if search:
            res = df[df["KSCO_title"].str.contains(search, na=False)]
            st.dataframe(res)
        else:
            st.dataframe(df.head(50))
    else:
        st.error("파일을 읽을 수 없습니다. 파일 이름이 정확한지 GitHub에서 확인해주세요.")

except Exception as e:
    # 에러가 나면 흰 화면 대신 에러 내용을 화면에 출력
    st.error(f"오류 발생: {e}")
