from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

MODEL_PATH = r'..\..\model\panel_model.joblib'

model = joblib.load(MODEL_PATH)

class ProjectInput(BaseModel):
    project_area: int
    project_type: int

@app.post("/predict-panel")
def predict_panel(input: ProjectInput):

    X_input = pd.DataFrame([{
        "type_encoded": input.project_type,
        "area_encoded": input.project_area
    }])
    
    # Get prediction probabilities
    probabilities = model.predict_proba(X_input)[0]
    class_indices = model.classes_

    # Return as dictionary
    result = {str(class_id): round(prob, 4) for class_id, prob in zip(class_indices, probabilities)}
    return {"predictions": result}
