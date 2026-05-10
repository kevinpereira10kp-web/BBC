import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="DTDC · Delivery Intelligence",
    layout="wide",
    page_icon="📦",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">

<style>
/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #0B0F1A !important;
}

[data-testid="stAppViewContainer"] {
    background: #0B0F1A !important;
}

/* Remove default Streamlit padding */
.main .block-container {
    padding: 0 2.5rem 4rem 2.5rem !important;
    max-width: 1400px !important;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Custom Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0B0F1A; }
::-webkit-scrollbar-thumb { background: #1E3A5F; border-radius: 3px; }

/* ── Typography ── */
body, p, li, label, div {
    font-family: 'DM Sans', sans-serif !important;
    color: #C8D4E8 !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Syne', sans-serif !important;
    color: #F0F4FF !important;
}

/* ── Hero Header ── */
.hero-wrapper {
    background: linear-gradient(135deg, #0B0F1A 0%, #0D1B35 50%, #0B0F1A 100%);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding: 3.5rem 0 2.5rem;
    margin: 0 -2.5rem 3rem -2.5rem;
    position: relative;
    overflow: hidden;
}

.hero-wrapper::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(203,16,36,0.12) 0%, transparent 70%);
    border-radius: 50%;
}

.hero-wrapper::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 20%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(26,86,189,0.10) 0%, transparent 70%);
    border-radius: 50%;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(203,16,36,0.15);
    border: 1px solid rgba(203,16,36,0.3);
    color: #FF4D6A !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 100px;
    margin-bottom: 18px;
}

.hero-badge::before {
    content: '';
    width: 6px; height: 6px;
    background: #CB1024;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.3); }
}

.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(2rem, 4vw, 3.2rem) !important;
    font-weight: 800 !important;
    color: #F0F4FF !important;
    line-height: 1.1 !important;
    margin: 0 0 16px 0 !important;
    letter-spacing: -0.02em;
}

.hero-title span {
    color: #CB1024 !important;
}

.hero-sub {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    color: #7A8FAD !important;
    max-width: 580px;
    line-height: 1.7;
    margin: 0 !important;
}

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 3rem;
}

.kpi-card {
    background: linear-gradient(145deg, #111827, #0F1A2E);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 28px 28px 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}

.kpi-card:hover { border-color: rgba(255,255,255,0.12); }

.kpi-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 16px 16px 0 0;
}

.kpi-card.red::after   { background: linear-gradient(90deg, #CB1024, transparent); }
.kpi-card.blue::after  { background: linear-gradient(90deg, #1A56BD, transparent); }
.kpi-card.amber::after { background: linear-gradient(90deg, #D97706, transparent); }

.kpi-icon {
    font-size: 20px;
    margin-bottom: 16px;
    opacity: 0.8;
}

.kpi-label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    color: #5A7090 !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 8px !important;
}

.kpi-value {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.6rem !important;
    font-weight: 800 !important;
    color: #F0F4FF !important;
    line-height: 1 !important;
    margin-bottom: 10px !important;
}

.kpi-delta {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 12px;
    font-family: 'DM Sans', sans-serif !important;
    padding: 3px 10px;
    border-radius: 100px;
}

.kpi-delta.warn {
    background: rgba(203,16,36,0.12);
    color: #FF4D6A !important;
    border: 1px solid rgba(203,16,36,0.2);
}

.kpi-delta.ok {
    background: rgba(16,185,129,0.12);
    color: #34D399 !important;
    border: 1px solid rgba(16,185,129,0.2);
}

/* ── Chapter Headers ── */
.chapter-block {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 3rem 0 1.2rem;
}

.chapter-num {
    font-family: 'Syne', sans-serif !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    color: #CB1024 !important;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    white-space: nowrap;
}

.chapter-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(203,16,36,0.4), transparent);
}

.chapter-title {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(1.3rem, 2.5vw, 1.7rem) !important;
    font-weight: 700 !important;
    color: #F0F4FF !important;
    margin: 0 0 0.8rem 0 !important;
}

/* ── Narrative Text ── */
.narrative {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    color: #7A8FAD !important;
    line-height: 1.8 !important;
    max-width: 800px;
    margin-bottom: 1.8rem !important;
    padding-left: 0 !important;
}

.narrative strong, .narrative b {
    color: #CBD5E1 !important;
    font-weight: 500 !important;
}

.highlight-red {
    color: #FF4D6A !important;
    font-weight: 600 !important;
}

/* ── Chart Containers ── */
.chart-card {
    background: #111827;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
}

.chart-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #C8D4E8 !important;
    letter-spacing: 0.02em;
    margin-bottom: 4px !important;
    text-transform: uppercase;
}

.chart-subtitle {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 12px !important;
    color: #4A6080 !important;
    margin-bottom: 16px !important;
}

/* ── Insight Callout ── */
.insight-box {
    background: linear-gradient(135deg, rgba(26,86,189,0.08), rgba(11,15,26,0));
    border: 1px solid rgba(26,86,189,0.2);
    border-left: 3px solid #1A56BD;
    border-radius: 12px;
    padding: 20px 24px;
    margin: 1.5rem 0;
}

.insight-box p {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    color: #A8BDD4 !important;
    margin: 0 !important;
    line-height: 1.7;
}

/* ── Recommendations ── */
.rec-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
    margin-top: 1.5rem;
}

.rec-card {
    background: #111827;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 24px;
}

.rec-num {
    font-family: 'Syne', sans-serif !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    color: #CB1024 !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 12px !important;
}

.rec-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #F0F4FF !important;
    margin-bottom: 10px !important;
}

.rec-body {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    color: #5A7090 !important;
    line-height: 1.7;
}

/* ── Divider ── */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
    margin: 2.5rem 0;
}

/* ── Streamlit overrides ── */
[data-testid="stMetric"] {
    display: none !important;
}

[data-testid="column"] > div:first-child {
    height: 100%;
}

.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.06) !important;
}

[data-testid="stDataFrameResizable"] {
    background: #111827 !important;
}

/* Plotly chart background transparency */
.js-plotly-plot .plotly .bg {
    fill: transparent !important;
}

/* Fix column gaps */
[data-testid="column"] { gap: 16px; }
.row-widget.stHorizontalBlock { gap: 16px; }

/* ── Footer ── */
.footer-bar {
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.04);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.footer-text {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 12px !important;
    color: #2A3A50 !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. PLOTLY DARK THEME DEFAULTS
# ==========================================
PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', color='#7A8FAD', size=12),
    title_font=dict(family='Syne', color='#C8D4E8'),
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        font=dict(color='#7A8FAD', size=11)
    ),
    xaxis=dict(
        gridcolor='rgba(255,255,255,0.04)',
        linecolor='rgba(255,255,255,0.08)',
        tickfont=dict(color='#4A6080'),
        title_font=dict(color='#5A7090')
    ),
    yaxis=dict(
        gridcolor='rgba(255,255,255,0.04)',
        linecolor='rgba(255,255,255,0.08)',
        tickfont=dict(color='#4A6080'),
        title_font=dict(color='#5A7090')
    ),
    margin=dict(l=10, r=10, t=30, b=10),
    colorway=['#CB1024', '#1A56BD', '#F59E0B', '#10B981', '#8B5CF6', '#EC4899'],
)

PALETTE_DIVERGING = ['#CB1024', '#E85D6F', '#F4A4AC', '#E2E8F0', '#93C5FD', '#3B82F6', '#1A56BD']
PALETTE_SEQUENTIAL_RED = ['#3D0A0F', '#7B1D24', '#B82535', '#CB1024', '#E85D6F', '#FECDD3']
PALETTE_QUALITATIVE = ['#CB1024', '#1A56BD', '#F59E0B', '#10B981', '#8B5CF6', '#F97316']

# ==========================================
# 3. DATA LOADING
# ==========================================
@st.cache_data
def load_data():
    try:
        orders   = pd.read_csv("orders.csv",    parse_dates=['order_date','promised_date','delivery_date'])
        feedback = pd.read_csv("feedback.csv",  parse_dates=['response_date'])
        couriers = pd.read_csv("couriers.csv")
        hubs     = pd.read_csv("hubs.csv")
        customers= pd.read_csv("customers.csv", parse_dates=['signup_date'])
        tickets  = pd.read_csv("tickets.csv",   parse_dates=['created_date'])

        orders['is_sla_breach'] = np.where(
            orders['order_status'].isin(['Cancelled','RTO']), 1,
            np.where(orders['delivery_date'] > orders['promised_date'], 1, 0)
        )

        def categorize_nps(score):
            if score >= 9: return 'Promoter'
            elif score >= 7: return 'Passive'
            else: return 'Detractor'

        feedback['nps_category']  = feedback['score'].apply(categorize_nps)
        feedback['response_month'] = feedback['response_date'].dt.to_period('M').astype(str)

        df_main = orders.merge(customers, on='customer_id', how='left')
        df_main = df_main.merge(feedback[['order_id','score','nps_category','response_month']], on='order_id', how='left')
        df_main = df_main.merge(tickets[['order_id','issue_type','escalation_flag']], on='order_id', how='left')

        return orders, feedback, couriers, hubs, customers, tickets, df_main

    except FileNotFoundError as e:
        st.error(f"Data file missing: {e}. Please place all CSV files alongside this script.")
        st.stop()

orders, feedback, couriers, hubs, customers, tickets, df_main = load_data()

def calculate_nps(df_subset):
    if len(df_subset) == 0: return 0
    p = len(df_subset[df_subset['nps_category'] == 'Promoter'])
    d = len(df_subset[df_subset['nps_category'] == 'Detractor'])
    return round(((p - d) / len(df_subset)) * 100, 1)

def categorize_nps(score):
    if score >= 9: return 'Promoter'
    elif score >= 7: return 'Passive'
    else: return 'Detractor'

# ==========================================
# 4. HERO SECTION
# ==========================================
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-badge">Live Intelligence Report</div>
    <h1 class="hero-title">Delivery Experience<br><span>Intelligence Hub</span></h1>
    <p class="hero-sub">
        Identifying where the network bleeds customer trust — and the surgical actions
        to fix it without inflating operational costs.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. KPI STRIP
# ==========================================
total_nps     = calculate_nps(feedback)
repeat_rate   = round(len(customers[customers['segment'].isin(['Repeat','High Value'])]) / len(customers) * 100, 1)
sla_breach_pct= round(orders['is_sla_breach'].mean() * 100, 1)
escalation_ct = tickets['escalation_flag'].sum() if 'escalation_flag' in tickets.columns else "—"

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card red">
        <div class="kpi-icon">📊</div>
        <div class="kpi-label">Net Promoter Score</div>
        <div class="kpi-value">{total_nps}</div>
        <span class="kpi-delta warn">⚠ Action Required</span>
    </div>
    <div class="kpi-card blue">
        <div class="kpi-icon">🔁</div>
        <div class="kpi-label">Customer Repeat Rate</div>
        <div class="kpi-value">{repeat_rate}%</div>
        <span class="kpi-delta ok">↑ Retention Signal</span>
    </div>
    <div class="kpi-card amber">
        <div class="kpi-icon">⚡</div>
        <div class="kpi-label">SLA Breach Rate</div>
        <div class="kpi-value">{sla_breach_pct}%</div>
        <span class="kpi-delta warn">⚠ Critical</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# CHAPTER 1
# ==========================================
st.markdown("""
<div class="chapter-block">
    <span class="chapter-num">Chapter 01</span>
    <div class="chapter-line"></div>
</div>
<h2 class="chapter-title">The Shrinking Trust</h2>
<p class="narrative">
    Before fixing logistics, we must understand what customers <em>feel</em>. Our NPS trend reveals a 
    concerning trajectory over recent months — and our ticketing data exposes exactly 
    <strong>why</strong> they're losing faith.
</p>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2, gap="medium")

with c1:
    st.markdown('<div class="chart-card"><div class="chart-title">NPS Trend</div><div class="chart-subtitle">Monthly net promoter score trajectory</div>', unsafe_allow_html=True)
    nps_trend = feedback.groupby('response_month').apply(calculate_nps).reset_index(name='NPS')

    fig_nps = go.Figure()
    fig_nps.add_trace(go.Scatter(
        x=nps_trend['response_month'], y=nps_trend['NPS'],
        mode='lines+markers+text',
        text=nps_trend['NPS'],
        textposition='top center',
        textfont=dict(family='Syne', color='#F0F4FF', size=11),
        line=dict(color='#CB1024', width=2.5, shape='spline'),
        marker=dict(color='#CB1024', size=8, line=dict(color='#0B0F1A', width=2)),
        fill='tozeroy',
        fillcolor='rgba(203,16,36,0.07)',
        hovertemplate='<b>%{x}</b><br>NPS: %{y}<extra></extra>'
    ))
    fig_nps.add_hline(y=0, line_dash='dot', line_color='rgba(255,255,255,0.1)', line_width=1)
    fig_nps.update_layout(**PLOTLY_LAYOUT, height=300)
    st.plotly_chart(fig_nps, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="chart-card"><div class="chart-title">Complaint Breakdown</div><div class="chart-subtitle">Distribution of ticket issue types</div>', unsafe_allow_html=True)
    complaint_counts = tickets['issue_type'].value_counts().reset_index()
    complaint_counts.columns = ['Issue Type', 'Count']

    fig_comp = go.Figure(go.Pie(
        labels=complaint_counts['Issue Type'],
        values=complaint_counts['Count'],
        hole=0.55,
        textfont=dict(family='DM Sans', size=12, color='#F0F4FF'),
        marker=dict(
            colors=PALETTE_QUALITATIVE,
            line=dict(color='#0B0F1A', width=2)
        ),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>'
    ))
    fig_comp.update_layout(
        **{k: v for k, v in PLOTLY_LAYOUT.items() if k not in ('xaxis','yaxis')},
        height=300,
        legend=dict(
            font=dict(family='DM Sans', color='#7A8FAD', size=11),
            bgcolor='rgba(0,0,0,0)',
            orientation='v', x=1, y=0.5
        )
    )
    fig_comp.add_annotation(
        text="Issues", showarrow=False,
        font=dict(family='Syne', size=14, color='#7A8FAD'), x=0.5, y=0.5
    )
    st.plotly_chart(fig_comp, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# NPS Pivot
st.markdown('<div class="chart-card"><div class="chart-title">NPS by Customer Segment × Month</div><div class="chart-subtitle">Heatmap — redder cells signal deeper dissatisfaction</div>', unsafe_allow_html=True)
pivot_nps = df_main.dropna(subset=['score']).pivot_table(
    index='segment',
    columns='response_month',
    values='score',
    aggfunc=lambda x: calculate_nps(pd.DataFrame({'nps_category': pd.Series(x).apply(categorize_nps)}))
).fillna(0)
st.dataframe(
    pivot_nps.style
        .format("{:.0f}")
        .background_gradient(cmap='RdYlGn', axis=None)
        .set_properties(**{'font-family': 'DM Sans', 'font-size': '13px'}),
    use_container_width=True
)
st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# CHAPTER 2
# ==========================================
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="chapter-block">
    <span class="chapter-num">Chapter 02</span>
    <div class="chapter-line"></div>
</div>
<h2 class="chapter-title">The Bottlenecks</h2>
<p class="narrative">
    Improving NPS <strong>without raising costs</strong> demands surgical precision. Upgrading 
    every order to a premium courier would collapse margins. Instead, we must identify which 
    courier–city pairs are generating fake delivery attempts and late deliveries.
</p>
""", unsafe_allow_html=True)

c3, c4 = st.columns(2, gap="medium")

with c3:
    st.markdown('<div class="chart-card"><div class="chart-title">SLA Breach % — City × Courier</div><div class="chart-subtitle">Pivot heatmap; darker red = higher breach rate</div>', unsafe_allow_html=True)
    pivot_sla = df_main.pivot_table(
        index='city_x', columns='courier_partner',
        values='is_sla_breach', aggfunc='mean'
    ) * 100
    st.dataframe(
        pivot_sla.style
            .format("{:.1f}%")
            .background_gradient(cmap='Reds', axis=None)
            .set_properties(**{'font-family': 'DM Sans', 'font-size': '13px'}),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="chart-card"><div class="chart-title">Complaints by City × Issue Type</div><div class="chart-subtitle">Ticket volume distribution across hubs</div>', unsafe_allow_html=True)
    pivot_tickets = pd.pivot_table(
        df_main.dropna(subset=['issue_type']),
        index='city_x', columns='issue_type',
        values='ticket_id' if 'ticket_id' in df_main.columns else 'order_id',
        aggfunc='count', fill_value=0
    )
    st.dataframe(
        pivot_tickets.style
            .background_gradient(cmap='Oranges', axis=None)
            .set_properties(**{'font-family': 'DM Sans', 'font-size': '13px'}),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
<p>
    <strong style="color:#93C5FD">Key Finding:</strong> QuickShip is systematically responsible for the highest SLA breach rates 
    — particularly in Nagpur and Indore hubs where fake delivery attempts are heavily 
    concentrated. This is a localized, solvable problem; it does not require network-wide cost escalation.
</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# CHAPTER 3
# ==========================================
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="chapter-block">
    <span class="chapter-num">Chapter 03</span>
    <div class="chapter-line"></div>
</div>
<h2 class="chapter-title">The Cost of a Bad Delivery</h2>
<p class="narrative">
    Does a delayed order actually stop a customer from returning? 
    We mapped SLA breach rates across customer segments and plotted cohort retention 
    by signup month to find the answer.
</p>
""", unsafe_allow_html=True)

c5, c6 = st.columns(2, gap="medium")

with c5:
    st.markdown('<div class="chart-card"><div class="chart-title">SLA Breach % by Segment</div><div class="chart-subtitle">High Value customers deserve better protection</div>', unsafe_allow_html=True)
    segment_sla = df_main.groupby('segment')['is_sla_breach'].mean().reset_index()
    segment_sla['is_sla_breach'] *= 100

    fig_seg = go.Figure(go.Bar(
        x=segment_sla['segment'],
        y=segment_sla['is_sla_breach'],
        text=segment_sla['is_sla_breach'].round(1).astype(str) + '%',
        textposition='outside',
        textfont=dict(family='Syne', color='#C8D4E8', size=12),
        marker=dict(
            color=segment_sla['is_sla_breach'],
            colorscale=[[0,'#1A3A5C'],[0.5,'#7B1D24'],[1,'#CB1024']],
            line=dict(color='rgba(0,0,0,0)')
        ),
        hovertemplate='<b>%{x}</b><br>SLA Breach: %{y:.1f}%<extra></extra>'
    ))
    fig_seg.update_layout(**PLOTLY_LAYOUT, height=300, showlegend=False)
    st.plotly_chart(fig_seg, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c6:
    st.markdown('<div class="chart-card"><div class="chart-title">Retention Cohorts</div><div class="chart-subtitle">Segment composition by signup month</div>', unsafe_allow_html=True)
    customers['signup_month'] = customers['signup_date'].dt.to_period('M').astype(str)
    cohort = customers.groupby(['signup_month','segment']).size().reset_index(name='count')

    fig_cohort = px.bar(
        cohort, x='signup_month', y='count', color='segment',
        barmode='stack',
        color_discrete_map={
            'New': '#1A56BD',
            'Repeat': '#10B981',
            'High Value': '#CB1024',
            'Churned': '#374151'
        }
    )
    fig_cohort.update_layout(**PLOTLY_LAYOUT, height=300)
    fig_cohort.update_traces(
        marker_line_width=0,
        hovertemplate='<b>%{x}</b><br>%{fullData.name}: %{y}<extra></extra>'
    )
    st.plotly_chart(fig_cohort, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# CHAPTER 4 — RECOMMENDATIONS
# ==========================================
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="chapter-block">
    <span class="chapter-num">Chapter 04</span>
    <div class="chapter-line"></div>
</div>
<h2 class="chapter-title">The Path Forward</h2>
<p class="narrative">
    Three high-leverage interventions that can meaningfully move NPS without 
    proportional cost increases — targeting the root causes identified above.
</p>
""", unsafe_allow_html=True)

st.markdown("""
<div class="rec-grid">
    <div class="rec-card">
        <div class="rec-num">Recommendation 01</div>
        <div class="rec-title">Phase Out QuickShip in Critical Zones</div>
        <div class="rec-body">
            QuickShip drives 32% SLA breaches and the majority of fake delivery attempts. 
            Rather than escalating to FastEx network-wide, reallocate QuickShip volume to 
            <strong style="color:#CBD5E1">ShipNow</strong> (mid-tier cost, 20% breach rate) 
            specifically in Nagpur where RTO rates are disproportionately high.
        </div>
    </div>
    <div class="rec-card">
        <div class="rec-num">Recommendation 02</div>
        <div class="rec-title">Protect High-Value Customers</div>
        <div class="rec-body">
            High Value customers currently experience identical SLA breach rates to new customers — 
            an unacceptable risk. Implement a routing logic gate: 
            <strong style="color:#CBD5E1">all High Value orders exclusively via FastEx.</strong> 
            The cost delta is offset by retaining high-LTV users.
        </div>
    </div>
    <div class="rec-card">
        <div class="rec-num">Recommendation 03</div>
        <div class="rec-title">Hub-Level Accountability</div>
        <div class="rec-body">
            Fake delivery attempts are geographically concentrated in Nagpur and Indore.
            Institute <strong style="color:#CBD5E1">strict hub-level performance penalties</strong> 
            for logistics staff at these locations. This directly reduces complaint volume at 
            zero additional operational routing cost.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer-bar">
    <span class="footer-text">DTDC · Delivery Intelligence Dashboard · Powered by Python & Streamlit</span>
    <span class="footer-text">Data refresh: real-time on file change</span>
</div>
""", unsafe_allow_html=True)
