import streamlit as st
from datetime import datetime

st.set_page_config(page_title="収支管理ツール", layout="centered")
st.title("💰 収支管理ツール")

# リロード対策
if "data" in st.query_params and 'history' not in st.session_state:
    st.session_state.history = st.query_params["data"]

if 'history' not in st.session_state:
    st.session_state.history = ""

def save(text):
    st.session_state.history += text
    st.query_params["data"] = st.session_state.history

# --- 入力エリア ---
with st.form("input_form", clear_on_submit=True):
    date = st.date_input("日付", datetime.now())
    memo = st.text_input("備考（機種名など）")
    toushi = st.number_input("投資 (円)", min_value=0, step=1000)
    kaishu = st.number_input("回収 (円)", min_value=0, step=1000)
    
    submit = st.form_submit_button("記録する")
    if submit:
        shuchi = kaishu - toushi
        res = f"{date} | {memo} | 投資:{toushi} 回収:{kaishu} 収支:{shuchi}\n"
        save(res)
        st.success("記録しました！")

# --- 表示エリア ---
st.divider()
st.subheader("📊 収支履歴")
st.text_area("履歴データ", value=st.session_state.history, height=300)

if st.button("全データを削除"):
    st.session_state.history = ""
    st.query_params.clear()
    st.rerun()

