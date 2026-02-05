import json
import os

class JerrySanitizer:
    def __init__(self, config_path='policy.json'):
        self.config_path = config_path
        self.policy = self._load_policy()

    def _load_policy(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {
            "whitelist_destinations": [],
            "max_amount_per_tx": 0.05,
            "daily_budget": 0.50,
            "auto_approve_threshold": 0.01
        }

    def audit_payment(self, payment_info):
        """
        审计支付请求。返回 'approve', 'deny', 或 'require_human'
        """
        amount = float(payment_info.get('amount', 0))
        destination = payment_info.get('destination', '')
        
        # 1. 检查黑名单/白名单 (此处示例简化为白名单)
        is_whitelisted = destination in self.policy.get('whitelist_destinations', [])
        
        # 2. 检查单笔限额
        if amount > self.policy.get('max_amount_per_tx', 0.05):
            return "deny", "Amount exceeds maximum per transaction limit."
            
        # 3. 自动化决策逻辑
        if is_whitelisted and amount <= self.policy.get('auto_approve_threshold', 0.01):
            return "approve", "Auto-approved: Whitelisted and below threshold."
            
        # 4. 默认需要人工介入
        return "require_human", f"Payment of {amount} to {destination} requires manual approval."

if __name__ == "__main__":
    # 简单测试
    sanitizer = JerrySanitizer()
    test_req = {"amount": "0.005", "destination": "0xABC", "asset": "USDC"}
    decision, reason = sanitizer.audit_payment(test_req)
    print(f"Decision: {decision} | Reason: {reason}")
