import pandas as pd
import os
from openai import OpenAI


# 1. Initialize OpenAI Client

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# 2. Load Dataset

data = pd.read_csv("data.csv")
data.fillna(0, inplace=True)


# 3. Risk Assessment Logic

def assess_risk(row):
    if row["credit_utilization"] > 0.8 and row["missed_payments"] >= 3:
        return "High"
    elif row["credit_utilization"] > 0.5 or row["missed_payments"] >= 1:
        return "Medium"
    else:
        return "Low"

data["risk_level"] = data.apply(assess_risk, axis=1)


# 4. AI Explanation (LATEST OpenAI API)

def generate_ai_explanation(row):
    prompt = f"""
You are a financial risk analyst.
Explain the customer's credit risk clearly in 2–3 professional sentences.

Details:
Income: {row['income']}
Credit Utilization: {row['credit_utilization']}
Missed Payments: {row['missed_payments']}
Outstanding Balance: {row['outstanding_balance']}
Risk Level: {row['risk_level']}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You explain financial risk clearly."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()

    except Exception:
        # Fallback logic (NO API COST)
        if row["risk_level"] == "High":
            return (
                "High credit utilization combined with multiple missed payments "
                "indicates a strong likelihood of delinquency and requires immediate attention."
            )
        elif row["risk_level"] == "Medium":
            return (
                "Moderate credit usage or limited missed payments suggest potential risk. "
                "The account should be closely monitored."
            )
        else:
            return (
                "Low credit utilization and stable payment behavior indicate minimal delinquency risk."
            )


# 5. Agent Actions

def agent_action(row):
    if row["risk_level"] == "High":
        return "Flag account and recommend immediate collections follow-up"
    elif row["risk_level"] == "Medium":
        return "Send reminder and monitor account"
    else:
        return "No action required"

data["agent_action"] = data.apply(agent_action, axis=1)


# 6. Save Outputs

# Ensure column exists
if "ai_explanation" not in data.columns:
    data["ai_explanation"] = "Explanation not available"

data.to_csv("risk_assessment_output.csv", index=False)

with open("report.txt", "w") as file:
    file.write("AI-Powered Credit Risk Assessment Report\n")
    file.write("=" * 50 + "\n\n")

    for _, row in data.iterrows():
        file.write(f"Customer ID: {row['customer_id']}\n")
        file.write(f"Risk Level: {row['risk_level']}\n")
        file.write(f"AI Explanation: {row['ai_explanation']}\n")
        file.write(f"Recommended Action: {row['agent_action']}\n")
        file.write("-" * 50 + "\n")

print("AI Agent executed successfully.")
