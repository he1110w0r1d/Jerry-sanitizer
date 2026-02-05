import requests
import json
from sanitizer_engine import JerrySanitizer

class JerryHttpClient:
    def __init__(self):
        self.sanitizer = JerrySanitizer()

    def get_with_payment(self, url):
        print(f"Requesting: {url}")
        
        # 1. 尝试第一次请求
        response = requests.get(url)
        
        # 2. 检查是否触发 402 Payment Required
        if response.status_code == 402:
            print("HTTP 402: Payment Required detected.")
            
            # 从 Header 中提取支付指令 (x402 标准)
            payment_header = response.headers.get('PAYMENT-REQUIRED')
            if not payment_header:
                print("Error: 402 received but no PAYMENT-REQUIRED header found.")
                return response
            
            payment_info = json.loads(payment_header)
            
            # 3. 调用审计引擎
            decision, reason = self.sanitizer.audit_payment(payment_info)
            print(f"Audit Decision: {decision} ({reason})")
            
            if decision == "approve":
                # 模拟支付过程 (实际会调用钱包 SDK)
                print(f"Auto-paying {payment_info['amount']} {payment_info['asset']}...")
                mock_signature = "sig_valid_payment_from_jerry"
                
                # 4. 带着支付签名再次请求
                final_response = requests.get(url, headers={'PAYMENT-SIGNATURE': mock_signature})
                return final_response
            
            elif decision == "require_human":
                print(f"ALERT: Please approve payment on Telegram: {reason}")
                # 这里未来会集成 message 工具发送 Telegram 按钮
                return response
            
            else:
                print(f"Denied: {reason}")
                return response
        
        return response

if __name__ == "__main__":
    client = JerryHttpClient()
    # 模拟访问我们的 Mock Server
    res = client.get_with_payment("http://localhost:8042/api/secret-data")
    
    if res.status_code == 200:
        print(f"Final Data Received: {res.json()}")
    else:
        print(f"Failed with status: {res.status_code}")
