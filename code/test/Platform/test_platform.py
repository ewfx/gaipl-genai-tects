import unittest
from unittest.mock import patch, MagicMock
from Platform.main import get_operation, process_operation, create_main_graph, UserInput


class TestMain(unittest.TestCase):
    @patch("Platform.main.os.path.join")
    @patch("Platform.main.open", create=True)
    def test_get_operation(self, mock_open, mock_path_join):
        """
        Test the get_operation function to ensure it reads the file correctly.
        """
        # Mock file reading
        mock_open.return_value.__enter__.return_value.read.return_value = "Mock file content"
        mock_path_join.return_value = "mocked_path/downtime.txt"

        # Create a mock state
        state = {"input": "downtime.txt", "continue_execution": True}

        # Call the function
        result = get_operation(state)

        # Assertions
        self.assertEqual(result["input"], "Mock file content")
        self.assertFalse(result["continue_conversation"])
        mock_open.assert_called_once_with("mocked_path/downtime.txt", "r")

    @patch("Platform.main.create_graph")
    def test_process_operation(self, mock_create_graph):
        """
        Test the process_operation function to ensure it invokes the graph correctly.
        """
        # Mock the graph and its invoke method
        mock_graph = MagicMock()
        mock_graph.invoke.return_value = {"history": "Mock execution history"}
        mock_create_graph.return_value = mock_graph

        # Create a mock state
        state = {"input": "Mock operation input", "continue_execution": True}

        # Call the function
        result = process_operation(state)

        # Assertions
        mock_graph.invoke.assert_called_once_with(
            {"operation": "Mock operation input", "history": '{"history":[]}'}
        )
        self.assertEqual(result, state)

    def test_create_main_graph(self):
        """
        Test the create_main_graph function to ensure it creates the workflow correctly.
        """
        workflow = create_main_graph()

        # Assertions
        self.assertIsNotNone(workflow)
        self.assertTrue(callable(workflow.invoke))

    @patch("Platform.main.create_main_graph")
    def test_main_workflow_execution(self, mock_create_main_graph):
        """
        Test the main workflow execution to ensure the graph is invoked correctly.
        """
        # Mock the graph and its invoke method
        mock_graph = MagicMock()
        mock_graph.invoke.return_value = {"history": "Mock final result"}
        mock_create_main_graph.return_value = mock_graph

        # Call the main function
        from Platform.main import main
        main()

        # Assertions
        mock_graph.invoke.assert_called_once_with(
            {"input": "downtime.txt", "continue_conversation": True}
        )


if __name__ == "__main__":
    unittest.main()