import pytest
import sys, os
# Ensure project root is in PYTHONPATH so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app
from pipelines.process import AnalysisText  # if you want to directly test your text analysis logic


def test_homepage():
    """Test that the homepage loads successfully"""
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"Sentiment" in response.data or b"Review" in response.data  # adjust to expected HTML/text


def test_sentiment_prediction():
    """Test the /predict endpoint with a sample review"""
    client = app.test_client()
    sample_review = {"review": "The product is excellent!"}

    response = client.post('/predict', json=sample_review)
    assert response.status_code == 200

    data = response.get_json()
    assert "sentiment" in data
    assert data["sentiment"] in ["positive", "negative", "neutral"]  # adjust to your labels


def test_analysis_text_direct():
    """Directly test AnalysisText pipeline (unit test without Flask)"""
    text = "This is amazing!"
    result = AnalysisText(text)
    assert result in ["positive", "negative", "neutral"]
