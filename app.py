"""
app.py
------
Smart Waste – AI for a Cleaner Future
Main Streamlit application.

Pages:
  1. Home
  2. Waste Analyzer
  3. Dashboard
  4. How It Works
  5. About
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from PIL import Image
import io
import base64

# ── project utils ──────────────────────────────────────────────────────────
from utils.classifier import classify_waste, CATEGORY_INFO, ALL_CATEGORIES
from utils.recommendations import (
    get_recommendation,
    calculate_env_impact,
    ITEM_SAVINGS,
)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Smart Waste – AI for a Cleaner Future",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #064e3b 0%, #065f46 50%, #047857 100%);
}
[data-testid="stSidebar"] * { color: #d1fae5 !important; }
[data-testid="stSidebar"] .stRadio label { color: #d1fae5 !important; }
[data-testid="stSidebar"] hr { border-color: #6ee7b7; }

/* ── metric cards ── */
.metric-card {
    background: white;
    border-radius: 16px;
    padding: 1.4rem 1.2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.07);
    border-left: 5px solid;
    transition: transform .2s ease, box-shadow .2s ease;
    height: 100%;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 28px rgba(0,0,0,0.13);
}
.metric-value { font-size: 2.2rem; font-weight: 800; margin: .2rem 0; line-height: 1; }
.metric-label { font-size: .85rem; font-weight: 500; color: #6b7280; text-transform: uppercase; letter-spacing: .05em; }
.metric-icon  { font-size: 1.8rem; }

/* ── result card ── */
.result-card {
    background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
    border-radius: 20px;
    padding: 2rem;
    border: 2px solid #86efac;
    box-shadow: 0 8px 32px rgba(34,197,94,.15);
}

/* ── info pill / badge ── */
.badge {
    display: inline-block;
    padding: .25rem .9rem;
    border-radius: 999px;
    font-size: .75rem;
    font-weight: 700;
    letter-spacing: .06em;
    text-transform: uppercase;
}

/* ── step card ── */
.step-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 4px 16px rgba(0,0,0,.07);
    text-align: center;
    height: 100%;
    border-top: 4px solid #22c55e;
    transition: transform .2s ease;
}
.step-card:hover { transform: translateY(-4px); }
.step-number {
    width: 48px; height: 48px;
    background: linear-gradient(135deg,#22c55e,#16a34a);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 1.2rem; color: white;
    margin: 0 auto .8rem;
}

/* ── hero banner ── */
.hero {
    background: linear-gradient(135deg,#064e3b 0%,#065f46 40%,#047857 70%,#059669 100%);
    border-radius: 24px;
    padding: 3.5rem 2.5rem;
    color: white;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; top:-60px; right:-60px;
    width: 300px; height: 300px;
    background: rgba(255,255,255,.05);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute; bottom:-80px; left:-40px;
    width: 250px; height: 250px;
    background: rgba(255,255,255,.04);
    border-radius: 50%;
}
.hero h1 { font-size: 2.8rem; font-weight: 800; margin-bottom: .5rem; line-height: 1.1; }
.hero p  { font-size: 1.15rem; opacity: .88; max-width: 600px; }

/* ── section title ── */
.section-title {
    font-size: 1.6rem; font-weight: 700; color: #064e3b;
    border-left: 5px solid #22c55e;
    padding-left: .8rem; margin: 1.5rem 0 1rem;
}

/* ── upload zone ── */
.upload-hint {
    background: #f0fdf4;
    border: 2px dashed #86efac;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    color: #15803d;
    font-size: 1rem;
}

/* ── tip box ── */
.tip-box {
    background: linear-gradient(135deg,#fffbeb,#fef3c7);
    border-left: 5px solid #f59e0b;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
}

/* ── timeline (How It Works) ── */
.timeline-step {
    display: flex;
    align-items: flex-start;
    gap: 1.2rem;
    margin-bottom: 2rem;
}
.timeline-dot {
    min-width: 52px; height: 52px;
    background: linear-gradient(135deg,#22c55e,#16a34a);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    box-shadow: 0 4px 12px rgba(34,197,94,.4);
}
.timeline-content {
    background: white; border-radius: 14px;
    padding: 1.2rem 1.5rem; flex: 1;
    box-shadow: 0 3px 12px rgba(0,0,0,.07);
    border-left: 4px solid #22c55e;
}
.timeline-content h4 { margin: 0 0 .4rem; color: #064e3b; font-size: 1.05rem; font-weight: 700; }
.timeline-content p  { margin: 0; color: #6b7280; font-size: .9rem; line-height: 1.5; }

/* ── confidence bar ── */
.conf-bar-bg {
    background: #e5e7eb; border-radius: 999px; height: 12px; overflow: hidden;
}
.conf-bar-fill {
    height: 100%; border-radius: 999px;
    background: linear-gradient(90deg,#22c55e,#16a34a);
    transition: width .6s ease;
}

/* ── about team card ── */
.team-card {
    background: white; border-radius: 16px;
    padding: 1.5rem; text-align: center;
    box-shadow: 0 4px 16px rgba(0,0,0,.07);
    border-top: 4px solid #22c55e;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ═══════════════════════════════════════════════════════════════════════════
def _init_state():
    defaults = {
        "history": [],          # list of classification result dicts
        "last_result": None,    # most recent classification
        "page": "Home",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()


# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════
def render_sidebar():
    with st.sidebar:
        st.markdown("## ♻️ Smart Waste")
        st.markdown("**AI for a Cleaner Future**")
        st.markdown("---")

        pages = {
            "🏠  Home":           "Home",
            "🔍  Waste Analyzer":  "Analyzer",
            "📊  Dashboard":       "Dashboard",
            "⚙️  How It Works":   "How It Works",
            "ℹ️  About":          "About",
        }

        selected_label = st.radio(
            "Navigate",
            list(pages.keys()),
            index=list(pages.values()).index(st.session_state.page),
            label_visibility="collapsed",
        )
        st.session_state.page = pages[selected_label]

        st.markdown("---")

        # Mini stats in sidebar
        total = len(st.session_state.history)
        st.markdown(f"**Items Analyzed:** {total}")

        if total > 0:
            counts = {c: 0 for c in ALL_CATEGORIES}
            for h in st.session_state.history:
                counts[h["category"]] += 1
            top = max(counts, key=counts.get)
            st.markdown(f"**Top Category:** {CATEGORY_INFO[top]['icon']} {top}")

        st.markdown("---")
        st.markdown(
            "<small style='opacity:.7'>Built for ICV Hackathon 2026<br>"
            "Smart City · Green Tech</small>",
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════════════════
# HELPER: image → base64 for HTML display
# ═══════════════════════════════════════════════════════════════════════════
def _img_to_b64(pil_img, max_size=(400, 400)):
    pil_img.thumbnail(max_size)
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 1 – HOME
# ═══════════════════════════════════════════════════════════════════════════
def page_home():
    # Hero
    st.markdown("""
    <div class="hero">
        <h1>♻️ Smart Waste</h1>
        <p>AI-powered waste segregation for a greener tomorrow.<br>
        Upload a photo — our AI identifies your waste and tells you exactly
        how to dispose of it responsibly.</p>
    </div>
    """, unsafe_allow_html=True)

    # CTA buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🔍 Analyze Waste", use_container_width=True, type="primary"):
            st.session_state.page = "Analyzer"
            st.rerun()
    with col2:
        if st.button("📊 View Dashboard", use_container_width=True):
            st.session_state.page = "Dashboard"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature cards
    st.markdown('<div class="section-title">What Smart Waste Can Do</div>', unsafe_allow_html=True)

    features = [
        ("🤖", "AI Classification",
         "MobileNetV2 deep learning model classifies waste into 6 categories with high accuracy."),
        ("♻️", "Smart Recommendations",
         "Step-by-step disposal instructions and recycling guidance for every waste type."),
        ("📊", "Live Dashboard",
         "Track your recycling habits with beautiful real-time charts and statistics."),
        ("🌍", "Environmental Impact",
         "See exactly how much CO₂, energy, and water you save with every item recycled."),
        ("📱", "Easy to Use",
         "Just upload a photo and get instant results — no technical knowledge required."),
        ("🏙️", "Smart City Ready",
         "Designed for integration into smart city waste management infrastructure."),
    ]

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="step-card" style="margin-bottom:1rem;">
                <div style="font-size:2.2rem;margin-bottom:.5rem;">{icon}</div>
                <h4 style="color:#064e3b;font-size:1rem;font-weight:700;margin:.3rem 0;">{title}</h4>
                <p style="color:#6b7280;font-size:.87rem;margin:0;line-height:1.5;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Waste categories preview
    st.markdown('<div class="section-title">Waste Categories We Detect</div>', unsafe_allow_html=True)

    cat_cols = st.columns(6)
    cat_descriptions = {
        "Plastic":  "Bottles, bags, containers",
        "Paper":    "Newspaper, cardboard, books",
        "Metal":    "Cans, tins, scrap metal",
        "Glass":    "Bottles, jars, windows",
        "Organic":  "Food scraps, garden waste",
        "E-Waste":  "Phones, laptops, cables",
    }
    for i, cat in enumerate(ALL_CATEGORIES):
        info = CATEGORY_INFO[cat]
        with cat_cols[i]:
            st.markdown(f"""
            <div style="background:white;border-radius:14px;padding:1rem .8rem;
                        text-align:center;box-shadow:0 3px 14px rgba(0,0,0,.08);
                        border-top:4px solid {info['color']};margin-bottom:.5rem;">
                <div style="font-size:2rem;">{info['icon']}</div>
                <div style="font-weight:700;font-size:.95rem;color:#111;margin:.3rem 0;">{cat}</div>
                <div style="font-size:.78rem;color:#9ca3af;">{cat_descriptions[cat]}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick stats strip
    st.markdown('<div class="section-title">The Global Waste Crisis</div>', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    stats = [
        ("2.1B", "Tonnes of solid waste generated globally per year", "#ef4444"),
        ("91%",  "Of plastic is never recycled",                     "#f97316"),
        ("62M",  "Tonnes of e-waste produced in 2022",               "#8b5cf6"),
        ("8%",   "Of global emissions from food waste",              "#22c55e"),
    ]
    for col, (val, label, color) in zip([s1, s2, s3, s4], stats):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color:{color};text-align:center;">
                <div class="metric-value" style="color:{color};">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 2 – WASTE ANALYZER
# ═══════════════════════════════════════════════════════════════════════════
def page_analyzer():
    st.markdown("""
    <div style="background:linear-gradient(135deg,#064e3b,#065f46);
                border-radius:20px;padding:2rem 2.5rem;color:white;margin-bottom:1.5rem;">
        <h2 style="margin:0 0 .4rem;font-size:1.9rem;font-weight:800;">🔍 Waste Analyzer</h2>
        <p style="margin:0;opacity:.85;">Upload or capture an image — our AI will classify it and
        give you precise disposal instructions.</p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1, 1], gap="large")

    # ── LEFT: upload ────────────────────────────────────────────────────
    with left:
        st.markdown('<div class="section-title">Upload Waste Image</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="upload-hint">
            📸 Drag & drop a <strong>JPG or PNG</strong> image below<br>
            <small>Supported: bottles, cans, paper, food scraps, electronics…</small>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Choose image",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed",
        )

        # Camera input (optional, works in supported browsers)
        use_camera = st.checkbox("📷 Use camera instead")
        camera_img = None
        if use_camera:
            camera_img = st.camera_input("Take a photo of the waste item")

        # Determine active image
        active_file = camera_img if use_camera and camera_img else uploaded

        if active_file:
            image_bytes = active_file.read()
            pil_img = Image.open(io.BytesIO(image_bytes))
            b64 = _img_to_b64(pil_img)

            st.markdown(f"""
            <div style="background:#f0fdf4;border-radius:16px;padding:1rem;
                        border:2px solid #86efac;margin-top:1rem;text-align:center;">
                <img src="data:image/png;base64,{b64}"
                     style="max-width:100%;border-radius:12px;max-height:280px;
                            object-fit:contain;">
                <p style="margin:.6rem 0 0;color:#15803d;font-size:.85rem;font-weight:500;">
                    ✅ Image loaded — ready to analyze
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            analyze_clicked = st.button(
                "🚀 Analyze Waste",
                type="primary",
                use_container_width=True,
            )

            if analyze_clicked:
                with st.spinner("🤖 AI is analyzing your waste image…"):
                    result = classify_waste(image_bytes)
                    rec = get_recommendation(result["category"])
                    result.update({
                        "recommendation": rec,
                        "timestamp": datetime.now().strftime("%H:%M:%S  %d %b %Y"),
                        "filename": getattr(active_file, "name", "camera_capture.png"),
                    })
                    st.session_state.last_result = result
                    st.session_state.history.append(result)
                st.success("✅ Analysis complete! See results →")
                st.rerun()
        else:
            st.markdown("""
            <div style="background:#fafafa;border-radius:12px;padding:1.5rem;
                        text-align:center;color:#9ca3af;margin-top:1rem;">
                <div style="font-size:3rem;">📂</div>
                <p style="margin:.5rem 0 0;font-size:.9rem;">No image selected yet</p>
            </div>
            """, unsafe_allow_html=True)

        # Tips
        st.markdown("""
        <div class="tip-box">
            <strong>💡 Tips for best results:</strong><br>
            <small>• Use clear, well-lit photos with a plain background<br>
            • Keep the waste item centred in the frame<br>
            • Avoid blurry or very dark images<br>
            • One item per photo gives the most accurate result</small>
        </div>
        """, unsafe_allow_html=True)

    # ── RIGHT: results ──────────────────────────────────────────────────
    with right:
        st.markdown('<div class="section-title">Analysis Results</div>', unsafe_allow_html=True)

        result = st.session_state.last_result

        if result is None:
            # Placeholder cards showing example categories
            st.markdown("""
            <div style="background:#f9fafb;border-radius:16px;padding:2.5rem;
                        text-align:center;border:2px dashed #d1d5db;">
                <div style="font-size:4rem;">🤖</div>
                <h3 style="color:#374151;margin:.8rem 0 .4rem;">AI Ready</h3>
                <p style="color:#9ca3af;font-size:.95rem;">
                    Upload an image and click <strong>Analyze Waste</strong><br>
                    to see your classification results here.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Example categories we detect:**")
            eg_cols = st.columns(3)
            for i, cat in enumerate(ALL_CATEGORIES):
                info = CATEGORY_INFO[cat]
                with eg_cols[i % 3]:
                    st.markdown(f"""
                    <div style="background:white;border-radius:10px;padding:.8rem;
                                text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.06);
                                border-top:3px solid {info['color']};margin-bottom:.5rem;">
                        <div style="font-size:1.5rem;">{info['icon']}</div>
                        <div style="font-size:.8rem;font-weight:600;color:#374151;">{cat}</div>
                    </div>
                    """, unsafe_allow_html=True)
            return

        # ── Detected category banner ──
        rec = result["recommendation"]
        cat = result["category"]
        conf = result["confidence"]
        info = CATEGORY_INFO[cat]

        st.markdown(f"""
        <div class="result-card">
            <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.2rem;">
                <div style="font-size:3.5rem;">{info['icon']}</div>
                <div>
                    <div style="font-size:.75rem;font-weight:700;letter-spacing:.1em;
                                color:#15803d;text-transform:uppercase;">Detected Waste Type</div>
                    <div style="font-size:2rem;font-weight:800;color:#064e3b;line-height:1.1;">
                        {cat}
                    </div>
                    <span class="badge"
                          style="background:{rec['badge_color']};color:{rec['badge_text_color']};">
                        {rec['badge']}
                    </span>
                </div>
            </div>

            <div style="margin-bottom:1rem;">
                <div style="display:flex;justify-content:space-between;
                            font-size:.85rem;font-weight:600;color:#374151;margin-bottom:.3rem;">
                    <span>AI Confidence</span>
                    <span style="color:{info['color']};">{int(conf*100)}%</span>
                </div>
                <div class="conf-bar-bg">
                    <div class="conf-bar-fill"
                         style="width:{int(conf*100)}%;background:linear-gradient(90deg,{info['color']},{info['color']}aa);">
                    </div>
                </div>
            </div>

            <div style="display:flex;flex-wrap:wrap;gap:.5rem;font-size:.82rem;color:#374151;">
                <span>🗑️ <strong>Dispose:</strong> {rec['disposal_method']}</span>
                <span style="color:#9ca3af;">|</span>
                <span>🤖 <strong>Method:</strong> {result['method']}</span>
                <span style="color:#9ca3af;">|</span>
                <span>🕐 {result['timestamp']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Confidence bar chart ──
        scores = result["all_scores"]
        df_scores = pd.DataFrame({
            "Category":   list(scores.keys()),
            "Confidence": [round(v * 100, 1) for v in scores.values()],
            "Color":      [CATEGORY_INFO[c]["color"] for c in scores.keys()],
        }).sort_values("Confidence", ascending=True)

        fig = go.Figure(go.Bar(
            x=df_scores["Confidence"],
            y=df_scores["Category"],
            orientation="h",
            marker_color=df_scores["Color"].tolist(),
            text=[f"{v:.1f}%" for v in df_scores["Confidence"]],
            textposition="outside",
        ))
        fig.update_layout(
            title="Classification Scores",
            xaxis_title="Confidence (%)",
            xaxis=dict(range=[0, 105]),
            height=280,
            margin=dict(l=10, r=40, t=40, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter"),
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── Disposal Steps ──
        st.markdown('<div class="section-title">How to Dispose</div>', unsafe_allow_html=True)
        for i, step in enumerate(rec["steps"], 1):
            st.markdown(f"""
            <div style="display:flex;align-items:flex-start;gap:.8rem;margin-bottom:.7rem;">
                <div style="min-width:28px;height:28px;background:linear-gradient(135deg,#22c55e,#16a34a);
                            border-radius:50%;display:flex;align-items:center;justify-content:center;
                            color:white;font-weight:700;font-size:.8rem;">{i}</div>
                <div style="background:white;border-radius:10px;padding:.7rem 1rem;flex:1;
                            box-shadow:0 2px 8px rgba(0,0,0,.06);font-size:.9rem;color:#374151;">
                    {step}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Recycling instruction ──
        st.markdown(f"""
        <div style="background:#eff6ff;border-left:5px solid #3b82f6;border-radius:12px;
                    padding:1.2rem 1.5rem;margin-top:.5rem;">
            <strong style="color:#1d4ed8;">♻️ Recycling Instruction</strong><br>
            <span style="color:#374151;font-size:.9rem;">{rec['recycling_instruction']}</span>
        </div>
        """, unsafe_allow_html=True)

        # ── Env tip ──
        st.markdown(f"""
        <div class="tip-box" style="margin-top:.8rem;">
            <strong>🌱 Environmental Tip</strong><br>
            <span style="font-size:.9rem;">{rec['env_tip']}</span>
        </div>
        """, unsafe_allow_html=True)

        # ── Fun fact ──
        st.markdown(f"""
        <div style="background:#f5f3ff;border-left:5px solid #8b5cf6;border-radius:12px;
                    padding:1.2rem 1.5rem;margin-top:.8rem;">
            <strong style="color:#6d28d9;">💡 Did You Know?</strong><br>
            <span style="color:#374151;font-size:.9rem;">{rec['fun_fact']}</span>
        </div>
        """, unsafe_allow_html=True)

        # ── Environmental savings for this item ──
        savings = {k: v for k, v in calculate_env_impact([result]).items()}
        s_cols = st.columns(4)
        savings_display = [
            ("💨", f"{savings['co2_reduced']} kg", "CO₂ Reduced"),
            ("⚡", f"{savings['energy_saved']} kWh", "Energy Saved"),
            ("💧", f"{savings['water_saved']} L", "Water Saved"),
            ("🌳", f"{savings['trees_saved']}", "Trees Saved"),
        ]
        st.markdown("<br><strong style='color:#064e3b;'>Impact of recycling this item:</strong>",
                    unsafe_allow_html=True)
        for col, (icon, val, label) in zip(s_cols, savings_display):
            with col:
                st.markdown(f"""
                <div style="background:white;border-radius:12px;padding:.9rem;text-align:center;
                            box-shadow:0 3px 10px rgba(0,0,0,.07);border-top:3px solid #22c55e;">
                    <div style="font-size:1.4rem;">{icon}</div>
                    <div style="font-weight:800;font-size:1.1rem;color:#064e3b;">{val}</div>
                    <div style="font-size:.72rem;color:#9ca3af;text-transform:uppercase;">{label}</div>
                </div>
                """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 3 – DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════
def page_dashboard():
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1e3a5f,#1d4ed8);
                border-radius:20px;padding:2rem 2.5rem;color:white;margin-bottom:1.5rem;">
        <h2 style="margin:0 0 .4rem;font-size:1.9rem;font-weight:800;">📊 Smart Waste Dashboard</h2>
        <p style="margin:0;opacity:.85;">Real-time overview of your waste segregation activity
        and environmental impact.</p>
    </div>
    """, unsafe_allow_html=True)

    history = st.session_state.history
    total = len(history)

    # Demo data toggle
    if total == 0:
        st.info("📌 No data yet. Showing **demo data** to preview the dashboard. "
                "Analyze some waste images to see your own stats!")
        # Inject demo history
        import random
        random.seed(42)
        demo_categories = (
            ["Plastic"] * 12 + ["Paper"] * 9 + ["Metal"] * 6 +
            ["Glass"] * 5 + ["Organic"] * 10 + ["E-Waste"] * 4
        )
        history = [{"category": c, "confidence": round(random.uniform(0.75, 0.97), 2)}
                   for c in demo_categories]
        total = len(history)

    # ── KPI row ──────────────────────────────────────────────────────────
    counts = {c: sum(1 for h in history if h["category"] == c) for c in ALL_CATEGORIES}
    impact = calculate_env_impact(history)

    k0, k1, k2, k3 = st.columns(4)
    kpi_data = [
        (k0, "🗂️", str(total),             "Total Items Analyzed",  "#22c55e"),
        (k1, "💨", f"{impact['co2_reduced']} kg",  "CO₂ Reduced",   "#3b82f6"),
        (k2, "⚡", f"{impact['energy_saved']} kWh","Energy Saved",  "#f59e0b"),
        (k3, "💧", f"{impact['water_saved']} L",   "Water Saved",   "#06b6d4"),
    ]
    for col, icon, val, label, color in kpi_data:
        with col:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color:{color};">
                <div class="metric-icon">{icon}</div>
                <div class="metric-value" style="color:{color};">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Category count cards ──────────────────────────────────────────────
    st.markdown('<div class="section-title">Waste Breakdown by Category</div>', unsafe_allow_html=True)
    cat_cols = st.columns(6)
    for i, cat in enumerate(ALL_CATEGORIES):
        info = CATEGORY_INFO[cat]
        pct = round(counts[cat] / total * 100, 1) if total else 0
        with cat_cols[i]:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color:{info['color']};text-align:center;">
                <div style="font-size:2rem;">{info['icon']}</div>
                <div class="metric-value" style="color:{info['color']};font-size:1.8rem;">
                    {counts[cat]}
                </div>
                <div class="metric-label">{cat}</div>
                <div style="font-size:.75rem;color:#9ca3af;margin-top:.3rem;">{pct}%</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row ───────────────────────────────────────────────────────
    chart_left, chart_right = st.columns([1.1, 1], gap="large")

    with chart_left:
        st.markdown('<div class="section-title">Distribution by Category</div>',
                    unsafe_allow_html=True)

        df_pie = pd.DataFrame({
            "Category": list(counts.keys()),
            "Count":    list(counts.values()),
            "Color":    [CATEGORY_INFO[c]["color"] for c in counts.keys()],
        })
        df_pie = df_pie[df_pie["Count"] > 0]

        fig_pie = go.Figure(go.Pie(
            labels=df_pie["Category"],
            values=df_pie["Count"],
            hole=0.45,
            marker_colors=df_pie["Color"].tolist(),
            textinfo="label+percent",
            textfont_size=12,
            pull=[0.04] * len(df_pie),
        ))
        fig_pie.update_layout(
            height=340,
            margin=dict(l=0, r=0, t=20, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter"),
            legend=dict(orientation="h", y=-0.1),
            annotations=[dict(text=f"<b>{total}</b><br>items", x=0.5, y=0.5,
                              font_size=14, showarrow=False)],
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with chart_right:
        st.markdown('<div class="section-title">Category Comparison</div>',
                    unsafe_allow_html=True)

        df_bar = pd.DataFrame({
            "Category": list(counts.keys()),
            "Count":    list(counts.values()),
            "Color":    [CATEGORY_INFO[c]["color"] for c in counts.keys()],
        })

        fig_bar = go.Figure(go.Bar(
            x=df_bar["Category"],
            y=df_bar["Count"],
            marker_color=df_bar["Color"].tolist(),
            text=df_bar["Count"],
            textposition="outside",
        ))
        fig_bar.update_layout(
            height=340,
            margin=dict(l=0, r=0, t=20, b=40),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(248,250,252,1)",
            yaxis=dict(gridcolor="#e5e7eb", title="Count"),
            xaxis=dict(title=""),
            font=dict(family="Inter"),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── Environmental impact bar chart ────────────────────────────────────
    st.markdown('<div class="section-title">Environmental Impact by Category</div>',
                unsafe_allow_html=True)

    impact_data = []
    for cat in ALL_CATEGORIES:
        fake_history = [{"category": cat}] * counts[cat]
        cat_impact = calculate_env_impact(fake_history)
        impact_data.append({
            "Category":   cat,
            "CO₂ (kg)":   cat_impact["co2_reduced"],
            "Energy (kWh)": cat_impact["energy_saved"],
            "Water (L)":  cat_impact["water_saved"],
        })
    df_impact = pd.DataFrame(impact_data)

    fig_impact = go.Figure()
    for metric, color in [("CO₂ (kg)", "#3b82f6"), ("Energy (kWh)", "#f59e0b"), ("Water (L)", "#06b6d4")]:
        fig_impact.add_trace(go.Bar(
            name=metric,
            x=df_impact["Category"],
            y=df_impact[metric],
            marker_color=color,
        ))
    fig_impact.update_layout(
        barmode="group",
        height=320,
        margin=dict(l=0, r=0, t=20, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,250,252,1)",
        yaxis=dict(gridcolor="#e5e7eb"),
        font=dict(family="Inter"),
        legend=dict(orientation="h", y=1.1),
    )
    st.plotly_chart(fig_impact, use_container_width=True)

    # ── Recent history table ──────────────────────────────────────────────
    if st.session_state.history:
        st.markdown('<div class="section-title">Recent Analysis History</div>',
                    unsafe_allow_html=True)
        rows = []
        for h in reversed(st.session_state.history[-15:]):
            info = CATEGORY_INFO[h["category"]]
            rows.append({
                "Icon":       info["icon"],
                "Category":   h["category"],
                "Confidence": f"{int(h['confidence']*100)}%",
                "Method":     h.get("method", "AI"),
                "Time":       h.get("timestamp", "—"),
            })
        df_hist = pd.DataFrame(rows)
        st.dataframe(df_hist, use_container_width=True, hide_index=True)

        if st.button("🗑️ Clear History", type="secondary"):
            st.session_state.history = []
            st.session_state.last_result = None
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 4 – HOW IT WORKS
# ═══════════════════════════════════════════════════════════════════════════
def page_how_it_works():
    st.markdown("""
    <div style="background:linear-gradient(135deg,#064e3b,#065f46);
                border-radius:20px;padding:2rem 2.5rem;color:white;margin-bottom:1.5rem;">
        <h2 style="margin:0 0 .4rem;font-size:1.9rem;font-weight:800;">⚙️ How It Works</h2>
        <p style="margin:0;opacity:.85;">A visual walkthrough of our AI waste classification pipeline.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Visual pipeline ──────────────────────────────────────────────────
    st.markdown('<div class="section-title">The Smart Waste Pipeline</div>', unsafe_allow_html=True)

    pipeline = [
        ("📤", "1. Upload Waste Image",
         "User uploads a JPG/PNG photo of a waste item through the Waste Analyzer page. "
         "Alternatively, they can use their device camera to capture a live photo."),
        ("🔄", "2. Image Pre-processing",
         "The image is loaded using Pillow (PIL) and resized to 224×224 pixels — "
         "the standard input size for MobileNetV2. Pixel values are normalised "
         "to the range expected by the model."),
        ("🤖", "3. AI Inference (MobileNetV2)",
         "The preprocessed image is passed through MobileNetV2, a lightweight "
         "deep convolutional neural network pretrained on 1.2 million ImageNet images "
         "across 1,000 classes. The model outputs a probability distribution."),
        ("🗂️", "4. Waste Category Mapping",
         "The top-5 predicted ImageNet labels are checked against a curated "
         "keyword mapping table that links 50+ common object labels to our "
         "6 waste categories: Plastic, Paper, Metal, Glass, Organic, E-Waste."),
        ("🎨", "5. Heuristic Fallback",
         "If no ImageNet label maps to a waste category, a colour & texture "
         "heuristic analyses the image's RGB statistics — brightness, saturation, "
         "and texture variance — to make a reliable fallback classification."),
        ("📋", "6. Smart Recommendation",
         "The classified category is looked up in a curated recommendations database "
         "containing: disposal method, step-by-step instructions, recycling guidance, "
         "environmental tip, and a fun fact."),
        ("📊", "7. Dashboard Update",
         "The result is stored in session state. The Dashboard page automatically "
         "reflects the new count, updates charts, and recalculates the "
         "cumulative environmental impact."),
        ("🌍", "8. Cleaner Environment",
         "By correctly segregating waste, users reduce landfill, enable recycling, "
         "and contribute measurably to lower CO₂ emissions, energy savings, "
         "and water conservation."),
    ]

    for icon, title, desc in pipeline:
        st.markdown(f"""
        <div class="timeline-step">
            <div class="timeline-dot">{icon}</div>
            <div class="timeline-content">
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Tech stack ────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Technology Stack</div>', unsafe_allow_html=True)

    tech = [
        ("🐍", "Python 3.10+",      "Core programming language",             "#3b82f6"),
        ("⚡", "Streamlit",         "Interactive web application framework", "#ff4b4b"),
        ("🧠", "TensorFlow/Keras",  "MobileNetV2 deep learning model",       "#ff6f00"),
        ("🖼️", "Pillow (PIL)",      "Image loading and preprocessing",       "#22c55e"),
        ("📊", "Plotly",            "Interactive charts and visualisations", "#636efa"),
        ("🐼", "Pandas",            "Data manipulation and tables",          "#150458"),
        ("🔢", "NumPy",             "Numerical array operations",            "#4dabf7"),
    ]

    t_cols = st.columns(4)
    for i, (icon, name, desc, color) in enumerate(tech):
        with t_cols[i % 4]:
            st.markdown(f"""
            <div class="step-card" style="margin-bottom:1rem;border-top-color:{color};">
                <div style="font-size:2rem;">{icon}</div>
                <h4 style="color:#064e3b;font-size:.95rem;font-weight:700;margin:.3rem 0;">{name}</h4>
                <p style="color:#6b7280;font-size:.82rem;margin:0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # ── Model card ────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">About the AI Model</div>', unsafe_allow_html=True)

    col_m1, col_m2 = st.columns([1.2, 1])
    with col_m1:
        st.markdown("""
        <div style="background:white;border-radius:16px;padding:1.8rem;
                    box-shadow:0 4px 16px rgba(0,0,0,.08);">
            <h4 style="color:#064e3b;font-size:1.1rem;font-weight:700;margin-top:0;">
                MobileNetV2 – ImageNet Pretrained
            </h4>
            <p style="color:#374151;font-size:.9rem;line-height:1.6;">
                MobileNetV2 is a lightweight convolutional neural network architecture
                optimised for mobile and embedded vision applications. It uses
                <strong>inverted residuals</strong> and <strong>linear bottlenecks</strong>
                to achieve high accuracy with minimal compute.
            </p>
            <ul style="color:#374151;font-size:.88rem;line-height:1.8;padding-left:1.2rem;">
                <li><strong>Parameters:</strong> ~3.4 million (very lightweight)</li>
                <li><strong>Input size:</strong> 224 × 224 × 3 (RGB)</li>
                <li><strong>Training data:</strong> ImageNet (1.2M images, 1,000 classes)</li>
                <li><strong>Accuracy:</strong> 71.8% top-1 on ImageNet</li>
                <li><strong>Inference time:</strong> &lt; 1 second on a standard laptop</li>
                <li><strong>Download:</strong> Automatic via Keras (~14 MB)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#f0fdf4,#dcfce7);border-radius:16px;
                    padding:1.8rem;box-shadow:0 4px 16px rgba(34,197,94,.1);
                    border:2px solid #86efac;">
            <h4 style="color:#064e3b;font-size:1.1rem;font-weight:700;margin-top:0;">
                Why No Custom Training?
            </h4>
            <p style="color:#374151;font-size:.88rem;line-height:1.6;">
                Custom waste classification models require large labelled datasets
                (e.g. TrashNet) and GPU training time — not ideal for a hackathon demo.
            </p>
            <p style="color:#374151;font-size:.88rem;line-height:1.6;">
                Our approach uses <strong>transfer learning knowledge</strong> from
                ImageNet: the model already recognises bottles, cans, laptops,
                food items, and paper. We map those predictions to waste categories
                without any retraining.
            </p>
            <p style="color:#374151;font-size:.88rem;line-height:1.6;">
                This runs <strong>instantly on any laptop</strong>, requires
                <strong>no GPU</strong>, and downloads automatically on first run.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 5 – ABOUT
# ═══════════════════════════════════════════════════════════════════════════
def page_about():
    st.markdown("""
    <div style="background:linear-gradient(135deg,#064e3b,#065f46);
                border-radius:20px;padding:2rem 2.5rem;color:white;margin-bottom:1.5rem;">
        <h2 style="margin:0 0 .4rem;font-size:1.9rem;font-weight:800;">ℹ️ About Smart Waste</h2>
        <p style="margin:0;opacity:.85;">Our mission, vision, and the team behind the project.</p>
    </div>
    """, unsafe_allow_html=True)

    # Mission
    st.markdown('<div class="section-title">Our Mission</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:white;border-radius:16px;padding:2rem;
                box-shadow:0 4px 16px rgba(0,0,0,.07);margin-bottom:1rem;">
        <p style="color:#374151;font-size:1rem;line-height:1.8;margin:0;">
            <strong style="color:#064e3b;">Smart Waste</strong> is an AI-powered waste
            segregation assistant designed to make recycling effortless and accessible.
            We believe that technology can bridge the gap between good intentions and correct
            recycling behaviour — one photo at a time.
        </p>
        <p style="color:#374151;font-size:1rem;line-height:1.8;margin:.8rem 0 0;">
            Our platform is built with the vision of integration into <strong>Smart City
            waste management systems</strong>, enabling municipalities to provide citizens
            with instant, AI-driven guidance on waste disposal — reducing landfill waste,
            improving recycling rates, and contributing to a cleaner, greener future.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Problem & Solution
    ps_left, ps_right = st.columns(2, gap="large")
    with ps_left:
        st.markdown("""
        <div style="background:#fef2f2;border-radius:16px;padding:1.8rem;
                    border-left:5px solid #ef4444;height:100%;">
            <h4 style="color:#991b1b;font-size:1.1rem;font-weight:700;margin-top:0;">
                ❌ The Problem
            </h4>
            <ul style="color:#374151;font-size:.9rem;line-height:1.9;padding-left:1.2rem;">
                <li>2.1 billion tonnes of solid waste generated globally each year</li>
                <li>Less than 20% of global waste is properly recycled</li>
                <li>Incorrect segregation contaminates entire recycling batches</li>
                <li>Citizens lack clear, accessible guidance on disposal methods</li>
                <li>E-waste growing at 3–4× the rate of general waste</li>
                <li>Food waste generates 8% of global greenhouse gas emissions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with ps_right:
        st.markdown("""
        <div style="background:#f0fdf4;border-radius:16px;padding:1.8rem;
                    border-left:5px solid #22c55e;height:100%;">
            <h4 style="color:#166534;font-size:1.1rem;font-weight:700;margin-top:0;">
                ✅ Our Solution
            </h4>
            <ul style="color:#374151;font-size:.9rem;line-height:1.9;padding-left:1.2rem;">
                <li>Instant AI classification from a single photo upload</li>
                <li>Step-by-step disposal instructions for all 6 waste types</li>
                <li>Environmental impact metrics to motivate behaviour change</li>
                <li>Lightweight model — runs on any laptop, no GPU needed</li>
                <li>Real-time dashboard for tracking personal recycling habits</li>
                <li>Open, extensible architecture for smart city integration</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Impact metrics (targets)
    st.markdown('<div class="section-title">Our Impact Goals</div>', unsafe_allow_html=True)
    g1, g2, g3, g4 = st.columns(4)
    goals = [
        (g1, "🎯", "95%", "Classification Accuracy Target",    "#22c55e"),
        (g2, "🏙️", "100+", "Smart City Integrations Planned", "#3b82f6"),
        (g3, "👥", "10K+", "Users by End of 2027",            "#f59e0b"),
        (g4, "🌍", "500T", "CO₂ Reduction Target (tonnes/yr)","#8b5cf6"),
    ]
    for col, icon, val, label, color in goals:
        with col:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color:{color};text-align:center;">
                <div style="font-size:1.8rem;">{icon}</div>
                <div class="metric-value" style="color:{color};">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Future enhancements
    st.markdown('<div class="section-title">Future Enhancements</div>', unsafe_allow_html=True)
    future = [
        ("🎓", "Custom Trained Model",
         "Fine-tune MobileNetV2 on the TrashNet / TACO waste datasets "
         "to achieve >95% accuracy on real-world waste images."),
        ("📱", "Mobile App",
         "React Native mobile application with live camera classification "
         "and offline inference using TensorFlow Lite."),
        ("🗺️", "Nearest Recycling Map",
         "Integration with Google Maps API to show the nearest "
         "recycling centre, drop-off point, or collection schedule."),
        ("🔗", "IoT Smart Bin",
         "Raspberry Pi integration for automatic bin lid opening and "
         "compartment routing based on AI classification."),
        ("📈", "City Analytics",
         "Aggregated anonymised waste data for municipal planning, "
         "trend analysis, and infrastructure optimisation."),
        ("🌐", "Multi-language",
         "Support for regional languages to increase accessibility "
         "across diverse populations."),
    ]

    f_cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(future):
        with f_cols[i % 3]:
            st.markdown(f"""
            <div class="step-card" style="margin-bottom:1rem;">
                <div style="font-size:2rem;">{icon}</div>
                <h4 style="color:#064e3b;font-size:.95rem;font-weight:700;margin:.3rem 0;">{title}</h4>
                <p style="color:#6b7280;font-size:.83rem;margin:0;line-height:1.5;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Built with
    st.markdown("""
    <div style="background:linear-gradient(135deg,#f0fdf4,#dcfce7);border-radius:16px;
                padding:2rem;text-align:center;border:2px solid #86efac;">
        <div style="font-size:2.5rem;margin-bottom:.5rem;">♻️</div>
        <h3 style="color:#064e3b;font-weight:800;margin:.3rem 0;">Smart Waste</h3>
        <p style="color:#374151;font-size:.9rem;margin:0;">
            Built with ❤️ for the ICV Hackathon 2026 &nbsp;|&nbsp;
            AI for a Cleaner Future &nbsp;|&nbsp;
            Smart City · Green Technology
        </p>
        <p style="color:#6b7280;font-size:.8rem;margin:.5rem 0 0;">
            Python · Streamlit · TensorFlow · Plotly · Pandas · Pillow
        </p>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════════════════
def main():
    render_sidebar()

    page = st.session_state.page
    if page == "Home":
        page_home()
    elif page == "Analyzer":
        page_analyzer()
    elif page == "Dashboard":
        page_dashboard()
    elif page == "How It Works":
        page_how_it_works()
    elif page == "About":
        page_about()


if __name__ == "__main__":
    main()
