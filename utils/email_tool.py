from smolagents import Tool
import os
from huggingface_hub import InferenceClient
import requests

class EmailGenerationTool(Tool):
  name = "email_generator"
  description = """
  This tool generates a thank-you email response to users who reach out through the contact form.
  It researches the company's opearations and includes a personalized touch in the reply. It also takes into consideration the message from the user through the form.
  """
  inputs = {
    "company_name": {
      "type": "string",
      "description": "The name of the company the email is being sent from.",
    },
    "incoming_message": {
      "type": "string",
      "description": "The message received from the user.",
    }
  }
  output_type = "string"

  def forward(self, company_name: str, incoming_message: str):
    """Generate AI-powered email response."""

    # AI model setup
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.1", token=hf_token)

    # AI prompt
    prompt = f"""
    You are a professional email assistant. Below is an email received from a client. Generate a warm, professional thank-you response, including:
        - A thank-you note for reaching out through our form.
        - A personalized mention of the user's message through the form. You can combine it with results that you discover through the web search.


    Company: {company_name}

    Incoming message:
    {incoming_message}

    Respond professionally, keeping it concise and helpful.
    """

    # Generate response
    response = client.text_generation(prompt, max_new_tokens=200)
    return response

# Initialize tool instance
email_generator_tool = EmailGenerationTool()
