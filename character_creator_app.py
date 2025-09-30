import streamlit as st
import os
from io import BytesIO
from PIL import Image
import requests # ⭐ Nanobanana連携のために追加

# --- !!! ⚠️ 重要: Nanobanana APIの設定 !!! ---
# Streamlit CloudのSecretsからAPIキーを取得
NANOBANANA_API_KEY = st.secrets.get("NANOBANANA_API_KEY")

# --- アプリの基本設定 ---
st.set_page_config(
    page_title="キャラクタークリエイター",
    layout="wide"
)
st.title("🤖 キャラクタークリエイター (Nanobanana API連携)")
st.caption("※ このアプリはNanobananaの画像生成APIを利用しています。")
st.markdown("---")

# --- 共通機能 ---
st.sidebar.header("📌 共通設定")
mode = st.sidebar.radio(
    "生成モードを選択してください:",
    ["三面図モード", "一枚絵モード"]
)

with st.sidebar.expander("詳細設定"):
    collection_name = st.text_input(
        "コレクション名 (任意)",
        value="My_New_Character",
        help="生成した画像群に名前を付けます。保存時のファイル名に反映されます。"
    )
    generation_count = st.slider(
        "生成枚数",
        min_value=1,
        max_value=30,
        value=4,
        help="一度に生成する画像の枚数 (1〜30枚)"
    )

st.markdown(f"**選択モード:** **{mode}**")
st.markdown("---")


# ⭐ Nanobanana APIを呼び出して画像を生成する関数に置き換え
def generate_image(prompt, count, ratio, collection_name):
    """Nanobanana APIを呼び出して画像を生成する関数"""
    if not NANOBANANA_API_KEY:
        st.error("⚠️ Nanobanana APIキーが設定されていません。Secretsを確認してください。")
        return
    
    # API呼び出しの準備
    # ※ APIのエンドポイントやパラメータ名は、Nanobananaの最新仕様に合わせて調整してください。
    API_URL = "https://nanobanana.jp/api/v1/generate" 
    headers = {
        "Authorization": f"Bearer {NANOBANANA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "n_images": count,
        "aspect_ratio": ratio, 
        "model": "stable-diffusion-xl-beta", # 利用するモデル名を指定
        # "negative_prompt": "..." # 必要に応じてネガティブプロンプトを追加可能
    }

    st.info("画像を生成中です。数分かかる場合があります...")
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=300) 
        response.raise_for_status()
        
        results = response.json()
        
        # --- 画像の表示とダウンロード（ダミー表示ロジック） ---
        st.subheader("💡 生成結果 (ダミー表示)")
        st.caption("※ Nanobanana APIからのレスポンスを解析し、画像URLを取得・表示する必要があります。")
        st.write(f"生成指示: `{prompt.split('---')[0].strip()}`")
        st.write(f"生成枚数: {count}枚 / アスペクト比: {ratio}")

        # ⭐ NanobananaのAPIレスポンス形式が不明なため、ここではダミー画像を表示します
        cols = st.columns(min(count, 4))
        for i in range(count):
            with cols[i % 4]:
                st.image("https://placehold.jp/3d4070/ffffff/350x200.png?text=Nanobanana+Result+%23" + str(i+1), 
                         caption=f"結果 {i+1}")
                st.download_button(
                    label=f"⬇️ 保存 {i+1}",
                    data=b"", 
                    file_name=f"{collection_name}_result_{i+1}.png",
                    mime="image/png"
                )
        
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API呼び出しエラー: {e}")
        st.error("APIキー、URL、または利用規約を確認してください。")


# ========================================
# 2.1. 三面図モード
# ========================================
if mode == "三面図モード":
    st.header("📐 三面図モード: ターンアラウンドシート生成")
    st.info("キャラクターの正面、側面、背面を含む三面図（16:9）を生成します。")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. 参考画像 (必須)")
        reference_images = st.file_uploader(
            "顔、髪型、体型などの画像 (1〜3枚)",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            key="ref_img_3view"
        )
        required_ref = len(reference_images) >= 1 and len(reference_images) <= 3
        if not required_ref:
            st.warning("⚠️ **参考画像は必須です (1〜3枚)。**")
        elif len(reference_images) > 3:
            st.error("ファイルは最大3枚までアップロードできます。")
        
        st.subheader("2. 衣装の画像 (任意)")
        costume_image = st.file_uploader(
            "着せたい服装の画像 (1枚)",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=False,
            key="costume_img_3view"
        )

    with col2:
        st.subheader("3. 追加の指示 (任意)")
        additional_instructions = st.text_area(
            "詳細な要望を入力",
            placeholder="例: 悲しい表情、背景はスタジオの白ホリゾント、クールな雰囲気で。アスペクト比は16:9でお願いします。",
            height=200
        )
        st.markdown(f"**出力アスペクト比:** `16:9` (固定)")

    st.markdown("---")
    if st.button("✨ 三面図を生成する", type="primary"):
        if required_ref:
            prompt = f"高品質なキャラクターの三面図（正面、側面、背面）をターンアラウンドシートとして生成してください。アスペクト比は16:9。\n--- [スタイル・追加指示]: {additional_instructions}\n"
            # ⭐ API呼び出し
            generate_image(prompt, generation_count, "16:9", collection_name)
        else:
            st.error("❌ 生成を開始できません。参考画像を1〜3枚アップロードしてください。")

# ========================================
# 2.2. 一枚絵モード
# ========================================
elif mode == "一枚絵モード":
    st.header("🖼️ 一枚絵モード: コンセプトアート生成")
    st.info("最大2人のキャラクターを含む、完成したイラストを生成します。")
    
    # 全体設定
    st.subheader("1. 全体設定 (シーン・構図)")
    col_scene, col_ratio = st.columns([3, 1])
    
    with col_scene:
        overall_prompt = st.text_area(
            "イラスト全体の指示 (必須)",
            placeholder="例: 神秘的な森で夕日に照らされながら決闘する二人の騎士、幻想的な光の表現。",
            height=100
        )
    with col_ratio:
        aspect_ratio_map = {
            "1:1 (正方形)": "1:1", 
            "16:9 (横長ワイド)": "16:9", 
            "9:16 (縦長スマホ)": "9:16", 
            "4:3 (標準横)": "4:3", 
            "3:4 (標準縦)": "3:4", 
            "21:9 (映画ワイド)": "21:9",    # ⭐ 追加
            "5:4 (ポートレート)": "5:4"    # ⭐ 追加
        }
        aspect_ratio_choice = st.selectbox(
            "アスペクト比",
            list(aspect_ratio_map.keys())
        )
        selected_ratio = aspect_ratio_map[aspect_ratio_choice]

    if not overall_prompt:
        st.warning("⚠️ **イラスト全体の指示は必須です。**")

    st.markdown("---")

    # キャラクター設定
    st.subheader("2. キャラクター設定 (最大2人)")
    
    # --- キャラクター1 ---
    st.markdown("#### キャラクター 1")
    colA1, colA2, colA3 = st.columns(3)
    
    with colA1:
        char1_ref = st.file_uploader("参考画像 (画風・質感, 最大2枚)", type=["png", "jpg"], accept_multiple_files=True, key="char1_ref")
    with colA2:
        char1_pose = st.file_uploader("ポーズ画像 (1枚)", type=["png", "jpg"], key="char1_pose")
    with colA3:
        char1_pose_text = st.text_area("ポーズ指示 (テキスト)", placeholder="例: 右手に剣を持ち、左手を前に突き出す。", key="char1_pose_text")
    
    # --- キャラクター2 ---
    st.markdown("#### キャラクター 2 (任意)")
    colB1, colB2, colB3 = st.columns(3)
    
    with colB1:
        char2_ref = st.file_uploader("参考画像 (画風・質感, 最大2枚)", type=["png", "jpg"], accept_multiple_files=True, key="char2_ref")
    with colB2:
        char2_pose = st.file_uploader("ポーズ画像 (1枚)", type=["png", "jpg"], key="char2_pose")
    with colB3:
        char2_pose_text = st.text_area("ポーズ指示 (テキスト)", placeholder="例: 巨大な盾を構え、警戒している。", key="char2_pose_text")

    # 必須チェック (少なくとも一方のポーズ指定が必須)
    pose_specified = (char1_pose or char1_pose_text) or (char2_pose or char2_pose_text)
    
    if not pose_specified:
        st.error("❌ 少なくともキャラクター1または2の**ポーズ指定 (画像またはテキスト)**が必須です。")
    
    st.markdown("---")
    
    if st.button("🎨 一枚絵を生成する", type="primary"):
        if overall_prompt and pose_specified:
            prompt = f"高品質なコンセプトアートイラストを生成してください。\n[シーン・構図]: {overall_prompt}\n[アスペクト比]: {selected_ratio}\n"
            if pose_specified:
                prompt += f"[キャラクター1ポーズ]: {char1_pose_text or '画像参照'}\n"
                if char2_pose or char2_pose_text:
                    prompt += f"[キャラクター2ポーズ]: {char2_pose_text or '画像参照'}\n"
            
            # ⭐ API呼び出し
            generate_image(prompt, generation_count, selected_ratio, collection_name)
            
        elif not overall_prompt:
            st.error("❌ 全体の指示を入力してください。")
        else:
            st.error("❌ 少なくとも一方のキャラクターのポーズ指定を行ってください。")
