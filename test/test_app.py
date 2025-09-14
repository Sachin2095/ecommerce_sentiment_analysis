import pytest
import sys, os
from flask import template_rendered
from contextlib import contextmanager

# Ensure project root is in PYTHONPATH so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from pipelines.process import AnalysisText


def test_homepage():
    """Test that the homepage loads successfully (GET request)"""
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    # since you render index.html, check if the page contains keywords
    assert b"Sentiment" in response.data or b"Review" in response.data


def test_sentiment_prediction_form():
    """Test POST request to '/' with form data"""
    client = app.test_client()
    response = client.post('/', data={"review": "The product is excellent!"})
    assert response.status_code == 200
    # Flask renders template, so we expect HTML back
    assert b"Positive" in response.data or b"Negative" in response.data or b"Ok" in response.data


def test_analysis_text_direct():
    """Directly test AnalysisText pipeline (unit test without Flask)"""
    text = "This is amazing!"
    result = AnalysisText(text)
    assert isinstance(result, str)
    assert any(label in result for label in ["Positive", "Negative", "Ok"])
