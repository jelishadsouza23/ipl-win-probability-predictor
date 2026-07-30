import streamlit as st
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(
    page_title="FLAREBOARD - SaaS Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom Neubrutalism styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Public+Sans:wght@500;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Public Sans', sans-serif;
        background-color: #fdf9f0;
        color: #111111;
    }

    /* Main background grid */
    .stApp {
        background-color: #fdf9f0;
        background-image: radial-gradient(#111111 0.75px, transparent 0.75px);
        background-size: 24px 24px;
    }

    /* Base Neubrutalism Card Styling */
    .neu-card {
        background-color: #ffffff;
        border: 2px solid #111111;
        box-shadow: 4px 4px 0px #111111;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Primary Accent Pink Buttons/Pills */
    .neu-pill-pink {
        background-color: #ff3366;
        color: #ffffff !important;
        border: 2px solid #111111;
        box-shadow: 3px 3px 0px #111111;
        font-weight: 800;
        padding: 8px 16px;
        border-radius: 6px;
        display: inline-block;
    }

    /* Badges */
    .delta-mint {
        background-color: #a3e635;
        color: #111111;
        border: 1.5px solid #111111;
        box-shadow: 2px 2px 0px #111111;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.85rem;
    }

    .delta-coral {
        background-color: #fb7185;
        color: #111111;
        border: 1.5px solid #111111;
        box-shadow: 2px 2px 0px #111111;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.85rem;
    }

    /* Icon Tile Styling */
    .icon-tile {
        width: 42px;
        height: 42px;
        border: 2px solid #111111;
        box-shadow: 2px 2px 0px #111111;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.2rem;
    }

    .tile-yellow { background-color: #fde047; }
    .tile-blue { background-color: #38bdf8; }
    .tile-purple { background-color: #c084fc; }
    .tile-orange { background-color: #fb923c; }

    /* Custom Header Typography */
    .brand-title {
        font-family: 'Archivo Black', sans-serif;
        font-size: 1.8rem;
        letter-spacing: -0.5px;
        margin: 0;
    }

    .header-title {
        font-family: 'Archivo Black', sans-serif;
        font-size: 2.2rem;
        margin-bottom: 0px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    # Logo Header
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
            <div class="icon-tile tile-yellow" style="background-color: #ff3366; color: white;">⚡</div>
            <span class="brand-title">FLAREBOARD</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation Pills
    st.markdown('<div class="neu-pill-pink" style="width: 100%; text-align: center; margin-bottom: 12px;">📊 Overview</div>', unsafe_allow_html=True)
    
    st.button("📈 Analytics", use_container_width=True)
    st.button("👥 Audience", use_container_width=True)
    st.button("💵 Revenue", use_container_width=True)
    st.button("📝 Content", use_container_width=True)
    st.button("⚙️ Settings", use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Workspace Card
    st.markdown("""
        <div class="neu-card" style="background: #fef08a;">
            <div style="font-weight: 800; font-size: 0.9rem;">PRO WORKSPACE</div>
            <div style="font-size: 0.8rem; margin-top: 4px;">Acme Inc. Dashboard</div>
        </div>
    """, unsafe_allow_html=True)

# --- TOP BAR ---
top_left, top_right = st.columns([2, 2])

with top_left:
    st.markdown('<div class="header-title">Overview</div>', unsafe_allow_html=True)
    st.caption("Welcome back! Here is what is happening with your product today.")

with top_right:
    r_col1, r_col2, r_col3 = st.columns([2, 2, 1])
    with r_col1:
        st.text_input("Search", placeholder="🔍 Search...", label_visibility="collapsed")
    with r_col2:
        st.selectbox("Date Range", ["Last 30 days", "Last 7 days", "This Year"], label_visibility="collapsed")
    with r_col3:
        st.markdown('<div class="neu-pill-pink" style="padding: 6px 12px; font-size: 0.85rem;">Export</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- KPI CARDS ROW ---
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown("""
        <div class="neu-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div class="icon-tile tile-yellow">💰</div>
                <span class="delta-mint">+12.4%</span>
            </div>
            <div style="font-size: 0.85rem; color: #555; margin-top: 12px; font-weight: 700;">TOTAL REVENUE</div>
            <div style="font-size: 1.8rem; font-family: 'Archivo Black';">$48.2k</div>
        </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown("""
        <div class="neu-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div class="icon-tile tile-blue">👥</div>
                <span class="delta-mint">+8.1%</span>
            </div>
            <div style="font-size: 0.85rem; color: #555; margin-top: 12px; font-weight: 700;">ACTIVE USERS</div>
            <div style="font-size: 1.8rem; font-family: 'Archivo Black';">12,940</div>
        </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown("""
        <div class="neu-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div class="icon-tile tile-purple">🎯</div>
                <span class="delta-coral">-2.1%</span>
            </div>
            <div style="font-size: 0.85rem; color: #555; margin-top: 12px; font-weight: 700;">CONVERSION RATE</div>
            <div style="font-size: 1.8rem; font-family: 'Archivo Black';">3.8%</div>
        </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown("""
        <div class="neu-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div class="icon-tile tile-orange">⚡</div>
                <span class="delta-mint">+15.6%</span>
            </div>
            <div style="font-size: 0.85rem; color: #555; margin-top: 12px; font-weight: 700;">NEW SIGNUPS</div>
            <div style="font-size: 1.8rem; font-family: 'Archivo Black';">6,214</div>
        </div>
    """, unsafe_allow_html=True)

# --- MAIN CONTENT SECTION ---
main_chart_col, side_info_col = st.columns([2, 1])

with main_chart_col:
    st.markdown("""
        <div class="neu-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <span style="font-family: 'Archivo Black'; font-size: 1.2rem;">Revenue over time</span>
                <div>
                    <span style="color: #ff3366; font-weight: 800; font-size: 0.85rem;">■ This Year</span>
                    <span style="color: #c084fc; font-weight: 800; font-size: 0.85rem; margin-left: 12px;">■ Last Year</span>
                </div>
            </div>
            <svg viewBox="0 0 600 220" style="width: 100%; height: auto;">
                <!-- Grid Lines -->
                <line x1="40" y1="30" x2="580" y2="30" stroke="#111111" stroke-width="1" stroke-dasharray="4" opacity="0.2" />
                <line x1="40" y1="80" x2="580" y2="80" stroke="#111111" stroke-width="1" stroke-dasharray="4" opacity="0.2" />
                <line x1="40" y1="130" x2="580" y2="130" stroke="#111111" stroke-width="1" stroke-dasharray="4" opacity="0.2" />
                <line x1="40" y1="180" x2="580" y2="180" stroke="#111111" stroke-width="2" />
                
                <!-- Y-Axis Labels -->
                <text x="5" y="35" font-size="10" font-weight="700">$50k</text>
                <text x="5" y="85" font-size="10" font-weight="700">$30k</text>
                <text x="5" y="135" font-size="10" font-weight="700">$10k</text>
                <text x="20" y="185" font-size="10" font-weight="700">$0k</text>
                
                <!-- SVG Bars (Sample Grouped Bar Chart) -->
                <!-- Jan -->
                <rect x="55" y="100" width="12" height="80" fill="#ff3366" stroke="#111" stroke-width="1.5" />
                <rect x="70" y="120" width="8" height="60" fill="#c084fc" stroke="#111" stroke-width="1.5" />
                <text x="58" y="200" font-size="10" font-weight="700">Jan</text>

                <!-- Feb -->
                <rect x="100" y="80" width="12" height="100" fill="#ff3366" stroke="#111" stroke-width="1.5" />
                <rect x="115" y="110" width="8" height="70" fill="#c084fc" stroke="#111" stroke-width="1.5" />
                <text x="103" y="200" font-size="10" font-weight="700">Feb</text>

                <!-- Mar -->
                <rect x="145" y="60" width="12" height="120" fill="#ff3366" stroke="#111" stroke-width="1.5" />
                <rect x="160" y="90" width="8" height="90" fill="#c084fc" stroke="#111" stroke-width="1.5" />
                <text x="147" y="200" font-size="10" font-weight="700">Mar</text>

                <!-- Apr -->
                <rect x="190" y="90" width="12" height="90" fill="#ff3366" stroke="#111" stroke-width="1.5" />
                <rect x="205" y="130" width="8" height="50" fill="#c084fc" stroke="#111" stroke-width="1.5" />
                <text x="192" y="200" font-size="10" font-weight="700">Apr</text>

                <!-- May -->
                <rect x="235" y="50" width="12" height="130" fill="#ff3366" stroke="#111" stroke-width="1.5" />
                <rect x="250" y="85" width="8" height="95" fill="#c084fc" stroke="#111" stroke-width="1.5" />
                <text x="237" y="200" font-size="10" font-weight="700">May</text>

                <!-- Jun -->
                <rect x="280" y="40" width="12" height="140" fill="#ff3366" stroke="#111" stroke-width="1.5" />
                <rect x="295" y="70" width="8" height="110" fill="#c084fc" stroke="#111" stroke-width="1.5" />
                <text x="282" y="200" font-size="10" font-weight="700">Jun</text>

                <!-- Jul-Dec repeated pattern for complete SVG layout -->
                <rect x="325" y="65" width="12" height="115" fill="#ff3366" stroke="#111" stroke-width="1.5" />
                <rect x="340" y="100" width="8" height="80" fill="#c084fc" stroke="#111" stroke-width="1.5" />
                <text x="329" y="200" font-size="10" font-weight="700">Jul</text>

                <rect x="370" y="45" width="12" height="135" fill="#ff3366" stroke="#111" stroke-width="1.5" />
                <rect x="385" y="80" width="8" height="100" fill="#c084fc" stroke="#111" stroke-width="1.5" />
                <text x="372" y="200" font-size="10" font-weight="700">Aug</text>

                <rect x="415" y="35" width="12" height="145" fill="#ff3366" stroke="#111" stroke-width="1.5" />
                <rect x="430" y="75" width="8" height="105" fill="#c084fc" stroke="#111" stroke-width="1.5" />
                <text x="419" y="200" font-size="10" font-weight="700">Sep</text>

                <rect x="460" y="50" width="12" height="130" fill="#ff3366" stroke="#111" stroke-width="1.5" />
                <rect x="475" y="90" width="8" height="90" fill="#c084fc" stroke="#111" stroke-width="1.5" />
                <text x="464" y="200" font-size="10" font-weight="700">Oct</text>

                <rect x="505" y="30" width="12" height="150" fill="#ff3366" stroke="#111" stroke-width="1.5" />
                <rect x="520" y="65" width="8" height="115" fill="#c084fc" stroke="#111" stroke-width="1.5" />
                <text x="508" y="200" font-size="10" font-weight="700">Nov</text>

                <rect x="550" y="20" width="12" height="160" fill="#ff3366" stroke="#111" stroke-width="1.5" />
                <rect x="565" y="55" width="8" height="125" fill="#c084fc" stroke="#111" stroke-width="1.5" />
                <text x="553" y="200" font-size="10" font-weight="700">Dec</text>
            </svg>
        </div>
    """, unsafe_allow_html=True)

with side_info_col:
    # Traffic Sources Donut Card
    st.markdown("""
        <div class="neu-card">
            <span style="font-family: 'Archivo Black'; font-size: 1.1rem;">Traffic Sources</span>
            <div style="position: relative; width: 140px; height: 140px; margin: 16px auto;">
                <svg viewBox="0 0 36 36" style="transform: rotate(-90deg); width: 100%; height: 100%;">
                    <circle cx="18" cy="18" r="15.915" fill="none" stroke="#ff3366" stroke-width="4" stroke-dasharray="42 58" stroke-dashoffset="0" />
                    <circle cx="18" cy="18" r="15.915" fill="none" stroke="#38bdf8" stroke-width="4" stroke-dasharray="28 72" stroke-dashoffset="-42" />
                    <circle cx="18" cy="18" r="15.915" fill="none" stroke="#fde047" stroke-width="4" stroke-dasharray="18 82" stroke-dashoffset="-70" />
                    <circle cx="18" cy="18" r="15.915" fill="none" stroke="#c084fc" stroke-width="4" stroke-dasharray="12 88" stroke-dashoffset="-88" />
                </svg>
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                    <span style="font-family: 'Archivo Black'; font-size: 0.9rem;">12.9k</span>
                    <span style="font-size: 0.65rem; font-weight: 700; color: #666;">SESSIONS</span>
                </div>
            </div>
            <div style="font-size: 0.8rem; font-weight: 700; line-height: 1.8;">
                <div><span style="color: #ff3366;">■</span> Direct: 42%</div>
                <div><span style="color: #38bdf8;">■</span> Search: 28%</div>
                <div><span style="color: #fde047;">■</span> Social: 18%</div>
                <div><span style="color: #c084fc;">■</span> Referral: 12%</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Top Content Card
    st.markdown("""
        <div class="neu-card">
            <span style="font-family: 'Archivo Black'; font-size: 1.1rem;">Top Content</span>
            <div style="margin-top: 12px; font-size: 0.85rem; font-weight: 700;">
                <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1.5px stroke #111;">
                    <span>/blog/neubrutalism-design</span>
                    <span>4.2k</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1.5px stroke #111;">
                    <span>/docs/api-getting-started</span>
                    <span>2.8k</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 6px 0;">
                    <span>/pricing-plans-2026</span>
                    <span>1.9k</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
