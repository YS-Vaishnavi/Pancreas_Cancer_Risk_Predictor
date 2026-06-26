import streamlit as st
import numpy as np
import pickle
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 🎨 PAGE CONFIG
st.set_page_config(
    page_title="PancreaSafe AI Portal",
    page_icon="🧠",
    layout="wide"
)

# 📦 INITIALIZE STATE VARIABLES
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None  # Options: 'patient', 'doctor'

# 🎨 PREMIUM ENTERPRISE CSS INJECTION
st.markdown("""
<style>
/* App Canvas Background */
.stApp {
    background-color: #f8fafc;
}

/* 🎯 SAFE TYPOGRAPHY: Targets only core dashboard headings and specific custom text classes */
.stApp h1, .stApp h2, .stApp h3, .role-description, .demo-banner {
    font-family: 'Inter', -apple-system, sans-serif;
}

/* Custom Alert Banner Styling */
.demo-banner {
    background-color: #f0fdf4; 
    padding: 14px 20px; 
    border-radius: 12px; 
    margin-bottom: 25px; 
    font-size: 0.9rem; 
    border: 1px solid #bbf7d0; 
    color: #166534;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

/* Role Selection Card Descriptions */
.role-description {
    color: #475569;
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 1.5rem;
    min-height: 80px;
}

/* Dashboard Information Container Frameworks */
.left-box {
    background-color: #f0f9ff;
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #e0f2fe;
}
.right-box {
    background-color: #fefaf6;
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #fff5eb;
}

/* Strategic Dashboard Summary Tiles (Doctor Dashboard) */
.metric-tile {
    background-color: #ffffff;
    padding: 1.5rem;
    border-radius: 14px;
    border-left: 5px solid #2563eb;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}
</style>
""", unsafe_allow_html=True)

# 📦 CACHED ML MODEL LOADING
@st.cache_resource
def load_pancreatic_model():
    return pickle.load(open("model.pkl", "rb"))

model = load_pancreatic_model()

# 🎯 STANDARD REFERENCE THRESHOLDS (Clinical Upper Boundaries)
CLINICAL_NORMAL_MAX = {
    'ALT': 45.0,        # U/L
    'AST': 40.0,        # U/L
    'Amylase': 140.0,   # U/L
    'Bilirubin': 1.2,   # mg/dL
    'CA19-9': 37.0,     # U/mL
    'Glucose': 100.0,   # mg/dL
    'Lipase': 160.0,    # U/L
    'WBC': 11000.0      # cells/mcL
}


# ==========================================
# GATEWAY LAYER 1: AUTHENTICATION INTERFACE
# ==========================================
if not st.session_state.logged_in:
    # Create a centered column framework for the login layout
    _, login_col, _ = st.columns([1.5, 2, 1.5])
    
    with login_col:
        st.markdown("<div style='margin-top: 5rem;'></div>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #0f172a; margin-bottom: 0px;'>PancreaSafe AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748b; font-size: 1.05rem; margin-bottom: 2.5rem;'>Secure Clinical Identity Management Portal</p>", unsafe_allow_html=True)
        
        # Clean custom HTML info banner
        st.markdown("""
        <div class="demo-banner">
            🔑 <b>Authorized Demo Access:</b><br>
            <span style='font-size: 0.85rem;'>User ID: <code style='background:#dcfce7; padding:2px 4px; border-radius:4px;'>admin</code> | Certificate Key: <code style='background:#dcfce7; padding:2px 4px; border-radius:4px;'>password</code></span>
        </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("User ID / Clinician ID", placeholder="Enter official authorization handle")
        password = st.text_input("Security Certificate Key", type="password", placeholder="••••••••")
        
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        if st.button("Authenticate Identity", use_container_width=True, type="primary"):
            if username == "admin" and password == "password":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("🔒 Authentication Failed. Invalid credential token or certificate signature.")
                
        st.markdown("<p style='text-align: center; font-size: 0.8rem; color: #94a3b8; margin-top: 3.5rem;'>Protected under standard clinical simulated framework encryption protocols.</p>", unsafe_allow_html=True)


# ==========================================
# GATEWAY LAYER 2: ROLE SELECTION ROUTING
# ==========================================
elif st.session_state.logged_in and st.session_state.user_role is None:
    st.markdown("<div style='margin-top: 4rem;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #0f172a; margin-bottom: 8px;'>Welcome to PancreaSafe Ecosystem</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size:1.1rem; margin-bottom: 4rem;'>Select your designated systemic access domain below</p>", unsafe_allow_html=True)
    
    _, col_p, _, col_d, _ = st.columns([0.5, 2, 0.4, 2, 0.5])
    
    with col_p:
        st.markdown("<h2 style='color: #0284c7; margin-bottom: 10px;'>👤 Patient Portal</h2>", unsafe_allow_html=True)
        st.markdown("<p class='role-description'>Track personalized metabolic biomarkers, check preventative prognostic risk indexes, and interpret machine learning explainability charts.</p>", unsafe_allow_html=True)
        if st.button("Access Patient Trackers →", use_container_width=True, type="secondary"):
            st.session_state.user_role = "patient"
            st.rerun()
        
    with col_d:
        st.markdown("<h2 style='color: #2563eb; margin-bottom: 10px;'>🩺 Clinician Workspace</h2>", unsafe_allow_html=True)
        st.markdown("<p class='role-description'>Ingest comprehensive cohort spreadsheets via batch CSV systems, calculate automated populations urgency triage scores, and download structured analytical manifests.</p>", unsafe_allow_html=True)
        if st.button("Initialize Doctor Console →", use_container_width=True, type="primary"):
            st.session_state.user_role = "doctor"
            st.rerun()


# ==========================================
# MODULE 3A: PATIENT PORTAL INTERFACE VIEW
# ==========================================
elif st.session_state.logged_in and st.session_state.user_role == "patient":
    nav_left, nav_right = st.columns([9, 1.5])
    with nav_left:
        st.title("🧠 PancreaSafe AI Dashboard")
        st.caption("AI-powered diagnostic assistance system — Patient Access Domain")
    with nav_right:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Change Domain", use_container_width=True):
            st.session_state.user_role = None
            st.rerun()

    st.sidebar.header("📝 Patient Inputs")
    age = st.sidebar.slider("Age", 20, 80, value=20)
    gender = st.sidebar.selectbox("Gender", ["Male", "Female"])

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔬 Lab Biomarkers")
    ca19 = st.sidebar.number_input("CA19-9", 0, 500, value=0)
    lipase = st.sidebar.number_input("Lipase", 0, 500, value=0)
    amylase = st.sidebar.number_input("Amylase", 0, 300, value=0)
    glucose = st.sidebar.number_input("Glucose", 50, 300, value=50) 
    bilirubin = st.sidebar.number_input("Bilirubin", 0.0, 5.0, value=0.0)
    alt = st.sidebar.number_input("ALT", 0, 200, value=0)
    ast = st.sidebar.number_input("AST", 0, 200, value=0)
    wbc = st.sidebar.number_input("WBC", 4000, 20000, value=4000) 

    st.sidebar.markdown("---")
    st.sidebar.subheader("🤒 Clinical Symptoms")
    symptoms = st.sidebar.multiselect(
        "Select present symptoms:",
        ["Abdominal Pain", "Jaundice (Yellowing of skin/eyes)", "Unexplained Weight Loss", "Loss of Appetite"]
    )

    ast_alt_ratio = float(ast) / float(alt) if alt > 0 else 0.0
    gender_val = 1 if gender == "Female" else 0

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="left-box">', unsafe_allow_html=True)
        st.subheader("📊 Health Indicators")
        
        metrics_list = ['ALT', 'AST', 'Amylase', 'Bilirubin', 'CA19-9', 'Glucose', 'Lipase', 'WBC']
        user_values = [float(alt), float(ast), float(amylase), float(bilirubin), float(ca19), float(glucose), float(lipase), float(wbc)]
        normal_bounds = [CLINICAL_NORMAL_MAX[m] for m in metrics_list]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=metrics_list, y=normal_bounds, name='Normal Upper Limit', marker_color='#cbd5e1', opacity=0.6, text=normal_bounds, textposition='inside'))
        fig.add_trace(go.Bar(x=metrics_list, y=user_values, name='Patient Current Value', marker_color='#2563eb', text=user_values, textposition='outside'))
        fig.update_layout(barmode='group', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis_type="log", yaxis_title="Clinical Units (Log Scale)")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 🧮 Derived Clinical Metrics")
        if ast_alt_ratio > 2.0:
            st.error(f"⚠️ **De Ritis (AST/ALT) Ratio:** {ast_alt_ratio:.2f} (Elevated — May indicate deep tissue/liver injury)")
        else:
            st.info(f"ℹ️ **De Ritis (AST/ALT) Ratio:** {ast_alt_ratio:.2f} (Normal baseline range)")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="right-box">', unsafe_allow_html=True)
        st.subheader("🧠 Risk Analysis")

        if st.button("🔍 Analyze Risk"):
            data = np.array([[age, gender_val, ca19, lipase, amylase, glucose, bilirubin, alt, ast, wbc]]).astype(float)
            prediction = model.predict(data)[0]
            
            try:
                probabilities = model.predict_proba(data)[0]
                risk_percentage = probabilities[prediction] * 100
                prob_text = f" ({risk_percentage:.1f}% Confidence)"
            except:
                prob_text = ""

            if prediction == 0:
                st.success(f"🟢 Low Risk{prob_text}")
                risk = "Low Risk"
                advice = "- Maintain healthy diet\n- Exercise regularly\n- Annual health checkups"
            elif prediction == 1:
                st.warning(f"🟡 Medium Risk{prob_text}")
                risk = "Medium Risk"
                advice = "- Reduce sugar & fatty foods\n- Avoid alcohol & smoking\n- Monitor enzyme levels"
            else:
                st.error(f"🔴 High Risk{prob_text}")
                risk = "High Risk"
                advice = "- Consult a doctor immediately\n- Consider imaging tests (CT/MRI)\n- Strict dietary control"

            if symptoms:
                advice += "\n\n**⚠️ Symptom-Driven Advisory Additions:**"
                if "Jaundice (Yellowing of skin/eyes)" in symptoms or "Abdominal Pain" in symptoms:
                    advice += "\n- Immediate biliary tree evaluation recommended due to visible symptom presentations."
                if "Unexplained Weight Loss" in symptoms or "Loss of Appetite" in symptoms:
                    advice += "\n- Monitor nutritional intake closely and schedule functional GI imaging checks."

            st.markdown("### 📋 Preventive Measures")
            st.write(advice)

            st.markdown("### 🔍 Patient-Specific Risk Contributors")
            features = ["Age", "Gender", "CA19-9", "Lipase", "Amylase", "Glucose", "Bilirubin", "ALT", "AST", "WBC"]
            global_importance = model.feature_importances_

            patient_contributions = []
            for i, feat in enumerate(features):
                weight = global_importance[i]
                if feat in CLINICAL_NORMAL_MAX:
                    normal_max = CLINICAL_NORMAL_MAX[feat]
                    current_val = data[0][i]
                    direction = (current_val - normal_max) / normal_max if normal_max > 0 else 0.0
                    patient_contributions.append(direction * weight)
                else:
                    if feat == "Age":
                        patient_contributions.append(((age - 45) / 45) * weight)
                    else:
                        patient_contributions.append(0.01 * weight if gender_val == 1 else -0.01 * weight)

            contrib_df = pd.DataFrame({"Biomarker": features, "Impact Score": patient_contributions}).sort_values(by="Impact Score", key=abs, ascending=False)
            contrib_df['Risk Influence'] = contrib_df['Impact Score'].apply(lambda x: 'Increases Risk 🔺' if x > 0 else 'Reduces Risk 🔻')

            fig_contrib = px.bar(contrib_df, x="Impact Score", y="Biomarker", orientation='h', color='Risk Influence', color_discrete_map={'Increases Risk 🔺': '#ef4444', 'Reduces Risk 🔻': '#10b981'}, title="Biomarker Contribution to Current Diagnosis")
            fig_contrib.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_contrib, use_container_width=True)

            symptoms_joined = ", ".join(symptoms) if symptoms else "None Reported"
            report = f"Pancreatic Risk Report\nAge: {age}\nGender: {gender}\nSymptoms: {symptoms_joined}\nAST/ALT Ratio: {ast_alt_ratio:.2f}\nPredicted Risk: {risk}{prob_text}\n\nAdvice:\n{advice}"
            st.download_button(label="📄 Download Report", data=report, file_name="pancreas_report.txt", mime="text/plain")

        st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# MODULE 3B: CLINICIAN/DOCTOR WORKSPACE VIEW
# ==========================================
elif st.session_state.logged_in and st.session_state.user_role == "doctor":
    nav_left, nav_right = st.columns([9, 1.5])
    with nav_left:
        st.title("🩺 Clinician Command Center")
        st.caption("High-volume clinical data decision analytics pipeline — Authorized Provider Domain")
    with nav_right:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Change Domain", use_container_width=True):
            st.session_state.user_role = None
            st.rerun()

    st.subheader("📂 Ingest Patient Cohort Registry")
    uploaded_file = st.file_uploader("Upload electronic laboratory spreadsheet (.csv format)", type="csv")
    
    with st.expander("📌 View Spreadsheet Layout Guidelines"):
        st.markdown("""
        The uploaded file must contain the following exactly-named feature headers:
        `Age`, `Gender` (1 for Female, 0 for Male), `CA19-9`, `Lipase`, `Amylase`, `Glucose`, `Bilirubin`, `ALT`, `AST`, `WBC`.
        """)
        template_df = pd.DataFrame([[45, 0, 56, 120, 85, 95, 0.9, 35, 38, 7500], [68, 1, 145, 230, 190, 140, 2.1, 78, 92, 12500]], 
                                   columns=["Age", "Gender", "CA19-9", "Lipase", "Amylase", "Glucose", "Bilirubin", "ALT", "AST", "WBC"])
        template_csv = template_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Mock Template CSV", data=template_csv, file_name="pancreasafe_cohort_template.csv", mime="text/csv")

    if uploaded_file is not None:
        try:
            cohort_data = pd.read_csv(uploaded_file)
            required_cols = ["Age", "Gender", "CA19-9", "Lipase", "Amylase", "Glucose", "Bilirubin", "ALT", "AST", "WBC"]
            
            if not all(col in cohort_data.columns for col in required_cols):
                st.error("❌ Schema mismatch. Verify all required medical lab column names exist in your CSV file.")
            else:
                predictions = model.predict(cohort_data[required_cols].values)
                probabilities = model.predict_proba(cohort_data[required_cols].values)
                
                cohort_data['Predicted_Risk_ID'] = predictions
                cohort_data['Risk Category'] = cohort_data['Predicted_Risk_ID'].map({0: "🟢 Low Risk", 1: "🟡 Medium Risk", 2: "🔴 High Risk"})
                cohort_data['Confidence %'] = [round(prob[pred] * 100, 1) for prob, pred in zip(probabilities, predictions)]
                cohort_data['AST/ALT Ratio'] = (cohort_data['AST'] / cohort_data['ALT']).round(2).fillna(0.0)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader("📊 Fleet Cohort Statistics")
                m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                
                with m_col1:
                    st.markdown(f'<div class="metric-tile" style="border-left-color: #64748b;"><h5>Total Ingested Records</h5><h2>{len(cohort_data)}</h2></div>', unsafe_allow_html=True)
                with m_col2:
                    high_risk_count = len(cohort_data[cohort_data['Predicted_Risk_ID'] == 2])
                    st.markdown(f'<div class="metric-tile" style="border-left-color: #ef4444;"><h5>High Risk Flagged</h5><h2>{high_risk_count}</h2></div>', unsafe_allow_html=True)
                with m_col3:
                    med_risk_count = len(cohort_data[cohort_data['Predicted_Risk_ID'] == 1])
                    st.markdown(f'<div class="metric-tile" style="border-left-color: #eab308;"><h5>Medium Risk Flagged</h5><h2>{med_risk_count}</h2></div>', unsafe_allow_html=True)
                with m_col4:
                    mean_ratio = cohort_data['AST/ALT Ratio'].mean()
                    st.markdown(f'<div class="metric-tile" style="border-left-color: #10b981;"><h5>Mean AST/ALT Ratio</h5><h2>{mean_ratio:.2f}</h2></div>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader("📋 Priority Triage Routing Queue")
                
                display_df = cohort_data[["Risk Category", "Confidence %", "AST/ALT Ratio", "Age", "CA19-9", "Lipase", "Amylase", "Glucose", "Bilirubin"]]
                st.dataframe(display_df.sort_values(by=["Risk Category", "Confidence %"], ascending=[False, False]), use_container_width=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader("📈 Cohort Clustering Analytics")
                
                fig_scatter = px.scatter(
                    cohort_data,
                    x="CA19-9",
                    y="Lipase",
                    color="Risk Category",
                    size="Age",
                    hover_data=["Amylase", "AST/ALT Ratio"],
                    color_discrete_map={"🟢 Low Risk": "#10b981", "🟡 Medium Risk": "#eab308", "🔴 High Risk": "#ef4444"},
                    title="Biomarker Cluster Matrix: CA19-9 vs. Lipase Concentration"
                )
                fig_scatter.update_layout(plot_bgcolor='rgba(255,255,255,1)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_scatter, use_container_width=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                processed_csv = cohort_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export Evaluated Triage Data (.CSV)",
                    data=processed_csv,
                    file_name="processed_triage_manifest.csv",
                    mime="text/csv",
                    type="primary"
                )
                
        except Exception as e:
            st.error(f"❌ File compilation pipeline aborted. Check file integrity. Details: {e}")