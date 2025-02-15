from langchain.tools import DuckDuckGoSearchResults
from flask import Flask, request, jsonify, render_template
from crewai import Agent, Task, Crew, LLM
import os

# Define LLM

app = Flask(__name__)

# Securely retrieve API key from environment variables
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Configure the LLM (Anthropic Claude 3.5)
llm = LLM(
    model="claude-3-5-sonnet-20241022",
    api_key=anthropic_api_key
)

# 1️⃣ Research Crawler Agent
crawler_agent = Agent(
    role="Research Crawler",
    goal="Collect relevant research papers and articles on the given topic",
    backstory="A highly skilled researcher with expertise in scientific literature mining.",
    tools=[DuckDuckGoSearchResults()],
    allow_delegation=True,
    llm=llm
)

crawler_task = Task(
    description="Use APIs like ArXiv, Semantic Scholar, and Scrapy to collect research papers.",
    expected_output="List of 100+ research papers with metadata (title, author, abstract, citations)",
    agent=crawler_agent
)

# 2️⃣ Summarization & Extraction Agent
summarizer_agent = Agent(
    role="Summarization Specialist",
    goal="Extract and summarize key insights from research papers.",
    backstory="Expert in document analysis and knowledge extraction.",
    tools=[],
    llm=llm
)

summarization_task = Task(
    description="Summarize each research paper's abstract, methodology, key results, and discussion.",
    expected_output="Structured summaries with key takeaways for each research paper.",
    agent=summarizer_agent
)

# 3️⃣ Fact-Checking & Cross-Validation Agent
fact_checker_agent = Agent(
    role="Fact-Checking Specialist",
    goal="Verify claims using multiple sources and cross-reference facts.",
    backstory="Expert in validation of scientific claims and misinformation detection.",
    tools=[DuckDuckGoSearchResults()],
    llm=llm
)

fact_checking_task = Task(
    description="Cross-validate claims from multiple research papers using different sources.",
    expected_output="List of verified and debunked claims from the research dataset.",
    agent=fact_checker_agent
)

# 4️⃣ Citation & Trend Analysis Agent
citation_agent = Agent(
    role="Citation Analyst",
    goal="Analyze research trends and identify influential citations.",
    backstory="Data scientist specializing in citation networks and bibliometric analysis.",
    tools=[],
    llm=llm
)

citation_task = Task(
    description="Identify key research trends and construct a citation network.",
    expected_output="Graph-based analysis of influential research citations.",
    agent=citation_agent
)

# 5️⃣ Thesis Writing & Refinement Agent
writer_agent = Agent(
    role="Academic Writer",
    goal="Generate a structured research thesis based on validated findings.",
    backstory="A PhD-level researcher skilled in academic writing and LaTeX formatting.",
    tools=[],
    llm=llm
)

writing_task = Task(
    description="Generate a well-structured research thesis with introduction, methodology, findings, and conclusion.",
    expected_output="A complete research thesis draft with citations and references.",
    agent=writer_agent
)

# 🏆 Assemble the Crew
crew = Crew(
    agents=[crawler_agent, summarizer_agent, fact_checker_agent, citation_agent, writer_agent],
    tasks=[crawler_task, summarization_task, fact_checking_task, citation_task, writing_task]
)

# 🚀 Run the Research Process
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
    app.run(host="0.0.0.0", port=80, debug=True)