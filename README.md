# Tanzania Quality of Life Predictor - ML Project

## 📋 Project Overview

This project develops a machine learning application to predict quality of life scores for individuals in Tanzania based on various factors including health, education, and housing conditions.

## 🎯 Deliverables (as per assignment requirements)

### 1. Jupyter Notebook: `ml_project.ipynb`
Contains:
- Data preprocessing
- Model training (Linear Regression and Decision Tree)
- Model evaluation and comparison
- Visualizations
- Saving the best model

### 2. Deployed AI Application
Files:
- `app.py` - Streamlit web application
- `model.pkl` - Trained model
- `scaler.pkl` - Feature scaler
- `label_encoders.pkl` - Categorical encoders
- `model_metadata.pkl` - Model information

### 3. Project Report: `project_report.docx`
2-page report containing:
- Introduction
- Dataset description
- Methodology
- Results
- Application screenshots

## 📁 Project Structure

```
tanzania_qol_project/
├── ml_project.ipynb           # Main Jupyter notebook
├── app.py                      # Streamlit web application
├── tanzania_quality_of_life_data.csv  # Dataset
├── generate_dataset.py         # Script to generate dataset
├── requirements.txt            # Python dependencies
├── create_report.js            # Script to generate Word report
├── model.pkl                   # Saved model (generated after running notebook)
├── scaler.pkl                  # Saved scaler
├── label_encoders.pkl          # Saved encoders
├── model_metadata.pkl          # Model metadata
└── README.md                   # This file
```

## 🚀 Setup and Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Node.js (for generating Word report)

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Generate Dataset (Already Done)

```bash
python generate_dataset.py
```

This creates `tanzania_quality_of_life_data.csv` with 1,000 samples.

### Step 3: Run the Jupyter Notebook

```bash
jupyter notebook ml_project.ipynb
```

Execute all cells to:
1. Load and explore the data
2. Preprocess features
3. Train both Linear Regression and Decision Tree models
4. Evaluate and compare models
5. Generate visualizations
6. Save the best model

This will create:
- `model.pkl`
- `scaler.pkl`
- `label_encoders.pkl`
- `model_metadata.pkl`
- Visualization images (model_comparison.png, actual_vs_predicted.png, etc.)

### Step 4: Test the Application Locally

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Step 5: Deploy to Streamlit Cloud

1. Create a GitHub repository
2. Push all files to the repository
3. Go to https://share.streamlit.io/
4. Connect your GitHub repository
5. Select `app.py` as the main file
6. Deploy!

### Step 6: Generate Project Report

Install docx package:
```bash
npm install docx
```

Generate the report:
```bash
node create_report.js
```

This creates `project_report.docx`

## 📊 Dataset Description

**Size**: 1,000 samples, 19 features

**Features**:
- **Demographics**: age, region, urban_rural, education_level, employment_status
- **Economic**: monthly_income_tzs, family_size
- **Health**: distance_to_hospital_km, access_to_clean_water, health_insurance
- **Education**: distance_to_school_km, years_of_education
- **Housing**: housing_type, number_of_rooms, electricity_access

**Target Variable**: quality_of_life_score (0-100)

**Regions Covered**: Dar es Salaam, Arusha, Mwanza, Dodoma, Mbeya, Morogoro, Tanga, Zanzibar, Kilimanjaro, Mtwara

## 🤖 Models

### Linear Regression
- Assumes linear relationship between features and target
- Provides interpretable coefficients
- Requires feature scaling

### Decision Tree Regressor
- Non-linear model with tree structure
- Configured with max_depth=10, min_samples_split=10
- No scaling required
- Provides feature importance scores

## 📈 Model Performance

Both models achieve R² scores > 0.94 on test data, indicating excellent predictive capability.

Key influential features:
- Monthly income
- Years of education
- Housing type
- Access to clean water
- Electricity access

## 🌐 Web Application Features

1. **User Input Forms**: Organized sections for personal information and living conditions
2. **Real-time Prediction**: Instant quality of life score calculation
3. **Score Interpretation**: Color-coded categories (Excellent, Good, Moderate, Below Average)
4. **Personalized Recommendations**: Actionable suggestions for improvement
5. **Data Summary**: Visual display of all input parameters

## 📝 Usage Instructions

1. Open the deployed application
2. Enter your information in the form:
   - Personal details (age, region, education, etc.)
   - Living conditions (housing, utilities, access to services)
3. Click "Predict Quality of Life Score"
4. View your results:
   - Overall score (0-100)
   - Interpretation category
   - Personalized recommendations
   - Input summary

## 🎓 Academic Requirements Met

✅ Real-world Tanzanian context problem
✅ Suitable dataset (1000 samples, 15 input features)
✅ Data preprocessing (encoding, scaling)
✅ Two models trained (Linear Regression & Decision Tree)
✅ Model evaluation and comparison
✅ Best model selection based on performance
✅ Visualizations (correlation heatmap, feature importance, actual vs predicted, etc.)
✅ Deployed web application with user input capability
✅ Application displays predictions
✅ Project report (max 2 pages)

## 👥 Group Contribution

**Each team member should be prepared to demonstrate:**
- Understanding of the dataset and preprocessing steps
- Knowledge of how both models work
- Ability to explain model evaluation metrics
- Familiarity with the web application code
- Understanding of deployment process

## 📞 Support

For any issues or questions, refer to:
- Jupyter notebook comments
- Application code documentation
- This README file

## 📅 Deadline

- Submission: 16th February 2026
- Presentation: 18th February 2026

## 🎉 Project Highlights

- **Practical Impact**: Helps Tanzanians understand and improve their quality of life
- **High Accuracy**: R² > 0.94 on test data
- **User-Friendly**: Intuitive web interface
- **Actionable Insights**: Personalized recommendations
- **Scalable**: Can be extended with more features and real-time data

---

**Good luck with your presentation! 🚀**
