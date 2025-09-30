import streamlit as st

st.set_page_config(page_title="オリジナルキャラクタークリエイター", layout="wide")

st.title("🧙 オリジナルキャラクタークリエイター 🤖")
st.subheader("あなたの物語の主人公をデザインしましょう！")

# サイドバーの設定
st.sidebar.header("キャラクター設定")

# 1. 名前
name = st.sidebar.text_input("名前 (Name)", "アルテミス")

# 2. 職業/タイプ
job = st.sidebar.selectbox(
    "職業/タイプ (Job/Type)",
    ["騎士", "魔法使い", "サイボーグ", "冒険家", "商人", "学者", "その他"]
)

# 3. 性格
personality = st.sidebar.slider("性格 (Personality)", 1, 10, 5, help="1:冷静沈着、10:情熱的")

# 4. 特徴 (チェックボックス)
st.sidebar.subheader("特徴 (Traits)")
trait_brave = st.sidebar.checkbox("勇敢な")
trait_wise = st.sidebar.checkbox("賢い")
trait_mysterious = st.sidebar.checkbox("神秘的な")

# --- メイン画面への表示 ---
st.header(f"✨ キャラクタープロフィール: {name} ✨")

# キャラクターの基本情報の表示
col1, col2 = st.columns(2)

with col1:
    st.markdown("**基本情報**")
    st.info(f"**名前:** {name}")
    st.info(f"**職業/タイプ:** {job}")

with col2:
    st.markdown("**性格と特徴**")
    st.progress(personality / 10)
    if personality <= 3:
        st.success("性格: 冷静沈着")
    elif personality >= 8:
        st.success("性格: 情熱的")
    else:
        st.success("性格: バランス型")
    
    # 特徴リストの作成
    traits_list = []
    if trait_brave:
        traits_list.append("勇敢な")
    if trait_wise:
        traits_list.append("賢い")
    if trait_mysterious:
        traits_list.append("神秘的な")

    if traits_list:
        st.write(f"**特別な特徴:** {', '.join(traits_list)}")
    else:
        st.write("**特別な特徴:** なし")

st.markdown("---")
st.subheader("📜 キャラクターの概要 (Summary)")
st.write(
    f"{name} は、{job} として世界を旅する、ユニークな存在です。"
    f"彼の性格は{personality}点と評価され、"
    f"{'そして' + '、'.join(traits_list) + 'という特徴を持っています。' if traits_list else '物語の可能性は無限大です！'}"
)
