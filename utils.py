from sklearn.preprocessing import StandardScaler
from typing import Optional
import logging
from fastapi import Header, HTTPException
from jose.jwt import decode as jwt_decode
from jose.exceptions import JWTError


JWT_SECRET_KEY = "secretkey"
ALGORITHM = "HS256"

# Define function for Standarization
def standardize(data: dict) -> dict:
    """
    This function standardizes data using StandardScaler.
    """
    new_data = dict()
    for key in data.keys():
        sensor_data = [[el] for el in data[key]]
        stdsc = StandardScaler()
        standardized_data = stdsc.fit_transform(sensor_data)
        new_key = key.replace("_", "")
        new_data[new_key] = standardized_data.flatten().tolist()
    logging.info("Data standardization successful.")
    return new_data

# Authorization function with JWT
def verify_jwt(authorization: Optional[str] = Header()):
    """
    This function verifies if user has a valid JWT token.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="No token provided")
    jwt_token = authorization.split(" ", 1)[1]
    try:
        jwt_decode(token=jwt_token, key=JWT_SECRET_KEY, algorithms=ALGORITHM)
        logging.info("User is authorized to access protected functions.")
    except JWTError:
        raise HTTPException(status_code=401, detail="Unauthorized token")