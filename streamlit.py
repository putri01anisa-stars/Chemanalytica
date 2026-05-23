import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ChemAnalytica",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Outfit:wght@300;400;600;800&display=swap');

:root {
    --teal:   #00f5d4;
    --indigo: #7b5ea7;
    --gold:   #f7c59f;
    --dark:   #0d1117;
    --card:   #161b22;
    --border: #30363d;
    --text:   #e6edf3;
    --muted:  #8b949e;
}

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    background: var(--dark);
    color: var(--text);
}

/* Animated gradient header */
.hero-header {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 40%, #1a1f2e 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    text-align: center;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(from 0deg at 50% 50%,
        transparent 0deg,
        rgba(0,245,212,0.07) 60deg,
        transparent 120deg,
        rgba(123,94,167,0.07) 180deg,
        transparent 240deg,
        rgba(247,197,159,0.05) 300deg,
        transparent 360deg);
    animation: spin 12s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(90deg, var(--teal), var(--indigo), var(--gold));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    position: relative;
    z-index: 1;
    margin: 0;
}
.hero-sub {
    font-size: 1.1rem;
    color: var(--muted);
    position: relative;
    z-index: 1;
    margin-top: 0.5rem;
    letter-spacing: 0.05em;
}

/* Feature badges */
.badge-row {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin-top: 1rem;
    position: relative;
    z-index: 1;
}
.badge {
    background: rgba(0,245,212,0.1);
    border: 1px solid rgba(0,245,212,0.3);
    border-radius: 999px;
    padding: 0.3rem 0.9rem;
    font-size: 0.8rem;
    color: var(--teal);
    font-family: 'Space Mono', monospace;
}

/* Module cards */
.module-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}
.module-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s;
}
.module-card:hover {
    border-color: var(--teal);
    box-shadow: 0 0 20px rgba(0,245,212,0.15);
    transform: translateY(-3px);
}
.module-icon { font-size: 2rem; }
.module-name { font-size: 0.9rem; font-weight: 600; margin-top: 0.4rem; color: var(--text); }
.module-desc { font-size: 0.75rem; color: var(--muted); margin-top: 0.2rem; }

/* Result cards */
.result-box {
    background: linear-gradient(135deg, rgba(0,245,212,0.05), rgba(123,94,167,0.05));
    border: 1px solid rgba(0,245,212,0.25);
    border-radius: 12px;
    padding: 1.2rem;
    margin: 0.5rem 0;
}
.result-label { font-size: 0.8rem; color: var(--muted); font-family: 'Space Mono', monospace; }
.result-value { font-size: 1.8rem; font-weight: 800; color: var(--teal); }
.result-unit  { font-size: 0.9rem; color: var(--gold); margin-left: 0.3rem; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--card);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container { padding-top: 1rem; }

/* Streamlit overrides */
.stSelectbox > div > div { background: var(--card); border-color: var(--border); color: var(--text); }
.stNumberInput input, .stTextInput input, .stTextArea textarea {
    background: var(--card) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}
.stButton > button {
    background: linear-gradient(135deg, var(--teal), var(--indigo));
    color: #0d1117;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    padding: 0.5rem 1.5rem;
    font-family: 'Outfit', sans-serif;
    font-size: 1rem;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.85; }

.stTabs [data-baseweb="tab"] {
    background: var(--card);
    border-radius: 8px 8px 0 0;
    color: var(--muted);
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
}
.stTabs [aria-selected="true"] { color: var(--teal) !important; border-bottom: 2px solid var(--teal) !important; }

.stDataFrame { background: var(--card) !important; }

h1,h2,h3,h4 { font-family: 'Outfit', sans-serif; }

.info-pill {
    display: inline-block;
    background: rgba(123,94,167,0.15);
    border: 1px solid rgba(123,94,167,0.4);
    border-radius: 999px;
    padding: 0.2rem 0.8rem;
    font-size: 0.78rem;
    color: #b39ddb;
    font-family: 'Space Mono', monospace;
}
.warn-pill {
    display: inline-block;
    background: rgba(247,197,159,0.1);
    border: 1px solid rgba(247,197,159,0.35);
    border-radius: 999px;
    padding: 0.2rem 0.8rem;
    font-size: 0.78rem;
    color: var(--gold);
    font-family: 'Space Mono', monospace;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--teal);
    font-family: 'Space Mono', monospace;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.4rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
  <div class="hero-title">⚗️ ChemAnalytica</div>
  <div class="hero-sub">Platform Analisis Kimia Terpadu · Politeknik AKA Bogor</div>
  <div class="badge-row">
    <span class="badge">Titrimetri</span>
    <span class="badge">Spektrofotometri</span>
    <span class="badge">Stoikiometri</span>
    <span class="badge">Larutan Buffer</span>
    <span class="badge">Konversi Satuan</span>
    <span class="badge">Visualisasi Data</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚗️ **ChemAnalytica**")
    st.markdown("---")
    menu = st.radio(
        "🔬 Pilih Modul",
        [
            "🏠 Beranda",
            "🧪 Titrimetri & Volumetri",
            "🌈 Spektrofotometri (Beer-Lambert)",
            "⚗️ Stoikiometri & Mol",
            "🧫 Larutan Buffer (Henderson)",
            "📊 Kurva Kalibrasi",
            "🔁 Konversi & Utilitas Kimia",
        ],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown('<span class="info-pill">v1.0 · 2026</span>', unsafe_allow_html=True)
    st.markdown('<br><span class="warn-pill">Tugas LPK Kimia Analitik</span>', unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Dibuat dengan Streamlit + Plotly")

# ═══════════════════════════════════════════════════════════
# MODUL: BERANDA
# ═══════════════════════════════════════════════════════════
if menu == "🏠 Beranda":
    st.markdown("## Selamat Datang di ChemAnalytica")
    st.markdown("""
    **ChemAnalytica** adalah platform analisis kimia terpadu yang dirancang untuk mendukung
    praktikum dan pembelajaran kimia analitik. Aplikasi ini menyediakan berbagai alat kalkulasi,
    visualisasi data, dan referensi kimia dalam satu antarmuka yang modern dan intuitif.
    """)

    st.markdown("""
    <div class="module-grid">
      <div class="module-card">
        <div class="module-icon">🧪</div>
        <div class="module-name">Titrimetri</div>
        <div class="module-desc">Hitung normalitas, konsentrasi, % kemurnian & lebih</div>
      </div>
      <div class="module-card">
        <div class="module-icon">🌈</div>
        <div class="module-name">Spektrofotometri</div>
        <div class="module-desc">Hukum Beer-Lambert, absorbansi, transmitansi</div>
      </div>
      <div class="module-card">
        <div class="module-icon">⚗️</div>
        <div class="module-name">Stoikiometri</div>
        <div class="module-desc">Mol, massa, reaktan pembatas, hasil teoritis</div>
      </div>
      <div class="module-card">
        <div class="module-icon">🧫</div>
        <div class="module-name">Buffer</div>
        <div class="module-desc">pH Henderson-Hasselbalch, kapasitas buffer</div>
      </div>
      <div class="module-card">
        <div class="module-icon">📊</div>
        <div class="module-name">Kurva Kalibrasi</div>
        <div class="module-desc">Regresi linier, R², LOD, LOQ, sampel unknown</div>
      </div>
      <div class="module-card">
        <div class="module-icon">🔁</div>
        <div class="module-name">Konversi</div>
        <div class="module-desc">Satuan konsentrasi, suhu, tekanan & referensi MW</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Demo chart
    st.markdown("---")
    st.markdown('<div class="section-title">📈 Demo: Simulasi Kurva Titrasi Asam-Basa</div>', unsafe_allow_html=True)
    vol = np.linspace(0, 50, 500)
    ph  = 14 - np.log10(np.abs(25 - vol) / (vol + 25) + 1e-10)
    ph  = np.clip(ph, 1, 13)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=vol, y=ph,
        mode='lines',
        line=dict(color='#00f5d4', width=3),
        name='Kurva Titrasi'
    ))
    fig.add_vline(x=25, line_dash="dash", line_color="#f7c59f",
                  annotation_text="Titik Ekivalen", annotation_font_color="#f7c59f")
    fig.add_hline(y=7, line_dash="dot", line_color="#7b5ea7",
                  annotation_text="pH 7", annotation_font_color="#b39ddb")
    fig.update_layout(
        paper_bgcolor='#161b22', plot_bgcolor='#0d1117',
        font=dict(color='#e6edf3'),
        xaxis=dict(title='Volume NaOH (mL)', gridcolor='#21262d'),
        yaxis=dict(title='pH', gridcolor='#21262d', range=[0,14]),
        margin=dict(l=40, r=40, t=30, b=40),
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# MODUL: TITRIMETRI
# ═══════════════════════════════════════════════════════════
elif menu == "🧪 Titrimetri & Volumetri":
    st.markdown("## 🧪 Titrimetri & Volumetri")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Normalitas & Konsentrasi",
        "% Kemurnian Sampel",
        "Titrasi Kompleksometri",
        "Iodimetri / Iodometri"
    ])

    # ── Tab 1: Normalitas ──────────────────────────────────
    with tab1:
        st.markdown('<div class="section-title">Kalkulator Normalitas & Konsentrasi</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            V1 = st.number_input("Volume Titran (V₁, mL)", min_value=0.0, value=10.0, step=0.1)
            N1 = st.number_input("Normalitas Titran (N₁, N)", min_value=0.0, value=0.1, step=0.001, format="%.4f")
        with c2:
            V2 = st.number_input("Volume Sampel (V₂, mL)", min_value=0.1, value=25.0, step=0.1)
            BM = st.number_input("Berat Molekul Analit (g/mol)", min_value=1.0, value=204.23, step=0.01)
            ekivalen = st.number_input("Jumlah Ekivalen (n)", min_value=1, value=1, step=1)

        if st.button("⚡ Hitung Normalitas & Molaritas"):
            N2 = (V1 * N1) / V2
            M2 = N2 / ekivalen
            konsentrasi_g = (M2 * BM)
            st.markdown(f"""
            <div class="result-box">
              <div class="result-label">NORMALITAS SAMPEL (N₂)</div>
              <div class="result-value">{N2:.5f}<span class="result-unit">N</span></div>
            </div>
            <div class="result-box">
              <div class="result-label">MOLARITAS SAMPEL</div>
              <div class="result-value">{M2:.5f}<span class="result-unit">M</span></div>
            </div>
            <div class="result-box">
              <div class="result-label">KONSENTRASI (g/L)</div>
              <div class="result-value">{konsentrasi_g:.4f}<span class="result-unit">g/L</span></div>
            </div>
            """, unsafe_allow_html=True)

            # Plot V1 vs N2
            v_range = np.linspace(1, 30, 100)
            n2_range = (v_range * N1) / V2
            fig = go.Figure(go.Scatter(x=v_range, y=n2_range, mode='lines',
                                       line=dict(color='#00f5d4', width=2.5)))
            fig.add_trace(go.Scatter(x=[V1], y=[N2], mode='markers',
                                     marker=dict(color='#f7c59f', size=12, symbol='star'),
                                     name='Titik Anda'))
            fig.update_layout(
                title='Grafik V₁ vs N₂',
                paper_bgcolor='#161b22', plot_bgcolor='#0d1117',
                font=dict(color='#e6edf3'),
                xaxis=dict(title='V₁ (mL)', gridcolor='#21262d'),
                yaxis=dict(title='N₂ (N)', gridcolor='#21262d'),
                height=300, margin=dict(l=40, r=20, t=40, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)

    # ── Tab 2: % Kemurnian ──────────────────────────────────
    with tab2:
        st.markdown('<div class="section-title">Perhitungan % Kemurnian Sampel</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            vt2 = st.number_input("Vol. Titran (mL)", min_value=0.0, value=12.5, step=0.01, key="vt2")
            nt2 = st.number_input("Normalitas Titran (N)", min_value=0.0, value=0.1, step=0.0001, format="%.4f", key="nt2")
            bst = st.number_input("Berat Sampel (mg)", min_value=0.1, value=250.0, step=0.1)
        with c2:
            bmt2 = st.number_input("BM Analit (g/mol)", min_value=1.0, value=176.12, step=0.01, key="bmt2")
            nt2_eq = st.number_input("Ekivalen", min_value=1, value=2, step=1, key="nt2_eq")

        if st.button("⚡ Hitung % Kemurnian"):
            mg_ekiv = bmt2 / nt2_eq
            mg_analit = vt2 * nt2 * mg_ekiv
            pct = (mg_analit / bst) * 100
            st.markdown(f"""
            <div class="result-box">
              <div class="result-label">MASSA ANALIT TERDETEKSI</div>
              <div class="result-value">{mg_analit:.3f}<span class="result-unit">mg</span></div>
            </div>
            <div class="result-box">
              <div class="result-label">% KEMURNIAN</div>
              <div class="result-value">{pct:.2f}<span class="result-unit">%</span></div>
            </div>
            """, unsafe_allow_html=True)
            grade = "✅ Sangat Murni" if pct >= 98 else "⚠️ Cukup Murni" if pct >= 90 else "❌ Perlu Pemurnian"
            st.info(f"**Interpretasi:** {grade} (batas farmakope ≥ 98.0%)")

    # ── Tab 3: Kompleksometri ──────────────────────────────
    with tab3:
        st.markdown('<div class="section-title">Titrasi Kompleksometri (EDTA)</div>', unsafe_allow_html=True)
        st.caption("Menghitung kadar logam (Ca, Mg, Zn, dll.) dengan titrasi EDTA")
        c1, c2 = st.columns(2)
        with c1:
            logam = st.selectbox("Ion Logam", ["Ca²⁺ (40.08)", "Mg²⁺ (24.31)", "Zn²⁺ (65.38)", "Cu²⁺ (63.55)", "Fe³⁺ (55.85)"])
            bm_dict = {"Ca²⁺ (40.08)": 40.08, "Mg²⁺ (24.31)": 24.31, "Zn²⁺ (65.38)": 65.38,
                       "Cu²⁺ (63.55)": 63.55, "Fe³⁺ (55.85)": 55.85}
            bm_logam = bm_dict[logam]
            v_edta   = st.number_input("Volume EDTA (mL)", 0.0, value=15.0, step=0.01)
            n_edta   = st.number_input("Normalitas EDTA (N)", 0.0, value=0.05, step=0.001, format="%.4f")
        with c2:
            vol_sampel = st.number_input("Volume Sampel (mL)", 0.1, value=100.0)
            fp         = st.number_input("Faktor Pengenceran", 1.0, value=1.0)

        if st.button("⚡ Hitung Kadar Logam"):
            mmol_logam = v_edta * n_edta
            mg_logam   = mmol_logam * bm_logam
            mg_per_L   = (mg_logam / vol_sampel) * 1000 * fp
            ppm        = mg_per_L
            st.markdown(f"""
            <div class="result-box">
              <div class="result-label">KADAR {logam.split('(')[0].strip()}</div>
              <div class="result-value">{ppm:.3f}<span class="result-unit">mg/L (ppm)</span></div>
            </div>
            <div class="result-box">
              <div class="result-label">MASSA LOGAM DALAM SAMPEL</div>
              <div class="result-value">{mg_logam:.4f}<span class="result-unit">mg</span></div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 4: Iodimetri ──────────────────────────────────
    with tab4:
        st.markdown('<div class="section-title">Iodimetri / Iodometri — Vitamin C (Asam Askorbat)</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            v_i2   = st.number_input("Volume Iodium / Na₂S₂O₃ (mL)", 0.0, value=8.5, step=0.01, key="vi2")
            n_i2   = st.number_input("Normalitas (N)", 0.0, value=0.01, step=0.0001, format="%.4f", key="ni2")
        with c2:
            berat_tab = st.number_input("Berat Tablet (mg)", 0.1, value=500.0)
            vol_labu  = st.number_input("Volume Labu Ukur (mL)", 1.0, value=100.0)
            vol_pip   = st.number_input("Volume Pipet (mL)", 0.1, value=10.0)

        if st.button("⚡ Hitung Vitamin C"):
            BM_vit_c = 176.12
            fp_iod   = vol_labu / vol_pip
            mg_vc    = v_i2 * n_i2 * (BM_vit_c / 2) * fp_iod
            pct_vc   = (mg_vc / berat_tab) * 100
            st.markdown(f"""
            <div class="result-box">
              <div class="result-label">KADAR VITAMIN C</div>
              <div class="result-value">{mg_vc:.2f}<span class="result-unit">mg/tablet</span></div>
            </div>
            <div class="result-box">
              <div class="result-label">% LABEL CLAIM</div>
              <div class="result-value">{pct_vc:.1f}<span class="result-unit">%</span></div>
            </div>
            """, unsafe_allow_html=True)
            st.info("Syarat USP: Label Claim 90.0%–110.0%")


# ═══════════════════════════════════════════════════════════
# MODUL: SPEKTROFOTOMETRI
# ═══════════════════════════════════════════════════════════
elif menu == "🌈 Spektrofotometri (Beer-Lambert)":
    st.markdown("## 🌈 Spektrofotometri — Hukum Beer-Lambert")
    st.latex(r"A = \varepsilon \cdot b \cdot c \quad \Leftrightarrow \quad A = \log\frac{I_0}{I} = -\log T")

    tab1, tab2 = st.tabs(["Kalkulator A / T / c", "Simulasi Spektrum Absorpsi"])

    with tab1:
        mode = st.radio("Mode Perhitungan", ["A → c (konsentrasi)", "c → A (absorbansi)", "A ↔ T"])

        if mode == "A → c (konsentrasi)":
            c1, c2 = st.columns(2)
            with c1:
                A_val  = st.number_input("Absorbansi (A)", 0.0, 3.0, 0.45, step=0.001)
                eps    = st.number_input("ε (L·mol⁻¹·cm⁻¹)", 0.1, value=8000.0, step=10.0)
            with c2:
                b_val  = st.number_input("Tebal Sel (b, cm)", 0.1, value=1.0, step=0.1)
            if st.button("⚡ Hitung Konsentrasi"):
                c_val = A_val / (eps * b_val)
                T_val = 10 ** (-A_val)
                st.markdown(f"""
                <div class="result-box"><div class="result-label">KONSENTRASI</div>
                <div class="result-value">{c_val:.6f}<span class="result-unit">mol/L</span></div></div>
                <div class="result-box"><div class="result-label">KONSENTRASI (µmol/L)</div>
                <div class="result-value">{c_val*1e6:.4f}<span class="result-unit">µM</span></div></div>
                <div class="result-box"><div class="result-label">TRANSMITANSI</div>
                <div class="result-value">{T_val*100:.2f}<span class="result-unit">%T</span></div></div>
                """, unsafe_allow_html=True)

        elif mode == "c → A (absorbansi)":
            c1, c2 = st.columns(2)
            with c1:
                c_in   = st.number_input("Konsentrasi (mol/L)", 0.0, value=0.0001, step=0.00001, format="%.6f")
                eps2   = st.number_input("ε (L·mol⁻¹·cm⁻¹)", 0.1, value=8000.0, step=10.0, key="eps2")
            with c2:
                b2     = st.number_input("Tebal Sel (cm)", 0.1, value=1.0, step=0.1, key="b2")
            if st.button("⚡ Hitung Absorbansi"):
                A_out  = eps2 * b2 * c_in
                T_out  = 10 ** (-A_out)
                st.markdown(f"""
                <div class="result-box"><div class="result-label">ABSORBANSI (A)</div>
                <div class="result-value">{A_out:.4f}</div></div>
                <div class="result-box"><div class="result-label">TRANSMITANSI (%T)</div>
                <div class="result-value">{T_out*100:.2f}<span class="result-unit">%</span></div></div>
                """, unsafe_allow_html=True)

        else:  # A ↔ T
            c1, c2 = st.columns(2)
            with c1:
                A_conv = st.number_input("Absorbansi (A)", 0.0, 3.0, 0.301, step=0.001, key="a_conv")
            with c2:
                T_conv = st.number_input("%T", 0.01, 100.0, 50.0, step=0.1, key="t_conv")
            if st.button("⚡ Konversi"):
                T_from_A = 10 ** (-A_conv) * 100
                A_from_T = -math.log10(T_conv / 100)
                c1o, c2o = st.columns(2)
                with c1o:
                    st.markdown(f"""<div class="result-box"><div class="result-label">A={A_conv:.3f} → %T</div>
                    <div class="result-value">{T_from_A:.2f}<span class="result-unit">%</span></div></div>""",
                    unsafe_allow_html=True)
                with c2o:
                    st.markdown(f"""<div class="result-box"><div class="result-label">%T={T_conv:.1f} → A</div>
                    <div class="result-value">{A_from_T:.4f}</div></div>""",
                    unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-title">Simulasi Kurva Absorpsi Multikomponen</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            λmax1 = st.slider("λmax Komponen 1 (nm)", 350, 750, 450)
            ε1    = st.slider("ε₁ (×10³)", 1, 50, 15)
        with col2:
            λmax2 = st.slider("λmax Komponen 2 (nm)", 350, 750, 600)
            ε2    = st.slider("ε₂ (×10³)", 1, 50, 20)

        λ = np.linspace(300, 800, 500)
        A1 = ε1 * 1e3 * 1e-5 * np.exp(-0.5 * ((λ - λmax1) / 40) ** 2)
        A2 = ε2 * 1e3 * 1e-5 * np.exp(-0.5 * ((λ - λmax2) / 40) ** 2)
        A_total = A1 + A2

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=λ, y=A1, name='Komponen 1', line=dict(color='#00f5d4', width=2)))
        fig.add_trace(go.Scatter(x=λ, y=A2, name='Komponen 2', line=dict(color='#f7c59f', width=2)))
        fig.add_trace(go.Scatter(x=λ, y=A_total, name='Total', line=dict(color='#b39ddb', width=2.5, dash='dot')))
        fig.update_layout(
            paper_bgcolor='#161b22', plot_bgcolor='#0d1117',
            font=dict(color='#e6edf3'),
            xaxis=dict(title='Panjang Gelombang (nm)', gridcolor='#21262d'),
            yaxis=dict(title='Absorbansi', gridcolor='#21262d'),
            height=380, margin=dict(l=40, r=20, t=30, b=40),
            legend=dict(bgcolor='#161b22', bordercolor='#30363d')
        )
        st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# MODUL: STOIKIOMETRI
# ═══════════════════════════════════════════════════════════
elif menu == "⚗️ Stoikiometri & Mol":
    st.markdown("## ⚗️ Stoikiometri & Kalkulasi Mol")

    tab1, tab2 = st.tabs(["Konversi Mol ↔ Massa ↔ Partikel", "Reaktan Pembatas & Yield"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            bm_stoik = st.number_input("Berat Molekul (g/mol)", 1.0, value=98.08, step=0.01)
            nilai_in  = st.number_input("Nilai Input", 0.0, value=1.0, step=0.001, format="%.6f")
            satuan_in = st.selectbox("Satuan Input", ["gram", "mol", "mmol", "partikel (×10²³)"])
        with c2:
            st.markdown("#### Hasil Konversi")
            if st.button("⚡ Konversi"):
                NA = 6.022e23
                if satuan_in == "gram":
                    mol = nilai_in / bm_stoik
                elif satuan_in == "mol":
                    mol = nilai_in
                elif satuan_in == "mmol":
                    mol = nilai_in / 1000
                else:
                    mol = nilai_in * 1e23 / NA
                gram      = mol * bm_stoik
                partikel  = mol * NA
                st.markdown(f"""
                <div class="result-box"><div class="result-label">MOL</div>
                <div class="result-value">{mol:.6f}<span class="result-unit">mol</span></div></div>
                <div class="result-box"><div class="result-label">MASSA</div>
                <div class="result-value">{gram:.4f}<span class="result-unit">gram</span></div></div>
                <div class="result-box"><div class="result-label">JUMLAH PARTIKEL</div>
                <div class="result-value">{partikel:.3e}<span class="result-unit">partikel</span></div></div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-title">Reaktan Pembatas & % Yield</div>', unsafe_allow_html=True)
        st.caption("Masukkan data dua reaktan dan koefisien reaksi")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Reaktan A**")
            massa_A  = st.number_input("Massa A (g)", 0.1, value=5.0, step=0.1, key="mA")
            BM_A     = st.number_input("BM A (g/mol)", 1.0, value=98.08, step=0.01, key="bmA")
            koef_A   = st.number_input("Koefisien A", 1, value=1, step=1, key="kA")
        with c2:
            st.markdown("**Reaktan B**")
            massa_B  = st.number_input("Massa B (g)", 0.1, value=4.0, step=0.1, key="mB")
            BM_B     = st.number_input("BM B (g/mol)", 1.0, value=40.00, step=0.01, key="bmB")
            koef_B   = st.number_input("Koefisien B", 1, value=2, step=1, key="kB")
        with c3:
            st.markdown("**Produk**")
            BM_P     = st.number_input("BM Produk (g/mol)", 1.0, value=74.09, step=0.01, key="bmP")
            koef_P   = st.number_input("Koefisien Produk", 1, value=1, step=1, key="kP")
            massa_aktual = st.number_input("Massa Aktual Produk (g)", 0.0, value=3.5, step=0.01)

        if st.button("⚡ Hitung Reaktan Pembatas & Yield"):
            mol_A    = massa_A / BM_A
            mol_B    = massa_B / BM_B
            ratio_A  = mol_A / koef_A
            ratio_B  = mol_B / koef_B
            pembatas = "A" if ratio_A < ratio_B else "B"
            mol_produk_teor = min(ratio_A, ratio_B) * koef_P
            massa_teor = mol_produk_teor * BM_P
            pct_yield  = (massa_aktual / massa_teor) * 100 if massa_teor > 0 else 0

            st.markdown(f"""
            <div class="result-box"><div class="result-label">REAKTAN PEMBATAS</div>
            <div class="result-value">Reaktan {pembatas}</div></div>
            <div class="result-box"><div class="result-label">MASSA PRODUK TEORITIS</div>
            <div class="result-value">{massa_teor:.4f}<span class="result-unit">gram</span></div></div>
            <div class="result-box"><div class="result-label">% YIELD</div>
            <div class="result-value">{pct_yield:.2f}<span class="result-unit">%</span></div></div>
            """, unsafe_allow_html=True)

            # Gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pct_yield,
                number={'suffix': '%', 'font': {'color': '#00f5d4', 'size': 36}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#8b949e'},
                    'bar': {'color': '#00f5d4'},
                    'steps': [
                        {'range': [0, 60], 'color': '#21262d'},
                        {'range': [60, 80], 'color': '#2d2020'},
                        {'range': [80, 100], 'color': '#1a2d20'}
                    ],
                    'threshold': {'line': {'color': '#f7c59f', 'width': 3}, 'value': 80}
                }
            ))
            fig.update_layout(
                paper_bgcolor='#161b22', font=dict(color='#e6edf3'),
                height=280, margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# MODUL: BUFFER
# ═══════════════════════════════════════════════════════════
elif menu == "🧫 Larutan Buffer (Henderson)":
    st.markdown("## 🧫 Larutan Buffer — Henderson-Hasselbalch")
    st.latex(r"pH = pK_a + \log\frac{[A^-]}{[HA]}")

    tab1, tab2 = st.tabs(["Kalkulator pH Buffer", "Kapasitas Buffer"])

    with tab1:
        asam_pilih = st.selectbox("Sistem Asam-Basa", [
            "Asam Asetat / Asetat (pKa=4.76)",
            "Asam Fosfat H₂PO₄⁻/HPO₄²⁻ (pKa=7.20)",
            "Karbonat H₂CO₃/HCO₃⁻ (pKa=6.35)",
            "Amonia NH₄⁺/NH₃ (pKa=9.25)",
            "Kustom"
        ])
        pka_dict = {
            "Asam Asetat / Asetat (pKa=4.76)": 4.76,
            "Asam Fosfat H₂PO₄⁻/HPO₄²⁻ (pKa=7.20)": 7.20,
            "Karbonat H₂CO₃/HCO₃⁻ (pKa=6.35)": 6.35,
            "Amonia NH₄⁺/NH₃ (pKa=9.25)": 9.25,
        }
        if asam_pilih == "Kustom":
            pka = st.number_input("pKa Kustom", 0.0, 14.0, 5.0, step=0.01)
        else:
            pka = pka_dict[asam_pilih]

        c1, c2 = st.columns(2)
        with c1:
            c_basa = st.number_input("[A⁻] Basa konjugat (M)", 0.001, value=0.1, step=0.001, format="%.4f")
        with c2:
            c_asam = st.number_input("[HA] Asam (M)", 0.001, value=0.1, step=0.001, format="%.4f")

        if st.button("⚡ Hitung pH Buffer"):
            ph_buf = pka + math.log10(c_basa / c_asam)
            rasio  = c_basa / c_asam
            st.markdown(f"""
            <div class="result-box"><div class="result-label">pH LARUTAN BUFFER</div>
            <div class="result-value">{ph_buf:.3f}</div></div>
            <div class="result-box"><div class="result-label">RASIO [A⁻]/[HA]</div>
            <div class="result-value">{rasio:.4f}</div></div>
            """, unsafe_allow_html=True)

            # Kurva pH vs rasio
            rasio_r = np.linspace(0.01, 100, 500)
            ph_r    = pka + np.log10(rasio_r)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=np.log10(rasio_r), y=ph_r, mode='lines',
                                     line=dict(color='#00f5d4', width=2.5), name='Kurva pH'))
            fig.add_trace(go.Scatter(x=[math.log10(rasio)], y=[ph_buf],
                                     mode='markers',
                                     marker=dict(color='#f7c59f', size=12, symbol='star'),
                                     name='Kondisi Anda'))
            fig.add_hline(y=pka, line_dash="dash", line_color="#7b5ea7",
                          annotation_text=f"pKa={pka}", annotation_font_color="#b39ddb")
            fig.update_layout(
                paper_bgcolor='#161b22', plot_bgcolor='#0d1117',
                font=dict(color='#e6edf3'),
                xaxis=dict(title='log([A⁻]/[HA])', gridcolor='#21262d'),
                yaxis=dict(title='pH', gridcolor='#21262d'),
                height=340, margin=dict(l=40, r=20, t=30, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown('<div class="section-title">Kapasitas Buffer (β)</div>', unsafe_allow_html=True)
        st.latex(r"\beta = 2.303 \cdot C \cdot \frac{K_a [H^+]}{(K_a + [H^+])^2}")
        pka_b = st.number_input("pKa", 0.0, 14.0, 4.76, step=0.01, key="pkab")
        C_tot = st.number_input("Konsentrasi Total Buffer (M)", 0.001, value=0.1, step=0.001, format="%.4f")

        ph_range = np.linspace(pka_b - 3, pka_b + 3, 300)
        Ka  = 10 ** (-pka_b)
        H   = 10 ** (-ph_range)
        beta = 2.303 * C_tot * (Ka * H) / (Ka + H) ** 2

        fig = go.Figure(go.Scatter(x=ph_range, y=beta, mode='lines',
                                   line=dict(color='#7b5ea7', width=2.5)))
        fig.add_vline(x=pka_b, line_dash="dash", line_color="#00f5d4",
                      annotation_text=f"pH = pKa = {pka_b}", annotation_font_color="#00f5d4")
        fig.update_layout(
            paper_bgcolor='#161b22', plot_bgcolor='#0d1117',
            font=dict(color='#e6edf3'),
            xaxis=dict(title='pH', gridcolor='#21262d'),
            yaxis=dict(title='Kapasitas Buffer (β)', gridcolor='#21262d'),
            height=340, margin=dict(l=40, r=20, t=30, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info(f"Kapasitas buffer maksimum pada pH = pKa = **{pka_b}** (β_max = {0.576 * C_tot:.4f})")


# ═══════════════════════════════════════════════════════════
# MODUL: KURVA KALIBRASI
# ═══════════════════════════════════════════════════════════
elif menu == "📊 Kurva Kalibrasi":
    st.markdown("## 📊 Kurva Kalibrasi — Regresi Linier")
    st.markdown("Masukkan data standar (konsentrasi vs sinyal/absorbansi) untuk membangun kurva kalibrasi.")

    st.markdown('<div class="section-title">Data Standar</div>', unsafe_allow_html=True)
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        n_std = st.slider("Jumlah Titik Standar", 3, 10, 6)

    konsentrasi = []
    absorbansi  = []
    cols = st.columns(n_std)
    for i, col in enumerate(cols):
        with col:
            c_val = st.number_input(f"C{i+1} (ppm)", 0.0, value=float((i+1)*2), step=0.1, key=f"c{i}")
            a_val = st.number_input(f"A{i+1}", 0.0, value=round(0.045*(i+1)*2 + 0.002*i, 4),
                                    step=0.001, format="%.4f", key=f"a{i}")
            konsentrasi.append(c_val)
            absorbansi.append(a_val)

    # Unknown
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        A_unknown = st.number_input("Absorbansi Sampel Unknown", 0.0, value=0.25, step=0.001, format="%.4f")
    with c2:
        FP = st.number_input("Faktor Pengenceran Sampel", 1.0, value=1.0, step=0.1)

    if st.button("⚡ Buat Kurva Kalibrasi"):
        x = np.array(konsentrasi)
        y = np.array(absorbansi)
        n = len(x)
        # Regresi linier manual
        x_bar = np.mean(x);  y_bar = np.mean(y)
        Sxy = np.sum((x - x_bar) * (y - y_bar))
        Sxx = np.sum((x - x_bar) ** 2)
        Syy = np.sum((y - y_bar) ** 2)
        b   = Sxy / Sxx
        a   = y_bar - b * x_bar
        R2  = (Sxy ** 2) / (Sxx * Syy)
        R   = math.sqrt(R2)

        # Residuals & std error
        y_pred  = a + b * x
        resid   = y - y_pred
        sy      = math.sqrt(np.sum(resid**2) / (n - 2))
        # LOD & LOQ
        LOD = (3.3 * sy) / b
        LOQ = (10  * sy) / b
        # Unknown conc
        c_unk = ((A_unknown - a) / b) * FP

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class="result-box"><div class="result-label">SLOPE (b)</div>
            <div class="result-value">{b:.5f}</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="result-box"><div class="result-label">INTERCEPT (a)</div>
            <div class="result-value">{a:.5f}</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="result-box"><div class="result-label">R²</div>
            <div class="result-value">{R2:.6f}</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="result-box"><div class="result-label">R</div>
            <div class="result-value">{R:.6f}</div></div>""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""<div class="result-box"><div class="result-label">LOD</div>
            <div class="result-value">{LOD:.4f}<span class="result-unit">ppm</span></div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="result-box"><div class="result-label">LOQ</div>
            <div class="result-value">{LOQ:.4f}<span class="result-unit">ppm</span></div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="result-box"><div class="result-label">KONSENTRASI UNKNOWN</div>
            <div class="result-value">{c_unk:.4f}<span class="result-unit">ppm</span></div></div>""", unsafe_allow_html=True)

        # Plot
        x_line = np.linspace(0, max(x)*1.1, 200)
        y_line = a + b * x_line

        fig = make_subplots(rows=1, cols=2,
                            subplot_titles=["Kurva Kalibrasi", "Plot Residual"])
        fig.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines',
                                 line=dict(color='#00f5d4', width=2.5), name='Regresi'), row=1, col=1)
        fig.add_trace(go.Scatter(x=x, y=y, mode='markers',
                                 marker=dict(color='#f7c59f', size=10), name='Standar'), row=1, col=1)
        fig.add_trace(go.Scatter(x=[c_unk/FP], y=[A_unknown], mode='markers',
                                 marker=dict(color='#ff6b6b', size=14, symbol='star'),
                                 name='Unknown'), row=1, col=1)
        # Residual
        fig.add_trace(go.Bar(x=list(range(1, n+1)), y=resid,
                             marker_color=['#00f5d4' if r >= 0 else '#f7c59f' for r in resid],
                             name='Residual'), row=1, col=2)
        fig.add_hline(y=0, line_dash="dot", line_color="#8b949e", row=1, col=2)

        fig.update_layout(
            paper_bgcolor='#161b22', plot_bgcolor='#0d1117',
            font=dict(color='#e6edf3'),
            height=420, margin=dict(l=40, r=20, t=50, b=40),
            showlegend=True,
            legend=dict(bgcolor='#161b22', bordercolor='#30363d')
        )
        for ax in ['xaxis', 'xaxis2', 'yaxis', 'yaxis2']:
            fig.update_layout(**{ax: dict(gridcolor='#21262d')})
        fig.update_xaxes(title_text="Konsentrasi (ppm)", row=1, col=1)
        fig.update_yaxes(title_text="Absorbansi", row=1, col=1)
        fig.update_xaxes(title_text="Titik Standar ke-", row=1, col=2)
        fig.update_yaxes(title_text="Residual", row=1, col=2)

        st.plotly_chart(fig, use_container_width=True)

        r2_grade = "✅ Sangat Baik" if R2 >= 0.9999 else "✅ Baik" if R2 >= 0.999 else "⚠️ Cukup" if R2 >= 0.99 else "❌ Buruk"
        st.info(f"**Persamaan:** A = {b:.5f}·C + {a:.5f} | **Linearitas:** {r2_grade} (R² = {R2:.6f})")


# ═══════════════════════════════════════════════════════════
# MODUL: KONVERSI & UTILITAS
# ═══════════════════════════════════════════════════════════
elif menu == "🔁 Konversi & Utilitas Kimia":
    st.markdown("## 🔁 Konversi & Utilitas Kimia")

    tab1, tab2, tab3 = st.tabs(["Satuan Konsentrasi", "Suhu & Tekanan", "Referensi Berat Molekul"])

    with tab1:
        st.markdown('<div class="section-title">Konversi Satuan Konsentrasi</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            nilai_konv = st.number_input("Nilai", 0.0, value=1.0, step=0.0001, format="%.6f")
            satuan_dari = st.selectbox("Dari", ["mol/L (M)", "mmol/L (mM)", "µmol/L (µM)", "g/L", "mg/L (ppm)", "µg/L (ppb)", "%b/v"])
            BM_konv = st.number_input("Berat Molekul (g/mol)", 1.0, value=180.16, step=0.01)
        with c2:
            satuan_ke = st.selectbox("Ke", ["mol/L (M)", "mmol/L (mM)", "µmol/L (µM)", "g/L", "mg/L (ppm)", "µg/L (ppb)", "%b/v"])

        if st.button("⚡ Konversi Konsentrasi"):
            # semua ke mol/L terlebih dahulu
            to_M = {
                "mol/L (M)": 1, "mmol/L (mM)": 1e-3, "µmol/L (µM)": 1e-6,
                "g/L": 1/BM_konv, "mg/L (ppm)": 1e-3/BM_konv,
                "µg/L (ppb)": 1e-6/BM_konv, "%b/v": 10/BM_konv
            }
            from_M = {
                "mol/L (M)": 1, "mmol/L (mM)": 1e3, "µmol/L (µM)": 1e6,
                "g/L": BM_konv, "mg/L (ppm)": BM_konv*1e3,
                "µg/L (ppb)": BM_konv*1e6, "%b/v": BM_konv/10
            }
            val_M  = nilai_konv * to_M[satuan_dari]
            result = val_M * from_M[satuan_ke]
            st.markdown(f"""
            <div class="result-box">
              <div class="result-label">{nilai_konv} {satuan_dari} =</div>
              <div class="result-value">{result:.6g}<span class="result-unit">{satuan_ke}</span></div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-title">Konversi Suhu & Tekanan</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Suhu**")
            t_in  = st.number_input("Nilai Suhu", value=25.0, step=0.1)
            t_dari = st.selectbox("Dari Satuan", ["°C", "°F", "K"])
            if st.button("⚡ Konversi Suhu"):
                if t_dari == "°C":
                    tC, tF, tK = t_in, t_in * 9/5 + 32, t_in + 273.15
                elif t_dari == "°F":
                    tC = (t_in - 32) * 5/9; tK = tC + 273.15; tF = t_in
                else:
                    tC = t_in - 273.15; tF = tC*9/5+32; tK = t_in
                st.markdown(f"""
                <div class="result-box">
                  <div class="result-label">HASIL</div>
                  <div class="result-value">{tC:.2f} °C &nbsp;|&nbsp; {tF:.2f} °F &nbsp;|&nbsp; {tK:.2f} K</div>
                </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("**Tekanan**")
            p_in   = st.number_input("Nilai Tekanan", value=1.0, step=0.001, format="%.4f")
            p_dari = st.selectbox("Dari Satuan", ["atm", "Pa", "kPa", "bar", "mmHg", "psi"])
            if st.button("⚡ Konversi Tekanan"):
                to_Pa = {"atm": 101325, "Pa": 1, "kPa": 1000, "bar": 100000, "mmHg": 133.322, "psi": 6894.76}
                pa = p_in * to_Pa[p_dari]
                st.markdown(f"""
                <div class="result-box">
                  <div class="result-label">TEKANAN DALAM BERBAGAI SATUAN</div>
                  <div class="result-value" style="font-size:1rem">
                    {pa/101325:.5f} atm &nbsp;|&nbsp; {pa:.2f} Pa &nbsp;|&nbsp;
                    {pa/1000:.4f} kPa &nbsp;|&nbsp; {pa/100000:.6f} bar<br>
                    {pa/133.322:.4f} mmHg &nbsp;|&nbsp; {pa/6894.76:.5f} psi
                  </div>
                </div>""", unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="section-title">Referensi Berat Molekul Senyawa Umum</div>', unsafe_allow_html=True)
        data_bm = {
            "Air (H₂O)": 18.02, "NaCl": 58.44, "HCl": 36.46, "NaOH": 40.00,
            "H₂SO₄": 98.08, "HNO₃": 63.01, "KMnO₄": 158.03, "Na₂S₂O₃·5H₂O": 248.19,
            "EDTA (dinatrium)": 372.24, "Asam Asetat": 60.05, "Glukosa": 180.16,
            "Asam Askorbat (Vit C)": 176.12, "CaCO₃": 100.09, "K₂Cr₂O₇": 294.19,
            "KIO₃": 214.00, "Na₂CO₃": 105.99, "Asam Salisilat": 138.12,
            "Kafein": 194.19, "Parasetamol": 151.16, "Aspirin": 180.16,
        }
        col_a, col_b = st.columns(2)
        items = list(data_bm.items())
        for i, (nama, bm) in enumerate(items):
            col = col_a if i % 2 == 0 else col_b
            with col:
                st.markdown(f"""
                <div style="background:#161b22;border:1px solid #30363d;border-radius:8px;
                            padding:0.5rem 0.8rem;margin:0.2rem 0;display:flex;
                            justify-content:space-between;align-items:center;">
                  <span style="color:#e6edf3;font-size:0.85rem">{nama}</span>
                  <span style="color:#00f5d4;font-family:'Space Mono',monospace;font-size:0.9rem;font-weight:700">{bm}</span>
                </div>
                """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#30363d;font-size:0.75rem;font-family:'Space Mono',monospace;padding:0.5rem">
  ⚗️ ChemAnalytica · Politeknik AKA Bogor · Tugas LPK Kimia Analitik · 2026
</div>
""", unsafe_allow_html=True)
