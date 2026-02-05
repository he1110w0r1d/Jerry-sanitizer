#!/usr/bin/sh

# 1. 确保在正确的项目目录
cd C:/Users/Administrator/clawd/projects/jerry-sanitizer

echo "🧪 Starting Jerry-Sanitizer Sandbox Test..."

# 2. 在后台启动 Mock 402 服务器
echo "📡 Launching Mock 402 Server on port 8042..."
python mock_402_server.py &
SERVER_PID=$!

# 给服务器一点启动时间
sleep 2

# 3. 运行客户端进行支付流程测试
echo "🤖 Running JerryHttpClient to fetch paid content..."
python request_client.py

# 4. 测试结束，清理后台进程
echo "🧹 Cleaning up..."
kill $SERVER_PID

echo "✅ Sandbox test completed."
