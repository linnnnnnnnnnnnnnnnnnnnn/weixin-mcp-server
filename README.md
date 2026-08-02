# weixin-mcp-server

微信 MCP Server，基于 `pyweixin`，兼容微信 **4.1+**（最新 4.1.12）。通过标准 MCP 协议接入，让 AI 助手能驱动桌面微信发消息、发文件、查聊天记录等。

## 特性

- ✅ 兼容微信 **4.1.12**（最新官方版）
- ✅ 基于 `pyweixin`（非 pywechat），**pyweixin 已内置（vendored）于仓库，开箱即用，无需额外安装**
- ✅ 9 个 MCP 工具：发消息、发文件、查聊天记录、搜索联系人等
- ✅ 通过标准 MCP 协议接入（Hermes / WorkBuddy / Claude Desktop 等）
- ✅ **不再依赖 cwd**：`src/server.py` 会自动将仓库根加入 `sys.path`，并推荐以「绝对路径启动 server.py」的方式接入，即使 MCP 客户端未传递工作目录也能正确运行

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/linnnnnnnnnnnnnnnnnnnnn/weixin-mcp-server.git
cd weixin-mcp-server
```

### 2. 安装依赖

```bash
# 推荐：用虚拟环境（避免污染系统 Python）
python -m venv .venv
.venv\Scripts\python.exe -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 或直接装到当前 Python
pip install -r requirements.txt
```

> Windows 用户也可直接双击 `install.bat`（已配置清华镜像）。
> **无需** `pip install pyweixin` —— 该包未发布到 PyPI，本项目已将其直接内置。

### 3. 配置 MCP 客户端

> **推荐用「绝对路径启动 server.py」**（如下方示例），这是最稳的方式：不依赖客户端是否传递 `cwd`，也不需要额外的 `PYTHONPATH`。
> 如果你的客户端一定会正确传递 `cwd`，也可改用 `args: ["-m", "src.server"]` + `cwd` 的形式（两者均可）。

**Hermes**（`config.yaml` 或 MCP 管理界面）：
```yaml
mcp_servers:
  weixin-server:
    command: "C:\\path\\to\\weixin-mcp-server\\.venv\\Scripts\\python.exe"
    args: ["C:\\path\\to\\weixin-mcp-server\\src\\server.py"]
    cwd: "C:\\path\\to\\weixin-mcp-server"   # 可省略
```

**WorkBuddy**（`mcp.json`）：
```json
{
  "mcpServers": {
    "weixin-server": {
      "command": "C:\\path\\to\\weixin-mcp-server\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\weixin-mcp-server\\src\\server.py"]
    }
  }
}
```

**Claude Desktop**（`claude_desktop_config.json`）：
```json
{
  "mcpServers": {
    "weixin-server": {
      "command": "C:\\path\\to\\weixin-mcp-server\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\weixin-mcp-server\\src\\server.py"]
    }
  }
}
```

### 4. 重启客户端

重启 Hermes / WorkBuddy / Claude，MCP 服务器会自动启动。确保**微信 PC 版已登录且运行中**（pyweixin 通过 UI 自动化驱动微信客户端）。

## MCP 工具

| 工具 | 功能 |
|------|------|
| `wechat_send_message` | 向好友发送单条消息 |
| `wechat_send_multiple_messages` | 向好友发送多条消息 |
| `wechat_send_to_multiple_friends` | 向多人发送同一条消息 |
| `wechat_send_file` | 向好友发送文件（PDF、图片等） |
| `wechat_search_contacts` | 搜索微信联系人 |
| `wechat_get_chat_history` | 获取聊天记录 |
| `wechat_open_dialog` | 打开与好友的聊天窗口 |
| `wechat_get_status` | 获取微信运行状态 |
| `wechat_run_command` | 执行系统命令 |

## 要求

- Python 3.10+
- 微信 PC 版 4.1+（已登录、运行中）
- Windows（pyweixin 依赖 `pywinauto` / `pywin32` 等 Windows 专用库）

## 第三方组件与许可

本项目将 [`pyweixin`](https://github.com/Hello-Mr-Crab/pywechat)（来自 `Hello-Mr-Crab/pywechat`，位于仓库根 `pyweixin/` 目录）以 vendored 形式内置，以规避其未发布到 PyPI 导致无法 `pip install` 的问题。其许可遵循上游仓库，使用前请自行查阅上游 LICENSE。

## License

MIT
