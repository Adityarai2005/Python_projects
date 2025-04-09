import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib
data = {
    "date": ["2025-04-01", "2025-04-01", "2025-04-02", "2025-04-02", "2025-04-03", "2025-04-03", "2025-04-04", "2025-04-04"],
    "time": ["08:00", "14:00", "09:00", "13:00", "11:00", "15:00", "08:00", "12:00"],
    "sleep_hours": [5.5, 5.5, 6.0, 6.0, 7.0, 7.0, 4.5, 4.5],
    "subject": ["Math", "English", "Chemistry", "Math", "English", "Math", "Chemistry", "English"],
    "attended": [0, 0, 1, 0, 1, 1, 0, 1]
}

df = pd.DataFrame(data)
df['hour'] = df['time'].apply(lambda x: int(x.split(":")[0]))
df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
df['subject_code'] = df['subject'].astype('category').cat.codes

X = df[['hour', 'sleep_hours', 'day_of_week', 'subject_code']]
y = df['attended']
model = DecisionTreeClassifier()
model.fit(X, y)
joblib.dump(model, "enhanced_decision_tree_model.pkl")
print("✅ Model saved as enhanced_decision_tree_model.pkl")
