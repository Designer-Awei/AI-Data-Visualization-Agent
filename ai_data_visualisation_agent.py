import os
import json
import re
import sys
import io
import contextlib
import warnings
import requests
from typing import Optional, List, Any, Tuple
from PIL import Image
import streamlit as st
import pandas as pd
import base64
from io import BytesIO
from e2b_code_interpreter import Sandbox
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv('local.env')

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

pattern = re.compile(r"```python\n(.*?)\n```", re.DOTALL)

def code_interpret(e2b_code_interpreter: Sandbox, code: str) -> Optional[List[Any]]:
    with st.spinner('Executing code in E2B sandbox...'):
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                exec = e2b_code_interpreter.run_code(code)

        if stderr_capture.getvalue():
            print("[Code Interpreter Warnings/Errors]", file=sys.stderr)
            print(stderr_capture.getvalue(), file=sys.stderr)

        if stdout_capture.getvalue():
            print("[Code Interpreter Output]", file=sys.stdout)
            print(stdout_capture.getvalue(), file=sys.stdout)

        if exec.error:
            print(f"[Code Interpreter ERROR] {exec.error}", file=sys.stderr)
            return None
        return exec.results

def match_code_blocks(llm_response: str) -> str:
    match = pattern.search(llm_response)
    if match:
        code = match.group(1)
        return code
    return ""

def chat_with_llm_code_only(e2b_code_interpreter: Sandbox, user_message: str, dataset_path: str) -> Tuple[Optional[str], str]:
    """
    第一步：只让LLM生成Python代码，不要解释。
    @param e2b_code_interpreter {Sandbox} E2B沙盒实例
    @param user_message {str} 用户输入的问题
    @param dataset_path {str} 数据集在沙盒中的路径
    @returns {Tuple} (代码字符串, LLM原始回复)
    """
    system_prompt = f"""你是一名Python数据科学家。你拿到数据集路径'{dataset_path}'和用户问题后，只需输出一段Python代码（markdown代码块），用于分析或可视化数据，不要输出任何解释或说明。代码读取数据时必须使用'{dataset_path}'变量。"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]
    with st.spinner('正在从SiliconFlow大模型获取分析代码...'):
        url = "https://api.siliconflow.cn/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {st.session_state.siliconflow_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": st.session_state.model_name,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 0.9,
            "frequency_penalty": 0.5
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            if "choices" in response_data and len(response_data["choices"]) > 0:
                response_message = response_data["choices"][0]["message"]["content"]
                python_code = match_code_blocks(response_message)
                if python_code:
                    return python_code, response_message
                else:
                    st.warning(f"未能从模型响应中匹配到Python代码")
                    return None, response_message
            else:
                st.error("API响应格式错误")
                return None, "API响应格式错误，无法获取模型回答"
        except requests.exceptions.RequestException as e:
            st.error(f"API请求错误: {str(e)}")
            return None, f"API请求错误: {str(e)}"

def chat_with_llm_explain(user_message: str, exec_result: str) -> str:
    system_prompt = "你是一名数据分析专家。请根据用户问题和下方的代码执行结果，用简明中文为用户详细解释结果。"
    user_prompt = f"用户问题：{user_message}\n代码执行结果：{exec_result}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    with st.spinner('正在让大模型为你解释分析结果...'):
        url = "https://api.siliconflow.cn/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {st.session_state.siliconflow_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": st.session_state.model_name,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1024,
            "top_p": 0.9,
            "frequency_penalty": 0.5
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            if "choices" in response_data and len(response_data["choices"]) > 0:
                return response_data["choices"][0]["message"]["content"]
            else:
                st.error("API响应格式错误")
                return "API响应格式错误，无法获取模型解释"
        except requests.exceptions.RequestException as e:
            st.error(f"API请求错误: {str(e)}")
            return f"API请求错误: {str(e)}"

def upload_dataset(code_interpreter: Sandbox, uploaded_file) -> str:
    dataset_path = f"./{uploaded_file.name}"
    
    try:
        code_interpreter.files.write(dataset_path, uploaded_file)
        return dataset_path
    except Exception as error:
        st.error(f"Error during file upload: {error}")
        raise error


def main():
    """Main Streamlit application."""
    st.title("📊 AI 数据可视化助手")
    st.write("上传您的数据集并提出问题！")

    # 从环境变量获取API密钥
    default_siliconflow_api_key = os.getenv("SILICONFLOW_API_KEY", "")
    default_e2b_api_key = os.getenv("E2B_API_KEY", "")

    # Initialize session state variables
    if 'siliconflow_api_key' not in st.session_state:
        st.session_state.siliconflow_api_key = default_siliconflow_api_key
    if 'e2b_api_key' not in st.session_state:
        st.session_state.e2b_api_key = default_e2b_api_key
    if 'model_name' not in st.session_state:
        st.session_state.model_name = ''

    with st.sidebar:
        st.header("API密钥和模型配置")
        st.session_state.siliconflow_api_key = st.sidebar.text_input("SiliconFlow API密钥", 
                                                                   value=st.session_state.siliconflow_api_key,
                                                                   type="password")
        st.sidebar.info("💡 SiliconFlow - 中国领先的AI云平台")
        st.sidebar.markdown("[获取SiliconFlow API密钥](https://cloud.siliconflow.cn/account/ak)")
        
        st.session_state.e2b_api_key = st.sidebar.text_input("E2B API密钥", 
                                                           value=st.session_state.e2b_api_key,
                                                           type="password")
        st.sidebar.markdown("[获取E2B API密钥](https://e2b.dev/docs/legacy/getting-started/api-key)")
        
        # 添加SiliconFlow模型选项
        model_options = {
            "Qwen/Qwen2.5-7B-Instruct (默认，32K文本，免费)": "Qwen/Qwen2.5-7B-Instruct",
            "THUDM/glm-4-9b-chat (备选，128K文本，免费)": "THUDM/glm-4-9b-chat",
            "Qwen/Qwen2.5-14B-Instruct (备选，32K文本，付费)": "Qwen/Qwen2.5-14B-Instruct",
            "deepseek-ai/DeepSeek-V3 (备选，64k文本，付费)": "deepseek-ai/DeepSeek-V3"
        }
        st.session_state.model_name = st.selectbox(
            "选择模型",
            options=list(model_options.keys()),
            index=0  # 默认选择第一个选项
        )
        st.session_state.model_name = model_options[st.session_state.model_name]

    uploaded_file = st.file_uploader("选择CSV文件", type="csv")
    
    if uploaded_file is not None:
        # Display dataset with toggle
        df = pd.read_csv(uploaded_file)
        st.write("数据集:")
        show_full = st.checkbox("显示完整数据集")
        if show_full:
            st.dataframe(df)
        else:
            st.write("预览(前5行):")
            st.dataframe(df.head())
        # Query input
        query = st.text_area("您想了解数据的什么信息？",
                            "能否比较不同类别之间两人的平均成本？")
        
        if st.button("分析"):
            if not st.session_state.siliconflow_api_key or not st.session_state.e2b_api_key:
                st.error("请在侧边栏中输入两个API密钥。")
            else:
                with Sandbox(api_key=st.session_state.e2b_api_key) as code_interpreter:
                    dataset_path = upload_dataset(code_interpreter, uploaded_file)
                    # 第一步：只生成代码
                    python_code, llm_code_response = chat_with_llm_code_only(code_interpreter, query, dataset_path)
                    st.write("AI生成的分析代码：")
                    st.code(python_code, language="python")
                    # 第二步：沙盒执行
                    code_results = code_interpret(code_interpreter, python_code) if python_code else None
                    # 展示可视化/表格等
                    if code_results:
                        for result in code_results:
                            if hasattr(result, 'png') and result.png:
                                png_data = base64.b64decode(result.png)
                                image = Image.open(BytesIO(png_data))
                                st.image(image, caption="生成的可视化", use_container_width=False)
                            elif hasattr(result, 'figure'):
                                fig = result.figure
                                st.pyplot(fig)
                            elif hasattr(result, 'show'):
                                st.plotly_chart(result)
                            elif isinstance(result, (pd.DataFrame, pd.Series)):
                                st.dataframe(result)
                            elif isinstance(result, list) and all(isinstance(x, str) for x in result):
                                st.info(f"该数据集包含以下字段：{', '.join(result)}")
                            elif isinstance(result, str) and result.startswith("[") and result.endswith("]"):
                                try:
                                    import ast
                                    fields = ast.literal_eval(result)
                                    if isinstance(fields, list) and all(isinstance(x, str) for x in fields):
                                        st.info(f"该数据集包含以下字段：{', '.join(fields)}")
                                    else:
                                        st.write(result)
                                except Exception:
                                    st.write(result)
                            else:
                                st.write(result)
                        # 取第一个结果文本用于解释
                        explain_input = code_results[0] if len(code_results) == 1 else str(code_results)
                        st.write("AI结果解释：")
                        st.write(chat_with_llm_explain(query, explain_input))
                    else:
                        st.warning("代码执行未返回结果，无法生成解释。")

if __name__ == "__main__":
    main()
