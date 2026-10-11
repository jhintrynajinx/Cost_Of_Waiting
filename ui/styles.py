"""
ui/styles.py
Google Stitch visual styling system for The Cost of Waiting Streamlit application.
Matches Stitch typography (Plus Jakarta Sans + Inter), colors (Teal #0f766e, Orange #ea580c, Navy #0b1c30),
clean white backgrounds, subtle borders (#e2e8f0), and 1920x1080 boardroom layout.
Enforces light input-field backgrounds and high-contrast text across all operating system themes.
"""

STITCH_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

/* Reset and Global Base */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #ffffff !important;
    color: #0b1c30 !important;
}

/* Remove Streamlit default header decoration */
header[data-testid="stHeader"] {
    background-color: transparent !important;
    height: 0px !important;
}
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
    max-width: 1440px !important;
    background-color: #ffffff !important;
}

/* Typography tokens & Type Scale */
h1, .font-title {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 32px !important;
    font-weight: 800 !important;
    color: #0b1c30 !important;
    line-height: 1.25 !important;
}

h2, .font-section {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 24px !important;
    font-weight: 700 !important;
    color: #0b1c30 !important;
    line-height: 1.3 !important;
}

h3, .font-card-title {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 19px !important;
    font-weight: 700 !important;
    color: #0b1c30 !important;
    line-height: 1.35 !important;
}

h4 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    color: #0b1c30 !important;
}

p, span, div {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #0b1c30;
}

/* ==========================================================================
   INPUT FIELDS & CONTROLS (Permanent fix for dark/black input bug across all OS/browser themes)
   ========================================================================== */

/* Outer form container: clean white card with subtle border */
div[data-testid="stForm"] {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
}

/* Number, text, and base input container boxes */
div[data-baseweb="input"],
div[data-baseweb="base-input"],
div[data-testid="stNumberInput"] div[data-baseweb="input"],
div[data-testid="stTextInput"] div[data-baseweb="input"],
div[data-testid="stNumberInputContainer"],
div.react-aria-TextField div[data-testid="stNumberInputContainer"] {
    background-color: #ffffff !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 8px !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    color: #0b1c30 !important;
}

/* Input hover state */
div[data-baseweb="input"]:hover,
div[data-baseweb="base-input"]:hover,
div[data-testid="stNumberInputContainer"]:hover {
    border-color: #0f766e !important;
    background-color: #f8fafc !important;
}

/* Input focus state */
div[data-baseweb="input"]:focus-within,
div[data-baseweb="base-input"]:focus-within,
div[data-testid="stNumberInputContainer"]:focus-within {
    border-color: #0f766e !important;
    box-shadow: 0 0 0 2px rgba(15, 118, 110, 0.2) !important;
    background-color: #ffffff !important;
}

/* Actual input text element inside widget - NEVER transparent, ALWAYS visible */
div[data-baseweb="input"] input,
div[data-baseweb="base-input"] input,
input[data-testid="stNumberInputField"],
input[type="number"],
input[type="text"] {
    background-color: #ffffff !important;
    color: #0b1c30 !important;
    -webkit-text-fill-color: #0b1c30 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 16.5px !important;
    font-weight: 600 !important;
    padding: 9px 14px !important;
}

/* Number input step buttons (+ / -) */
button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {
    background-color: #f8fafc !important;
    color: #334155 !important;
    border-color: #cbd5e1 !important;
}
button[data-testid="stNumberInputStepDown"]:hover,
button[data-testid="stNumberInputStepUp"]:hover {
    background-color: #e2e8f0 !important;
    color: #0f766e !important;
}

/* Widget labels (Increased to 16px with dark high-contrast color) */
label[data-testid="stWidgetLabel"],
label[data-testid="stWidgetLabel"] p,
label[data-testid="stWidgetLabel"] span {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #0b1c30 !important;
    margin-bottom: 5px !important;
}

/* Captions & helper text below inputs (Clean 14px size) */
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p,
small {
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    color: #475569 !important;
    margin-top: 3px !important;
}

/* Radio buttons container and labels */
div[data-testid="stRadio"] {
    background-color: #f8fafc !important;
    padding: 8px 16px !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
}
div[data-testid="stRadio"] label,
div[data-testid="stRadio"] label p,
div[data-testid="stRadio"] label span {
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #0b1c30 !important;
}

/* Slider component — Enhanced contrast, visible track, handle, and tick labels */
div[data-testid="stSlider"] {
    padding-top: 8px !important;
    padding-bottom: 8px !important;
    pointer-events: auto !important;
}
div[data-testid="stSlider"] div[data-baseweb="slider"],
div[data-testid="stSlider"] div[data-rac] {
    pointer-events: auto !important;
}
/* Slider Base Track */
div[data-testid="stSlider"] div[data-baseweb="slider"] > div,
div[data-testid="stSlider"] div[data-rac][data-orientation="horizontal"] > div:first-child {
    background-color: #cbd5e1 !important;
    height: 9px !important;
    border-radius: 5px !important;
}
/* Slider Filled Progress Bar */
div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div:first-child {
    background-color: #0f766e !important;
    height: 9px !important;
    border-radius: 5px !important;
}
/* Slider Thumb Handle */
div[data-testid="stSlider"] div[role="slider"],
div[data-testid="stSlider"] div[data-rac][style*="position: absolute"] {
    background-color: #0f766e !important;
    border: 2.5px solid #ffffff !important;
    box-shadow: 0 2px 6px rgba(15, 118, 110, 0.45) !important;
    width: 22px !important;
    height: 22px !important;
    border-radius: 50% !important;
    cursor: grab !important;
    pointer-events: auto !important;
}
div[data-testid="stSlider"] div[role="slider"]:active,
div[data-testid="stSlider"] div[data-rac][style*="position: absolute"]:active {
    cursor: grabbing !important;
    box-shadow: 0 3px 10px rgba(15, 118, 110, 0.7) !important;
}
/* Slider Thumb Value badge */
div[data-testid="stSliderThumbValue"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 14.5px !important;
    font-weight: 800 !important;
    color: #0f766e !important;
    background-color: #f0fdfa !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
    border: 1px solid #99f6e4 !important;
}
/* Slider Tick Bar Labels - High contrast slate-800 instead of faint grey */
div[data-testid="stSlider"] div[data-testid="stTickBar"],
div[data-testid="stSliderTickBar"],
div[data-testid="stSlider"] div[data-rac] div[style*="font-size"] {
    color: #1e293b !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}

/* ==========================================================================
   BUTTONS (Primary & Secondary / Outline)
   Streamlit ≥1.45 renders buttons with data-testid="baseButton-secondary"
   and data-testid="baseButton-primary". The old button[kind] attribute
   selector never matched, causing primary buttons to inherit secondary
   styles and secondary buttons to go black on active/focus.
   ========================================================================== */

/* ---------- Secondary / default buttons ---------- */
div.stButton > button,
button[data-testid="baseButton-secondary"] {
    border-radius: 8px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    transition: background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease !important;
    background-color: #ffffff !important;
    color: #0b1c30 !important;
    border: 1px solid #cbd5e1 !important;
    box-shadow: 0 1px 2px rgba(11, 28, 48, 0.04) !important;
    padding: 6px 16px !important;
}

div.stButton > button:hover,
button[data-testid="baseButton-secondary"]:hover {
    background-color: #f8fafc !important;
    color: #0f766e !important;
    border-color: #0f766e !important;
    box-shadow: 0 2px 4px rgba(15, 118, 110, 0.1) !important;
}

div.stButton > button:focus,
button[data-testid="baseButton-secondary"]:focus {
    background-color: #ffffff !important;
    color: #0b1c30 !important;
    border-color: #0f766e !important;
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(15, 118, 110, 0.25) !important;
}

div.stButton > button:active,
button[data-testid="baseButton-secondary"]:active {
    background-color: #f0fdfa !important;
    color: #0b1c30 !important;
    border-color: #0f766e !important;
}

div.stButton > button:disabled,
button[data-testid="baseButton-secondary"]:disabled {
    background-color: #f8fafc !important;
    color: #94a3b8 !important;
    border-color: #e2e8f0 !important;
    cursor: not-allowed !important;
}

/* ---------- Primary buttons (Generate Trajectory) ----------
   Streamlit 1.45+ renders data-testid="baseButton-primary"
   instead of the old button[kind="primary"] attribute.
   Both selectors are included for forward/backward compatibility.
   ---------------------------------------------------------------- */
div.stButton > button[kind="primary"],
button[data-testid="baseButton-primary"] {
    background-color: #0f766e !important;
    color: #ffffff !important;
    border: none !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 4px rgba(15, 118, 110, 0.25) !important;
    padding: 8px 20px !important;
}

div.stButton > button[kind="primary"]:hover,
button[data-testid="baseButton-primary"]:hover {
    background-color: #0d655f !important;
    color: #ffffff !important;
    box-shadow: 0 4px 8px rgba(15, 118, 110, 0.35) !important;
}

div.stButton > button[kind="primary"]:focus,
button[data-testid="baseButton-primary"]:focus {
    background-color: #0f766e !important;
    color: #ffffff !important;
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(15, 118, 110, 0.45) !important;
}

div.stButton > button[kind="primary"]:active,
button[data-testid="baseButton-primary"]:active {
    background-color: #0a514c !important;
    color: #ffffff !important;
}

/* ==========================================================================
   STITCH COMPONENT CARDS & BADGES
   ========================================================================== */

.stitch-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1.5rem;
    background: #ffffff;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(11, 28, 48, 0.03);
}

.stitch-brand {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800;
    font-size: 15px;
    letter-spacing: -0.02em;
    color: #0b1c30;
    display: flex;
    align-items: center;
    gap: 8px;
}

.stitch-pill {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 3px 9px;
    border-radius: 4px;
    background: rgba(15, 118, 110, 0.1);
    color: #0f766e;
    border: 1px solid rgba(15, 118, 110, 0.2);
}

.stitch-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(11, 28, 48, 0.02);
    margin-bottom: 1rem;
}

.stitch-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 0.75rem;
    margin-bottom: 1.25rem;
}

.stitch-card-title {
    font-size: 13.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #0f766e;
    display: flex;
    align-items: center;
    gap: 6px;
}

.stitch-badge-bmi {
    background: rgba(254, 147, 44, 0.12);
    border: 1px solid rgba(234, 88, 12, 0.3);
    border-radius: 10px;
    padding: 1rem;
    margin-top: 1rem;
}

.stitch-badge-bmi-ok {
    background: rgba(15, 118, 110, 0.08);
    border: 1px solid rgba(15, 118, 110, 0.3);
    border-radius: 10px;
    padding: 1rem;
    margin-top: 1rem;
}

/* Stitch Metric Cards */
.metric-box-a {
    border-top: 3px solid #ea580c !important;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1.25rem;
}

.metric-box-b {
    border-top: 3px solid #0f766e !important;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1.25rem;
}

.metric-box-delta {
    border: 1px solid #99f6e4;
    background: #f0fdfa;
    border-radius: 8px;
    padding: 1.25rem;
}

/* Expander styling
   Streamlit 1.65 wraps expander summary text in a <p> and may apply
   a dark CSS variable — target the summary and all descendants explicitly.
*/
div[data-testid="stExpander"] {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    margin-bottom: 8px !important;
}
div[data-testid="stExpander"] details summary,
div[data-testid="stExpander"] details summary p,
div[data-testid="stExpander"] details summary span,
div[data-testid="stExpander"] details summary svg {
    color: #0b1c30 !important;
    fill: #0b1c30 !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
}
div[data-testid="stExpander"] details summary:hover,
div[data-testid="stExpander"] details summary:hover p,
div[data-testid="stExpander"] details summary:hover span {
    color: #0f766e !important;
}
div[data-testid="stExpander"] details summary:hover svg {
    fill: #0f766e !important;
}

/* ==========================================================================
   PAGE TRANSITIONS & ANIMATIONS (Requirement 2 & 6)
   Subtle 150ms pure opacity fade without vertical displacement to prevent
   layout shifts, text blur, or flickering. Respects prefers-reduced-motion.
   ========================================================================== */
@keyframes stitchReportFadeIn {
    0% {
        opacity: 0;
    }
    100% {
        opacity: 1;
    }
}

.report-screen-fadein, .main .block-container {
    animation: stitchReportFadeIn 150ms ease-out both;
}

/* Subtle transition for Plotly chart container on state change */
div[data-testid="stPlotlyChart"] {
    transition: opacity 0.2s ease-in-out, filter 0.2s ease-in-out !important;
}

@media (prefers-reduced-motion: reduce) {
    .report-screen-fadein, .main .block-container, div[data-testid="stPlotlyChart"] {
        animation: none !important;
        transition: none !important;
        opacity: 1 !important;
    }
}

/* ==========================================================================
   WHERE DO THE COSTS COME FROM? CATEGORY BREAKDOWN TABLE & BADGES (Task 3 & 5)
   ========================================================================== */
.breakdown-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin-top: 0.75rem;
    font-size: 13px;
}

.breakdown-table th {
    background: #f8fafc;
    color: #475569;
    font-size: 11.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 10px 12px;
    border-top: 1px solid #e2e8f0;
    border-bottom: 1px solid #e2e8f0;
    text-align: left;
}

.breakdown-table th.num-col, .breakdown-table td.num-col {
    text-align: right;
}

.breakdown-table td {
    padding: 11px 12px;
    border-bottom: 1px solid #f1f5f9;
    vertical-align: middle;
    color: #0b1c30;
    font-size: 13.5px;
}

.breakdown-table tr:hover td {
    background-color: #fafbfd;
}

.breakdown-badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    white-space: nowrap;
}

.badge-saving {
    background: rgba(15, 118, 110, 0.1);
    color: #0f766e;
    border: 1px solid rgba(15, 118, 110, 0.25);
}

.badge-outlay {
    background: rgba(2, 132, 199, 0.1);
    color: #0284c7;
    border: 1px solid rgba(2, 132, 199, 0.25);
}

.badge-assumption {
    background: rgba(217, 119, 6, 0.1);
    color: #b45309;
    border: 1px solid rgba(217, 119, 6, 0.25);
}

.badge-unsupported {
    background: #f1f5f9;
    color: #64748b;
    border: 1px solid #cbd5e1;
}

/* Category Progress Ratio Bar */
.cat-bar-bg {
    width: 100%;
    height: 5px;
    background: #f1f5f9;
    border-radius: 3px;
    overflow: hidden;
    margin-top: 3px;
}

.cat-bar-fill-a {
    height: 100%;
    background: #ea580c;
    border-radius: 3px;
}

.cat-bar-fill-b {
    height: 100%;
    background: #0f766e;
    border-radius: 3px;
}

/* Footer note */
.stitch-footer {
    text-align: center;
    border-top: 1px solid #e2e8f0;
    padding-top: 0.75rem;
    margin-top: 2rem;
    color: #64748b;
    font-size: 12px;
}

/* ==========================================================================
   SCROLLBARS — match app's teal/slate theme
   Supported in Chromium (Chrome, Edge, Electron-based Streamlit viewer)
   and WebKit (Safari). Firefox uses scrollbar-color / scrollbar-width.
   Does not break keyboard or mouse scrolling.
   ========================================================================== */

/* Chromium / WebKit scrollbar — thin, theme-matched */
::-webkit-scrollbar {
    width: 7px;
    height: 7px;
}
::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb {
    background: #94a3b8;
    border-radius: 4px;
    border: 1px solid #f1f5f9;
}
::-webkit-scrollbar-thumb:hover {
    background: #0f766e;
}
::-webkit-scrollbar-corner {
    background: #f1f5f9;
}

/* Firefox scrollbar (thin, theme-matched) */
* {
    scrollbar-width: thin;
    scrollbar-color: #94a3b8 #f1f5f9;
}
</style>
"""
