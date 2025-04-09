from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import joblib
from datetime import datetime
import plotly.express as px
import plotly.io as pio

app = FastAPI()
model = joblib.load("enhanced_decision_tree_model.pkl")
df = pd.read_csv("sample.csv")

df['hour'] = df['time'].apply(lambda x: int(x.split(":")[0]))
df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
df['subject_code'] = df['subject'].astype('category').cat.codes
X = df[['hour', 'sleep_hours', 'day_of_week', 'subject_code']]
df['predicted_attendance'] = model.predict(X)

low_sleep_morning = df[(df['hour'] < 10) & (df['sleep_hours'] < 6) & (df['predicted_attendance'] == 0)]
drowsy_afternoon = df[(df['hour'].between(13, 16)) & (df['predicted_attendance'] == 0)]

subject_attendance = df.groupby('subject')['attended'].mean().reset_index()
day_attendance = df.groupby('day_of_week')['attended'].mean().reset_index()

subject_fig = px.bar(subject_attendance, x='subject', y='attended', title='Subject-wise Attendance')
day_fig = px.bar(day_attendance, x='day_of_week', y='attended', title='Day-wise Attendance')

subject_chart = pio.to_html(subject_fig, full_html=False)
day_chart = pio.to_html(day_fig, full_html=False)

@app.get("/insights", response_class=HTMLResponse)
def get_insights():
    html_content = f"""
    <html>
        <head><title>Student Attendance Insights</title></head>
        <body>
            <h1>📊 Student Attendance Insights</h1>
            <p><strong>❗ Missed morning classes due to low sleep:</strong> {len(low_sleep_morning)} times</p>
            <p><strong>💤 Missed afternoon classes (possible drowsiness):</strong> {len(drowsy_afternoon)} times</p>
            <h2>📚 Subject-wise Attendance</h2>
            {subject_chart}
            <h2>📅 Day-wise Attendance</h2>
            {day_chart}
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
#pip install fastapi uvicorn pandas plotly joblib
#uvicorn app:app --reload