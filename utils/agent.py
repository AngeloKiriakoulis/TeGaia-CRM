from smolagents import HfApiModel, CodeAgent, GoogleSearchTool
import os
from dotenv import load_dotenv
# Fix import for utils (add to sys.path if needed)
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.email_tool import EmailGenerationTool

load_dotenv()

class EmailAgent:
    """
    An AI-powered email drafting agent that:
    - Uses GoogleSearchTool to fetch the latest company announcement.
    - Generates a professional thank-you email with EmailGenerationTool.
    """

    def __init__(self, company_name: str, message: str):
        """Initializes the EmailAgent with company details and user message."""
        self.company_name = company_name
        self.message = message

        # Load Hugging Face API token
        self.hf_token = os.getenv("HUGGINGFACE_TOKEN")
        if not self.hf_token:
            raise ValueError("HUGGINGFACE_TOKEN is missing. Please set it in your environment variables.")

        # Initialize CodeAgent with necessary tools
        self.agent = CodeAgent(
            tools=[GoogleSearchTool(), EmailGenerationTool()],
            model=HfApiModel(token=self.hf_token),
            add_base_tools=True
        )

    def run(self) -> dict:
        """Runs the agent to generate an email response."""
        try:
            response = self.agent.run(
                "Draft an email to this company!",
                additional_args={
                    "company_name": self.company_name,
                    "incoming_message": self.message
                }
            )
            return response
        except Exception as e:
            return {"error": f"Failed to generate email: {str(e)}"}

