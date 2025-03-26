from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Please set the GEMINI_API_KEY environment variable.")    

def format_debugging_steps_with_llm(steps):
    """
    Formats debugging steps into a structured logical debugging flow using Gemini LLM.
    """
    # Prepare the prompt for the LLM
    prompt = f"""
    You are a helpful assistant. Format the following debugging steps into a structured logical debugging flow:
    
    Steps:
    {steps}
    
    Provide the output as a structured list of steps with logical flow. And match style with 
    "The goal of the this operation is to determine the reason for downtime of a application
    Check the application log to see if there are any errors,
    Only if error status is yellow or red then check for most common error,
    If status of logs were green we proceed to checking the queue health
    If the most common error is database related then check the database connection
    If the database connection is up then check if too many connections are made to database
    If database is the not the issue then check queue health
    to check the queue health check the queload and then check the queue response time
    If database health is red or the queue health is red then we know that it is the cause of the downtime
    When the cause of the downtime is confirmed then summarize the analysis done and complete the operation
    If cause cannot be determined after all the checks then just say reason is NotFound and complete the operation
    completed

    """

    try:
        # Configure the Gemini API
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash') #changed model name
        response = model.generate_content(prompt) #changed how the response is generated
        # Extract and return the formatted steps
        formatted_steps = response.text.strip() #changed how the result is extracted
        return formatted_steps

    except Exception as e:
        print(f"Error while formatting debugging steps with Gemini: {e}")
        return "Error: Unable to format debugging steps."

# Example usage
if __name__ == "__main__":
    sample_steps = "Check the network connection. Restart the server. Analyze the logs for errors. Verify the database connection."
    formatted_steps = format_debugging_steps_with_llm(sample_steps)
    print("Formatted Debugging Steps:")
    print(formatted_steps)