"""
Anthropic API工具函数

提供安全加载API密钥和创建客户端的辅助函数
"""

import os
import anthropic
from dotenv import load_dotenv

def create_safe_anthropic_client(env_file=None):
    """
    安全创建Anthropic客户端
    
    Args:
        env_file (str, optional): 要加载的.env文件路径. 默认None.
    
    Returns:
        anthropic.Anthropic: Anthropic客户端实例
    
    Raises:
        ValueError: 如果API密钥未设置或无效
    """
    # 加载指定的环境变量文件
    if env_file:
        load_dotenv(env_file)
    else:
        load_dotenv()  # 默认加载.env文件
    
    # 获取API密钥
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY环境变量未设置")
    
    if len(api_key) < 20:  # 简单验证密钥长度
        raise ValueError("ANTHROPIC_API_KEY格式无效")
    
    # 创建客户端
    return anthropic.Anthropic(api_key=api_key)

def test_api_connection(client):
    """
    测试API连接是否正常工作
    
    Args:
        client (anthropic.Anthropic): Anthropic客户端实例
    
    Returns:
        tuple: (成功标志, 响应文本, 错误信息)
    """
    try:
        # 发送简单测试请求
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            messages=[
                {"role": "user", "content": "Hello"}
            ]
        )
        
        return True, response.content[0].text, None
    except Exception as e:
        return False, None, str(e) 