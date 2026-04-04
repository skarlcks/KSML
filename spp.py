import streamlit as st
import pandas as pd
import plotly.express as px
@st.cache_data
def load_data():
    file_path = "KSML_fully_linked_experimental.xlsx - ksco_495_final.csv" # 여기에 실제 파일명을 넣으세요
    
    try:
        # 1. 가장 범용적인 utf-8-sig 시도
        return pd.read_csv(file_path, encoding="utf-8-sig")
    except:
        try:
            # 2. 윈도우 한글 표준 cp949 시도
            return pd.read_csv(file_path, encoding="cp949")
        except:
            try:
                # 3. 인코딩 무시하고 강제로 읽기 (에러 방지용)
                return pd.read_csv(file_path, encoding="latin1", sep=",")
            except Exception as e:
                st.error(f"파일을 읽을 수 없습니다. 에러 메시지: {e}")
                return pd.DataFrame()
