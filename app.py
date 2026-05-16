# ================================================
# SIDEBAR
# ================================================
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0;'>
        <h2 style='color:#1A6B72; margin:0; font-size:24px;'>📊 BeruAnalytics</h2>
        <p style='color:#888; font-size:12px; margin:4px 0 0 0;'>
            AI-Powered Data Analytics
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    page = st.radio(
        "Navigate",
        ["🏠 Home",
         "📊 Dashboard",
         "🤖 BeruDataNarrate",
         "💬 AI Assistant",
         "📋 Data Explorer",
         "ℹ️ About"],
        label_visibility="collapsed"
    )

    st.divider()

    if st.session_state.df is not None:
        df = st.session_state.df
        st.success(f"✅ Data loaded")
        st.caption(f"📁 {st.session_state.file_name}")
        st.caption(f"📊 {len(df):,} rows × {len(df.columns)} cols")
        if st.button("🗑️ Clear Data", use_container_width=True):
            st.session_state.df = None
            st.session_state.file_name = None
            st.session_state.analysis = None
            st.rerun()
    else:
        st.warning("⚠️ No data loaded")
        st.caption("Upload a file to get started")

    st.divider()
    st.caption("Built by Felix Beru Tsinzole")
    st.caption("Nairobi, Kenya 🇰🇪")
