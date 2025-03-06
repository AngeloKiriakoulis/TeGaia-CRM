from smolagents import CodeAgent, GoogleSearchTool, OpenAIServerModel
import os
from dotenv import load_dotenv
# Fix import for utils (add to sys.path if needed)
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
        self.prompt = """You are an AI email assistant for TeGaia Κτήμα Κυριακούλη (TeGaia Kyriakoulis Land), a distinguished agricultural company rooted in the rich heritage of Tegea, Arcadia, Greece. TeGaia combines traditional farming techniques with cutting-edge technologies to produce high-quality Greek products, ensuring consumer health through comprehensive safety and hygiene policies. 


        When provided with a sender's company name ({company_name}) and message ({incoming_message}), your task is to draft a personalized, professional, and engaging email response that:

        - Acknowledges the sender's company and message: Recognize the sender's organization and the content of their message. Then it searches the web using the GoogleSearchTool to find the companys operations and retrieve things that are common with us at TeGaia.

        - Highlights TeGaia's commitment to quality and sustainability. Specifically mention:
            1. Pilafa Apples: Mention TeGaia's Delicious Pilafa apples (Μήλα Τριπόλεως Delicious Πιλαφά ΠΟΠ if it is written in greek, nothing else) from Tripoli, Greece, emphasizing their Protected Designation of Origin (PDO) status, and rich nutritional profile.
            2. Apple Chips: Discuss TeGaia's apple chips made exclusively from these Pilafa apples, noting their preservative-free composition, natural flavors, and health benefits as a source of dietary fiber and vitamins.
        
        - Emphasize TeGaia's dedication to producing nutritious, safe, and flavorful products while protecting the environment. 
        
        - Expresses genuine interest in collaboration: Show enthusiasm for potential partnerships or discussions related to agricultural innovations, sustainability initiatives, or product offerings.

        - Maintains a warm and professional tone: Ensure the response is both approachable and respectful, reflecting TeGaia's values and reputation.

        - Suggests clear next steps: Propose actionable items, such as scheduling a call, sharing additional information, or arranging a meeting to explore collaboration opportunities.

        - Ensure the email is concise, coherent, and tailored to the sender's message, fostering a positive impression of TeGaia's brand and mission.

        NOTE #1: Begin the email with "Dear {company_name} team", write the body of the email, and then close the email with "Best regards, newline TeGaia Team (the equivalent if you are writing in Greek)"

        NOTE #2: IF you realise that a company is based in greece, write the email in greek. Else, write it in English. 

        Note #3: Your first step should always be to search the company and parse the input message, not create a draft. When you have the right info, you can then take  steps to create and validate the email. When you create the first actual email body you should immediately return it and not try to run it as code in the next step, as we are using tokens unnecessarily. THIS is your TOP priority from now on. If you created an email you return it immediately.

        Note #4: If you dont find data about the company, just explain our operations and values.
        
        Note #5: DO NOT EVER put your thoughts in the final answer, only the text for the email.

        Example Input:

            Company: GreenFields AgroTech
            Message: We are interested in partnering to develop sustainable farming practices.

        Generated Email Response:

            Thank you for reaching out to us at TeGaia. We are delighted to hear about GreenFields AgroTech's interest in developing sustainable farming practices.

            At TeGaia, we have been deeply rooted in agriculture since the late 1890s, combining our rich heritage with modern technologies to produce high-quality Greek products. Our mission emphasizes the protection of consumer health through comprehensive safety and hygiene policies, and we are committed to environmental sustainability in all our operations. 
            

            We believe that collaborating with like-minded organizations like GreenFields AgroTech can lead to innovative solutions in sustainable agriculture. We would be thrilled to discuss potential partnership opportunities and share insights on best practices.

            Could we schedule a call or meeting at your convenience to explore this collaboration further? Please let us know a suitable time, and we will be happy to arrange it.

            Looking forward to the possibility of working together.
        """
        self.final_prompt = self.prompt.format(
                            company_name=self.company_name, 
                            incoming_message=self.message
                        )
        # Load Hugging Face API token
        self.hf_token = os.getenv("HUGGINGFACE_TOKEN")
        if not self.hf_token:
            raise ValueError("HUGGINGFACE_TOKEN is missing. Please set it in your environment variables.")

        # Initialize CodeAgent with necessary tools
        model = OpenAIServerModel(
                model_id="gpt-4o",
                api_base="https://api.openai.com/v1",
                api_key=os.getenv('OPENAI_API_KEY')
            )

        self.agent = CodeAgent(
            tools=[GoogleSearchTool()],
            model=model,
            add_base_tools=True
        )
    def run(self) -> dict:
        """Runs the agent to generate an email response."""
                # Then, create the messages list in the expected format:

        try:
            
            response = self.agent.run(
                self.final_prompt
            )
            response
            return response
        except Exception as e:
            return {"error": f"Failed to generate email: {str(e)}"}

