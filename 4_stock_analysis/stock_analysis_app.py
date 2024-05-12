import streamlit as st 
import stock_analysis_lib as glib 
import stock_analysis_database_lib as databaselib 
from langchain.callbacks import StreamlitCallbackHandler
import time
import pandas as pd

def print_result(st, response):
    try:
        st.subheader("주가 데이터:")
        st.dataframe(response['intermediate_steps'][1][1])
        st.subheader("주식 차트:")
        df = pd.DataFrame(response['intermediate_steps'][1][1],columns=['Close','Volume'])
        df['Volume'] = df['Volume']/10000000
        df.rename(columns={'Close':'Price(USD)','Volume':'Volume(10 millions)'},inplace=True)
        st.line_chart(df)
        st.subheader("결과:")
        st.write(response['output'])
    except:
        st.write(response['output'])


def stock_analysis():
    st.header("주식 분석 에이전트")
    st.write("회사 이름을 입력해 주세요. Amazon, Tesla, Apple, 삼성전자, NAVER, 카카오, KB금융 등")

    if 'database' not in st.session_state: 
        with st.spinner("Initial Database"): 
            databaselib.initial_database() 
        
    if 'chat_history' not in st.session_state: 
        st.session_state.chat_history = [] 

    agent = glib.initializeAgent()
    input_text = st.chat_input("검색하고 싶은 상장 주식(국내주식, 해외주식)의 회사 이름을 입력해 주세요!") 
    ph = st.empty()
    if input_text:
        ph.empty()
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent({
            "input": input_text,
            "chat_history": st.session_state.chat_history,
         },
            callbacks=[st_callback])
        print_result(st,response)



    

