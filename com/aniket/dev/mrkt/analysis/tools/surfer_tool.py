import logging
import requests
from crewai import Agent, Task
from langchain.tools import tool
from unstructured.partition.html import partition_html
from bs4 import BeautifulSoup

class SurferTool:
    # Constants
    CHUNK_SIZE = 8000
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

    AGENT_ROLE = 'Elite Web Content Analyst and Summarization Specialist'

    AGENT_GOAL = ('Extract critical insights from web content, synthesize complex information, and produce '
                  'concise, high-impact summaries that capture the essence of the source material while '
                  'highlighting key trends, facts, and implications.')

    AGENT_BACKSTORY = ("You are a world-renowned expert in digital content analysis with a track record of "
                       "distilling vast amounts of online information into actionable intelligence. Your unique "
                       "ability to rapidly process and synthesize web content has made you an invaluable asset "
                       "to leading tech companies and research institutions. Your summaries have influenced "
                       "major business decisions and shaped public policy. You approach each task with laser "
                       "focus, always striving to uncover hidden patterns and extract the most crucial information.")

    TASK_DESCRIPTION_TEMPLATE = (
        "Conduct a comprehensive analysis of the following web content, adhering to these guidelines:\n"
        "1. Identify and extract the core message and primary arguments.\n"
        "2. Highlight key facts, statistics, and noteworthy quotes.\n"
        "3. Recognize emerging trends, patterns, or shifts in perspective.\n"
        "4. Assess the credibility and potential biases of the source.\n"
        "5. Contextualize the information within broader industry or societal trends.\n"
        "6. Synthesize your findings into a concise, impactful summary.\n"
        "7. Ensure your summary is clear, objective, and free of extraneous commentary.\n\n"
        "CONTENT TO ANALYZE:\n--------------------\n{}\n\n"
        "Deliver a summary that would empower decision-makers with actionable insights."
    )

    TOOL_NAME = "Advanced Web Content Analysis and Summarization Engine"

    TOOL_DESCRIPTION = ("Harness cutting-edge NLP and web scraping technologies to extract, analyze, and "
                        "synthesize content from any given website. This tool goes beyond simple summarization, "
                        "providing deep insights, trend analysis, and contextual understanding of web content.")

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    @tool(TOOL_NAME)
    def scrape_and_summarize_website(self, website):
        """Scrape and summarize website content."""
        self.logger.info(f"Scraping website: {website}")

        headers = {'User-Agent': self.USER_AGENT}
        response = requests.get(website, headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')
        elements = partition_html(text=str(soup))
        content = "\n\n".join([str(el) for el in elements])

        chunks = [content[i:i + self.CHUNK_SIZE] for i in range(0, len(content), self.CHUNK_SIZE)]
        self.logger.info(f"Content split into {len(chunks)} chunks")

        summaries = []
        for i, chunk in enumerate(chunks, 1):
            self.logger.info(f"Processing chunk {i}/{len(chunks)}")
            agent = self._create_agent()
            task = self._create_task(agent, chunk)
            summary = task.execute()
            summaries.append(summary)

        final_summary = "\n\n".join(summaries)
        self.logger.info("Summarization completed")
        return final_summary

    def _create_agent(self):
        return Agent(
            role=self.AGENT_ROLE,
            goal=self.AGENT_GOAL,
            backstory=self.AGENT_BACKSTORY,
            allow_delegation=False
        )

    def _create_task(self, agent, content):
        return Task(
            agent=agent,
            description=self.TASK_DESCRIPTION_TEMPLATE.format(content)
        )