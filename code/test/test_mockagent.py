import unittest
from typing import Dict, Any
from mockagent_with_history import get_analyze_logs, get_database_health, get_server_state, production_support,app
from unittest.mock import MagicMock, patch,Mock
from flask import jsonify,Flask
import time
from langsmith import Client
from flask import Flask
from flask_testing import TestCase


class TestServerMonitoringAgent(unittest.TestCase):

    @patch('mockagent_with_history.check_availability')
    @patch('mockagent_with_history.check_performance')
    @patch('mockagent_with_history.check_latency')
    def test_get_server_state(self, mock_check_latency, mock_check_performance, mock_check_availability):
        # Mock the return values of the external functions
        mock_check_availability.return_value = "Available"
        mock_check_performance.return_value = "Optimal"
        mock_check_latency.return_value = 50  # 50 ms latency

        # Call the function under test
        result = get_server_state()

        # Expected output
        expected_health = {
            "availability": "Available",
            "performance": "Optimal",
            "latency": 50,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Assertions
        self.assertEqual(result, str(expected_health))
        mock_check_availability.assert_called_once()
        mock_check_performance.assert_called_once()
        mock_check_latency.assert_called_once()

    @patch('random.randint')
    def test_get_analyze_logs(self, mock_randint):
        # Mock random.randint to return a specific value
        mock_randint.return_value = 3  # Simulate 3 errors

        # Call the function under test
        result = get_analyze_logs()

        # Expected output
        expected_logs = {
            "errors_found": 3,
            "log_status": "Unhealthy"
        }

        # Assertions
        self.assertEqual(result, str(expected_logs))
        mock_randint.assert_called_once_with(0, 5)

    @patch('random.random')
    @patch('random.uniform')
    def test_get_database_health(self, mock_uniform, mock_random):
        # Mock random.random to return a value less than 0.8 (simulate healthy)
        mock_random.return_value = 0.7
        # Mock random.uniform to return a specific response time
        mock_uniform.return_value = 500.0  # 500 ms response time

        # Call the function under test
        result = get_database_health()

        # Expected output
        expected_db_health = {
            "status": "Healthy",
            "response_time": 500.0
        }

        # Assertions
        self.assertEqual(result, str(expected_db_health))
        mock_random.assert_called_once()
        mock_uniform.assert_called_once_with(100, 1000)


class TestProductionSupport(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_production_support_success(self):
        # Mock the initialize_agent and invoke_agent functions
        
        mock_agent = {"agent": "mock_agent", "health_summary": "mock_summary"}
        mock_response = "mock_agent_response"

        with patch('mockagent_with_history.intialize_agent', return_value=mock_agent), \
             patch('mockagent_with_history.invoke_agent', return_value=mock_response):

            response = self.client.get("/production_support")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {
                "status": "success",
                "response": mock_response
            })


if __name__ == "__main__":
    unittest.main()