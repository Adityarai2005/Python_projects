from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

# Load model and encoders
model = joblib.load("simple_forecast_model.pkl")
le_day = joblib.load("day_encoder.pkl")
le_subject = joblib.load("subject_encoder.pkl")
df = pd.read_csv("sample_forecast_data.csv")

app = FastAPI()

class AttendanceRequest(BaseModel):
    day: str
    subject: str

@app.post("/predict")
def predict_attendance(data: AttendanceRequest):
    try:
        day_encoded = le_day.transform([data.day])[0]
        subject_encoded = le_subject.transform([data.subject])[0]
        prediction = model.predict(np.array([[day_encoded, subject_encoded]]))[0]
        return {
            "day": data.day,
            "subject": data.subject,
            "prediction": "✅ Attending" if prediction == 1 else "❌ Not Attending"
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/insights/subjects")
def subject_insights():
    stats = df.groupby("subject")["attended"].mean().reset_index()
    stats["attendance_rate"] = (stats["attended"] * 100).round(2)
    return stats[["subject", "attendance_rate"]].to_dict(orient="records")

@app.get("/insights/days")
def day_insights():
    stats = df.groupby("day")["attended"].mean().reset_index()
    stats["attendance_rate"] = (stats["attended"] * 100).round(2)
    return stats[["day", "attendance_rate"]].to_dict(orient="records")

@app.get("/insights/summary")
def summary_insight():
    total_classes = len(df)
    attended_classes = df["attended"].sum()
    return {
        "total_classes": total_classes,
        "attended_classes": int(attended_classes),
        "attendance_percentage": round((attended_classes / total_classes) * 100, 2)
    }
