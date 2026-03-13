import streamlit as st
from datetime import datetime

st.set_page_config(page_title="収支管理ツール", layout="centered")
st.title("💰 収支管理ツール")

# --- 1. URLからデータを復元する処理 ---
query_params = st.query_params

# 履歴データの復元
if "data" in query_params and 'history' not in st.session_state:
    st.session_state.history = query_params["data"]
if 'history' not in st.session_state:
    st.session_state.history = ""

# ユーザー名リストの復元
if "users" in query_params and 'user_list' not in st.session_state:
    st.session_state.user_list = query_params["users"].split(",")
if 'user_list' not in st.session_state:
    st.session_state.user_list = ["(未選択)"]

# --- 2. データの保存関数 ---
def sync_url():
    st.query_params["data"] = st.session_state.history
    st.query_params["users"] = ",".join(st.session_state.user_list)

# --- 3. ユーザー名の管理エリア ---
st.subheader("👤 ユーザー設定")
with st.expander("新規ユーザーを登録する"):
    new_user = st.text_input("新しい名前を入力")
    if st.button("登録"):
        if new_user and new_user not in st.session_state.user_list:
            st.session_state.user_list.append(new_user)
            sync_url()
            st.success(f"{new_user} を登録しました")
            st.rerun()

# --- 4. 収支入力エリア ---
st.subheader("📝 収支入力")
selected_user = st.selectbox("ユーザーを選択", st.session_state.user_list)
date = st.date_input("日付", datetime.now())
memo = st.text_input("備考（機種名など）")

c1, c2 = st.columns(2)
with c1:
    toushi = st.number_input("投資 (円)", min_value=0, step=1000)
with c2:
    kaishu = st.number_input("回収 (円)", min_value=0, step=1000)

if st.button("📈 記録を保存"):
    if selected_user == "(未選択)":
        st.error("ユーザーを選択してください")
    else:
        shuchi = kaishu - toushi
        res = f"{date} | {selected_user} | {memo} | 投:{toushi} 回:{kaishu} 収:{shuchi}\n"
        st.session_state.history += res
        sync_url()
        st.success("記録しました！")
        st.rerun()

# --- 5. 表示エリア ---
st.divider()
st.subheader("📊 収支履歴")
st.text_area("履歴（コピー用）", value=st.session_state.history, height=300)

# リセットボタン
if st.button("⚠️ 全データをリセット"):
    st.session_state.history = ""
    st.session_state.user_list = ["(未選択)"]
    st.query_params.clear()
    st.rerun()
