import logging
from fastapi import FastAPI, Depends
from jose.jwt import encode as jwt_encode

from models import StandardizedData, SensorData
from utils import standardize, verify_jwt, JWT_SECRET_KEY, ALGORITHM

app = FastAPI()


# Authentication function
@app.post("/api/v1/token")
def login_for_access_token(payload: dict):
    """
    This function authenticates the user with the credentials provided.
    """
    # Check user authentication here
    access_token = jwt_encode(claims=payload, key=JWT_SECRET_KEY, algorithm=ALGORITHM)
    logging.info("User authentication successful.")
    return {"access_token": access_token, "token_type": "bearer"}


# Data Standardization function secured with JWT
@app.post(
    "/api/v1/standarize",
    response_model=StandardizedData,
    dependencies=[Depends(verify_jwt)],
)
def standardize_data(data: SensorData):
    """
    This function standardizes the input data using the standardize function.
    """
    try:
        result = standardize(data)
        logging.info("Data has been standardized successfully.")
    except Exception as e:
        logging.error("Data standardization error.")
        return {"success": False}
    return {"success": True, "result": result}
