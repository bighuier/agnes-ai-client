import sys, flask, json, os, sqlite3, uuid, urllib.request, datetime, re, webbrowser, base64
from flask import request, jsonify, send_from_directory
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key().decode()

def get_encryption_key():
    key_path = os.path.join(DATA_DIR, ".key")
    if os.path.exists(key_path):
        with open(key_path, 'r') as f:
            return f.read()
    key = generate_key()
    with open(key_path, 'w') as f:
        f.write(key)
    return key

def encrypt_api_key(api_key):
    if not api_key:
        return ""
    key = get_encryption_key()
    f = Fernet(key)
    return f.encrypt(api_key.encode()).decode()

def decrypt_api_key(encrypted_key):
    if not encrypted_key:
        return ""
    try:
        key = get_encryption_key()
        f = Fernet(key)
        return f.decrypt(encrypted_key.encode()).decode()
    except:
        return ""

def get_app_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APP_DIR = get_app_path()
DATA_DIR = os.path.join(APP_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
IMG_DIR = os.path.join(APP_DIR, "generated-images")
os.makedirs(IMG_DIR, exist_ok=True)

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), relative_path)

BASE = get_resource_path(".")
DB_PATH = os.path.join(DATA_DIR, "prompts.db")
CONFIG_PATH = os.path.join(DATA_DIR, "config.json")
def load(): 
    if os.path.exists(CONFIG_PATH):
        data = json.load(open(CONFIG_PATH))
        data["api_key"] = decrypt_api_key(data.get("api_key", ""))
        return data
    return {"api_key":"","agnes_api_base":"https://apihub.agnes-ai.com"}

def save(c): 
    data = dict(c)
    if "api_key" in data:
        data["api_key"] = encrypt_api_key(data["api_key"])
    json.dump(data, open(CONFIG_PATH,"w"), indent=2)

cfg = load(); AGNES = cfg.get("agnes_api_base", "https://apihub.agnes-ai.com")
def init_db():
    c = sqlite3.connect(DB_PATH)
    c.execute("CREATE TABLE IF NOT EXISTS prompts(id INTEGER PRIMARY KEY AUTOINCREMENT,text TEXT,title_cn TEXT,category TEXT,tags TEXT,style TEXT,focal_length TEXT,aperture TEXT,lighting TEXT,composition TEXT,perspective TEXT,color_tone TEXT,quality_style TEXT,shot_type TEXT,camera_movement TEXT,transition TEXT,focus_technique TEXT,character_action TEXT,character_expression TEXT,mood_atmosphere TEXT,usage_ TEXT,source_tab TEXT,favorite INTEGER DEFAULT 0,rating INTEGER DEFAULT 0,notes TEXT,created_at TEXT,updated_at TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS categories(name TEXT PRIMARY KEY,count INTEGER DEFAULT 0)")
    c.commit()
    for col in ["focal_length","aperture","lighting","composition","perspective","color_tone","quality_style","shot_type","camera_movement","transition","focus_technique","character_action","character_expression","mood_atmosphere","rating","notes"]:
        try: c.execute("ALTER TABLE prompts ADD COLUMN "+col+" TEXT"); c.commit()
        except: pass
    c.execute("INSERT OR IGNORE INTO categories(name) SELECT DISTINCT category FROM prompts WHERE category!=''")
    c.execute("UPDATE categories SET count=(SELECT COUNT(*) FROM prompts WHERE category=name)")
    c.commit(); c.close()
init_db()
def proxy(url, body=None, method="GET"):
    key = cfg.get("api_key","")
    if not key:
        return ({"error":"API Key 未配置，请先在设置中填写 API Key"}, "application/json")
    headers = {"Authorization":"Bearer "+key,"Content-Type":"application/json"}
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(req, timeout=300)
        raw = resp.read(); ct = resp.headers.get("Content-Type","")
        if "image" in ct: return raw, ct
        return json.loads(raw), ct
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print("[API Error]", e.code, url, err[:500])
        try:
            err_json = json.loads(err)
            return (err_json, "application/json")
        except:
            return ({"error":"API返回错误 HTTP "+str(e.code)+": "+err[:300]}, "application/json")
    except Exception as e:
        print("[Proxy Error]", url, str(e))
        return ({"error":str(e)}, "application/json")
app = flask.Flask(__name__, static_folder=os.path.join(BASE, "static"), static_url_path="/static")
@app.after_request
def cors(r):
    r.headers["Access-Control-Allow-Origin"]="*"
    r.headers["Access-Control-Allow-Headers"]="*"
    r.headers["Access-Control-Allow-Methods"]="*"
    return r
@app.route("/")
def idx():
    h=open(os.path.join(BASE,"templates","index.html"),encoding="utf-8").read()
    v="?v=20260622"
    h=h.replace("</body></html>","<script src=/static/js/enhance.js"+v+"></script><script src=/static/js/enhance2.js"+v+"></script><script src=/static/js/enhance4.js"+v+"></script><script src=/static/js/enhance5.js"+v+"></script><script src=/static/js/enhance6.js"+v+"></script><script src=/static/js/enhance7.js"+v+"></script><script src=/static/js/enhance8.js"+v+"></script><script src=/static/js/enhance9.js"+v+"></script></body></html>")
    return h
@app.route("/api/config", methods=["GET","POST","DELETE"])
def cfg_route():
    if request.method == "POST":
        d = request.json
        if "api_key" in d: cfg["api_key"]=d["api_key"]; save(cfg)
        return jsonify({"ok":True})
    if request.method == "DELETE":
        cfg["api_key"] = ""
        save(cfg)
        return jsonify({"ok":True})
    return jsonify({"has_key":bool(cfg.get("api_key"))})
@app.route("/api/v1/images/generations", methods=["POST"])
def proxy_img(): r,c=proxy(AGNES+"/v1/images/generations",request.json,"POST"); return (jsonify(r), 400) if isinstance(r,dict) and r.get("error") else jsonify(r)
@app.route("/api/v1/videos", methods=["POST"])
def proxy_vid(): r,c=proxy(AGNES+"/v1/videos",request.json,"POST"); return (jsonify(r), 400) if isinstance(r,dict) and r.get("error") else jsonify(r)
@app.route("/api/videos/query", methods=["GET"])
def proxy_vq(): return jsonify(proxy(AGNES+"/agnesapi?video_id="+request.args.get("video_id","")+"&model_name="+request.args.get("model_name","agnes-video-v2.0"))[0])
@app.route("/api/v1/chat/completions", methods=["POST"])
def proxy_chat(): r,c=proxy(AGNES+"/v1/chat/completions",request.json,"POST"); return (jsonify(r), 400) if isinstance(r,dict) and r.get("error") else jsonify(r)
@app.route("/api/prompts/enhance", methods=["POST"])
def enhance():
    text = request.json.get("text","")
    vocab = request.json.get("vocab","")
    if not text: return jsonify({"error":"no text"}),400
    sys_msg="你是专业AI提示词工程师。将简单描述扩展为详细的专业提示词，包含摄影参数、光线、构图、风格等。输出以中文为主，仅保留必要的英文专业术语（如镜头参数焦段光圈等）。"
    user_msg="请扩展以下描述为专业提示词：\n"+text
    if vocab:
        sys_msg="你是专业AI提示词工程师。结合用户提供的专业词汇和描述，生成详细的专业提示词。自然地融入所有指定的专业词汇，使其与描述内容协调统一。输出以中文为主，仅保留必要的英文专业术语（如镜头参数焦段光圈等）。"
        user_msg="请根据以下专业词汇和描述生成专业提示词：\n\n【用户描述】\n"+text+"\n\n【选定的专业词汇】\n"+vocab+"\n\n请将上述专业词汇自然融入提示词中，生成一段连贯、专业的提示词。"
    r,c = proxy(AGNES+"/v1/chat/completions",{"model":"agnes-2.0-flash","messages":[
        {"role":"system","content":sys_msg},
        {"role":"user","content":user_msg}
    ]},"POST")
    if isinstance(r,dict)and r.get("error"): return jsonify({"enhanced":text})
    try: return jsonify({"enhanced":r["choices"][0]["message"]["content"].strip()})
    except: return jsonify({"enhanced":text})

@app.route("/api/prompts/reverse", methods=["POST"])
def reverse_prompt():
    image_data = request.json.get("image","")
    if not image_data: return jsonify({"error":"请先上传图片"}),400
    
    sys_msg="你是专业AI提示词工程师。分析图片并生成详细的专业提示词，直接输出可用于AI图像生成的提示词，不要包含额外解释。输出以英文为主，包含摄影参数、光线、构图、风格等要素。"
    user_msg="分析这张图片并生成专业的AI图像生成提示词："
    
    try:
        r,c = proxy(AGNES+"/v1/chat/completions",{"model":"agnes-2.0-flash","messages":[
            {"role":"system","content":sys_msg},
            {"role":"user","content":[
                {"type":"text","text":user_msg},
                {"type":"image_url","image_url":{"url":image_data}}
            ]}
        ]},"POST")
        
        if isinstance(r, dict):
            if r.get("error"): 
                return jsonify({"error":str(r.get("error"))}),400
            elif "choices" in r:
                try: 
                    prompt = r["choices"][0]["message"]["content"].strip()
                    prompt = prompt.replace('```', '').strip()
                    return jsonify({"prompt":prompt})
                except Exception as e:
                    return jsonify({"error":"解析失败: "+str(e)}),500
            else:
                return jsonify({"error":"未知响应格式"}),500
        else:
            return jsonify({"error":"API返回格式错误"}),500
            
    except Exception as e:
        return jsonify({"error":"请求失败: "+str(e)}),500
@app.route("/api/prompts/analyze_simple", methods=["POST"])
def analyze_simple():
    text = request.json.get("text","")
    if not text: return jsonify({"error":"no text"}),400
    t = text.lower(); cat="其他"; tl=["portrait","face","woman","man","person","girl","boy","people","character","model"]; sl=["landscape","mountain","ocean","beach","forest","sky","sunset","nature","cityscape"]; fl=["cyberpunk","futuristic","robot","spaceship","sci-fi","neon","mecha"]; fn=["fantasy","magic","dragon","elf","castle","witch","mythical","medieval"]; al=["cat","dog","animal","pet","wolf","bird","fish","horse","lion"]; bl=["architecture","building","interior","house","room","city","urban"]; pl=["product","commercial","still life","object"]; fol=["food","drink","coffee","dessert","meal","fruit","bread"]; stl=["street","candid","documentary","urban","travel"]; il=["illustration","concept art","painting","drawing","artwork","cartoon"]; ab=["abstract","geometric","pattern","texture","minimal"]; ph=["photo","photograph","shot","camera","lens","film"]
    if any(w in t for w in tl): cat="人物肖像"
    elif any(w in t for w in sl): cat="风景"
    elif any(w in t for w in fl): cat="科幻"
    elif any(w in t for w in fn): cat="奇幻"
    elif any(w in t for w in al): cat="动物"
    elif any(w in t for w in bl): cat="建筑"
    elif any(w in t for w in pl): cat="产品摄影"
    elif any(w in t for w in fol): cat="美食"
    elif any(w in t for w in stl): cat="街拍纪实"
    elif any(w in t for w in il): cat="插画概念艺术"
    elif any(w in t for w in ab): cat="抽象艺术"
    elif any(w in t for w in ph): cat="摄影通用"
    tags=[cat]
    if any(w in t for w in ["golden hour","sunset","sunrise"]): tags.append("黄金时刻")
    if any(w in t for w in ["cinematic","film","movie"]): tags.append("电影感")
    if any(w in t for w in ["bokeh","shallow","f/"]): tags.append("大光圈")
    if any(w in t for w in ["wide-angle","wide angle"]): tags.append("广角")
    if any(w in t for w in ["close-up","closeup","macro"]): tags.append("特写")
    if any(w in t for w in ["cyberpunk","neon"]): tags.append("赛博朋克")
    usage = "文生图"
    if any(w in t for w in ["video","motion","animation","movement","walking","running","turning"]): usage = "文生视频"
    title = re.split(r'[,，。\.\n]', text)[0][:25] if len(text)>25 else text
    return jsonify({"title_cn":title,"category":cat,"tags":tags,"style":"","focal_length":"","aperture":"","lighting":"","composition":"","perspective":"","color_tone":"","quality_style":"","shot_type":"","camera_movement":"","transition":"","focus_technique":"","character_action":"","character_expression":"","mood_atmosphere":"","usage":usage,"_mode":"simple"})
@app.route("/api/prompts/analyze", methods=["POST"])
def analyze():
    text = request.json.get("text","")
    if not text: return jsonify({"error":"no text"}),400
    prompt = 'You are a professional AI prompt analyst. Analyze the following AI image/video generation prompt and extract structured information.\nReturn ONLY a JSON object (no other text) with all fields filled. If a field is not found, use empty string or empty array.\n\nPrompt:\n'+text+'\n\nReturn JSON format:\n{"title_cn":"中文标题(15字内)","category":"主分类: 人物肖像/风景/科幻/奇幻/动物/建筑/产品摄影/美食/街拍纪实/插画概念艺术/抽象艺术/摄影通用/其他","tags":["标签"],"style":"一句话风格描述","focal_length":"焦距","aperture":"光圈","lighting":"光线","composition":"构图","perspective":"视角","color_tone":"色调","quality_style":"画质风格","shot_type":"景别","camera_movement":"运镜","transition":"镜头切换","focus_technique":"焦点技巧","character_action":"人物动作","character_expression":"人物表情","mood_atmosphere":"情绪氛围","usage":"适用场景"}'
    r,c = proxy(AGNES+"/v1/chat/completions",{"model":"agnes-2.0-flash","messages":[
        {"role":"system","content":"You analyze AI prompts and return structured JSON."},
        {"role":"user","content":prompt}
    ]},"POST")
    if isinstance(r,dict)and r.get("error"):
        return jsonify({"title_cn":"","category":"其他","tags":[],"style":"","focal_length":"","aperture":"","lighting":"","composition":"","perspective":"","color_tone":"","quality_style":"","shot_type":"","camera_movement":"","transition":"","focus_technique":"","character_action":"","character_expression":"","mood_atmosphere":"","usage":""})
    try:
        cnt = r["choices"][0]["message"]["content"]
        m = re.search(r"\{.*\}", cnt, re.DOTALL)
        return jsonify(json.loads(m.group() if m else cnt))
    except: return jsonify({"category":"其他","tags":[],"style":"","usage":""})
FIELDS = ["text","title_cn","category","tags","style","focal_length","aperture","lighting","composition","perspective","color_tone","quality_style","shot_type","camera_movement","transition","focus_technique","character_action","character_expression","mood_atmosphere","usage_","source_tab","favorite","rating","notes"]
@app.route("/api/prompts", methods=["GET","POST"])
def prompts():
    if request.method == "POST":
        d = request.json; now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        vals = [d.get(k,"") for k in FIELDS] + [now,now]
        c = sqlite3.connect(DB_PATH)
        cur = c.execute("INSERT INTO prompts("+",".join(FIELDS)+",created_at,updated_at) VALUES("+",".join(["?"]*len(FIELDS))+",?,?)", vals)
        pid = cur.lastrowid
        c.execute("INSERT OR IGNORE INTO categories(name) VALUES(?)",[d.get("category","其他")])
        c.execute("UPDATE categories SET count=(SELECT COUNT(*) FROM prompts WHERE category=name)")
        c.commit(); c.close()
        return jsonify({"id":pid,"ok":True})
    q = request.args.get("q",""); tag = request.args.get("tag",""); cat = request.args.get("category",""); fav = request.args.get("fav","")
    params=[]; where=[]
    if q:
        like="%"+q+"%"
        where.append("(text LIKE ? OR title_cn LIKE ? OR tags LIKE ? OR style LIKE ? OR focal_length LIKE ? OR aperture LIKE ? OR lighting LIKE ? OR composition LIKE ? OR perspective LIKE ? OR color_tone LIKE ? OR quality_style LIKE ? OR shot_type LIKE ? OR camera_movement LIKE ? OR transition LIKE ? OR focus_technique LIKE ? OR character_action LIKE ? OR character_expression LIKE ? OR mood_atmosphere LIKE ?)")
        params.extend([like]*18)
    if tag: where.append("tags LIKE ?"); params.append("%"+tag+"%")
    if cat: where.append("category=?"); params.append(cat)
    if fav: where.append("favorite=1")
    w = "WHERE "+" AND ".join(where) if where else ""
    c = sqlite3.connect(DB_PATH); c.row_factory = sqlite3.Row
    rows = c.execute("SELECT * FROM prompts "+w+" ORDER BY created_at DESC LIMIT 100",params).fetchall()
    total = c.execute("SELECT COUNT(*) FROM prompts "+w,params).fetchone()[0]
    cat_rows = c.execute("SELECT name,count FROM categories ORDER BY count DESC").fetchall()
    if not cat_rows:
        cat_rows = c.execute("SELECT category,COUNT(*) FROM prompts WHERE category!='' GROUP BY category ORDER BY COUNT(*) DESC").fetchall()
    cats = {r[0]:r[1] for r in cat_rows}
    c.close()
    items = [{k:row[k] for k in row.keys()} for row in rows]
    for it in items:
        if isinstance(it.get("tags"),str):
            try: it["tags"]=json.loads(it["tags"])
            except: it["tags"]=[]
    return jsonify({"items":items,"total":total,"categories":cats})
@app.route("/api/prompts/<int:pid>", methods=["GET","PUT","DELETE"])
def prompt_detail(pid):
    c = sqlite3.connect(DB_PATH)
    if request.method == "DELETE":
        c.execute("DELETE FROM prompts WHERE id=?",[pid]); c.commit()
        c.execute("UPDATE categories SET count=(SELECT COUNT(*) FROM prompts WHERE category=name)"); c.commit(); c.close()
        return jsonify({"ok":True})
    if request.method == "PUT":
        d = request.json; sets=[]; params=[]
        for k in FIELDS:
             if k not in d: continue
             val = d[k]
             if isinstance(val, list):
                 val = json.dumps(val)
             sets.append(k+"=?"); params.append(val)
        sets.append("updated_at=?")
        params.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")); params.append(pid)
        c.execute("UPDATE prompts SET "+",".join(sets)+" WHERE id=?",params); c.commit()
        c.execute("UPDATE categories SET count=(SELECT COUNT(*) FROM prompts WHERE category=name)"); c.commit()
    c.row_factory = sqlite3.Row
    row = c.execute("SELECT * FROM prompts WHERE id=?",[pid]).fetchone(); c.close()
    if not row: return jsonify({"error":"not found"}),404
    it = {k:row[k] for k in row.keys()}
    if isinstance(it.get("tags"),str):
        try: it["tags"]=json.loads(it["tags"])
        except: it["tags"]=[]
    return jsonify(it)
@app.route("/save-image", methods=["POST"])
def save_img():
    u = request.json.get("url","")
    if not u: return jsonify({"error":"no url"}),400
    e=".png"; l=u.lower()
    if ".jpg" in l or ".jpeg" in l: e=".jpg"
    elif ".webp" in l: e=".webp"
    fn = uuid.uuid4().hex[:8]+e
    try:
        urllib.request.urlretrieve(u, os.path.join(IMG_DIR, fn))
        return jsonify({"local_url":"/generated-images/"+fn,"filename":fn})
    except: return jsonify({"error":"save failed"}),500
@app.route("/generated-images/<path:fn>")
def serve_img(fn): return send_from_directory(IMG_DIR, fn)
@app.route("/api/categories", methods=["GET","POST"])
def categories_route():
    c = sqlite3.connect(DB_PATH)
    if request.method == "POST":
        name = request.json.get("name","").strip()
        if name: c.execute("INSERT OR IGNORE INTO categories(name) VALUES(?)",[name]); c.commit()
    rows = c.execute("SELECT name,count FROM categories ORDER BY count DESC").fetchall()
    if not rows:
        rows = c.execute("SELECT category,COUNT(*) FROM prompts WHERE category!='' GROUP BY category ORDER BY COUNT(*) DESC").fetchall()
    c.close()
    return jsonify({r[0]:r[1] for r in rows})
@app.route("/api/categories/add", methods=["POST"])
def category_add():
    name = request.json.get("name","").strip()
    if not name: return jsonify({"error":"empty"}),400
    c = sqlite3.connect(DB_PATH)
    c.execute("INSERT OR IGNORE INTO categories(name) VALUES(?)",[name]); c.commit(); c.close()
    return jsonify({"ok":True})
@app.route("/api/categories/rename", methods=["POST"])
def category_rename():
    old = request.json.get("old","").strip()
    new = request.json.get("new","").strip()
    if not old or not new: return jsonify({"error":"bad request"}),400
    c = sqlite3.connect(DB_PATH)
    c.execute("UPDATE prompts SET category=? WHERE category=?",[new,old])
    c.execute("INSERT OR IGNORE INTO categories(name) VALUES(?)",[new])
    c.execute("DELETE FROM categories WHERE name=?",[old])
    c.execute("UPDATE categories SET count=(SELECT COUNT(*) FROM prompts WHERE category=name)")
    c.commit(); c.close()
    return jsonify({"ok":True})
@app.route("/api/categories/delete", methods=["POST"])
def category_delete():
    name = request.json.get("name","").strip()
    if not name: return jsonify({"error":"empty"}),400
    c = sqlite3.connect(DB_PATH)
    c.execute("UPDATE prompts SET category=? WHERE category=?",["\u5176\u4ed6",name])
    c.execute("DELETE FROM categories WHERE name=?",[name])
    c.execute("UPDATE categories SET count=(SELECT COUNT(*) FROM prompts WHERE category=name)")
    c.commit(); c.close()
    return jsonify({"ok":True})
@app.route("/api/prompts/export", methods=["GET"])
def prompts_export():
    c = sqlite3.connect(DB_PATH); c.row_factory = sqlite3.Row
    rows = c.execute("SELECT * FROM prompts ORDER BY created_at DESC").fetchall()
    items = [{k:row[k] for k in row.keys()} for row in rows]
    for it in items:
        if isinstance(it.get("tags"),str):
            try: it["tags"]=json.loads(it["tags"])
            except: it["tags"]=[]
    cats = {r[0]:r[1] for r in c.execute("SELECT name,count FROM categories").fetchall()}
    c.close()
    return jsonify({"items":items,"categories":cats,"exported_at":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"version":"1.0"})
@app.route("/api/prompts/import", methods=["POST"])
def prompts_import():
    d = request.json
    items = d.get("items",[])
    if not items: return jsonify({"error":"no items"}),400
    c = sqlite3.connect(DB_PATH)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    added = 0; skipped = 0
    for it in items:
        text = it.get("text","")
        if not text: skipped+=1; continue
        if isinstance(it.get("tags"),list):
            it["tags"] = json.dumps(it["tags"],ensure_ascii=False)
        vals = [it.get(k,"") for k in FIELDS] + [now,now]
        c.execute("INSERT INTO prompts("+",".join(FIELDS)+",created_at,updated_at) VALUES("+",".join(["?"]*len(FIELDS))+",?,?)",vals)
        cat = it.get("category","")
        if cat:
            c.execute("INSERT OR IGNORE INTO categories(name) VALUES(?)",[cat])
        added+=1
    c.execute("UPDATE categories SET count=(SELECT COUNT(*) FROM prompts WHERE category=name)")
    c.commit(); c.close()
    return jsonify({"ok":True,"added":added,"skipped":skipped})
TEMPLATES = [
  # 人像摄影
  {"name":"电影感人像","desc":"电影级光影人像，适合人物特写","category":"人物肖像","tags":["电影感","人像","光影"],"text":"cinematic portrait, dramatic side lighting, shallow depth of field, soft skin texture, professional studio lighting, 85mm lens, f/1.8, warm color grading, film grain","style":"电影级人像","focal_length":"85mm","aperture":"f/1.8","lighting":"侧光+轮廓光","composition":"三分法","perspective":"平视","color_tone":"暖色调","quality_style":"电影胶片质感","shot_type":"特写","mood_atmosphere":"戏剧性","usage":"文生图"},
  {"name":"自然光人像","desc":"柔和自然光户外人像","category":"人物肖像","tags":["自然光","户外","柔光"],"text":"natural light outdoor portrait, golden hour soft sunlight, bokeh background, gentle wind blowing hair, relaxed expression, 50mm lens, f/2.0, warm and soft tones, shallow depth of field","style":"自然光人像","focal_length":"50mm","aperture":"f/2.0","lighting":"黄金时刻自然光","composition":"居中构图","perspective":"平视","color_tone":"暖金色调","quality_style":"高清细腻","shot_type":"半身","mood_atmosphere":"温馨自然","usage":"文生图"},
  {"name":"时尚杂志人像","desc":"高端时尚杂志封面风格","category":"人物肖像","tags":["时尚","杂志","高端"],"text":"high fashion editorial portrait, dramatic studio lighting, bold makeup, sleek hairstyle, designer outfit, clean white background, sharp focus, 105mm lens, f/2.8, magazine cover style, vogue aesthetic","style":"时尚杂志","focal_length":"105mm","aperture":"f/2.8","lighting":"影棚闪光灯","composition":"居中对称","perspective":"微仰视","color_tone":"冷白色调","quality_style":"超高清","shot_type":"半身","mood_atmosphere":"高端精致","usage":"文生图"},
  {"name":"复古胶片人像","desc":"怀旧胶片风格人像","category":"人物肖像","tags":["复古","胶片","怀旧"],"text":"vintage film portrait, 35mm film grain, faded colors, light leaks, soft focus, nostalgic mood, analog camera aesthetic, warm muted tones, Kodak Portra 400 style, casual pose","style":"复古胶片","focal_length":"35mm","aperture":"f/2.8","lighting":"柔和散射光","composition":"随意抓拍","perspective":"平视","color_tone":"复古褪色","quality_style":"胶片颗粒感","shot_type":"半身","mood_atmosphere":"怀旧温馨","usage":"文生图"},
  # 风景摄影
  {"name":"黄金时刻风景","desc":"日出日落时分的壮丽风景","category":"风景","tags":["黄金时刻","日落","壮丽"],"text":"golden hour landscape, dramatic sunset sky with clouds, warm orange and pink light, silhouetted mountains, reflective lake, wide angle, f/11, deep depth of field, HDR, vivid colors, professional landscape photography","style":"风光大片","focal_length":"24mm","aperture":"f/11","lighting":"黄金时刻逆光","composition":"三分法+前景","perspective":"俯视","color_tone":"暖橙色调","quality_style":"HDR高清","shot_type":"远景","mood_atmosphere":"壮丽震撼","usage":"文生图"},
  {"name":"雾中森林","desc":"神秘朦胧的森林晨雾","category":"风景","tags":["森林","雾气","神秘"],"text":"misty forest at dawn, fog between tall trees, sunbeams breaking through canopy, mossy ground, ethereal atmosphere, cool blue tones, 35mm lens, f/8, long exposure, moody landscape","style":"意境风光","focal_length":"35mm","aperture":"f/8","lighting":"晨光穿雾","composition":"纵深引导线","perspective":"平视","color_tone":"冷蓝灰色调","quality_style":"细腻朦胧","shot_type":"中景","mood_atmosphere":"神秘宁静","usage":"文生图"},
  {"name":"星空银河","desc":"璀璨星空银河夜景","category":"风景","tags":["星空","银河","夜景"],"text":"milky way galaxy over mountain, starry night sky, astrophotography, long exposure, 14mm ultra wide angle, f/2.8, ISO 3200, 25 seconds exposure, dark sky location, purple and blue nebula colors, silhouette foreground","style":"星空摄影","focal_length":"14mm","aperture":"f/2.8","lighting":"星光+月光","composition":"前景+天空","perspective":"仰视","color_tone":"深蓝紫色","quality_style":"长曝光","shot_type":"超广角","mood_atmosphere":"浩瀚震撼","usage":"文生图"},
  {"name":"城市夜景","desc":"繁华都市夜景灯光","category":"风景","tags":["城市","夜景","灯光"],"text":"city skyline at night, long exposure light trails, neon reflections on wet streets, skyscrapers illuminated, urban photography, blue hour, 24mm wide angle, f/8, tripod shot, vibrant city lights","style":"城市风光","focal_length":"24mm","aperture":"f/8","lighting":"城市灯光+蓝调天空","composition":"对称构图","perspective":"微俯视","color_tone":"蓝紫+暖光","quality_style":"长曝光","shot_type":"远景","mood_atmosphere":"繁华现代","usage":"文生图"},
  # 产品摄影
  {"name":"白底产品照","desc":"电商白底商品展示图","category":"产品摄影","tags":["白底","电商","产品"],"text":"professional product photography on pure white background, studio lighting, soft shadows, clean and minimal, commercial product shot, 100mm macro lens, f/8, even lighting, high detail, e-commerce style","style":"电商白底","focal_length":"100mm","aperture":"f/8","lighting":"均匀柔光","composition":"居中","perspective":"平视","color_tone":"中性白","quality_style":"超清细节","shot_type":"特写","mood_atmosphere":"专业简洁","usage":"文生图"},
  {"name":"氛围产品照","desc":"带场景氛围的高端产品图","category":"产品摄影","tags":["氛围","高端","场景"],"text":"premium lifestyle product photography, elegant scene setup, natural props, warm ambient lighting, shallow depth of field, luxury feel, 85mm lens, f/2.8, soft bokeh background, editorial style, high-end brand aesthetic","style":"氛围产品","focal_length":"85mm","aperture":"f/2.8","lighting":"氛围暖光","composition":"黄金分割","perspective":"微俯视","color_tone":"暖棕色调","quality_style":"高端质感","shot_type":"中景","mood_atmosphere":"精致高级","usage":"文生图"},
  {"name":"美食特写","desc":"诱人的美食微距特写","category":"美食","tags":["美食","微距","诱人"],"text":"delicious food photography, steaming hot dish, close-up macro shot, shallow depth of field, warm appetizing colors, natural window light, 100mm macro lens, f/2.8, garnish details, professional food styling, mouth-watering presentation","style":"美食摄影","focal_length":"100mm","aperture":"f/2.8","lighting":"侧窗自然光","composition":"对角线构图","perspective":"45度俯拍","color_tone":"暖色调","quality_style":"微距高清","shot_type":"特写","mood_atmosphere":"诱人温暖","usage":"文生图"},
  {"name":"咖啡饮品","desc":"精致咖啡饮品拍摄","category":"美食","tags":["咖啡","饮品","精致"],"text":"artisan coffee photography, latte art close-up, ceramic cup on wooden table, steam rising, warm cafe atmosphere, bokeh background, 50mm lens, f/2.0, soft window light, cozy morning vibe, professional beverage styling","style":"饮品摄影","focal_length":"50mm","aperture":"f/2.0","lighting":"窗边柔光","composition":"偏心构图","perspective":"45度角","color_tone":"暖棕色调","quality_style":"高清细腻","shot_type":"特写","mood_atmosphere":"温馨惬意","usage":"文生图"},
  # 建筑摄影
  {"name":"现代建筑外观","desc":"现代建筑外观拍摄","category":"建筑","tags":["建筑","现代","外观"],"text":"modern architecture exterior, clean geometric lines, glass and steel facade, blue sky background, symmetrical composition, 24mm tilt-shift lens, f/11, converging lines, professional architectural photography, sharp detail","style":"建筑摄影","focal_length":"24mm移轴","aperture":"f/11","lighting":"侧光","composition":"对称构图","perspective":"仰视","color_tone":"冷蓝色调","quality_style":"超高清","shot_type":"全景","mood_atmosphere":"现代大气","usage":"文生图"},
  {"name":"室内设计","desc":"精美室内空间展示","category":"建筑","tags":["室内","设计","空间"],"text":"interior design photography, spacious modern living room, natural light through large windows, minimalist furniture, wide angle, 16mm lens, f/8, HDR, balanced exposure, real estate photography style, clean and bright","style":"室内摄影","focal_length":"16mm","aperture":"f/8","lighting":"自然光+补光","composition":"一点透视","perspective":"平视","color_tone":"明亮中性","quality_style":"HDR","shot_type":"全景","mood_atmosphere":"宽敞明亮","usage":"文生图"},
  # 动物摄影
  {"name":"宠物写真","desc":"可爱宠物肖像拍摄","category":"动物","tags":["宠物","可爱","写真"],"text":"adorable pet portrait, shallow depth of field, catchlight in eyes, soft fur texture, 85mm lens, f/2.0, natural outdoor light, bokeh green background, professional pet photography, warm and cute","style":"宠物写真","focal_length":"85mm","aperture":"f/2.0","lighting":"自然柔光","composition":"三分法","perspective":"平视","color_tone":"暖色调","quality_style":"高清细腻","shot_type":"特写","mood_atmosphere":"可爱温馨","usage":"文生图"},
  {"name":"野生动物","desc":"野生动物自然栖息地","category":"动物","tags":["野生动物","自然","壮丽"],"text":"wildlife photography, majestic animal in natural habitat, telephoto lens, 400mm, f/4, fast shutter speed, golden hour, National Geographic style, sharp detail, blurred background, dramatic natural scene","style":"野生动物","focal_length":"400mm","aperture":"f/4","lighting":"黄金时刻","composition":"三分法","perspective":"平视","color_tone":"自然色调","quality_style":"超清远摄","shot_type":"中景","mood_atmosphere":"壮丽自然","usage":"文生图"},
  # 插画概念艺术
  {"name":"赛博朋克城市","desc":"霓虹灯下的未来城市","category":"插画概念艺术","tags":["赛博朋克","霓虹","未来"],"text":"cyberpunk cityscape, neon lights reflecting on wet streets, futuristic skyscrapers, holographic advertisements, rain, purple and cyan color scheme, blade runner aesthetic, 35mm lens, moody atmosphere, sci-fi urban","style":"赛博朋克","focal_length":"35mm","aperture":"f/2.8","lighting":"霓虹灯光","composition":"纵深构图","perspective":"仰视","color_tone":"紫青色调","quality_style":"概念艺术","shot_type":"远景","mood_atmosphere":"未来压抑","usage":"文生图"},
  {"name":"奇幻角色","desc":"奇幻风格角色概念设计","category":"插画概念艺术","tags":["奇幻","角色","概念设计"],"text":"fantasy character concept art, detailed armor and weapons, magical glowing effects, dramatic backlighting, epic pose, digital painting style, rich color palette, concept design sheet, professional illustration","style":"奇幻概念","focal_length":"","aperture":"","lighting":"背光+魔法光效","composition":"居中","perspective":"微仰视","color_tone":"丰富色彩","quality_style":"数字绘画","shot_type":"全身","mood_atmosphere":"史诗奇幻","usage":"文生图"},
  # 视频专用
  {"name":"电影运镜-推镜头","desc":"缓慢推近的电影级运镜","category":"摄影通用","tags":["运镜","推镜头","电影"],"text":"slow cinematic push-in camera movement, dolly shot, gradually approaching the subject, smooth and steady, dramatic reveal, film production quality, 50mm lens, shallow depth of field, professional cinematography","style":"电影运镜","focal_length":"50mm","aperture":"f/2.8","lighting":"电影灯光","composition":"居中","perspective":"平视","color_tone":"电影色调","quality_style":"电影级","shot_type":"中景","camera_movement":"缓慢推近","mood_atmosphere":"戏剧张力","usage":"文生视频"},
  {"name":"电影运镜-环绕","desc":"360度环绕拍摄运镜","category":"摄影通用","tags":["运镜","环绕","电影"],"text":"cinematic orbit shot, 360 degree camera movement around subject, smooth circular motion, dramatic lighting, professional cinematography, shallow depth of field, epic reveal, steady cam movement","style":"电影运镜","focal_length":"35mm","aperture":"f/2.0","lighting":"三点布光","composition":"环绕","perspective":"平视","color_tone":"电影色调","quality_style":"电影级","shot_type":"中景","camera_movement":"环绕","mood_atmosphere":"震撼史诗","usage":"文生视频"},
  {"name":"延时摄影","desc":"时间流逝的延时效果","category":"风景","tags":["延时","时间流逝","风景"],"text":"timelapse photography, clouds moving fast, day to night transition, smooth motion, long exposure effect, 24mm wide angle, f/8, stabilized shot, professional timelapse, dynamic sky movement","style":"延时摄影","focal_length":"24mm","aperture":"f/8","lighting":"自然光变化","composition":"三分法","perspective":"平视","color_tone":"渐变色调","quality_style":"延时序列","shot_type":"远景","camera_movement":"固定机位","mood_atmosphere":"时间流逝","usage":"文生视频"},
  # 街拍纪实
  {"name":"街头纪实","desc":"真实自然的街头抓拍","category":"街拍纪实","tags":["街拍","纪实","抓拍"],"text":"street photography, candid moment, urban life, natural unposed, 35mm lens, f/2.8, black and white or muted colors, decisive moment, documentary style, rain or fog atmosphere, authentic human story","style":"街头纪实","focal_length":"35mm","aperture":"f/2.8","lighting":"自然光","composition":"抓拍","perspective":"平视","color_tone":"黑白/低饱和","quality_style":"纪实风格","shot_type":"中景","mood_atmosphere":"真实故事感","usage":"文生图"},
  # 抽象艺术
  {"name":"极简几何","desc":"极简主义几何构图","category":"抽象艺术","tags":["极简","几何","抽象"],"text":"minimalist geometric composition, clean lines, simple shapes, negative space, pastel or monochrome colors, modern art, architectural details, abstract patterns, balanced and harmonious design","style":"极简主义","focal_length":"50mm","aperture":"f/5.6","lighting":"均匀柔光","composition":"对称/黄金比例","perspective":"正面","color_tone":"低饱和","quality_style":"高清锐利","shot_type":"特写","mood_atmosphere":"宁静平衡","usage":"文生图"},
]

@app.route("/api/templates", methods=["GET"])
def get_templates():
    cat = request.args.get("category","")
    usage = request.args.get("usage","")
    result = TEMPLATES
    if cat:
        result = [t for t in result if t["category"] == cat]
    if usage:
        result = [t for t in result if t.get("usage","") == usage]
    return jsonify({"templates":result})

@app.route("/api/templates/<int:idx>/apply", methods=["POST"])
def apply_template(idx):
    if idx < 0 or idx >= len(TEMPLATES):
        return jsonify({"error":"模板不存在"}),404
    t = dict(TEMPLATES[idx])
    if isinstance(t.get("tags"),list):
        t["tags"] = json.dumps(t["tags"],ensure_ascii=False)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    c = sqlite3.connect(DB_PATH)
    vals = [t.get(k,"") for k in FIELDS] + [now,now]
    cur = c.execute("INSERT INTO prompts("+",".join(FIELDS)+",created_at,updated_at) VALUES("+",".join(["?"]*len(FIELDS))+",?,?)",vals)
    pid = cur.lastrowid
    cat = t.get("category","")
    if cat:
        c.execute("INSERT OR IGNORE INTO categories(name) VALUES(?)",[cat])
    c.execute("UPDATE categories SET count=(SELECT COUNT(*) FROM prompts WHERE category=name)")
    c.commit(); c.close()
    return jsonify({"ok":True,"id":pid,"text":t["text"]})

if __name__ == "__main__":
    url = "http://localhost:3001"
    print("========================================")
    print("    Agnes AI Client")
    print("========================================")
    print("Server: "+url)
    print("DB: "+DB_PATH)
    print("API Key: "+("Configured" if cfg.get("api_key") else "NOT set"))
    print("Opening browser...")
    print("========================================")
    webbrowser.open(url)
    app.run(host="0.0.0.0", port=3001, debug=False)
