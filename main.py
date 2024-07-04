import streamlit as st
import logging
from crewai import Crew
from textwrap import dedent
from com.aniket.dev.mrkt.analysis.agents.market_observers import MarketObserverAgents
from com.aniket.dev.mrkt.analysis.tasks.employee_goals import AgentGoals
from dotenv import load_dotenv
import threading
import queue
import time
import sys
import os

# Load environment variables
load_dotenv()

class TeeLogger(object):
    def __init__(self, filename, mode="a", original_stream=None):
        self.file = open(filename, mode, buffering=1)  # Line-buffered
        self.original_stream = original_stream

    def write(self, message):
        self.file.write(message)
        self.file.flush()  # Force flush after each write
        if self.original_stream:
            self.original_stream.write(message)
            self.original_stream.flush()

    def flush(self):
        self.file.flush()
        if self.original_stream:
            self.original_stream.flush()

    def close(self):
        self.file.close()

# Configure logging
log_file = "analysis_logs.txt"
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=log_file,
                    filemode='w')
logger = logging.getLogger(__name__)

# Ensure logger flushes immediately
for handler in logger.handlers:
    handler.flush = lambda: None

def read_new_logs(last_position):
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            file.seek(last_position)
            new_content = file.read()
            new_position = file.tell()
        return new_content, new_position
    return "", 0

class MarketAnalysis:
    def __init__(self, company):
        self.company = company
        logger.info(f"Initialized MarketAnalysis for company: {company}")

    def run(self):
        try:
            agents = MarketObserverAgents()
            tasks = AgentGoals()

            research_analyst_agent = agents.research_analyst_employee()
            financial_analyst_agent = agents.financial_analyst_employee()
            investment_advisor_agent = agents.investment_consultant_employee()

            logger.info("Created agents for analysis")

            research_task = tasks.research(research_analyst_agent, self.company)
            financial_task = tasks.analyst_employee(financial_analyst_agent)
            filings_task = tasks.research_on_filling_employee(financial_analyst_agent)
            recommend_task = tasks.final_report_employee(investment_advisor_agent)

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

def run_analysis(company):
    try:
        financial_crew = MarketAnalysis(company)
        result = financial_crew.run()
        logger.info("Analysis completed successfully")  # Add final log
        return result
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"

def update_logs(log_placeholder, status_placeholder, stop_event):
    last_position = 0
    full_logs = ""
    while not stop_event.is_set():
        new_logs, last_position = read_new_logs(last_position)
        if new_logs:
            full_logs += new_logs
            log_placeholder.markdown(f"""
            <div style="height: 300px; overflow-y: scroll; background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
                <pre>{full_logs}</pre>
            </div>
            """, unsafe_allow_html=True)
        status_placeholder.text("Analysis in progress...")
        time.sleep(10)


def main():
    st.set_page_config(page_title="Market Analysis Tool", page_icon="📊", layout="wide")

    st.title("Market Analysis Tool")
    st.write("This tool analyzes a company using AI agents to provide insights.")

    company = st.text_input("Enter the company you want to analyze:")

    if st.button("Start Analysis"):
        if company:
            # Create placeholders for logs and status
            log_placeholder = st.empty()
            status_placeholder = st.empty()

            # Redirect stdout and stderr to the log file
            sys.stdout = TeeLogger(log_file, "w", sys.stdout)
            sys.stderr = TeeLogger(log_file, "a", sys.stderr)

            # Run the analysis in a separate thread
            result_queue = queue.Queue()
            analysis_thread = threading.Thread(target=lambda q: q.put(run_analysis(company)), args=(result_queue,))
            analysis_thread.start()

            # Update logs and status while the analysis is running
            last_position = 0
            full_logs = ""
            while analysis_thread.is_alive():
                new_logs, last_position = read_new_logs(last_position)
                if new_logs:
                    full_logs += new_logs
                    log_placeholder.markdown(f"""
                    <div style="height: 300px; overflow-y: scroll; background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
                        <pre>{full_logs}</pre>
                    </div>
                    """, unsafe_allow_html=True)
                status_placeholder.text("Analysis in progress...")
                time.sleep(1)  # Check more frequently

            # Get the final result
            result = result_queue.get()

            # Restore original stdout and stderr
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            # Display the final result
            st.subheader("Analysis Report")
            st.text_area("Result", result, height=400)
        else:
            st.warning("Please enter a company name.")

if __name__ == "__main__":
    main()