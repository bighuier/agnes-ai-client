# Agnes AI 诊断工具
import requests, sys

BASE = "http://localhost:3001"

def check(label, fn):
    try:
        r = fn()
        print(f"[OK] {label}")
        return True
    except Exception as e:
        print(f"[FAIL] {label}: {e}")
        return False

def main():
    print("Agnes AI 诊断工具")
    print("="*50)
    check("服务器响应", lambda: requests.get(BASE, timeout=5))
    check("配置接口", lambda: requests.get(f"{BASE}/api/config", timeout=5))
    check("提示词列表", lambda: requests.get(f"{BASE}/api/prompts", timeout=5))
    print("="*50)
    print("诊断完成")

if __name__ == "__main__":
    main()
