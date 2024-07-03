import logging
from crewai import Crew
from textwrap import dedent
from com.aniket.build.mrkt.analysis.agents.market_observers import MarketObserverAgents
from com.aniket.build.mrkt.analysis.tasks.employee_goals import AgentGoals
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MarketAnalysis:
    def __init__(self, company):
        self.company = company
        logger.info(f"Initialized MarketAnalysis for company: {company}")

    def run(self):
        try:
            agents  = MarketObserverAgents()
            tasks   = AgentGoals()

            research_analyst_agent      = agents.research_analyst_employee()
            financial_analyst_agent     = agents.financial_analyst_employee()
            investment_advisor_agent    = agents.investment_consultant_employee()

            logger.info("Created agents for analysis")

            research_task   = tasks.research(research_analyst_agent, self.company)
            financial_task  = tasks.analyst_employee(financial_analyst_agent)
            filings_task    = tasks.research_on_filling_employee(financial_analyst_agent)
            recommend_task  = tasks.final_report_employee(investment_advisor_agent)

            logger.info("Created tasks for analysis")

            crew = Crew(
                agents=[research_analyst_agent, financial_analyst_agent, investment_advisor_agent],
                tasks=[research_task, financial_task, filings_task, recommend_task],
                verbose=True
            )

            logger.info("Initiating crew kickoff")
            result = crew.kickoff()
            logger.info("Crew analysis completed successfully")
            return result
        except Exception as e:
            logger.error(f"An error occurred during the analysis: {str(e)}")
            raise

def main():
    print('-------------------------------')
    print("Entering into Market Analysis")
    print('-------------------------------')

    try:
        company = input(dedent("What is the company you want to analyze? "))
        logger.info(f"User input received for company: {company}")

        financial_crew = MarketAnalysis(company)
        result = financial_crew.run()

        print("\n\n########################")
        print("## Here is the Report")
        print("########################\n")
        print(result)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
        print("\nProgram interrupted. Exiting...")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")
    finally:
        logger.info("Program execution completed")


if __name__ == "__main__":
    main()