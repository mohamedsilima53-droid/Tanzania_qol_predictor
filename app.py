"""
Tanzania Quality of Life Predictor
Web Application using Streamlit
"""

import streamlit as st
import pandas as pd
import numpy as np
import os

# Page configuration
st.set_page_config(
    page_title="Tanzania Quality of Life Predictor",
    page_icon="🏠",
    layout="wide"
)

# Try to import joblib
try:
    import joblib
except ImportError:
    st.error("Please install joblib: pip install joblib")
    st.stop()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .prediction-box {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin: 2rem 0;
    }
    .score-display {
        font-size: 4rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    .score-excellent { color: #28a745; }
    .score-good { color: #17a2b8; }
    .score-fair { color: #ffc107; }
    .score-poor { color: #dc3545; }
</style>
""", unsafe_allow_html=True)

# Load model components
@st.cache_resource
def load_model_components():
    """Load all saved model components"""
    try:
        # Debug: Show current directory and files
        current_dir = os.getcwd()
        files_in_dir = os.listdir('.')
        
        # Check if required files exist
        required_files = {
            'model.pkl': 'Trained model',
            'label_encoders.pkl': 'Category encoders',
            'model_metadata.pkl': 'Model configuration'
        }
        
        missing = []
        for file, desc in required_files.items():
            if not os.path.exists(file):
                missing.append(f"{file} ({desc})")
        
        if missing:
            st.error("⚠️ Missing required files:")
            for m in missing:
                st.error(f"  • {m}")
            st.info(f"📁 Current directory: {current_dir}")
            st.info(f"📄 Files found: {', '.join([f for f in files_in_dir if f.endswith('.pkl')])}")
            return None, None, None, None
        
        # Load files
        model = joblib.load('model.pkl')
        label_encoders = joblib.load('label_encoders.pkl')
        metadata = joblib.load('model_metadata.pkl')
        
        # Load scaler if needed
        scaler = None
        if metadata.get('use_scaling', False):
            if os.path.exists('scaler.pkl'):
                scaler = joblib.load('scaler.pkl')
        
        st.success("✅ Model loaded successfully!")
        return model, metadata, label_encoders, scaler
        
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        return None, None, None, None

# Load components
model, metadata, label_encoders, scaler = load_model_components()

# Title
st.markdown('<h1 class="main-header">🏠 Tanzania Quality of Life Predictor</h1>', unsafe_allow_html=True)
st.markdown("---")

# Only show app if model loaded successfully
if model is None:
    st.stop()

# Sidebar info
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    This application predicts Quality of Life scores for individuals in Tanzania.
    """)
    
    if metadata:
        st.header("📊 Model Info")
        st.write(f"**Type**: {metadata.get('model_type', 'Unknown').replace('_', ' ').title()}")
        st.write(f"**R² Score**: {metadata.get('test_r2_score', 0):.4f}")
        st.write(f"**RMSE**: {metadata.get('test_rmse', 0):.4f}")
    
    st.header("🎯 Score Guide")
    st.write("""
    - **80-100**: Excellent
    - **60-79**: Good  
    - **40-59**: Fair
    - **0-39**: Needs Improvement
    """)

# Main prediction form
st.header("📝 Enter Your Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("👤 Personal")
    age = st.number_input("Age", 18, 100, 30)
    
    regions = ['Dar es Salaam', 'Arusha', 'Mwanza', 'Dodoma', 'Mbeya', 
               'Morogoro', 'Tanga', 'Kagera', 'Shinyanga', 'Mara',
               'Kilimanjaro', 'Tabora', 'Pwani', 'Rukwa', 'Kigoma']
    region = st.selectbox("Region", regions)
    
    area_type = st.radio("Area Type", ["Urban", "Rural"])
    family_size = st.number_input("Family Size", 1, 15, 4)

with col2:
    st.subheader("🎓 Education & Work")
    
    education_level = st.selectbox("Education Level",
        ["No Education", "Primary", "Secondary", "Certificate", "Diploma", "Degree"])
    
    education_years_map = {
        "No Education": 0, "Primary": 7, "Secondary": 11,
        "Certificate": 13, "Diploma": 15, "Degree": 17
    }
    years_of_education = education_years_map[education_level]
    
    employment = st.selectbox("Employment",
        ["Unemployed", "Informal Employment", "Formal Employment", "Self Employed", "Student"])
    
    income = st.number_input("Monthly Income (TZS)", 0, 10000000, 500000, 50000)
    
    distance_to_school = st.number_input("Distance to School (km)", 0.0, 100.0, 2.0, 0.5)

with col3:
    st.subheader("🏥 Health & Housing")
    
    distance_to_hospital = st.number_input("Distance to Hospital (km)", 0.0, 200.0, 5.0, 0.5)
    
    clean_water = st.radio("Clean Water Access", ["No", "Yes"])
    electricity = st.radio("Electricity", ["No", "Yes"])
    health_insurance = st.radio("Health Insurance", ["No", "Yes"])
    
    housing_type = st.selectbox("Housing Type",
        ["Mud/Grass", "Unburnt Bricks", "Burnt Bricks", "Cement/Concrete"])
    
    rooms = st.number_input("Number of Rooms", 1, 15, 3)

# Calculate component scores
def calculate_scores(inputs):
    """Calculate health, education, and housing component scores"""
    # Health score
    health = 50
    if inputs['distance_to_hospital_km'] < 5: health += 20
    elif inputs['distance_to_hospital_km'] < 15: health += 10
    if inputs['access_to_clean_water']: health += 15
    if inputs['health_insurance']: health += 15
    
    # Education score
    education = 50 + (inputs['years_of_education'] * 2)
    if inputs['distance_to_school_km'] < 3: education += 10
    elif inputs['distance_to_school_km'] < 10: education += 2
    
    # Housing score
    housing_map = {"Mud/Grass": 50, "Unburnt Bricks": 70, "Burnt Bricks": 85, "Cement/Concrete": 100}
    housing = housing_map.get(inputs['housing_type'], 50)
    if inputs['electricity_access']: housing = min(100, housing + 10)
    
    return min(100, health), min(100, education), min(100, housing)

# Prediction button
if st.button("🔮 Predict Quality of Life", type="primary", use_container_width=True):
    
    # Prepare input
    input_data = {
        'age': age,
        'region_encoded': label_encoders['region'].transform([region])[0],
        'urban_rural_encoded': label_encoders['urban_rural'].transform([area_type])[0],
        'education_level_encoded': label_encoders['education_level'].transform([education_level])[0],
        'employment_status_encoded': label_encoders['employment_status'].transform([employment])[0],
        'monthly_income_tzs': income,
        'family_size': family_size,
        'distance_to_hospital_km': distance_to_hospital,
        'distance_to_school_km': distance_to_school,
        'access_to_clean_water': 1 if clean_water == "Yes" else 0,
        'electricity_access': 1 if electricity == "Yes" else 0,
        'housing_type_encoded': label_encoders['housing_type'].transform([housing_type])[0],
        'years_of_education': years_of_education,
        'number_of_rooms': rooms,
        'health_insurance': 1 if health_insurance == "Yes" else 0,
        'housing_type': housing_type
    }
    
    # Calculate component scores
    health_score, edu_score, house_score = calculate_scores(input_data)
    input_data['health_score'] = health_score
    input_data['education_score'] = edu_score
    input_data['housing_score'] = house_score
    
    # Prepare for model
    input_df = pd.DataFrame([input_data])
    
    try:
        # Make prediction
        if metadata.get('use_scaling', False) and scaler is not None:
            input_scaled = scaler.transform(input_df)
            prediction = model.predict(input_scaled)[0]
        else:
            prediction = model.predict(input_df)[0]
        
        prediction = max(0, min(100, prediction))
        
        # Display result
        st.markdown("---")
        st.header("📊 Your Results")
        
        # Determine category
        if prediction >= 80:
            category, emoji, color = "Excellent", "🌟", "score-excellent"
        elif prediction >= 60:
            category, emoji, color = "Good", "😊", "score-good"
        elif prediction >= 40:
            category, emoji, color = "Fair", "😐", "score-fair"
        else:
            category, emoji, color = "Needs Improvement", "😟", "score-poor"
        
        # Display score
        st.markdown(f"""
        <div class="prediction-box">
            <h2>Your Quality of Life Score</h2>
            <div class="score-display {color}">{prediction:.1f}/100</div>
            <h3>{emoji} {category}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Component breakdown
        st.subheader("📋 Score Breakdown")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏥 Health", f"{health_score:.0f}/100")
        with col2:
            st.metric("🎓 Education", f"{edu_score:.0f}/100")
        with col3:
            st.metric("🏠 Housing", f"{house_score:.0f}/100")
        
        # Recommendations
        st.markdown("---")
        st.subheader("💡 Recommendations")
        
        recs = []
        if health_score < 70:
            recs.append("🏥 Consider living closer to health facilities or getting health insurance")
        if edu_score < 70:
            recs.append("🎓 Invest in further education or skills training")
        if house_score < 70:
            recs.append("🏠 Work towards improving housing quality and utilities")
        if income < 500000:
            recs.append("💰 Explore income growth opportunities")
        if not input_data['access_to_clean_water']:
            recs.append("💧 Prioritize access to clean water")
        if not input_data['electricity_access']:
            recs.append("⚡ Access to electricity improves quality of life")
        
        if recs:
            for r in recs:
                st.write(r)
        else:
            st.success("✅ Great! You're doing well in all areas!")
            
    except Exception as e:
        st.error(f"❌ Prediction error: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Tanzania Quality of Life Predictor | ML Project 2026</p>
</div>
""", unsafe_allow_html=True)
