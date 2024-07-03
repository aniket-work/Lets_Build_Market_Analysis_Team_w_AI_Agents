from crewai import Agent
import os
from com.aniket.dev.mrkt.analysis.tools.surfer_tool import SurferTool
from com.aniket.dev.mrkt.analysis.tools.calc_tools import CalculatorTools
from com.aniket.dev.mrkt.analysis.tools.search_tools import SearchTools
from com.aniket.dev.mrkt.analysis.tools.sec_tools import SECTools
from langchain_groq import ChatGroq
from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from com.aniket.dev.mrkt.analysis.constant.constants import *

load_dotenv()


class MarketObserverAgents:
  """
  A class for creating and managing market observer agents with different roles.

  This class provides methods to create agents with specific roles such as
  financial analyst, research analyst, and investment consultant. It supports
  using either Groq or OpenAI language models for agent interactions.

  Attributes:
      llm (Union[ChatGroq, ChatOpenAI]): The language model used by the agents.

  """

  def __init__(self, use_groq=False):
    """
    Initialize the MarketObserverAgents class.

    Args:
        use_groq (bool, optional): If True, use the Groq language model.
                                   If False, use the OpenAI language model.
                                   Defaults to False.
    """
    if use_groq:
      self.llm = ChatGroq(
        api_key=os.getenv(GROQ_API_KEY),
        model=LLAMA3_70B_8192
      )
    else:
      self.llm = ChatOpenAI(
        model=CREWAI_LLAMA3_8B,
        base_url=OLLAMA_BASE_URL,
        request_timeout=REQUEST_TIMEOUT,
        api_key=PLACEHOLDER_API_KEY
      )

  def financial_analyst_employee(self):
    """
    Create a financial analyst agent.

    Returns:
        Agent: An agent configured with the role, goal, and tools of a financial analyst.
    """
    return Agent(
      role=FINANCIAL_ANALYST_ROLE,
      goal=FINANCIAL_ANALYST_GOAL,
      backstory=FINANCIAL_ANALYST_BACKSTORY,
      verbose=True,
      llm=self.llm,
      tools=[
        SurferTool.scrape_and_summarize_website,
        SearchTools.search_internet,
        CalculatorTools.calculate,
        SECTools.search_10q,
        SECTools.search_10k
      ]
    )

  def research_analyst_employee(self):
    """
    Create a research analyst agent.

    Returns:
        Agent: An agent configured with the role, goal, and tools of a research analyst.
    """
    return Agent(
      role=RESEARCH_ANALYST_ROLE,
      goal=RESEARCH_ANALYST_GOAL,
      backstory=RESEARCH_ANALYST_BACKSTORY,
      verbose=True,
      llm=self.llm,
      tools=[
        SurferTool.scrape_and_summarize_website,
        SearchTools.search_internet,
        SearchTools.search_news,
        YahooFinanceNewsTool(),
        SECTools.search_10q,
        SECTools.search_10k
      ]
    )

  def investment_consultant_employee(self):
    """
    Create an investment consultant agent.

    Returns:
        Agent: An agent configured with the role, goal, and tools of an investment consultant.
    """
    return Agent(
      role=INVESTMENT_ADVISOR_ROLE,
      goal=INVESTMENT_ADVISOR_GOAL,
      backstory=INVESTMENT_ADVISOR_BACKSTORY,
      verbose=True,
      llm=self.llm,
      tools=[
        SurferTool.scrape_and_summarize_website,
        SearchTools.search_internet,
        SearchTools.search_news,
        CalculatorTools.calculate,
        YahooFinanceNewsTool()
      ]
    )