import unittest
from unittest.mock import patch, MagicMock
from Platform.prediction_model.main import predict_debugging_step


class TestPredictDebuggingStep(unittest.TestCase):
    @patch("Platform.prediction_model.main.vectorizer")
    @patch("Platform.prediction_model.main.model")
    def test_predict_debugging_step(self, mock_model, mock_vectorizer):
        """
        Test the predict_debugging_step function with mocked model and vectorizer.
        """
        # Mock the vectorizer's transform method
        mock_vectorizer.transform.return_value = "mock_tfidf_vector"

        # Mock the model's predict method
        mock_model.predict.return_value = ["mock_debugging_step"]

        # Mock the LLM formatting function
        with patch("Platform.prediction_model.main.format_debugging_steps_with_llm") as mock_format_llm:
            mock_format_llm.return_value = "Formatted Debugging Step"

            # Call the function with a sample input
            incident_description = "Sample incident description"
            result = predict_debugging_step(incident_description)

            # Assertions
            mock_vectorizer.transform.assert_called_once_with([incident_description])
            mock_model.predict.assert_called_once_with("mock_tfidf_vector")
            mock_format_llm.assert_called_once_with("mock_debugging_step")
            self.assertEqual(result, "Formatted Debugging Step")


if __name__ == "__main__":
    unittest.main()