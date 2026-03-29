# ╔══════════════════════════════════════════════════════════════╗
# ║            DRai — Streamlit Frontend (frontend/app.py)       ║
# ║  Diabetes | Heart | X-Ray | OCR | AI Chat | Health Score    ║
# ║  Symptom | Medicine | Diet | Family Risk | PDF | About      ║
# ╚══════════════════════════════════════════════════════════════╝

import streamlit as st
import requests
import json
import plotly.graph_objects as go
from datetime import datetime

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="DRai – AI Health", page_icon="🧬",
                   layout="wide", initial_sidebar_state="expanded")

# ═══════════════════════════════════════════
#  TRANSLATIONS
# ═══════════════════════════════════════════
TR = {
    "en": {
        "high_risk": "High Risk Detected", "low_risk": "Low Risk — Normal",
        "consult": "Please consult a physician immediately.",
        "healthy": "Maintain a healthy lifestyle and schedule regular checkups.",
        "analyze": "Analyze", "download_pdf": "📄 Download PDF Report",
        "patient_name": "Patient Name (optional)", "age": "Age (years)",
        "flags": "Detected Abnormalities", "no_flags": "All values within normal range",
    },
    "ur": {
        "high_risk": "⚠️ زیادہ خطرہ", "low_risk": "✅ کم خطرہ — نارمل",
        "consult": "فوری طور پر ڈاکٹر سے مشورہ کریں۔",
        "healthy": "صحت مند طرزِ زندگی اپنائیں اور باقاعدہ معائنہ کرائیں۔",
        "analyze": "تجزیہ کریں", "download_pdf": "📄 PDF ڈاؤنلوڈ کریں",
        "patient_name": "مریض کا نام (اختیاری)", "age": "عمر (سال)",
        "flags": "غیر معمولی اقدار", "no_flags": "تمام اقدار معمول کے مطابق",
    }
}
def t(key):
    return TR[st.session_state.get("lang", "en")].get(key, key)


# ═══════════════════════════════════════════
#  CSS
# ═══════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
:root{--bg:#080c18;--surface:#0f1623;--card:#151e2e;--border:#1c2a40;
      --accent:#00d4ff;--purple:#7c3aed;--danger:#ef4444;--success:#10b981;
      --warn:#f59e0b;--text:#dde4f0;--muted:#5a7089;}
html,body,[data-testid="stAppViewContainer"]{background:var(--bg)!important;color:var(--text)!important;font-family:'DM Sans',sans-serif!important;}
[data-testid="stSidebar"]{background:var(--surface)!important;border-right:1px solid var(--border)!important;}
[data-testid="stSidebar"] *{color:var(--text)!important;}
#MainMenu,footer,header{visibility:hidden;}
h1,h2,h3,h4{font-family:'Syne',sans-serif!important;}
.dcard{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:22px 26px;transition:transform .2s,box-shadow .2s;}
.dcard:hover{transform:translateY(-3px);box-shadow:0 10px 36px rgba(0,212,255,.1);}
.res-high{background:linear-gradient(135deg,rgba(239,68,68,.12),rgba(239,68,68,.03));border:1px solid rgba(239,68,68,.35);border-radius:14px;padding:20px 24px;margin:12px 0;}
.res-low{background:linear-gradient(135deg,rgba(16,185,129,.12),rgba(16,185,129,.03));border:1px solid rgba(16,185,129,.35);border-radius:14px;padding:20px 24px;margin:12px 0;}
.res-title{font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;margin-bottom:5px;}
.kv{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--border);font-size:.88rem;}
.kv-k{color:var(--muted);} .kv-v{font-weight:600;}
.pill-d{display:inline-block;padding:3px 12px;border-radius:20px;font-size:.78rem;font-weight:600;margin:2px 3px;background:rgba(239,68,68,.15);color:#ef4444;border:1px solid rgba(239,68,68,.3);}
.pill-ok{display:inline-block;padding:3px 12px;border-radius:20px;font-size:.78rem;font-weight:600;margin:2px 3px;background:rgba(16,185,129,.15);color:#10b981;border:1px solid rgba(16,185,129,.3);}
.ref-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:12px 16px;margin-bottom:8px;}
.pbar{background:var(--border);border-radius:8px;height:9px;overflow:hidden;margin:7px 0;}
.pbar-f{height:100%;border-radius:8px;}
.chat-u{background:rgba(0,212,255,.08);border:1px solid rgba(0,212,255,.2);border-radius:12px 12px 2px 12px;padding:10px 14px;margin:5px 0;text-align:right;font-size:.9rem;}
.chat-b{background:var(--card);border:1px solid var(--border);border-radius:12px 12px 12px 2px;padding:10px 14px;margin:5px 0;font-size:.9rem;line-height:1.6;}
.sec{border-left:4px solid var(--accent);padding-left:12px;margin-bottom:16px;}
.sec h2{margin:0;font-size:1.45rem;} .sec p{margin:3px 0 0;color:var(--muted);font-size:.85rem;}
.stButton>button{background:linear-gradient(135deg,var(--accent),var(--purple))!important;color:#fff!important;border:none!important;border-radius:9px!important;font-family:'Syne',sans-serif!important;font-weight:700!important;font-size:.9rem!important;padding:11px 0!important;width:100%!important;}
label{color:var(--muted)!important;font-size:.87rem!important;}
[data-testid="stNumberInput"] input,[data-testid="stTextInput"] input,textarea{background:var(--card)!important;border:1px solid var(--border)!important;color:var(--text)!important;border-radius:8px!important;}
.emg{background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.25);border-radius:10px;padding:10px 14px;margin-bottom:6px;font-size:.82rem;}
.score-ring{text-align:center;padding:18px;}
.score-num{font-family:'Syne',sans-serif;font-size:4rem;font-weight:800;line-height:1;}
.score-lbl{color:var(--muted);font-size:.8rem;text-transform:uppercase;letter-spacing:.1em;margin-top:4px;}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════
def api_post(ep, payload=None):
    try:
        r = requests.post(f"{API}{ep}", json=payload, timeout=30)
        r.raise_for_status()
        return r.json(), None
    except requests.ConnectionError:
        return None, "❌ Backend offline. Terminal 1 mein run karo: `python -m uvicorn backend.main:app --reload`"
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

def backend_ok():
    try:
        return requests.get(f"{API}/health", timeout=3).status_code == 200
    except:
        return False

def prob_bar(prob, color):
    pct = int(prob * 100)
    return f"<div class='pbar'><div class='pbar-f' style='width:{pct}%;background:{color};'></div></div><small style='color:#5a7089;'>Confidence: {pct}%</small>"

def result_banner(result, disease):
    hi    = "High" in result["risk_level"] or "Detected" in result["risk_level"]
    color = "#ef4444" if hi else "#10b981"
    css   = "res-high" if hi else "res-low"
    icon  = "⚠️" if hi else "✅"
    sub   = t("consult") if hi else t("healthy")
    st.markdown(f"<div class='{css}'><div class='res-title' style='color:{color};'>{icon} {result['risk_level']} — {disease}</div><div style='color:#7a93b0;font-size:.88rem;'>{sub}</div></div>", unsafe_allow_html=True)
    st.markdown(prob_bar(result["probability"], color), unsafe_allow_html=True)
    if result.get("flags"):
        pills = "".join(f"<span class='pill-d'>⚑ {f}</span>" for f in result["flags"])
        st.markdown(f"<br><b>{t('flags')}:</b><br>{pills}", unsafe_allow_html=True)
    elif not hi:
        st.markdown(f"<span class='pill-ok'>✓ {t('no_flags')}</span>", unsafe_allow_html=True)

def show_referrals(result):
    if result.get("referrals"):
        st.markdown("#### 🏥 Recommended Specialists")
        for r in result["referrals"]:
            st.markdown(f"<div class='ref-card'><b>🏨 {r['name']}</b><div style='color:#5a7089;font-size:.82rem;'>📍 {r['location']}</div><div style='color:#5a7089;font-size:.82rem;'>📞 {r['phone']}</div></div>", unsafe_allow_html=True)

def download_pdf_btn(patient_name, age, dtype, result, input_data, ai_advice=""):
    rp = dict(patient_name=patient_name or "Anonymous", age=int(age),
              diagnosis_type=dtype, risk_level=result["risk_level"],
              probability=result["probability"],
              input_data={k: str(v) for k, v in input_data.items()},
              ai_advice=ai_advice)
    try:
        r = requests.post(f"{API}/report/generate", json=rp, timeout=30)
        st.download_button("⬇️ Save PDF", r.content,
                           file_name=f"DRai_{dtype.replace(' ','_')}_Report.pdf",
                           mime="application/pdf")
    except Exception as e:
        st.error(str(e))


# ═══════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════
with st.sidebar:
    st.markdown("""<div style='text-align:center;padding:20px 0 10px;'>
    <div style='font-family:Syne,sans-serif;font-size:2rem;font-weight:800;
    background:linear-gradient(135deg,#00d4ff,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
    🧬 DRai</div>
    <div style='color:#5a7089;font-size:.7rem;letter-spacing:.15em;'>AI HEALTH DIAGNOSTICS v2</div>
    </div><hr style='border-color:#1c2a40;margin:8px 0 14px;'>""", unsafe_allow_html=True)

    l1, l2 = st.columns(2)
    with l1:
        if st.button("🇬🇧 English"): st.session_state.lang = "en"
    with l2:
        if st.button("🇵🇰 اردو"):    st.session_state.lang = "ur"
    if "lang" not in st.session_state: st.session_state.lang = "en"

    st.markdown("<hr style='border-color:#1c2a40;margin:10px 0;'>", unsafe_allow_html=True)

    page = st.radio("", [
        "🏠  Dashboard",
        "🩸  Diabetes",
        "🫀  Heart Disease",
        "🫁  X-Ray Analysis",
        "🔬  OCR Lab Scanner",
        "🤖  AI Consultant",
        "🤒  Symptom Checker",
        "💊  Medicine Checker",
        "🥗  Diet Planner",
        "💯  Health Score",
        "👨‍👩‍👧  Family Risk",
        "🏆  Model Performance",
        "ℹ️  About DRai",
    ], label_visibility="collapsed")

    st.markdown("<hr style='border-color:#1c2a40;margin:12px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='color:#ef4444;font-size:.72rem;font-weight:700;letter-spacing:.08em;'>🚨 EMERGENCY CONTACTS</p>", unsafe_allow_html=True)
    for name, num in [("Edhi Ambulance", "115"), ("Rescue", "1122"),
                      ("NICVD Emergency", "021-99201300"),
                      ("Aga Khan Emergency", "021-111-911-911"),
                      ("Tabba Heart", "021-34130317")]:
        st.markdown(f"<div class='emg'><b>{name}</b><br><a href='tel:{num}' style='color:#ef4444;'>📞 {num}</a></div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1c2a40;margin:10px 0;'>", unsafe_allow_html=True)
    ok = backend_ok()
    st.markdown(f"<div style='text-align:center;font-size:.8rem;'>{'🟢 Backend Online' if ok else '🔴 Backend Offline'}</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  DASHBOARD
# ═══════════════════════════════════════════
if "Dashboard" in page:
    st.markdown("""<div style='padding:36px 0 8px;'>
    <div style='font-family:Syne,sans-serif;font-size:2.8rem;font-weight:800;line-height:1.1;'>
    Diagnose Smarter<br>
    <span style='background:linear-gradient(135deg,#00d4ff,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
    with AI Precision</span></div>
    <p style='color:#5a7089;font-size:1rem;margin-top:12px;max-width:580px;'>
    DRai combines deep learning models with Gemini AI for fast, explainable health risk assessments — localized for Pakistan.</p>
    </div><br>""", unsafe_allow_html=True)

    cols = st.columns(4)
    for col, icon, color, title, sub in [
        (cols[0], "🩸", "#00d4ff", "Diabetes",     "ANN · PIMA Dataset"),
        (cols[1], "🫀", "#7c3aed", "Heart Disease", "ANN · Cleveland Dataset"),
        (cols[2], "🫁", "#10b981", "X-Ray",         "CNN · Pneumonia Detection"),
        (cols[3], "🤖", "#f59e0b", "AI Consultant", "Gemini 1.5 Flash"),
    ]:
        with col:
            st.markdown(f"<div class='dcard' style='text-align:center;'><div style='font-size:2rem;'>{icon}</div><div style='font-family:Syne,sans-serif;font-size:1.2rem;font-weight:800;color:{color};margin:8px 0 3px;'>{title}</div><div style='color:#5a7089;font-size:.8rem;'>{sub}</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if not backend_ok():
        st.error("⚠️ **Backend offline.**\n```\npython -m uvicorn backend.main:app --reload\n```")
    else:
        st.success("✅ Backend online — all models loaded and ready.")
    st.info("⚠️ DRai is an AI screening tool only. Always consult a licensed physician.")


# ═══════════════════════════════════════════
#  DIABETES
# ═══════════════════════════════════════════
elif "Diabetes" in page:
    st.markdown("<div class='sec'><h2>🩸 Diabetes Risk Prediction</h2><p>ANN · PIMA Dataset · 8 biomarkers</p></div>", unsafe_allow_html=True)
    with st.form("diabetes"):
        c = st.columns(4)
        preg = c[0].number_input("Pregnancies", 0, 20, 1)
        gluc = c[1].number_input("Glucose (mg/dL)", 0, 300, 120)
        bp_v = c[2].number_input("Blood Pressure (mmHg)", 0, 200, 70)
        skin = c[3].number_input("Skin Thickness (mm)", 0, 100, 20)
        c2 = st.columns(4)
        insu  = c2[0].number_input("Insulin (μU/mL)", 0, 900, 80)
        bmi   = c2[1].number_input("BMI", 0.0, 70.0, 25.0, step=0.1)
        dpf   = c2[2].number_input("Diabetes Pedigree", 0.0, 3.0, 0.47, step=0.01)
        age   = c2[3].number_input(t("age"), 1, 120, 33)
        pname = st.text_input(t("patient_name"))
        sub   = st.form_submit_button(f"🔍 {t('analyze')}")

    if sub:
        res, err = api_post("/predict/diabetes", dict(
            pregnancies=preg, glucose=gluc, blood_pressure=bp_v,
            skin_thickness=skin, insulin=insu, bmi=bmi, dpf=dpf, age=age))
        if err: st.error(err)
        else:
            col_r, col_p = st.columns([3, 1])
            with col_r: result_banner(res, "Diabetes")
            with col_p:
                pct = int(res["probability"] * 100)
                c   = "#ef4444" if "High" in res["risk_level"] else "#10b981"
                st.markdown(f"<div class='score-ring'><div class='score-num' style='color:{c};'>{pct}%</div><div class='score-lbl'>Risk Score</div></div>", unsafe_allow_html=True)
            kv = {"Glucose": f"{gluc} mg/dL", "BMI": bmi, "Insulin": f"{insu} μU/mL",
                  "Blood Pressure": f"{bp_v} mmHg", "Age": f"{age} yrs"}
            st.markdown("#### Input Summary")
            st.markdown("".join(f"<div class='kv'><span class='kv-k'>{k}</span><span class='kv-v'>{v}</span></div>" for k, v in kv.items()), unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(t("download_pdf")):
                download_pdf_btn(pname, age, "Diabetes", res, kv)


# ═══════════════════════════════════════════
#  HEART DISEASE
# ═══════════════════════════════════════════
elif "Heart" in page:
    st.markdown("<div class='sec'><h2>🫀 Heart Disease Prediction</h2><p>ANN · Cleveland Dataset · 13 parameters</p></div>", unsafe_allow_html=True)
    with st.form("heart"):
        c1 = st.columns(3)
        age_h = c1[0].number_input(t("age"), 20, 100, 50)
        sex   = c1[1].selectbox("Sex", ["Male (1)", "Female (0)"])
        cp    = c1[2].selectbox("Chest Pain Type", ["0 – Typical Angina", "1 – Atypical Angina", "2 – Non-Anginal", "3 – Asymptomatic"])
        c2 = st.columns(3)
        tbps  = c2[0].number_input("Resting BP (mmHg)", 80, 250, 130)
        chol  = c2[1].number_input("Cholesterol (mg/dL)", 100, 600, 210)
        fbs   = c2[2].selectbox("Fasting BS > 120", ["No (0)", "Yes (1)"])
        c3 = st.columns(3)
        recg  = c3[0].selectbox("Resting ECG", ["0 – Normal", "1 – ST-T Abnormality", "2 – LV Hypertrophy"])
        thal  = c3[1].number_input("Max Heart Rate", 60, 250, 150)
        exang = c3[2].selectbox("Exercise Angina", ["No (0)", "Yes (1)"])
        c4 = st.columns(3)
        opeak = c4[0].number_input("ST Depression", 0.0, 10.0, 1.0, step=0.1)
        slope = c4[1].selectbox("ST Slope", ["0 – Upsloping", "1 – Flat", "2 – Downsloping"])
        ca    = c4[2].selectbox("Major Vessels (Ca)", [0, 1, 2, 3])
        thalc   = st.selectbox("Thalassemia", ["1 – Normal", "2 – Fixed Defect", "3 – Reversible Defect"])
        pname_h = st.text_input(t("patient_name"))
        sub_h   = st.form_submit_button(f"🔍 {t('analyze')}")

    if sub_h:
        res, err = api_post("/predict/heart", dict(
            age=age_h, sex=1 if "Male" in sex else 0, cp=int(cp[0]),
            trestbps=tbps, chol=chol, fbs=1 if "Yes" in fbs else 0,
            restecg=int(recg[0]), thalach=thal, exang=1 if "Yes" in exang else 0,
            oldpeak=opeak, slope=int(slope[0]), ca=ca, thal=int(thalc[0])))
        if err: st.error(err)
        else:
            col_r, col_p = st.columns([3, 1])
            with col_r: result_banner(res, "Heart Disease")
            with col_p:
                pct = int(res["probability"] * 100)
                c   = "#ef4444" if "High" in res["risk_level"] else "#10b981"
                st.markdown(f"<div class='score-ring'><div class='score-num' style='color:{c};'>{pct}%</div><div class='score-lbl'>Cardiac Risk</div></div>", unsafe_allow_html=True)
            show_referrals(res)
            kv = {"Age": age_h, "Cholesterol": f"{chol} mg/dL", "BP": f"{tbps} mmHg",
                  "Max HR": thal, "ST Depression": opeak}
            if st.button(t("download_pdf")):
                download_pdf_btn(pname_h, age_h, "Heart Disease", res, kv)


# ═══════════════════════════════════════════
#  X-RAY
# ═══════════════════════════════════════════
elif "X-Ray" in page:
    st.markdown("<div class='sec'><h2>🫁 Chest X-Ray Analysis</h2><p>CNN · Pneumonia vs Normal Classification</p></div>", unsafe_allow_html=True)
    col_u, col_p = st.columns(2)
    with col_u:
        f       = st.file_uploader("Upload Chest X-Ray (JPG/PNG)", type=["jpg", "jpeg", "png"])
        pname_x = st.text_input(t("patient_name"))
        btn     = st.button(f"🔍 {t('analyze')}")
    with col_p:
        if f: st.image(f, use_column_width=True, caption="Uploaded X-Ray")

    if btn:
        if not f: st.warning("Please upload an X-Ray image first.")
        else:
            with st.spinner("CNN analyzing image..."):
                try:
                    r2  = requests.post(f"{API}/predict/xray",
                                        files={"file": (f.name, f.getvalue(), f.type)}, timeout=60)
                    res = r2.json()
                    col_r, col_p2 = st.columns([3, 1])
                    with col_r:   result_banner(res, "Pneumonia")
                    with col_p2:
                        pct = int(res["probability"] * 100)
                        c   = "#ef4444" if "Detected" in res["risk_level"] else "#10b981"
                        st.markdown(f"<div class='score-ring'><div class='score-num' style='color:{c};'>{pct}%</div><div class='score-lbl'>CNN Score</div></div>", unsafe_allow_html=True)
                    show_referrals(res)
                    if st.button(t("download_pdf")):
                        download_pdf_btn(pname_x, 0, "X-Ray Pneumonia", res, {"Image": f.name})
                except Exception as e:
                    st.error(str(e))


# ═══════════════════════════════════════════
#  OCR LAB SCANNER
# ═══════════════════════════════════════════
elif "OCR" in page:
    st.markdown("<div class='sec'><h2>🔬 OCR Lab Report Scanner</h2><p>Upload Aga Khan / Chughtai lab report — AI extracts values automatically</p></div>", unsafe_allow_html=True)
    st.info("📋 Supported: JPG, PNG, PDF")
    ocr_file = st.file_uploader("Upload Lab Report", type=["jpg", "jpeg", "png", "pdf"])
    if ocr_file and st.button("🔬 Extract Values"):
        with st.spinner("Gemini Vision reading report..."):
            r2      = requests.post(f"{API}/ocr/extract",
                                    files={"file": (ocr_file.name, ocr_file.getvalue(), ocr_file.type)},
                                    timeout=60)
            ocr_res = r2.json()
        if ocr_res.get("status") == "success":
            st.success("✅ Values extracted successfully!")
            ext   = {k: v for k, v in ocr_res["extracted"].items() if v is not None}
            items = list(ext.items())
            c1, c2 = st.columns(2)
            half   = len(items) // 2
            with c1:
                for k, v in items[:half]:
                    st.markdown(f"<div class='kv'><span class='kv-k'>{k.replace('_',' ').title()}</span><span class='kv-v'>{v}</span></div>", unsafe_allow_html=True)
            with c2:
                for k, v in items[half:]:
                    st.markdown(f"<div class='kv'><span class='kv-k'>{k.replace('_',' ').title()}</span><span class='kv-v'>{v}</span></div>", unsafe_allow_html=True)
            if ext.get("glucose"):
                st.info(f"💡 Glucose detected: {ext['glucose']} — use this in the Diabetes page.")
        else:
            st.warning("Partial extraction.")
            if ocr_res.get("raw"): st.code(ocr_res["raw"])


# ═══════════════════════════════════════════
#  AI CONSULTANT
# ═══════════════════════════════════════════
elif "AI Consultant" in page:
    st.markdown("<div class='sec'><h2>🤖 AI Health Consultant</h2><p>Gemini 1.5 Flash · Ask anything health-related</p></div>", unsafe_allow_html=True)
    if "chat_hist" not in st.session_state: st.session_state.chat_hist = []
    if "api_hist"  not in st.session_state: st.session_state.api_hist  = []

    with st.expander("📋 Add Diagnostic Context (optional)"):
        ctx = st.text_area("Paste result for personalized advice", height=70,
                           placeholder="e.g. Diabetes Risk 73%, Glucose 185 mg/dL")

    for msg in st.session_state.chat_hist:
        css  = "chat-u" if msg["role"] == "user" else "chat-b"
        icon = "🧑" if msg["role"] == "user" else "🤖"
        st.markdown(f"<div class='{css}'>{icon} {msg['content']}</div>", unsafe_allow_html=True)

    if not st.session_state.chat_hist:
        st.markdown("<div style='text-align:center;padding:30px;color:#334155;'><div style='font-size:2.5rem;'>🤖</div><div style='font-family:Syne,sans-serif;margin-top:8px;'>Ask me about symptoms, medications, or your diagnostic results.</div></div>", unsafe_allow_html=True)

    ci, cb = st.columns([5, 1])
    with ci:  user_msg = st.text_input("", placeholder="Type message...", label_visibility="collapsed", key="ci")
    with cb:  send     = st.button("Send ➤")
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_hist = []; st.session_state.api_hist = []; st.rerun()

    if send and user_msg.strip():
        st.session_state.chat_hist.append({"role": "user", "content": user_msg})
        res, err = api_post("/chat", {"message": user_msg,
                                      "history": st.session_state.api_hist,
                                      "context": ctx if "ctx" in dir() else ""})
        if err: st.error(err)
        else:
            reply = res["reply"]
            st.session_state.chat_hist.append({"role": "assistant", "content": reply})
            st.session_state.api_hist.append({"role": "user",  "content": user_msg})
            st.session_state.api_hist.append({"role": "model", "content": reply})
            st.rerun()


# ═══════════════════════════════════════════
#  SYMPTOM CHECKER
# ═══════════════════════════════════════════
elif "Symptom" in page:
    st.markdown("<div class='sec'><h2>🤒 Symptom Checker</h2><p>Describe symptoms → AI suggests which module to use</p></div>", unsafe_allow_html=True)
    with st.form("symptoms"):
        syms   = st.text_area("Describe your symptoms", height=100,
                              placeholder="e.g. zyada pyaas, thakan, bar bar peshab, sir dard...")
        c1, c2 = st.columns(2)
        age_s  = c1.number_input("Age", 1, 120, 30)
        gender = c2.selectbox("Gender", ["Male", "Female", "Other"])
        sub_s  = st.form_submit_button("🔍 Check Symptoms")
    if sub_s and syms:
        res, err = api_post("/symptom/check", {"symptoms": syms, "age": age_s, "gender": gender})
        if err: st.error(err)
        else:
            st.markdown("### 🧠 AI Assessment")
            st.markdown(f"<div class='dcard'>{res['assessment'].replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  MEDICINE CHECKER
# ═══════════════════════════════════════════
elif "Medicine" in page:
    st.markdown("<div class='sec'><h2>💊 Medicine Safety Checker</h2><p>Check drug interactions and safety for your condition</p></div>", unsafe_allow_html=True)
    with st.form("medicine"):
        med   = st.text_input("Medicine Name", placeholder="e.g. Metformin, Aspirin, Atorvastatin")
        cond  = st.selectbox("Patient Condition", ["Diabetes", "Heart Disease", "Hypertension", "Kidney Disease", "General"])
        curr  = st.text_input("Current Medications (comma-separated)", placeholder="e.g. Insulin, Losartan")
        sub_m = st.form_submit_button("💊 Check Safety")
    if sub_m and med:
        curr_list = [x.strip() for x in curr.split(",") if x.strip()]
        res, err  = api_post("/medicine/check", {"medicine_name": med, "patient_condition": cond, "current_meds": curr_list})
        if err: st.error(err)
        else:
            st.markdown(f"### Safety Report: {med}")
            st.markdown(f"<div class='dcard'>{res['advice'].replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
            st.warning("⚠️ Always consult your doctor before taking or stopping any medication.")


# ═══════════════════════════════════════════
#  DIET PLANNER
# ═══════════════════════════════════════════
elif "Diet" in page:
    st.markdown("<div class='sec'><h2>🥗 Pakistani Diet Planner</h2><p>Personalized meal plan based on your condition</p></div>", unsafe_allow_html=True)
    with st.form("diet"):
        c1, c2 = st.columns(2)
        dtype  = c1.selectbox("Condition", ["Diabetes", "Heart Disease", "Obesity", "General Health"])
        rlvl   = c2.selectbox("Risk Level", ["High Risk", "Low Risk", "Prevention"])
        c3, c4 = st.columns(2)
        bmi_d  = c3.number_input("BMI", 10.0, 60.0, 25.0, step=0.1)
        age_d  = c4.number_input("Age", 1, 100, 35)
        pref   = st.text_input("Dietary Preferences", placeholder="e.g. vegetarian, no beef, low sugar")
        sub_d  = st.form_submit_button("🥗 Generate Diet Plan")
    if sub_d:
        res, err = api_post("/diet/recommend", {"diagnosis_type": dtype, "risk_level": rlvl,
                                                "bmi": bmi_d, "age": age_d, "preferences": pref})
        if err: st.error(err)
        else:
            st.markdown("### 🍽️ Your Personalized Diet Plan")
            st.markdown(f"<div class='dcard'>{res['plan'].replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  HEALTH SCORE
# ═══════════════════════════════════════════
elif "Health Score" in page:
    st.markdown("<div class='sec'><h2>💯 DRai Health Score</h2><p>Overall health score 0–100 combining clinical + lifestyle</p></div>", unsafe_allow_html=True)
    with st.form("hscore"):
        c1, c2, c3 = st.columns(3)
        hs_age   = c1.number_input("Age", 1, 100, 35)
        hs_bmi   = c2.number_input("BMI", 10.0, 60.0, 24.0, step=0.1)
        hs_bp    = c3.number_input("Systolic BP (mmHg)", 80, 250, 120)
        c4, c5, c6 = st.columns(3)
        hs_smoke = c4.selectbox("Smoker", ["No", "Yes"])
        hs_ex    = c5.number_input("Exercise Days/Week", 0, 7, 3)
        hs_sleep = c6.number_input("Sleep Hours/Night", 0.0, 12.0, 7.0, step=0.5)
        c7, _    = st.columns(2)
        hs_fv    = c7.number_input("Fruits/Veg Servings/Day", 0, 15, 4)
        st.markdown("**Optional: Add diagnostic probabilities for accurate score**")
        c8, c9   = st.columns(2)
        hs_dp    = c8.number_input("Diabetes Probability (0.0–1.0)", 0.0, 1.0, 0.0, step=0.01)
        hs_hp    = c9.number_input("Heart Probability (0.0–1.0)",   0.0, 1.0, 0.0, step=0.01)
        sub_hs   = st.form_submit_button("💯 Calculate Score")

    if sub_hs:
        res, err = api_post("/health-score", {
            "age": hs_age, "bmi": hs_bmi, "smoking": 1 if hs_smoke == "Yes" else 0,
            "exercise_days": hs_ex, "sleep_hours": hs_sleep,
            "diabetes_prob": hs_dp, "heart_prob": hs_hp,
            "systolic_bp": hs_bp, "fruits_veg": hs_fv})
        if err: st.error(err)
        else:
            col_sc, col_tips = st.columns([1, 2])
            with col_sc:
                st.markdown(f"<div class='score-ring' style='padding:30px;'><div class='score-num' style='color:{res['color']};font-size:5rem;'>{res['score']}</div><div style='font-family:Syne,sans-serif;font-size:1.8rem;font-weight:800;color:{res['color']};'>Grade {res['grade']}</div><div class='score-lbl'>{res['label']}</div></div>", unsafe_allow_html=True)
                fig = go.Figure(go.Indicator(mode="gauge+number", value=res["score"],
                    gauge={"axis": {"range": [0, 100]}, "bar": {"color": res["color"]},
                           "steps": [{"range": [0,  35], "color": "rgba(239,68,68,.2)"},
                                     {"range": [35, 65], "color": "rgba(245,158,11,.2)"},
                                     {"range": [65,100], "color": "rgba(16,185,129,.2)"}]}))
                fig.update_layout(paper_bgcolor="#0a0e1a", font_color="#dde4f0",
                                  height=200, margin=dict(t=0, b=0, l=20, r=20))
                st.plotly_chart(fig, use_container_width=True)
            with col_tips:
                st.markdown("#### 💡 Improvement Tips")
                for tip in res["tips"]:
                    st.markdown(f"<div class='dcard' style='margin-bottom:8px;padding:12px 16px;'>✦ {tip}</div>", unsafe_allow_html=True)
                if not res["tips"]:
                    st.success("🌟 Excellent health profile! Keep it up.")


# ═══════════════════════════════════════════
#  FAMILY RISK
# ═══════════════════════════════════════════
elif "Family" in page:
    st.markdown("<div class='sec'><h2>👨‍👩‍👧 Family Risk Assessment</h2><p>Genetic + lifestyle risk based on family history</p></div>", unsafe_allow_html=True)
    with st.form("family"):
        c1, c2 = st.columns(2)
        fr_age = c1.number_input("Your Age", 1, 100, 35)
        fr_bmi = c2.number_input("Your BMI", 10.0, 60.0, 24.0, step=0.1)
        st.markdown("**Family History — Diabetes**")
        c3, c4 = st.columns(2)
        pd_v   = c3.selectbox("Parent has Diabetes", ["No", "Yes"])
        sd_v   = c4.selectbox("Sibling has Diabetes", ["No", "Yes"])
        st.markdown("**Family History — Heart Disease**")
        c5, c6 = st.columns(2)
        ph_v   = c5.selectbox("Parent has Heart Disease", ["No", "Yes"])
        sh_v   = c6.selectbox("Sibling has Heart Disease", ["No", "Yes"])
        c7, c8 = st.columns(2)
        fr_smk = c7.selectbox("Smoker", ["No", "Yes"])
        fr_htn = c8.selectbox("Hypertension", ["No", "Yes"])
        sub_fr = st.form_submit_button("🧬 Calculate Genetic Risk")

    if sub_fr:
        res, err = api_post("/family-risk", {
            "age": fr_age, "bmi": fr_bmi,
            "parent_diabetes":  1 if pd_v == "Yes" else 0,
            "sibling_diabetes": 1 if sd_v == "Yes" else 0,
            "parent_heart":     1 if ph_v == "Yes" else 0,
            "sibling_heart":    1 if sh_v == "Yes" else 0,
            "smoking":          1 if fr_smk == "Yes" else 0,
            "hypertension":     1 if fr_htn == "Yes" else 0})
        if err: st.error(err)
        else:
            c1, c2 = st.columns(2)
            for col, title, g_val, t_val, level, color in [
                (c1, "🩸 Diabetes Risk", res["diabetes_genetic"], res["diabetes_total"], res["diabetes_level"], "#00d4ff"),
                (c2, "🫀 Heart Risk",    res["heart_genetic"],    res["heart_total"],    res["heart_level"],    "#7c3aed"),
            ]:
                with col:
                    lc = "#ef4444" if level == "High" else "#f59e0b" if level == "Moderate" else "#10b981"
                    st.markdown(f"""<div class='dcard' style='text-align:center;'>
                    <div style='font-family:Syne,sans-serif;font-weight:700;margin-bottom:10px;'>{title}</div>
                    <div style='font-size:.82rem;color:#5a7089;'>Genetic Component</div>
                    <div style='font-family:Syne,sans-serif;font-size:2rem;font-weight:800;color:{color};'>{g_val}%</div>
                    <div style='font-size:.82rem;color:#5a7089;margin-top:8px;'>Total Risk (incl. lifestyle)</div>
                    <div style='font-family:Syne,sans-serif;font-size:2.5rem;font-weight:800;color:{lc};'>{t_val}%</div>
                    <div style='font-weight:700;color:{lc};'>{level} Risk</div>
                    </div>""", unsafe_allow_html=True)
            st.markdown(f"<br><div class='dcard'>💡 {res['recommendation']}</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  MODEL PERFORMANCE
# ═══════════════════════════════════════════
elif "Model Performance" in page:
    st.markdown("<div class='sec'><h2>🏆 Model Performance Dashboard</h2><p>Update with your actual training results from Google Colab</p></div>", unsafe_allow_html=True)
    METRICS = {
        "🩸 Diabetes ANN":      {"accuracy": 0.79, "precision": 0.76, "recall": 0.72, "f1": 0.74, "dataset": "PIMA (768 samples)",       "epochs": 100},
        "🫀 Heart Disease ANN": {"accuracy": 0.85, "precision": 0.83, "recall": 0.81, "f1": 0.82, "dataset": "Cleveland (303 samples)",   "epochs": 80},
        "🫁 X-Ray CNN":         {"accuracy": 0.92, "precision": 0.90, "recall": 0.94, "f1": 0.92, "dataset": "Chest X-Ray (5216 images)", "epochs": 20},
    }
    for model_name, m in METRICS.items():
        st.markdown(f"#### {model_name}")
        cols = st.columns(4)
        for col, metric, val in zip(cols,
                ["Accuracy", "Precision", "Recall", "F1 Score"],
                [m["accuracy"], m["precision"], m["recall"], m["f1"]]):
            col.markdown(f"<div class='dcard' style='text-align:center;'><div style='font-family:Syne,sans-serif;font-size:2rem;font-weight:800;color:#00d4ff;'>{round(val*100,1)}%</div><div style='color:#5a7089;font-size:.82rem;'>{metric}</div></div>", unsafe_allow_html=True)
        fig = go.Figure(go.Bar(
            x=["Accuracy", "Precision", "Recall", "F1"],
            y=[m["accuracy"], m["precision"], m["recall"], m["f1"]],
            marker_color=["#00d4ff", "#7c3aed", "#10b981", "#f59e0b"],
            text=[f"{v*100:.1f}%" for v in [m["accuracy"], m["precision"], m["recall"], m["f1"]]],
            textposition="outside"))
        fig.update_layout(paper_bgcolor="#0a0e1a", plot_bgcolor="#0f1623", font_color="#dde4f0",
                          yaxis=dict(range=[0, 1.1]), height=220, margin=dict(t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"<small style='color:#5a7089;'>Dataset: {m['dataset']} · Epochs: {m['epochs']}</small><br><br>", unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  ABOUT
# ═══════════════════════════════════════════
elif "About" in page:
    st.markdown("<div class='sec'><h2>ℹ️ About DRai</h2><p>Research, datasets, architecture</p></div>", unsafe_allow_html=True)
    st.markdown("""<div class='dcard'>
    <div style='font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;margin-bottom:12px;'>🧬 DRai — AI-Driven Health & Diagnostic Ecosystem</div>
    <p>DRai is a Final Year Project (FYP) combining <b>Deep Learning</b> clinical models with <b>Google Gemini AI</b>
    to deliver a comprehensive health screening platform, localized for Pakistan.</p></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for col, title, content in [
        (c1, "🗄️ Datasets",     "**Diabetes:** PIMA Indian Diabetes (Kaggle)\n\n**Heart:** Cleveland Heart Disease (UCI)\n\n**X-Ray:** Chest X-Ray Images (Kaggle)"),
        (c2, "🏗️ Architecture", "**Frontend:** Streamlit\n\n**Backend:** FastAPI\n\n**Models:** TensorFlow/Keras ANN + CNN\n\n**LLM:** Google Gemini 1.5 Flash"),
        (c3, "🛠️ Tech Stack",   "**PDF:** ReportLab\n\n**Charts:** Plotly\n\n**OCR:** Gemini Vision\n\n**Language:** Python 3.13"),
    ]:
        with col:
            st.markdown(f"<div class='dcard'><div style='font-family:Syne,sans-serif;font-weight:700;margin-bottom:10px;'>{title}</div>", unsafe_allow_html=True)
            st.markdown(content)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class='dcard' style='border-color:rgba(0,212,255,.3);'>
    <div style='font-family:Syne,sans-serif;font-weight:700;margin-bottom:8px;'>📚 Key Features</div>
    <div style='display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:.88rem;color:#7a93b0;'>
    <div>✦ Multi-model diagnostic engine</div><div>✦ Gemini AI health consultation</div>
    <div>✦ Gemini Vision OCR lab scanner</div><div>✦ Pakistani diet planner</div>
    <div>✦ Medicine interaction checker</div><div>✦ Symptom triage system</div>
    <div>✦ Karachi hospital referrals</div><div>✦ Professional PDF reports</div>
    <div>✦ DRai overall health score</div><div>✦ Urdu language support</div>
    <div>✦ Family genetic risk assessment</div><div>✦ Model performance dashboard</div>
    </div></div>""", unsafe_allow_html=True)

    st.warning("⚠️ **Disclaimer:** DRai is developed for academic/FYP purposes. It does not replace professional medical diagnosis.")
