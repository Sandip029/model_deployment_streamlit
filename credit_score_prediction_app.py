# -*- coding: utf-8 -*-
"""credit_score_prediction_app

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RS5j5t96_TF4rdkQRd5zZgTMXd6xyvzX
"""

import subprocess
import sys

!pip install gdown

import gdown
import streamlit as st
import joblib
import pandas as pd
import requests
from joblib import load
from sklearn.preprocessing import LabelEncoder
from sklearn.base import BaseEstimator, TransformerMixin

import warnings
warnings.filterwarnings('ignore')

class FeatureEngineering(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X['Age_Income_Interaction'] = X['Age'] * X['Annual_Income']
        X['Debt_Income_Ratio'] = X['Outstanding_Debt'] / X['Annual_Income']

        selected_features = [
            'Age', 'Outstanding_Debt', 'Credit_Mix', 'Debt_Income_Ratio', 'Interest_Rate',
            'Age_Income_Interaction', 'Total_EMI_per_month', 'Num_Credit_Inquiries',
            'Delay_from_due_date', 'Payment_of_Min_Amount_encoded', 'Num_Credit_Card',
            'Num_Bank_Accounts', 'Credit_History_Age', 'Num_of_Delayed_Payment'
        ]

        return X[selected_features]

class CustomEncoder(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        X = X.copy()
        X['Credit_Score'] = LabelEncoder().fit_transform(X['Credit_Score'])
        self.occupation_means = X.groupby('Occupation')['Credit_Score'].mean()
        self.payment_of_min_amount_means = X.groupby('Payment_of_Min_Amount')['Credit_Score'].mean()
        self.payment_behaviour_means = X.groupby('Payment_Behaviour')['Credit_Score'].mean()
        self.credit_mix_map = {'Bad': 0, 'Standard': 1, 'Good': 2}
        return self

    def transform(self, X):
        X = X.copy()
        X['Occupation_encoded'] = X['Occupation'].map(self.occupation_means)
        X['Payment_of_Min_Amount_encoded'] = X['Payment_of_Min_Amount'].map(self.payment_of_min_amount_means)
        X['Payment_Behaviour_encoded'] = X['Payment_Behaviour'].map(self.payment_behaviour_means)
        X['Credit_Mix'] = X['Credit_Mix'].map(self.credit_mix_map)

        X.drop(['Occupation', 'Payment_of_Min_Amount', 'Payment_Behaviour'], axis=1, inplace=True)

        return X

# Download and load the dataset
url = 'https://drive.google.com/uc?id=1SHSBrl9T7qDoiQThluyfBJyPBg49iz0D'
output = 'dataset.csv'
gdown.download(url, output, quiet=False)
data = pd.read_csv(output)

label_encoder = LabelEncoder()
credit_score_mapping = {'Poor': 0, 'Standard': 1, 'Good': 2}
data['Credit_Score'] = data['Credit_Score'].map(credit_score_mapping)
label_encoder.fit(data['Credit_Score'])

custom_encoder = CustomEncoder()
data_transformed = custom_encoder.fit_transform(data)

url = 'https://drive.google.com/uc?id=1PsAdcOZx-FateAgSuXcDdIYRnvjTlX8b'
output = 'best_pipeline_credit.sav'
response = requests.get(url)
with open(output, 'wb') as f:
    f.write(response.content)

# Load the sav file
pipeline = load(output)

st.title('Credit Score Prediction')

ID = st.number_input('ID', min_value=1, value=1)
Customer_ID = st.number_input('Customer_ID', min_value=1, value=1)
Month = st.number_input('Month', min_value=1, max_value=12, value=7)
Name = st.text_input('Name', 'John Doe')
Age = st.number_input('Age', min_value=14, max_value=100, value=30)
SSN = st.text_input('SSN', '123-45-6789')
Occupation = st.selectbox('Occupation', ['Lawyer', 'Engineer', 'Architect', 'Mechanic', 'Scientist', 'Accountant', 'Developer', 'Media_Manager', 'Teacher','Entrepreneur', 'Doctor', 'Journalist', 'Manager', 'Musician', 'Writer'], index=1)
Annual_Income = st.number_input('Annual_Income', min_value=1000, value=50000)
Monthly_Inhand_Salary = st.number_input('Monthly_Inhand_Salary', min_value=100, value=4000)
Num_Bank_Accounts = st.number_input('Num_Bank_Accounts', min_value=1, value=2)
Num_Credit_Card = st.number_input('Num_Credit_Card', min_value=0, value=1)
Interest_Rate = st.number_input('Interest_Rate', min_value=1.0, format="%.2f", value=5.0)
Num_of_Loan = st.number_input('Num_of_Loan', min_value=0, value=1)
Type_of_Loan = st.selectbox('Type_of_Loan', ['Personal', 'Home', 'Car', 'Education'])
Delay_from_due_date = st.number_input('Delay_from_due_date', min_value=0, value=0)
Num_of_Delayed_Payment = st.number_input('Num_of_Delayed_Payment', min_value=0, value=1)
Changed_Credit_Limit = st.number_input('Changed_Credit_Limit', min_value=0, value=5000)
Num_Credit_Inquiries = st.number_input('Num_Credit_Inquiries', min_value=0, value=1)
Credit_Mix = st.selectbox('Credit_Mix', ['Bad', 'Standard', 'Good'])
Outstanding_Debt = st.number_input('Outstanding_Debt', min_value=0, value=1000)
Credit_Utilization_Ratio = st.number_input('Credit_Utilization_Ratio', min_value=20, value=30)
Credit_History_Age = st.number_input('Credit_History_Age', min_value=0, value=5)
Payment_of_Min_Amount = st.selectbox('Payment_of_Min_Amount', ['Yes', 'No'])
Total_EMI_per_month = st.number_input('Total_EMI_per_month', min_value=0, value=300)
Amount_invested_monthly = st.number_input('Amount_invested_monthly', min_value=0, value=1000)
Payment_Behaviour = st.selectbox('Payment_Behaviour', ['Low', 'Medium', 'High'])
Monthly_Balance = st.number_input('Monthly_Balance', min_value=-5000, value=1000)

new_data = pd.DataFrame({
    'ID': [ID],
    'Customer_ID': [Customer_ID],
    'Month': [Month],
    'Name': [Name],
    'Age': [Age],
    'SSN': [SSN],
    'Occupation': [Occupation],
    'Annual_Income': [Annual_Income],
    'Monthly_Inhand_Salary': [Monthly_Inhand_Salary],
    'Num_Bank_Accounts': [Num_Bank_Accounts],
    'Num_Credit_Card': [Num_Credit_Card],
    'Interest_Rate': [Interest_Rate],
    'Num_of_Loan': [Num_of_Loan],
    'Type_of_Loan': [Type_of_Loan],
    'Delay_from_due_date': [Delay_from_due_date],
    'Num_of_Delayed_Payment': [Num_of_Delayed_Payment],
    'Changed_Credit_Limit': [Changed_Credit_Limit],
    'Num_Credit_Inquiries': [Num_Credit_Inquiries],
    'Credit_Mix': [Credit_Mix],
    'Outstanding_Debt': [Outstanding_Debt],
    'Credit_Utilization_Ratio': [Credit_Utilization_Ratio],
    'Credit_History_Age': [Credit_History_Age],
    'Payment_of_Min_Amount': [Payment_of_Min_Amount],
    'Total_EMI_per_month': [Total_EMI_per_month],
    'Amount_invested_monthly': [Amount_invested_monthly],
    'Payment_Behaviour': [Payment_Behaviour],
    'Monthly_Balance': [Monthly_Balance]
})

new_data_transformed = custom_encoder.transform(new_data)

if st.button('Predict Score'):
    try:
        predicted_score = pipeline.predict(new_data_transformed)
        score_label = label_encoder.inverse_transform(predicted_score)[0]
        score_text = [key for key, value in credit_score_mapping.items() if value == score_label][0]
        st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; padding: 10px; border: 2px solid #4CAF50; border-radius: 10px; background-color: #f9f9f9; margin-top: 20px;">
                <h2 style="color: #4CAF50;">The Predicted Credit Score is: {score_text}</h2>
            </div>
        """, unsafe_allow_html=True)
    except KeyError as e:
        st.error(f"Error: {e}")