from urllib import response
import pytest
from rest_framework.test import APIClient
from rest_framework import status

def test_api_for_200():
    client = APIClient()
    response = client.get('/api/')
    assert response.status_code == status.HTTP_200_OK

