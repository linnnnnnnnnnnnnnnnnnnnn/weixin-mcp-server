@echo off
REM weixin-mcp-server installer for Windows
REM pyweixin 已内置（vendored）于仓库根 pyweixin\ 目录，无需 pip install pyweixin

echo Installing dependencies from requirements.txt...
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

echo.
echo Installation complete!
echo.
echo Configure your MCP client (Hermes / WorkBuddy / Claude) with:
echo   command: "C:\path\to\weixin-mcp-server\.venv\Scripts\python.exe"  (或你的 python 绝对路径)
echo   args:    ["-m", "src.server"]
echo   cwd:     "C:\path\to\weixin-mcp-server"   (可选，server.py 已自动注入仓库根到 sys.path)
echo.
echo NOTE: 使用绝对路径的 python 启动器，确保上述依赖可被找到。
echo.
pause
