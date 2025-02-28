AI-Powered Content Generation API

This Flask-based web application utilizes CrewAI to automate the process of deep research content creation, from planning to editing and hook generation. The AI-powered system uses Anthropic’s Claude 3.5 model and follows a structured approach with specialized agents:
	•	Content Planner: Researches and outlines a structured content plan.
	•	Content Writer: Crafts engaging long-form deep research articles.
	•	Editor: Ensures clarity, accuracy, and journalistic integrity.
	•	Hook Generator: Creates an engaging hook to attract readers.

This system enables seamless AI-driven content generation with a human-like workflow.

Features

✅ Fully automated AI-powered content creation
✅ Uses Anthropic Claude 3.5 for high-quality outputs
✅ Agent-based approach for structured writing
✅ Flask-based API with web UI support
✅ Deployable on Render Cloud with minimal setup

Installation & Setup

1. Clone the Repository
   
git clone https://github.com/your-repo-name/ai-content-generator.git
cd ai-content-generator

2. Install Dependencies
   
   pip install flask crewai

3. Set up API Keys

   Create an .env file or export your Anthropic API Key:
   export ANTHROPIC_API_KEY="your-anthropic-api-key"

4. Alternatively, set it in a .env file:

   ANTHROPIC_API_KEY=your-anthropic-api-key

Usage

Run the Flask Application Locally
python app.py

	•	Open your browser and navigate to http://localhost:80/
	•	Enter a topic in the input field and submit.
	•	The AI agents will process and generate a deep research post.

Deploying to Render Cloud

You can deploy this application to Render Cloud in just a few steps.

1. Create a New Web Service on Render
	•	Go to Render
	•	Click “New Web Service”
	•	Connect your GitHub repository or manually upload your code.

2. Set Environment Variables

Navigate to the Environment Variables section and add:
ANTHROPIC_API_KEY=your-anthropic-api-key

3. 3. Configure Deployment
	•	Select Python 3.9+
	•	Set the Start Command:

python app.py

	•	Choose Auto Deploy (recommended) for continuous updates.

4. Deploy

Click Deploy and wait for Render to build & deploy your app.

5. Access the Web App

Once deployed, visit the assigned Render URL (https://your-app-name.onrender.com/) to use the AI-powered content generator.


API Endpoints

Method	Endpoint	Description
GET	/	Home page with topic input form
POST	/	Processes the topic and returns AI-generated content


  
      
