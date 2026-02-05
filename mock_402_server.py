from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Mock402Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/secret-data':
            # 检查是否包含模拟的支付签名 (x402 protocol: PAYMENT-SIGNATURE)
            auth_header = self.headers.get('PAYMENT-SIGNATURE')
            
            if not auth_header:
                # 返回 402 Payment Required
                self.send_response(402)
                self.send_header('Content-Type', 'application/json')
                # x402 核心 Header：告知支付详情
                # 示例：金额 0.01 USDC, 收款地址, 链 ID (Base)
                payment_info = {
                    "amount": "0.01",
                    "asset": "USDC",
                    "destination": "0xJerrysWalletAddressPlaceholder",
                    "network": "eip155:8453", # Base Mainnet
                    "reason": "Access to Jerry's Secret Knowledge"
                }
                self.send_header('PAYMENT-REQUIRED', json.dumps(payment_info))
                self.end_headers()
                
                response = {
                    "error": "Payment Required",
                    "message": "This resource costs 0.01 USDC via x402 protocol."
                }
                self.wfile.write(json.dumps(response).encode())
            else:
                # 模拟支付验证通过
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"data": "Success! Here is the secret intelligence."}).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=Mock402Handler, port=8042):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting Mock 402 Server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
