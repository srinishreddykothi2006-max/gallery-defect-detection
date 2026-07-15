import streamlit as st
import cv2
import numpy as np
import pandas as pd
from detector import detect_defects
import os
import datetime
import json

# ========================================
# PAGE CONFIGURATION
# ========================================

st.set_page_config(
    page_title="Gallery Exhibit Defect Detection",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# ENHANCED CUSTOM CSS WITH LIGHT THEME
# ========================================

st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    [data-testid="stMainBlockContainer"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eff7 100%);
        padding: 2rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f0f4f9 100%);
        border-right: 2px solid #e0e8f0;
    }

    [data-testid="stSidebarNav"] {
        padding: 2rem 0;
    }

    h1, h2, h3 {
        color: #1a3a52;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    h1 {
        background: linear-gradient(135deg, #2563eb, #0891b2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem;
    }

    .stMetric {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        border-left: 4px solid #2563eb;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.1);
        transition: all 0.3s ease;
    }

    .stMetric:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.15);
    }

    .stButton > button {
        width: 100%;
        height: 50px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 16px;
        background: linear-gradient(135deg, #2563eb 0%, #0891b2 100%);
        color: white;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    .card-container {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        border: 1px solid #e0e8f0;
    }

    .card-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1a3a52;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .success-box {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 4px solid #10b981;
        color: #065f46;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
    }

    .error-box {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 4px solid #ef4444;
        color: #7f1d1d;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
    }

    .info-box {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 4px solid #3b82f6;
        color: #1e3a8a;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
    }

    .stSlider {
        padding: 1rem 0;
    }

    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #2563eb, #0891b2);
    }

    .stFileUploader {
        border: 2px dashed #2563eb;
        border-radius: 12px;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f0f9ff, #f5f3ff);
        transition: all 0.3s ease;
    }

    .stFileUploader:hover {
        background: linear-gradient(135deg, #dbeafe, #ede9fe);
    }

    .metric-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }

    .defect-critical {
        background: linear-gradient(135deg, #fee2e2, #fecaca);
        border-left: 4px solid #ef4444;
    }

    .defect-low {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        border-left: 4px solid #10b981;
    }

    .sidebar-item {
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .sidebar-item:hover {
        background: linear-gradient(135deg, #e0e7ff, #f5f3ff);
    }

    [data-testid="stMarkdownContainer"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #2563eb, transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# SESSION STATE INITIALIZATION
# ========================================

if 'detection_history' not in st.session_state:
    st.session_state.detection_history = []

if 'total_analyses' not in st.session_state:
    st.session_state.total_analyses = 0

if 'alerts' not in st.session_state:
    st.session_state.alerts = []

# ========================================
# SIDEBAR NAVIGATION
# ========================================

st.sidebar.markdown("""
<div style='text-align: center; padding: 1.5rem 0;'>
    <h2 style='color: #2563eb; font-size: 1.8rem; margin: 0;'>🖼️ Gallery Defect</h2>
    <p style='color: #666; font-size: 0.9rem; margin: 0;'>Detection System</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "📋 Navigation",
    [
        "🔍 Live Detection",
        "📊 Detection History",
        "⚠️ Alert Dashboard",
        "⚙️ System Settings"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

with st.sidebar.expander("📈 Quick Stats", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Analyses", st.session_state.total_analyses)
    with col2:
        st.metric("Alerts", len(st.session_state.alerts))

st.sidebar.markdown("---")
st.sidebar.caption("© 2024 Gallery Defect Detection System v1.0")

# ========================================
# LIVE DETECTION PAGE
# ========================================

if "Live Detection" in page:
    st.markdown("""
    <div style='text-align: center;'>
        <h1>🖼️ Gallery Exhibit Defect Detection</h1>
        <p style='font-size: 1.1rem; color: #4b5563;'>Advanced AI-powered surface defect detection for gallery exhibits</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1], gap="large")

    with col2:
        st.markdown("""
        <div class='card-container'>
            <div class='card-title'>⚙️ Detection Settings</div>
        </div>
        """, unsafe_allow_html=True)

        sensitivity = st.slider(
            "Detection Sensitivity",
            0.1, 1.0, 0.7, 0.1,
            help="Higher values detect smaller defects (may increase false positives)"
        )

        st.markdown("""
        <div class='info-box'>
            <strong>💡 Tip:</strong> Higher sensitivity detects more small defects but may include false positives.
        </div>
        """, unsafe_allow_html=True)

    with col1:
        st.markdown("""
        <div class='card-container'>
            <div class='card-title'>📤 Upload Image</div>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Drag and drop your exhibit image here",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )

        if uploaded_file is not None:
            file_bytes = np.asarray(
                bytearray(uploaded_file.read()),
                dtype=np.uint8
            )

            image = cv2.imdecode(
                file_bytes,
                cv2.IMREAD_COLOR
            )

            # Display original image
            col_orig, col_settings = st.columns([2, 1])

            with col_orig:
                st.markdown("""
                <div class='card-container'>
                    <div class='card-title'>📸 Original Image</div>
                </div>
                """, unsafe_allow_html=True)
                st.image(
                    cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
                    use_container_width=True,
                    caption="Uploaded exhibit image"
                )

            with col_settings:
                st.markdown("""
                <div class='card-container'>
                    <div class='card-title'>ℹ️ Image Info</div>
                    <p><strong>Dimensions:</strong> {}x{}</p>
                    <p><strong>File:</strong> {}</p>
                </div>
                """.format(image.shape[1], image.shape[0], uploaded_file.name), unsafe_allow_html=True)

            # Analyze button
            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

            col_analyze, col_empty = st.columns([1, 2])

            with col_analyze:
                if st.button("🔍 Analyze Image", use_container_width=True):
                    progress = st.progress(0)

                    with st.spinner("🔄 Analyzing image with AI..."):
                        for i in range(100):
                            progress.progress(i + 1)

                        processed_img, df, accuracy = detect_defects(
                            image,
                            sensitivity
                        )

                    st.session_state.total_analyses += 1
                    st.session_state.detection_history.append({
                        'timestamp': datetime.datetime.now().isoformat(),
                        'file': uploaded_file.name,
                        'accuracy': accuracy,
                        'defects_count': len(df),
                        'critical_count': len(df[df["Severity"] == "Critical"]) if len(df) > 0 else 0,
                        'results': df
                    })

                    # Success notification
                    st.markdown("""
                    <div class='success-box'>
                        <strong>✅ Analysis Completed Successfully!</strong>
                    </div>
                    """, unsafe_allow_html=True)

                    # Display results in tabs
                    st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

                    result_tabs = st.tabs(["📊 Results", "🔍 Processed Image", "📈 Statistics"])

                    with result_tabs[0]:
                        # Metrics
                        m1, m2, m3, m4 = st.columns(4)

                        with m1:
                            st.metric(
                                "Accuracy",
                                f"{accuracy:.2f}%",
                                delta="High" if accuracy > 95 else "Good"
                            )

                        with m2:
                            st.metric(
                                "Total Defects",
                                len(df),
                                delta=str(len(df)) + " found"
                            )

                        critical = len(df[df["Severity"] == "Critical"]) if len(df) > 0 else 0
                        low = len(df[df["Severity"] == "Low"]) if len(df) > 0 else 0

                        with m3:
                            st.metric(
                                "🔴 Critical",
                                critical,
                                delta="Needs attention" if critical > 0 else "None"
                            )

                        with m4:
                            st.metric(
                                "🟡 Low",
                                low,
                                delta="Monitor" if low > 0 else "None"
                            )

                        st.markdown("---")

                        # Display results table
                        st.markdown("""
                        <div class='card-container'>
                            <div class='card-title'>📋 Detection Results</div>
                        </div>
                        """, unsafe_allow_html=True)

                        if len(df) > 0:
                            styled_df = df.style.map(
                                lambda val: 'background-color: #fee2e2; color: #7f1d1d' if val == 'Critical' else 'background-color: #d1fae5; color: #065f46',
                                subset=['Severity']
                            )
                            st.dataframe(styled_df, use_container_width=True)
                        else:
                            st.info("No defects detected in this image.")

                        # Alert
                        if critical > 0:
                            st.markdown(f"""
                            <div class='error-box'>
                                <strong>⚠️ Warning:</strong> {critical} Critical Defect(s) Found! Immediate inspection recommended.
                            </div>
                            """, unsafe_allow_html=True)

                            # Add to alerts
                            st.session_state.alerts.append({
                                'timestamp': datetime.datetime.now().isoformat(),
                                'file': uploaded_file.name,
                                'critical_count': critical,
                                'severity': 'Critical'
                            })

                        else:
                            st.markdown("""
                            <div class='success-box'>
                                <strong>✅ Good News:</strong> No Critical Defects Detected. Exhibit is in good condition.
                            </div>
                            """, unsafe_allow_html=True)

                    with result_tabs[1]:
                        st.markdown("""
                        <div class='card-container'>
                            <div class='card-title'>🔍 Processed Image with Detections</div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.image(
                            cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB),
                            use_container_width=True,
                            caption="Defects highlighted in red (Critical) and green (Low)"
                        )

                    with result_tabs[2]:
                        st.markdown("""
                        <div class='card-container'>
                            <div class='card-title'>📈 Statistics</div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Summary stats
                        stats_col1, stats_col2, stats_col3 = st.columns(3)

                        with stats_col1:
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #dbeafe, #bfdbfe); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #3b82f6;'>
                                <h3 style='margin: 0; color: #1e3a8a;'>Detection Rate</h3>
                                <p style='font-size: 2rem; margin: 0.5rem 0; color: #2563eb; font-weight: bold;'>{accuracy:.1f}%</p>
                                <p style='margin: 0; color: #4b5563; font-size: 0.9rem;'>Model Confidence</p>
                            </div>
                            """, unsafe_allow_html=True)

                        with stats_col2:
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #fee2e2, #fecaca); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #ef4444;'>
                                <h3 style='margin: 0; color: #7f1d1d;'>Critical Issues</h3>
                                <p style='font-size: 2rem; margin: 0.5rem 0; color: #ef4444; font-weight: bold;'>{critical}</p>
                                <p style='margin: 0; color: #4b5563; font-size: 0.9rem;'>Require Attention</p>
                            </div>
                            """, unsafe_allow_html=True)

                        with stats_col3:
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #d1fae5, #a7f3d0); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #10b981;'>
                                <h3 style='margin: 0; color: #065f46;'>Low Issues</h3>
                                <p style='font-size: 2rem; margin: 0.5rem 0; color: #10b981; font-weight: bold;'>{low}</p>
                                <p style='margin: 0; color: #4b5563; font-size: 0.9rem;'>Monitor</p>
                            </div>
                            """, unsafe_allow_html=True)

# ========================================
# DETECTION HISTORY PAGE
# ========================================

elif "Detection History" in page:
    st.markdown("""
    <h1>📊 Detection History</h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='card-container'>
        <div class='card-title'>📈 Analysis History</div>
    </div>
    """, unsafe_allow_html=True)

    if len(st.session_state.detection_history) > 0:
        history_data = []
        for item in st.session_state.detection_history:
            history_data.append({
                'Timestamp': item['timestamp'],
                'File': item['file'],
                'Accuracy': f"{item['accuracy']:.2f}%",
                'Total Defects': item['defects_count'],
                'Critical': item['critical_count']
            })

        history_df = pd.DataFrame(history_data)
        st.dataframe(history_df, use_container_width=True)

        # Summary statistics
        st.markdown("---")
        st.markdown("""
        <div class='card-container'>
            <div class='card-title'>📊 Summary Statistics</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Analyses",
                len(st.session_state.detection_history),
                delta="Since session start"
            )

        with col2:
            avg_accuracy = np.mean([item['accuracy'] for item in st.session_state.detection_history])
            st.metric(
                "Average Accuracy",
                f"{avg_accuracy:.2f}%",
                delta="All analyses"
            )

        with col3:
            total_defects = sum([item['defects_count'] for item in st.session_state.detection_history])
            st.metric(
                "Total Defects Found",
                total_defects,
                delta="Across all analyses"
            )

    else:
        st.markdown("""
        <div class='info-box'>
            <strong>ℹ️ No History Yet</strong><br>
            Run some analyses in the Live Detection page to see the history here.
        </div>
        """, unsafe_allow_html=True)

# ========================================
# ALERT DASHBOARD PAGE
# ========================================

elif "Alert Dashboard" in page:
    st.markdown("""
    <h1>⚠️ Alert Dashboard</h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='card-container'>
        <div class='card-title'>🚨 Critical Alerts</div>
    </div>
    """, unsafe_allow_html=True)

    # Alert metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Active Alerts",
            len(st.session_state.alerts),
            delta="Critical only"
        )

    with col2:
        critical_count = sum([alert['critical_count'] for alert in st.session_state.alerts])
        st.metric(
            "Critical Issues",
            critical_count,
            delta="Require attention"
        )

    with col3:
        if len(st.session_state.detection_history) > 0:
            success_rate = len([h for h in st.session_state.detection_history if h['critical_count'] == 0]) / len(st.session_state.detection_history) * 100
            st.metric(
                "Success Rate",
                f"{success_rate:.1f}%",
                delta="No issues"
            )
        else:
            st.metric("Success Rate", "0%", delta="No analyses yet")

    st.markdown("---")

    if len(st.session_state.alerts) > 0:
        st.markdown("""
        <div class='card-container'>
            <div class='card-title'>🔴 Alert List</div>
        </div>
        """, unsafe_allow_html=True)

        for idx, alert in enumerate(st.session_state.alerts):
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #fee2e2, #fecaca); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #ef4444; margin-bottom: 1rem;'>
                <h4 style='margin: 0 0 0.5rem 0; color: #7f1d1d;'>🚨 Alert #{idx + 1}</h4>
                <p style='margin: 0.25rem 0; color: #5f1313;'><strong>File:</strong> {alert['file']}</p>
                <p style='margin: 0.25rem 0; color: #5f1313;'><strong>Critical Issues:</strong> {alert['critical_count']}</p>
                <p style='margin: 0.25rem 0; color: #5f1313;'><strong>Time:</strong> {alert['timestamp']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='success-box'>
            <strong>✅ No Alerts</strong><br>
            All exhibits are in good condition. Keep monitoring regularly!
        </div>
        """, unsafe_allow_html=True)

# ========================================
# SYSTEM SETTINGS PAGE
# ========================================

elif "System Settings" in page:
    st.markdown("""
    <h1>⚙️ System Settings</h1>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='card-container'>
            <div class='card-title'>🔧 Detection Configuration</div>
        </div>
        """, unsafe_allow_html=True)

        min_area = st.slider(
            "Minimum Defect Area (pixels)",
            50, 500, 150, 10,
            help="Defects smaller than this will be ignored"
        )

        confidence_threshold = st.slider(
            "Confidence Threshold (%)",
            50, 99, 60, 5,
            help="Only show defects above this confidence level"
        )

    with col2:
        st.markdown("""
        <div class='card-container'>
            <div class='card-title'>📊 Display Preferences</div>
        </div>
        """, unsafe_allow_html=True)

        show_bounding_boxes = st.checkbox(
            "Show Bounding Boxes",
            value=True,
            help="Display bounding boxes around detected defects"
        )

        show_confidence_scores = st.checkbox(
            "Show Confidence Scores",
            value=True,
            help="Display confidence percentages in results"
        )

    st.markdown("---")

    st.markdown("""
    <div class='card-container'>
        <div class='card-title'>ℹ️ System Information</div>
    </div>
    """, unsafe_allow_html=True)

    info_col1, info_col2, info_col3 = st.columns(3)

    with info_col1:
        st.info("📦 OpenCV: Ready")

    with info_col2:
        st.info("🐍 Python: Version 3.8+")

    with info_col3:
        st.info("💾 Session Storage: Active")

    st.markdown("---")

    st.markdown("""
    <div class='card-container'>
        <div class='card-title'>🗑️ Data Management</div>
    </div>
    """, unsafe_allow_html=True)

    col_clear1, col_clear2, col_clear3 = st.columns(3)

    with col_clear1:
        if st.button("Clear History", use_container_width=True):
            st.session_state.detection_history = []
            st.success("✅ Detection history cleared!")

    with col_clear2:
        if st.button("Clear Alerts", use_container_width=True):
            st.session_state.alerts = []
            st.success("✅ Alerts cleared!")

    with col_clear3:
        if st.button("Reset All", use_container_width=True):
            st.session_state.detection_history = []
            st.session_state.alerts = []
            st.session_state.total_analyses = 0
            st.success("✅ All data reset!")

    st.markdown("---")

    st.markdown("""
    <div style='background: linear-gradient(135deg, #dbeafe, #bfdbfe); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #3b82f6;'>
        <h4 style='margin: 0 0 1rem 0; color: #1e3a8a;'>📝 About This System</h4>
        <p style='margin: 0.5rem 0; color: #1e40af;'><strong>Version:</strong> 1.0</p>
        <p style='margin: 0.5rem 0; color: #1e40af;'><strong>Purpose:</strong> Advanced defect detection for gallery exhibits</p>
        <p style='margin: 0.5rem 0; color: #1e40af;'><strong>Technology:</strong> OpenCV + AI Image Processing</p>
        <p style='margin: 0.5rem 0; color: #1e40af;'><strong>Last Updated:</strong> 2024</p>
    </div>
    """, unsafe_allow_html=True)