# ================================================
# HELPER FUNCTIONS
# ================================================

def load_data(uploaded_file):
    """Load CSV or Excel file with data quality checks"""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='latin1')
        else:
            df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()

        # ── DATA QUALITY CHECKS ──
        warnings = []
        
        # Check file size
        if len(df) > 100000:
            warnings.append(f"⚠️ Large dataset detected ({len(df):,} rows) — analysis may be slower")
        
        # Check for empty dataframe
        if len(df) == 0:
            st.error("❌ The uploaded file is empty. Please upload a file with data.")
            return None
        
        # Check for missing values
        missing = df.isnull().sum().sum()
        if missing > 0:
            missing_pct = (missing / (len(df) * len(df.columns))) * 100
            warnings.append(f"⚠️ {missing:,} missing values found ({missing_pct:.1f}% of data) — this may affect analysis accuracy")
        
        # Check for duplicates
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            warnings.append(f"⚠️ {duplicates:,} duplicate rows detected — consider removing them for accurate analysis")
        
        # Check minimum columns
        if len(df.columns) < 2:
            warnings.append("⚠️ Only 1 column detected — charts and analysis work best with multiple columns")
        
        # Check for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) == 0:
            warnings.append("⚠️ No numeric columns detected — some charts may not be available")

        # Show warnings
        for w in warnings:
            st.warning(w)

        return df

    except Exception as e:
        st.error(f"❌ Could not read this file. Please make sure it is a valid CSV or Excel file. Technical details: {e}")
        return None


def get_sample_data():
    """Returns a sample Kenya business dataset for demo purposes"""
    np.random.seed(42)
    counties = ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret',
                'Thika', 'Malindi', 'Kitale', 'Garissa', 'Nyeri']
    products = ['Solar Panel', 'Battery', 'Inverter', 'Cable', 'Controller']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    data = []
    for _ in range(200):
        data.append({
            'Month': np.random.choice(months),
            'County': np.random.choice(counties),
            'Product': np.random.choice(products),
            'Units_Sold': np.random.randint(10, 500),
            'Revenue_KES': np.random.randint(5000, 200000),
            'Cost_KES': np.random.randint(3000, 150000),
            'Customer_Rating': round(np.random.uniform(3.0, 5.0), 1),
            'Returns': np.random.randint(0, 20),
        })
    
    df = pd.DataFrame(data)
    df['Profit_KES'] = df['Revenue_KES'] - df['Cost_KES']
    return df


def get_groq_key():
    """Get Groq API key from secrets or user input"""
    try:
        return st.secrets["GROQ_API_KEY"]
    except:
        return None


# ================================================
# PAGE 1 — HOME
# ================================================
if page == "🏠 Home":

    # Hero section
    st.markdown("""
    <div class='hero'>
        <h1>📊 BeruAnalytics</h1>
        <p>Upload your data. Get instant AI-powered analysis,
        interactive dashboards and professional reports in minutes.</p>
        <p style='font-size:14px; opacity:0.7;'>
            Powered by AI | Built for Kenya and beyond 🇰🇪
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── NAVIGATION BUTTONS WITH HOVER ──
    st.markdown("""
    <style>
    .nav-btn-container {
        display: flex;
        gap: 12px;
        margin: 24px 0;
        flex-wrap: wrap;
    }
    .nav-btn {
        background: white;
        border: 2px solid #1A6B72;
        border-radius: 8px;
        padding: 12px 20px;
        color: #1A6B72;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
        display: inline-block;
        position: relative;
    }
    .nav-btn:hover {
        background: #1A6B72;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(26,107,114,0.3);
    }
    .nav-btn .tooltip {
        visibility: hidden;
        background: #1A1A2E;
        color: white;
        text-align: center;
        border-radius: 6px;
        padding: 6px 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        white-space: nowrap;
        font-size: 12px;
        font-weight: 400;
        opacity: 0;
        transition: opacity 0.2s;
    }
    .nav-btn:hover .tooltip {
        visibility: visible;
        opacity: 1;
    }
    </style>

    <div class='nav-btn-container'>
        <div class='nav-btn'>
            📊 Dashboard
            <span class='tooltip'>Interactive charts and KPI cards from your data</span>
        </div>
        <div class='nav-btn'>
            🤖 BeruDataNarrate
            <span class='tooltip'>AI-powered Word and PDF report generator</span>
        </div>
        <div class='nav-btn'>
            💬 AI Assistant
            <span class='tooltip'>Ask questions about your data in plain English</span>
        </div>
        <div class='nav-btn'>
            📋 Data Explorer
            <span class='tooltip'>Search, filter and export your data</span>
        </div>
        <div class='nav-btn'>
            ℹ️ About
            <span class='tooltip'>Privacy, security and platform information</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("*👆 Hover over buttons to preview each feature — click pages in the sidebar to navigate*")

    st.divider()

    # ── GET STARTED ──
    st.markdown("<div class='section-header'>🚀 Get Started</div>",
                unsafe_allow_html=True)

    col_upload, col_sample = st.columns([3, 1])

    with col_upload:
        uploaded = st.file_uploader(
            "Upload your CSV or Excel file to begin",
            type=['csv', 'xlsx', 'xls'],
            help="Supported formats: CSV, Excel (.xlsx, .xls) | Max recommended: 100,000 rows"
        )

    with col_sample:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🎯 Try Sample Data",
                      use_container_width=True,
                      help="Load a sample Kenya sales dataset to explore all features"):
            df = get_sample_data()
            st.session_state.df = df
            st.session_state.file_name = "sample_kenya_sales_data.csv"
            st.success("✅ Sample dataset loaded — 200 rows of Kenya sales data!")
            st.info("👈 Navigate to Dashboard or BeruDataNarrate to explore")

    if uploaded:
        df = load_data(uploaded)
        if df is not None:
            st.session_state.df = df
            st.session_state.file_name = uploaded.name

            # ── DATA QUALITY REPORT ──
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

            st.divider()
            st.markdown("### ✅ Data Quality Report")

            q1, q2, q3, q4, q5 = st.columns(5)
            with q1:
                st.metric("Total Rows", f"{len(df):,}")
            with q2:
                st.metric("Total Columns", len(df.columns))
            with q3:
                missing = df.isnull().sum().sum()
                st.metric("Missing Values",
                          missing,
                          delta="Clean ✅" if missing == 0 else "⚠️ Found",
                          delta_color="normal" if missing == 0 else "inverse")
            with q4:
                dupes = df.duplicated().sum()
                st.metric("Duplicates",
                          dupes,
                          delta="Clean ✅" if dupes == 0 else "⚠️ Found",
                          delta_color="normal" if dupes == 0 else "inverse")
            with q5:
                st.metric("Numeric Cols", len(numeric_cols))

            st.success(f"✅ **{uploaded.name}** loaded — {len(df):,} rows, {len(df.columns)} columns")
            st.info("👈 Use the sidebar to navigate to Dashboard, BeruDataNarrate or Data Explorer")

            with st.expander("👀 Preview first 5 rows"):
                st.dataframe(df.head(), use_container_width=True)

    elif st.session_state.df is not None:
        st.success(f"✅ **{st.session_state.file_name}** is loaded and ready")
        st.info("👈 Navigate using the sidebar")

    st.divider()

    # Feature cards
    st.markdown("<div class='section-header'>✨ What BeruAnalytics Does</div>",
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3>📊 Interactive Dashboard</h3>
            <p>Automatic KPI cards, bar charts, line charts,
            scatter plots and correlation heatmaps generated
            instantly from your data with full interactivity.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3>🤖 AI Report Generator</h3>
            <p>BeruDataNarrate analyzes your data with AI and
            generates a professional Word and PDF report with
            executive summary, key findings and recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <h3>💬 AI Data Assistant</h3>
            <p>Ask questions about your data in plain English.
            Get instant AI-powered answers, insights and
            explanations without writing any code.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown("""
        <div class='feature-card'>
            <h3>📋 Data Explorer</h3>
            <p>Browse, search, sort and filter your data in a
            smart interactive table. Export filtered results
            as CSV or Excel instantly.</p>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown("""
        <div class='feature-card'>
            <h3>🔒 Data Quality Checks</h3>
            <p>Automatic checks for missing values, duplicates
            and data integrity issues on every upload —
            so your analysis is always based on clean data.</p>
        </div>
        """, unsafe_allow_html=True)
    with col6:
        st.markdown("""
        <div class='feature-card'>
            <h3>📥 Export Everything</h3>
            <p>Download your analysis as Word documents,
            PDF reports, CSV or Excel files.
            Share with stakeholders instantly.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.metric("File Formats", "CSV + Excel", delta="Supported")
    with s2:
        st.metric("Chart Types", "6+", delta="Interactive")
    with s3:
        st.metric("Report Formats", "Word + PDF", delta="Professional")
    with s4:
        st.metric("AI Powered", "Yes", delta="Groq LLaMA")

    st.divider()
    st.caption("BeruAnalytics | Built by Felix Beru Tsinzole | Nairobi, Kenya 🇰🇪")
