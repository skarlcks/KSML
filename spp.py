import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="KSML 직업 대시보드", layout="wide")

st.title("📊 KSML & Physical 직업 분석 대시보드")
st.markdown("한국형 직업 지표(KSML)와 신체적 강도를 분석한 결과입니다.")

# 데이터 로드 (파일 경로를 실제 파일명으로 수정하세요)
@st.cache_data
def load_data():
    df = pd.read_csv("KSML_fully_linked_experimental.xlsx")
    return df

try:
    df = load_data()

    # 사이드바: 필터링
    st.sidebar.header("필터 설정")
    selected_quadrant = st.sidebar.multiselect(
        "분면(Quadrant) 선택",
        options=df["Quadrant"].unique(),
        default=df["Quadrant"].unique()
    )

    filtered_df = df[df["Quadrant"].isin(selected_quadrant)]

    # 상단 지표
    col1, col2, col3 = st.columns(3)
    col1.metric("분석된 직업 수", f"{len(filtered_df)}개")
    col2.metric("평균 SML 점수", f"{filtered_df['SML_score'].mean():.2f}")
    col3.metric("평균 Physical 점수", f"{filtered_df['Physical_score'].mean():.2f}")

    # 메인 차트: 산점도
    st.subheader("SML vs Physical 분포")
    fig = px.scatter(
        filtered_df, 
        x="SML_score", 
        y="Physical_score", 
        color="Quadrant",
        hover_name="KSCO_title",
        labels={"SML_score": "SML 점수", "Physical_score": "신체적 강도 점수"},
        template="plotly_white",
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

    # 데이터 상세 검색
    st.subheader("직업 상세 검색")
    search_query = st.text_input("직업명을 입력하세요 (예: 회계사, 개발자)")
    if search_query:
        search_results = filtered_df[filtered_df["KSCO_title"].str.contains(search_query)]
        st.dataframe(search_results)
    else:
        st.dataframe(filtered_df.sort_values(by="SML_score", ascending=False))

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.info("파일 이름이 'KSML_fully_linked_experimental.xlsx - ksco_495_final.csv'인지 확인해주세요.")
