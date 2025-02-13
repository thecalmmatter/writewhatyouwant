from flask import Flask, request, jsonify, render_template
from crewai import Agent, Task, Crew, LLM
import streamlit as st
import os


app = Flask(__name__)

# Securely retrieve API key from environment variables
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Configure the LLM (Anthropic Claude 3.5)
llm = LLM(
    model="claude-3-5-sonnet-20241022",
    api_key=anthropic_api_key
)

# Define Agents
planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory=(
        "You're responsible for planning a linkedin article on {topic}. "
        "You collect information that helps the audience learn and make informed decisions. "
        "Your work serves as the foundation for the Content Writer."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm
)

writer = Agent(
    role="Content Writer",
    goal="Write an insightful and factually accurate opinion piece about {topic}",
    backstory=(
        "You are a writer crafting a compelling opinion piece on {topic}. "
        "You use the Content Planner’s outline to develop the article, ensuring clarity, accuracy, "
        "and engaging storytelling. Your writing is balanced and quirky acknowledging when statements are opinions."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm
)

editor = Agent(
    role="Editor",
    goal="Edit the Linkedin post to align with journalistic standards in the style of Joe Rogan or lex fridman or Chamath Palihapitiya, add some interesting icons and the brand’s voice.",
    backstory=(
        "As an editor, you refine the Linkedin post for clarity, grammar, structure and balance. "
        "Your focus is on journalistic integrity, ensuring the piece remains professional and unbiased."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm
)

hook_generator = Agent(
    role="Hook Generator",
    goal="Add a Linkedin post hook.",
    backstory=(
        "As a hook generator, you add the hook for quirkiness, compelling messages, and irresistible curiosity that makes people stop scrolling and dive in."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm
)

# Define Tasks
plan = Task(
    description=(
        "1. Research and prioritize the latest trends, key players, and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering their interests and pain points.\n"
        "3. Develop a detailed content outline including an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources."
    ),
    expected_output="A detailed content plan including an outline, audience analysis, SEO keywords, and resources.",
    agent=planner
)

write = Task(
    description=(
        "1. Use the content plan to craft a compelling 400 word linkedin post on {topic}.\n"
        "2. Naturally integrate SEO keywords.\n"
        "3. Structure sections/subtitles engagingly.\n"
        "4. Ensure the post has an engaging introduction, insightful body, and strong conclusion.\n"
        "5. Proofread for grammatical accuracy and alignment with the brand's voice."
    ),
    expected_output="A well-structured, engaging linkedin  post in markdown format, ready for publication.",
    agent=writer
)

edit = Task(
    description="Proofread and refine the linkedin post for clarity, grammar, structure, and tone consistency.",
    expected_output="A polished linkedin post in markdown format, ready for publication.",
    agent=editor
)

hook = Task(
    description="Craft an engaging, quirky, and compelling hook for a LinkedIn post that grabs attention instantly. The hook should spark curiosity, encourage engagement, and set the stage for the main content.",
    expected_output="A sharp, well-structured LinkedIn post hook in markdown format, ensuring clarity, grammatical accuracy, and an engaging tone, ready for publication.",
    agent=hook_generator
)

# Crew Execution Setup
crew = Crew(
    agents=[hook_generator, planner, writer, editor],
    tasks=[hook, plan, write, edit],
    verbose=True
)

    # Crew Execution Setup
crew = Crew(agents=[planner, writer, editor], tasks=[plan, write, edit], verbose=True)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        topic = request.form.get("topic")
        if topic:
            output = crew.kickoff(inputs={"topic": topic})  
            result = str(output)  # Convert CrewOutput object to a string
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)