import json
from fastapi.testclient import TestClient
from fastapi import status
from jose import jwt
import numpy as np
from unittest.mock import patch

from utils import standardize, JWT_SECRET_KEY, ALGORITHM
from run import app

client = TestClient(app)


def generate_token(payload):
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)


class TestStandarization:

    headers = {"Authorization": "Bearer {}".format(generate_token({"user": 3}))}

    @patch("utils.StandardScaler")
    def test_standardize(self, mock_scaler):
        # Mock data
        data = {"sensor_1": [1, 2, 3], "sensor_2": [4, 5, 6]}
        expected_result = {
            "sensor1": [-1.224744871391589, 0.0, 1.224744871391589],
            "sensor2": [-1.224744871391589, 0.0, 1.224744871391589],
        }
        mock_scaler().fit_transform.return_value = np.asarray([
            [-1.224744871391589],
            [0.0],
            [1.224744871391589],
        ])

        # Call function and assert result
        result = standardize(data)
        assert result == expected_result

    def test_standarization_post_payload(self):
        input_data = {
            "sensor_1": [5.44, 3.22, 6.55, 8.54, 1.24],
            "sensor_2": [5444.44, 33.22, 622.55, 812.54, 1233.24],
            "sensor_3": [0.44, 0.22, 0.55, 0.54, 0.24],
        }
        response = client.post(
            "/api/v1/standarize", headers=self.headers, data=json.dumps(input_data)
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "success": True,
            "result": {
                "sensor1": [
                    0.17354382198293136,
                    -0.6981016187458169,
                    0.6093665423473053,
                    1.3907063743519035,
                    -1.475515119936322,
                ],
                "sensor2": [
                    1.9602614701628547,
                    -0.8200093678533557,
                    -0.5172131383583263,
                    -0.41959676783288097,
                    -0.20344219611829167,
                ],
                "sensor3": [
                    0.29452117456293736,
                    -1.248208787433402,
                    1.0658861555611072,
                    0.9957620663794554,
                    -1.1079606090700984,
                ],
            },
        }

    def test_invalid_payload_keys(self):
        input_data = {
            "sensor_1": [5.44, 3.22, 6.55, 8.54],
            "sensor_2": [5444.44, 33.22, 622.55, 812.54, 1233.24],
            "sensor_3": [0.44, 0.22, 0.55, 0.54, 0.24],
        }
        response = client.post(
            "/api/v1/standarize", headers=self.headers, data=json.dumps(input_data)
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_invalid_payload_list_length(self):
        input_data = {
            "sensor_1": [5.44, 3.22, 6.55, 8.54, 1.24],
            "sensor_2": [5444.44, 33.22, 622.55],
            "sensor_3": [0.44, 0.22, 0.55, 0.54, 0.24],
        }
        response = client.post(
            "/api/v1/standarize", headers=self.headers, data=json.dumps(input_data)
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_unauthorized_access(self):
        input_data = {
            "sensor_1": [5.44, 3.22, 6.55, 8.54, 1.24],
            "sensor_2": [5444.44, 33.22, 622.55, 812.54, 1233.24],
            "sensor_3": [0.44, 0.22, 0.55, 0.54, 0.24],
        }
        response = client.post("/api/v1/standarize", data=json.dumps(input_data))
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
