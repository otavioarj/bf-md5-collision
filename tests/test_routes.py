"""Tests for Flask routes."""
import pytest
from src.main import app


@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestRoutes:
    """Test Flask routes."""
    
    def test_index_get(self, client):
        """Test GET request to index."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Brainfuck Challenge' in response.data
    
    def test_source_code_view(self, client):
        """Test source code endpoint."""
        response = client.get('/source')
        assert response.status_code == 200
        assert b'def interpret_brainfuck' in response.data
    
    def test_upload_without_files(self, client):
        """Test upload without files."""
        response = client.post('/', data={})
        assert response.status_code == 302  # Redirect
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        # Would need to implement /health endpoint first
        pass