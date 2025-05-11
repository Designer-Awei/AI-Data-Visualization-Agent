# 📊 AI 数据可视化助手
这个 Streamlit 应用程序创建了一个交互式数据可视化助手，它能够理解自然语言查询并使用大语言模型(LLMs)生成适当的可视化图表。
随着企业寻求更快速、更直观的数据理解方式，对 AI 驱动的数据可视化工具的需求正在激增。我们可以通过构建与现有数据工作流程无缝集成的 AI 驱动可视化工具来利用这一不断增长的市场。

![AI 数据可视化助手](https://github.com/GURPREETKAURJETHRA/AI-Data-Visualization-Agent/blob/main/img/AI%20DVA.jpg) 

我们将使用 SiliconFlow 强大的语言模型和 E2B 安全代码执行环境构建 AI 数据可视化助手。这个助手将理解关于您数据的自然语言查询，并自动生成适当的可视化，使数据探索变得直观高效。

![AI 数据可视化助手](https://github.com/GURPREETKAURJETHRA/AI-Data-Visualization-Agent/blob/main/img/AI%20DVA1.jpg)

对于任何刚开始使用这些库的人来说，本教程也可以被视为 E2B 代码解释器和 SiliconFlow 的演示！

功能:
💬 用于数据可视化的自然语言查询界面                                             
📊 支持多种可视化类型(折线图、柱状图、散点图、饼图、气泡图)                                      
🧹 自动数据预处理和清洗                                                        
🔐 在 E2B 的沙盒环境中安全执行代码                                                              
💻 交互式 Streamlit 界面，便于数据上传和可视化                                                        
⏳ 实时可视化生成和显示                                               
🤖 可用模型:                                   
     → Qwen/Qwen2.5-7B-Instruct (默认，32K文本，免费)                                
     → THUDM/glm-4-9b-chat (备选，128K文本，免费)                                 
     → Qwen/Qwen2.5-14B-Instruct (备选，32K文本，付费)                             
     → deepseek-ai/DeepSeek-V3 (备选，64k文本，付费)                                       
     
![AI 数据可视化助手](https://github.com/GURPREETKAURJETHRA/AI-Data-Visualization-Agent/blob/main/img/AI%20DVA2.jpg)

## 功能
一个由 LLMs 驱动的 Streamlit 应用程序，充当您的个人数据可视化专家。只需上传您的数据集并用自然语言提问 - AI 助手将分析您的数据，生成适当的可视化，并通过图表、统计和解释的组合提供洞察。

#### 自然语言数据分析
- 用简单的语言提问关于您数据的问题
- 获取即时可视化和统计分析
- 接收发现和洞察的解释
- 交互式后续提问

#### 智能可视化选择
- 自动选择适当的图表类型
- 动态可视化生成
- 统计可视化支持
- 自定义图表格式和样式

#### 多模型 AI 支持
- Qwen/Qwen2.5-7B-Instruct 用于快速分析（免费）
- THUDM/glm-4-9b-chat 用于复杂分析（免费）
- Qwen/Qwen2.5-14B-Instruct 用于详细洞察（付费）
- deepseek-ai/DeepSeek-V3 用于高级查询（付费）

![AI 数据可视化助手](https://github.com/GURPREETKAURJETHRA/AI-Data-Visualization-Agent/blob/main/img/AI%20DVA3.jpg)

## 如何运行

按照以下步骤设置并运行应用程序:
- 首先，请在此获取免费的 SiliconFlow API 密钥：https://cloud.siliconflow.cn/account/ak
- 在此获取免费的 E2B API 密钥：https://e2b.dev/ ; https://e2b.dev/docs/legacy/getting-started/api-key

1. **克隆仓库**
   ```bash
   git clone https://github.com/GURPREETKAURJETHRA/AI-Data-Visualization-Agent.git
   cd AI-Data-Visualization-Agent

   ```
2. **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```
3. **运行 Streamlit 应用**
    ```bash
    streamlit run ai_data_visualisation_agent.py
    ```

编码愉快！🚀✨

## ©️ 许可证 🪪 

根据 MIT 许可证分发。有关更多信息，请参阅 `LICENSE`。

---

#### **如果您喜欢这个 LLM 项目，请给这个仓库点 ⭐**
#### 关注我 [![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gurpreetkaurjethra/) &nbsp; [![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/GURPREETKAURJETHRA/)

---
