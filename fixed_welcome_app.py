import streamlit as st

# 页面配置 - 必须放在最前面
st.set_page_config(
    page_title="AI创业助理",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded",
)

import os
from dotenv import load_dotenv
import json
import time
from data.resources import RESOURCES, FREELANCE_TYPES

# 加载环境变量 - 从.env文件
load_dotenv()
# API密钥从环境变量获取，而不是硬编码
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# 初始化API客户端
ANTHROPIC_API_AVAILABLE = False
client = None

try:
    import anthropic
    # 尝试直接创建客户端
    client = anthropic.Anthropic()
    
    # 简单测试API连接
    test_message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=10,
        messages=[
            {"role": "user", "content": "Hello"}
        ]
    )
    
    if test_message and test_message.content:
        ANTHROPIC_API_AVAILABLE = True
        print("✅ Anthropic API 连接成功!")
        print(f"测试响应: {test_message.content[0].text}")
except Exception as e:
    print(f"❌ Anthropic API 连接失败: {e}")
    client = None

# 自定义CSS
st.markdown("""
<style>
    /* 全局样式 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #333333;
        line-height: 1.5;
        background-color: #ffffff;
    }
    
    .main-header {
        font-size: 2.2rem;
        color: #333333;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #666666;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* 聊天界面样式 */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding-bottom: 120px; /* 为底部输入框留出空间 */
    }
    
    /* 创建一个统一的宽度容器 */
    .message-container {
        width: 90%;
        max-width: 700px;
        margin: 0 auto;
    }
    
    .bot-message {
        background-color: #f1f1f1;
        padding: 1.2rem 1.5rem;
        border-radius: 1.2rem;
        margin-bottom: 1.5rem;
        font-size: 1rem;
        line-height: 1.6;
        width: 100%;
        max-width: 100%;
        display: inline-block;
        color: #333333;
        box-sizing: border-box;
    }
    
    .user-message {
        background-color: #e1f0ff;
        padding: 1.2rem 1.5rem;
        border-radius: 1.2rem;
        margin-bottom: 1.5rem;
        font-size: 1rem;
        color: #333333;
        line-height: 1.6;
        width: 100%;
        max-width: 100%;
        display: inline-block;
        float: right;
        box-sizing: border-box;
        clear: both;
    }
    
    /* 资源卡片样式 */
    .resource-card {
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 0.8rem;
        border: 1px solid #EEEEEE;
        margin-bottom: 0.8rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .warning {
        background-color: #FFF3CD;
        color: #856404;
        padding: 1rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        border-left: 3px solid #FFD166;
    }
    
    /* 输入框样式 */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #fff;
        padding: 1rem;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
        z-index: 1000;
    }
    
    /* 恢复简洁的输入框样式 */
    .stTextArea textarea {
        border-radius: 0.5rem !important;
        border: 1px solid #E0E0E0 !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        box-shadow: none !important;
        background-color: #f5f5f5 !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #7868e6 !important;
        background-color: #ffffff !important;
    }
    
    /* 发送按钮样式 */
    .stButton button {
        border-radius: 0.5rem !important;
        background-color: #fafafa !important;
        color: #333333 !important;
        border: 1px solid #E0E0E0 !important;
        font-weight: 400 !important;
        padding: 0.5rem 2rem !important;
        transition: all 0.2s ease !important;
        min-width: 120px !important;
        margin-top: 10px !important;
    }
    
    .stButton button:hover {
        background-color: #f0f0f0 !important;
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    .stApp {
        margin-top: -60px;
    }
    
    /* 聊天消息清除浮动 */
    .message-container::after {
        content: "";
        display: table;
        clear: both;
    }
    
    /* 为表单添加轻微的边框 */
    section[data-testid="stForm"] {
        border: 1px solid #E0E0E0 !important;
        border-radius: 0.8rem !important;
        padding: 1rem !important;
        background-color: #ffffff !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        margin-bottom: 1rem !important;
        width: 90% !important;
        max-width: 700px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    /* 统一宽度的容器类 */
    .unified-width {
        width: 90%;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* 调整Streamlit容器的宽度 */
    .block-container {
        max-width: 800px;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* 移动设备适配 */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.8rem !important;
        }
        
        .sub-header {
            font-size: 1rem !important;
        }
        
        .bot-message, .user-message {
            padding: 0.8rem 1rem !important;
            margin-bottom: 1rem !important;
            font-size: 0.95rem !important;
        }
        
        section[data-testid="stForm"] {
            padding: 0.5rem !important;
        }
        
        .stTextArea textarea {
            font-size: 0.95rem !important;
        }
        
        /* 提高按钮可点击性 */
        .stButton button {
            min-height: 44px !important;
        }
    }
    
    /* PWA 支持 - 添加全屏体验 */
    @media all and (display-mode: standalone) {
        body {
            margin: 0;
            padding: 0;
        }
    }
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
if 'messages' not in st.session_state:
    st.session_state.messages = []
    
if 'resources_shown' not in st.session_state:
    st.session_state.resources_shown = False

if 'current_freelance_type' not in st.session_state:
    st.session_state.current_freelance_type = None
    
if 'current_field' not in st.session_state:
    st.session_state.current_field = None

# 为输入框添加唯一key - 确保每次提交后清空输入框
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

# 添加一个标志来跟踪消息处理状态
if 'waiting_for_ai' not in st.session_state:
    st.session_state.waiting_for_ai = False

if 'user_message_to_process' not in st.session_state:
    st.session_state.user_message_to_process = None

# 添加一个标志来跟踪欢迎消息是否已显示
if 'welcome_shown' not in st.session_state:
    st.session_state.welcome_shown = False

# 标题设置在统一宽度的容器中
st.markdown('<div class="unified-width">', unsafe_allow_html=True)
st.markdown('<p class="main-header">👭AISIS</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">与AI对话，发现热爱与擅长，创造自由生活</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 显示API状态
if not ANTHROPIC_API_AVAILABLE:
    st.markdown('<div class="unified-width warning">⚠️ 啊哦，你的AI小姐妹出了一点技术问题，对话能力可能不太行，请允许我手刀前往修复！</div>', unsafe_allow_html=True)

# 预设欢迎消息
DEFAULT_WELCOME_MESSAGE = """
姐妹！很高兴见到你 👋

我是你的AI创业小姐妹，我想帮你找到擅长且热爱的领域，陪你走向自由的创业之路。

可以告诉我，你对哪方面的事更感兴趣吗？或者，你现在面临什么样的创业困惑？没有具体想法也没关系，我会陪你一起发现～
"""

# 预设回复
DEFAULT_RESPONSES = [
    "感谢分享！我很感兴趣您的经历和想法。能更详细地分享一下您的想法吗？",
    "这很有趣！您提到的经历很有价值。您有没有想过如何将这些经验发展成一种职业？",
    "您的经历非常宝贵。基于您分享的内容，您觉得自己在哪些方面有独特优势？",
    "我理解您的想法。您对这个领域似乎很有热情。您平时会花多少时间在这方面？",
    "谢谢您的详细分享！如果要将这些经验和兴趣发展为创业项目，您认为最大的机会和挑战会是什么？"
]

# 显示聊天历史
chat_container = st.container()
with chat_container:
    st.markdown('<div class="message-container">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 开始新对话 - 修正欢迎消息显示逻辑
if not st.session_state.messages and not st.session_state.welcome_shown:
    # 直接显示预设的欢迎消息，不调用API
    st.session_state.messages.append({"role": "assistant", "content": DEFAULT_WELCOME_MESSAGE})
    st.session_state.welcome_shown = True
    # 显示API不可用提示（如果API不可用）
    if not ANTHROPIC_API_AVAILABLE:
        st.warning("⚠️ 你的AI小伙伴暂时开小差了，请10分钟后再回来试试吧。")
    st.rerun()

# 如果有待处理的用户消息，则生成AI回复
if st.session_state.waiting_for_ai and st.session_state.user_message_to_process:
    current_input = st.session_state.user_message_to_process
    
    # 检查用户是否请求资源
    if "资源" in current_input or "推荐" in current_input or "书" in current_input or "课程" in current_input:
        st.session_state.resources_shown = True
    
    # 检查是否提到自由职业类型
    for ft_type in FREELANCE_TYPES.keys():
        if ft_type in current_input:
            st.session_state.current_freelance_type = ft_type
            break
    
    if ANTHROPIC_API_AVAILABLE:
        # 准备消息历史
        message_history = []
        for message in st.session_state.messages:
            message_history.append({"role": message["role"], "content": message["content"]})
        
        # 调用AI获取回复
        with st.spinner("AI助手正在思考..."):
            try:
                response = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=1000,
                    system="""你是一位温暖、善解人意的创业助理，专门帮助女性发现适合自己的创业机会，并引导她们迈向成功的创业之路。
你的目标用户是所有想要开创自己事业的女性，她们有热情、有动力、有创造力，但可能不知道如何开始。

在对话中，请遵循以下原则：
1. 温暖友好：使用亲切、鼓励的语气，创造安全的交流空间。
2. 提问引导：通过开放性问题引导用户自我探索，避免简单的是/否问题。
3. 深入洞察：帮助用户发现潜在的创业领域和个人优势，而不仅仅是表面的兴趣爱好。
4. 实用建议：根据用户回答提供具体可行的下一步建议。
5. 情感支持：承认用户的顾虑和困难，提供积极的情感支持。

你应该探索的主要领域包括：
- 用户的热情所在（她们喜欢做什么、会为什么而感到时间飞逝）
- 用户的优势能力（她们擅长什么、别人经常称赞她们哪方面）
- 用户的价值观（她们看重什么、希望通过工作实现什么）
- 用户的担忧和障碍（阻止她们追求热情的因素）

当用户表现出对特定领域的兴趣后，你可以提供相关的自由职业方向建议和具体资源推荐。

请不要一次性问太多问题，保持对话流畅自然，像朋友间的交谈。在用户没有明确表示需要资源前，不要急于推荐具体资源。""",
                    messages=message_history
                )
                assistant_message = response.content[0].text
                
                # 添加AI回复到对话历史
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                
                # 重置处理标志
                st.session_state.waiting_for_ai = False
                st.session_state.user_message_to_process = None
                
                st.rerun()
            except Exception as e:
                st.error(f"调用AI时出错: {e}")
                # 使用预设回复
                import random
                response_template = random.choice(DEFAULT_RESPONSES)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_template
                })
                
                # 重置处理标志
                st.session_state.waiting_for_ai = False
                st.session_state.user_message_to_process = None
                
                # 显示API不可用提示
                st.warning("⚠️ 你的AI小伙伴暂时开小差了，请10分钟后再回来试试吧。")
                
                st.rerun()
    else:
        # 使用预设回复
        import random
        response_template = random.choice(DEFAULT_RESPONSES)
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response_template
        })
        
        # 重置处理标志
        st.session_state.waiting_for_ai = False
        st.session_state.user_message_to_process = None
        
        # 显示API不可用提示
        st.warning("⚠️ 你的AI小伙伴暂时开小差了，请10分钟后再回来试试吧。")
        
        st.rerun()

# 只在AI不思考时显示输入表单
if not st.session_state.waiting_for_ai:
    # 使用表单来确保提交后重新运行
    with st.form(key="message_form", clear_on_submit=True):
        # 用户输入 - 使用text_area支持多行输入
        user_input = st.text_area(
            "输入你的回复...", 
            height=150,  # 设置较大的高度
            key="user_input_field")
        
        # 居中显示发送按钮
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            submit_button = st.form_submit_button("发送", use_container_width=True)

    # 处理表单提交
    if submit_button and user_input and user_input.strip():
        # 保存用户输入到临时变量并存储到会话状态
        current_input = user_input
        
        # 将用户输入添加到对话历史
        st.session_state.messages.append({"role": "user", "content": current_input})
        
        # 设置标志，表示需要处理这条消息
        st.session_state.waiting_for_ai = True
        st.session_state.user_message_to_process = current_input
        
        # 立即刷新页面以显示用户消息
        st.rerun()
else:
    # 当AI正在思考时，显示一条提示消息
    st.info("AI助手正在思考回复...")

# 资源推荐选项
if st.session_state.resources_shown:
    st.write("选择一个感兴趣的领域获取详细资源推荐:")
    cols = st.columns(3)
    resource_buttons = {}
    
    for i, field in enumerate(RESOURCES.keys()):
        with cols[i % 3]:
            resource_buttons[field] = st.button(field, key=f"resource_button_{field}")
    
    for field, clicked in resource_buttons.items():
        if clicked:
            st.session_state.current_field = field
            field_resources = RESOURCES.get(field, {})
            
            resource_message = f"""
            ## 📚 {field}领域资源推荐
            
            以下是一些帮助你在{field}领域起步的精选资源：
            
            ### 推荐书籍：
            """
            
            for book in field_resources.get("书籍", []):
                resource_message += f"""
                <div class="resource-card">
                <strong>{book['title']}</strong> - {book['author']}<br>
                {book['description']}
                </div>
                """
            
            resource_message += """
            ### 推荐课程：
            """
            
            for course in field_resources.get("课程", []):
                resource_message += f"""
                <div class="resource-card">
                <strong>{course['title']}</strong> - {course['platform']}<br>
                链接：<a href="{course['link']}" target="_blank">查看课程</a>
                </div>
                """
            
            resource_message += """
            ### 建议项目：
            """
            
            for project in field_resources.get("项目", []):
                resource_message += f"""
                <div class="resource-card">
                {project}
                </div>
                """
            
            st.session_state.messages.append({"role": "assistant", "content": resource_message})
            st.rerun()

# 自由职业类型推荐
if st.session_state.current_freelance_type:
    st.write("了解这种自由职业类型:")
    freelance_cols = st.columns(2)
    freelance_buttons = {}
    
    available_types = list(FREELANCE_TYPES.keys())
    half = len(available_types) // 2
    
    for i, ft_type in enumerate(available_types[:half]):
        with freelance_cols[0]:
            freelance_buttons[ft_type] = st.button(ft_type, key=f"ft_button_{ft_type}")
            
    for i, ft_type in enumerate(available_types[half:]):
        with freelance_cols[1]:
            freelance_buttons[ft_type] = st.button(ft_type, key=f"ft_button_{ft_type}")
    
    for ft_type, clicked in freelance_buttons.items():
        if clicked:
            ft_info = FREELANCE_TYPES.get(ft_type, {})
            
            ft_message = f"""
            ## 🚀 {ft_type}职业发展路径
            
            <div class="resource-card">
            <strong>描述：</strong>{ft_info.get('描述', '')}<br><br>
            <strong>所需技能：</strong>{', '.join(ft_info.get('所需技能', []))}<br><br>
            <strong>入门建议：</strong>{ft_info.get('入门建议', '')}
            </div>
            """
            
            st.session_state.messages.append({"role": "assistant", "content": ft_message})
            st.rerun()

# 重置对话
if st.sidebar.button("开始新对话"):
    for key in ['messages', 'resources_shown', 'current_freelance_type', 'current_field', 'waiting_for_ai', 'user_message_to_process', 'welcome_shown']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# 侧边栏
with st.sidebar:
    st.markdown("## 关于")
    st.markdown("""
    <h3 style="margin-bottom: 0.5rem;">AISIS</h3>
    
    👭我是你的AI创业小姐妹，我会用我的超级大脑跟你聊天，帮你找到热爱且擅长的创业机会，基于你的兴趣和能力为你推荐创业资源和学习路径，支持你迈向自由的创业之路。
    
    💪我们女孩有力量。
    """, unsafe_allow_html=True)
    
    st.markdown("## 使用提示")
    st.markdown("""
    1. 坦诚分享你的想法、技能和顾虑
    2. 特别是你不知疲倦的案例请展开说
    3. 提问任何创业相关"怎么做"问题
    4. 随时开始新对话讨论新的idea
    """)
    
    st.markdown("## 移动应用安装")
    st.markdown("""
    ### iOS用户
    1. 在Safari中打开应用
    2. 点击底部的"分享"按钮
    3. 选择"添加到主屏幕"
    
    ### Android用户
    1. 在Chrome中打开应用
    2. 点击菜单(三个点)
    3. 选择"添加到主屏幕"
    """)
    
    st.markdown("## 数据隐私")
    st.markdown("""
    所有对话内容仅用于为你提供个性化建议，不会被永久存储或用于其他目的。
    """) 