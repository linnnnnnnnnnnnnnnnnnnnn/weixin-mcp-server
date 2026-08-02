# weixin-mcp-server

微信 MCP Server，基于 `pyweixin`，兼容微信 **4.1+**（最新 4.1.12）。

## 特性

- ✅ 兼容微信 **4.1.12**（最新官方版）
- ✅ 基于 `pyweixin`（非 pywechat）
- ✅ 9 个 MCP 工具：发消息、发文件、查聊天记录、搜索联系人等
- ✅ 通过 Hermes MCP 标准协议接入
- ✅ 支持开机自启动

## 快速开始

### 1. 安装 pyweixin

```bash
pip install pyweixin
```

### 2. 安装到 Hermes

```bash
# 克隆仓库
git clone https://github.com/linnnnnnnnnnnnnnnnnnnnn/weixin-mcp-server.git

# 复制到 hermes-home/mcp/
cp -r weixin-mcp-server ~/.hermes/mcp/

# 配置 Hermes
hermes config set mcp_servers.weixin-server.command python
hermes config set mcp_servers.weixin-server.args '["-m", "src.server"]'
hermes config set mcp_servers.weixin-server.cwd "$HOME/.hermes/mcp/weixin-server"
```

### 3. 重启 Hermes

MCP 服务器会自动启动。

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
- 微信 PC 版 4.1+
- `pyweixin` 库
- `fastmcp` 库

## License

MIT
