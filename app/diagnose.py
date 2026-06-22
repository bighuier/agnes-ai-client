import http.client, json
H = "localhost"; P = 3001
def t(m, p, b=None):
    try:
        c = http.client.HTTPConnection(H, P, timeout=10)
        if b: c.request(m, p, json.dumps(b), {"Content-Type":"application/json"})
        else: c.request(m, p)
        r = c.getresponse(); b = r.read().decode()
        print(f"{m} {p} -> HTTP {r.status}, type={r.getheader('Content-Type','?')[:30]}, body={b[:200]}")
    except Exception as e: print(f"{m} {p} -> FAIL: {e}")
print(f"=== 诊断 {H}:{P} ===\n")
t("GET", "/")
t("GET", "/api/config")
t("POST", "/api/prompts/analyze", {"text":"cat on beach"})
t("GET", "/api/prompts")
print("\n如果1-4都返回200+JSON  -> Flask正常，前端问题")
print("如果1返回HTML (含DOCTYPE) -> 端口上有其他服务，不是Flask")
print("如果全部失败              -> Flask没启动")
print("修复: taskkill /F /PID 端口PID 再重启 server.py")
