@echo off
REM weixin-mcp-server installer for Windows

echo Installing pyweixin...
pip install pyweixin

echo Installing fastmcp...
pip install fastmcp

echo.
echo Installation complete!
echo.
echo Now add to Hermes config:
echo   hermes config set mcp_servers.weixin-server.command python
echo   hermes config set mcp_servers.weixin-server.args '["-m", "src.server"]'
echo   hermes config set mcp_servers.weixin-server.cwd "%cd%"
echo.
pause
