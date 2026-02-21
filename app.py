from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()

def exec_prompt(input_prompt, selected_item):
    if selected_item == "投資の専門家":
        messages = [
            SystemMessage(
                content=(
                    "あなたは投資の専門家です。明確で実用的、かつリスクに配慮した回答をしてください。"
                    "必要に応じて簡潔な確認質問を行い、個別の投資助言は避けてください。"
                )
            ),
            HumanMessage(content=f"{input_prompt}"),
        ]
    else:
        messages = [
            SystemMessage(
                content=(
                    "あなたは教育の専門家です。明確で構造化された、共感的な回答をしてください。"
                    "必要に応じて簡潔な確認質問を行い、学習者の理解度に合わせて説明してください。"
                )
            ),
            HumanMessage(content=f"{input_prompt}"),
        ]

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    result = llm(messages)
    return result.content

st.title("LLMサンプルアプリ")

st.write("##### 動作モード1:投資の専門家")
st.write("投資に関する一般的な知識、リスク、判断基準について答えます。")
st.write("##### 動作モード2: 教育の専門家")
st.write("学習設計や教え方、理解を深めるための支援について答えます。")

if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""
    st.session_state.last_question = ""
    st.session_state.last_mode = ""

if st.session_state.get("clear_input"):
    st.session_state.input_prompt = ""
    st.session_state.clear_input = False

with st.form("chat_form"):
    selected_item = st.radio(
        "どの専門家に質問しますか？",
        ["投資の専門家", "教育の専門家"]
    )
    input_prompt = st.text_input(label="質問してみましょう。", key="input_prompt")
    submitted = st.form_submit_button("実行")

st.divider()

if submitted:
    if input_prompt.strip():
        with st.spinner("回答を生成しています..."):
            answer = exec_prompt(input_prompt, selected_item)
        st.session_state.last_answer = answer
        st.session_state.last_question = input_prompt
        st.session_state.last_mode = selected_item
        st.session_state.clear_input = True
        st.rerun()
    else:
        st.warning("質問内容を入力してください。")

if st.session_state.last_answer:
    st.markdown(f"**[{st.session_state.last_mode}]**")
    st.write(f"Q: {st.session_state.last_question}")
    st.write(f"A: {st.session_state.last_answer}")

