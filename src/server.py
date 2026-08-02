"""
WeChat MCP Server for Hermes
基于 pyweixin，兼容微信 4.1+
提供：发消息、发文件、查聊天记录、搜索联系人、运行命令
"""

import asyncio
import json
import os
import sys
import logging
from pathlib import Path
from typing import Any

# 将仓库根目录加入 sys.path 前缀，使下方对 pyweixin 的 import 不再依赖
# MCP 客户端拉起子进程时是否传递了 cwd（实测部分客户端会忽略 cwd 字段，
# 导致从自身目录启动 `python -m src.server` 时找不到 pyweixin 而崩溃）。
# pyweixin 以 vendored 形式置于仓库根，仓库根进入 sys.path 即可被解析。
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from fastmcp import FastMCP
from pyweixin.WeChatTools import Navigator, Tools
from pyweixin.WeChatAuto import Messages
from pyweixin.WinSettings import SystemSettings
from pyweixin.Config import GlobalConfig

# 配置
GlobalConfig.close_weixin = False
GlobalConfig.is_maximize = False
GlobalConfig.search_pages = 10

logger = logging.getLogger(__name__)

mcp = FastMCP("weixin-server")


@mcp.tool()
def wechat_send_message(
    friend: str,
    message: str,
    delay: float = 0.5,
) -> dict:
    """
    向微信好友发送单条消息。
    
    Args:
        friend: 好友备注或昵称（需完整准确名称）
        message: 消息文本内容
        delay: 发送延迟（秒），防止被风控，默认0.5秒
    
    Returns:
        {"success": True/False, "summary": "结果描述"}
    """
    try:
        Messages.send_messages_to_friend(
            friend=friend,
            messages=[message],
            send_delay=delay,
            is_maximize=False,
            close_weixin=False,
        )
        return {"success": True, "summary": f"成功向 '{friend}' 发送消息"}
    except Exception as e:
        return {"success": False, "summary": f"发送失败: {str(e)}"}


@mcp.tool()
def wechat_send_multiple_messages(
    friend: str,
    messages: list[str],
    delay: float = 0.5,
) -> dict:
    """
    向微信好友发送多条消息。
    
    Args:
        friend: 好友备注或昵称
        messages: 消息文本列表
        delay: 每条消息之间的延迟（秒）
    
    Returns:
        {"success": True/False, "summary": "结果描述"}
    """
    try:
        Messages.send_messages_to_friend(
            friend=friend,
            messages=messages,
            delay=delay,
            is_maximize=False,
            close_weixin=False,
        )
        return {"success": True, "summary": f"成功向 '{friend}' 发送 {len(messages)} 条消息"}
    except Exception as e:
        return {"success": False, "summary": f"发送失败: {str(e)}"}


@mcp.tool()
def wechat_send_to_multiple_friends(
    friends: list[str],
    message: str,
    delay: float = 0.5,
) -> dict:
    """
    向多个好友发送同一条消息。
    
    Args:
        friends: 好友列表
        message: 消息内容
        delay: 每条消息之间的延迟（秒）
    
    Returns:
        {"success": True/False, "summary": "结果描述"}
    """
    errors = []
    success_count = 0
    for friend in friends:
        try:
            Messages.send_messages_to_friend(
                friend=friend,
                messages=[message],
                delay=delay,
                is_maximize=False,
                close_weixin=False,
            )
            success_count += 1
        except Exception as e:
            errors.append(f"{friend}: {e}")
    
    summary = f"成功发送给 {success_count}/{len(friends)} 位好友"
    if errors:
        summary += f"；失败: {'; '.join(errors)}"
    return {"success": success_count > 0, "summary": summary}


@mcp.tool()
def wechat_send_file(
    friend: str,
    file_path: str,
) -> dict:
    """
    向微信好友发送文件。
    
    Args:
        friend: 好友备注或昵称
        file_path: 本地文件绝对路径
    
    Returns:
        {"success": True/False, "summary": "结果描述"}
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return {"success": False, "summary": f"文件不存在: {file_path}"}
        
        from pyweixin.WeChatAuto import Files
        Files.send_files_to_friend(
            friend=friend,
            files=[str(path)],
            send_delay=0.5,
            close_weixin=False,
        )
        return {"success": True, "summary": f"成功向 '{friend}' 发送文件: {path.name}"}
    except Exception as e:
        return {"success": False, "summary": f"发送文件失败: {str(e)}"}


@mcp.tool()
def wechat_search_contacts(
    keyword: str,
    page_limit: int = 5,
) -> dict:
    """
    搜索微信联系人。
    
    Args:
        keyword: 搜索关键词（昵称/备注/微信号）
        page_limit: 搜索翻页次数
    
    Returns:
        {"success": True, "contacts": [...], "summary": "..."}
    """
    try:
        from pyweixin.WeChatAuto import Contacts
        # 打开搜索并获取结果
        GlobalConfig.search_pages = page_limit
        results = Contacts.search_contacts(keyword=keyword)
        contacts = []
        if results:
            for r in results:
                contacts.append({
                    "nickname": getattr(r, "nickname", str(r)),
                    "remark": getattr(r, "remark", ""),
                    "wxid": getattr(r, "wxid", ""),
                })
        return {"success": True, "contacts": contacts, "summary": f"搜索到 {len(contacts)} 个联系人"}
    except Exception as e:
        return {"success": False, "contacts": [], "summary": f"搜索失败: {str(e)}"}


@mcp.tool()
def wechat_get_chat_history(
    friend: str,
    pages: int = 5,
) -> dict:
    """
    获取与好友的最近聊天记录。
    
    Args:
        friend: 好友备注或昵称
        pages: 向上翻取的页数
    
    Returns:
        {"success": True, "messages": [...], "summary": "..."}
    """
    try:
        GlobalConfig.search_pages = pages
        history = Messages.dump_chat_history(friend=friend, pages=pages)
        messages = []
        if history:
            for msg in history:
                messages.append({
                    "sender": getattr(msg, "sender", ""),
                    "time": getattr(msg, "time", ""),
                    "content": getattr(msg, "content", str(msg)),
                })
        return {"success": True, "messages": messages, "summary": f"获取到 {len(messages)} 条消息"}
    except Exception as e:
        return {"success": False, "messages": [], "summary": f"获取聊天记录失败: {str(e)}"}


@mcp.tool()
def wechat_run_command(command: str) -> dict:
    """
    执行系统命令（用于微信自动化相关操作，如打开微信等）。
    
    Args:
        command: 要执行的命令
    
    Returns:
        {"success": True/False, "summary": "结果描述"}
    """
    try:
        import subprocess
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout.strip() or result.stderr.strip()
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "output": output,
            "summary": f"命令执行{'成功' if result.returncode == 0 else '失败'}: {output[:200]}"
        }
    except Exception as e:
        return {"success": False, "summary": f"命令执行失败: {str(e)}"}


@mcp.tool()
def wechat_get_status() -> dict:
    """
    获取微信运行状态。
    
    Returns:
        {"success": True, "running": True/False, "version": "...", "wxid": "..."}
    """
    try:
        running = Tools.is_weixin_running()
        version = Tools.get_weixin_version() if running else ""
        wxid = Tools.get_current_wxid() if running else ""
        return {
            "success": True,
            "running": running,
            "version": version,
            "wxid": wxid,
            "summary": f"微信{'运行中' if running else '未运行'} (版本: {version}, wxid: {wxid})"
        }
    except Exception as e:
        return {"success": False, "summary": f"获取状态失败: {str(e)}"}


@mcp.tool()
def wechat_open_dialog(friend: str) -> dict:
    """
    打开与好友的聊天窗口。
    
    Args:
        friend: 好友备注或昵称
    
    Returns:
        {"success": True/False, "summary": "结果描述"}
    """
    try:
        GlobalConfig.search_pages = 10
        window = Navigator.open_dialog_window(friend=friend, is_maximize=False)
        return {"success": True, "summary": f"已打开与 '{friend}' 的聊天窗口"}
    except Exception as e:
        return {"success": False, "summary": f"打开聊天窗口失败: {str(e)}"}


def main():
    """MCP 服务入口，供 `python -m src.server` 与 pyproject scripts 调用。"""
    mcp.run()


if __name__ == "__main__":
    main()
