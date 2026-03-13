import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="収支管理ツール", layout="centered")
st.title("💰 収支管理ツール")

# --- 1. URLからデータを復元 ---
query_params = st.query_params

if "data" in query_params and 'history' not in st.session_state:
    st.session_state.history = query_params["data"]
if 'history' not in st.session_state:
    st.session_state.history = ""

if "users" in query_params and 'user_list' not in st.session_state:
    st.session_state.user_list = query_params["users"].split(",")
if 'user_list' not in st.session_state:
    st.session_state.user_list = ["(未選択)"]

def sync_url():
    st.query_params["data"] = st.session_state.history
    st.query_params["users"] = ",".join(st.session_state.user_list)

# --- 2. データの解析（表にするための処理） ---
def get_df():
    if not st.session_state.history:
        return pd.DataFrame()
    rows = [line.split(" | ") for line in st.session_state.history.strip().split("\n")]
    df = pd.DataFrame(rows, columns=["日付", "名前", "備考", "詳細"])
    # 収支数値だけを抜き出す
    df["収支"] = df["詳細"].apply(lambda x: int(x.split("収:")[1]))
    return df

df = get_df()

# --- 3. 合計収支の表示 ---
if not df.empty:
    total_score = df["収支"].sum()
    color = "blue" if total_score >= 0 else "red"
    st.metric("📊 合計収支", f"{total_score:,} 円", delta=None)
    st.markdown(f"<h2 style='text-align: center; color: {color};'>累計: {total_score:,} 円</h2>", unsafe_allow_index=True)

# --- 4. 入力エリア ---
with st.expander("👤 ユーザー・収支入力", expanded=df.empty):
    new_user = st.text_input("新規登録")
    if st.button("登録"):
        if new_user and new_user not in st.session_state.user_list:
            st.session_state.user_list.append(new_user)
            sync_url(); st.rerun()
    
    st.divider()
    selected_user = st.selectbox("ユーザー", st.session_state.user_list)
    date = st.date_input("日付", datetime.now())
    memo = st.text_input("備考")
    c1, c2 = st.columns(2)
    with c1: toushi = st.number_input("投資", min_value=0, step=1000)
    with c2: kaishu = st.number_input("回収", min_value=0, step=1000)
    
    if st.button("📈 記録を保存"):
        if selected_user == "(未選択)": st.error("ユーザーを選択してください")
        else:
            shuchi = kaishu - toushi
            res = f"{date} | {selected_user} | {memo} | 投:{toushi} 回:{kaishu} 収:{shuchi}\n"
            st.session_state.history += res
            sync_url(); st.success("記録しました！"); st.rerun()

# --- 5. 表示エリア（表形式） ---
st.divider()
st.subheader("📊 収支履歴一覧")
if not df.empty:
    # 見やすく整理した表を表示
    st.table(df[["日付", "名前", "備考", "収支"]])
    
    # コピー用のテキストエリア（隠し）
    with st.expander("コピー用テキストを表示"):
        st.text_area("履歴データ", value=st.session_state.history, height=200)
else:
    st.info("データがありません。")

if st.button("⚠️ 全データをリセット"):
    st.session_state.history = ""; st.session_state.user_list = ["(未選択)"]
    st.query_params.clear(); st.rerun()
