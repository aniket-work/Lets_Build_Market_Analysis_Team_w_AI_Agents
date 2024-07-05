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
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

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

import re

from ansi2html import Ansi2HTMLConverter

conv = Ansi2HTMLConverter()

def read_new_logs(last_position):
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            file.seek(last_position)
            new_content = file.read()
            new_position = file.tell()
        # Convert ANSI to HTML
        new_content = conv.convert(new_content)
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


import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space


def main():
    st.set_page_config(page_title="AI Agents - Powered Market Analysis Tool", page_icon="📊", layout="wide")

    # Custom CSS for a more professional look and better alignment
    st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        font-weight: bold;
        height: 3em;
    }
    .log-container {
        border: 1px solid #ddd;
        border-radius: 5px;
        background-color: white;
        height: 400px;
        overflow-y: scroll;
        padding: 10px;
        font-family: monospace;
    }
    .status-text {
        font-weight: bold;
        color: #1E90FF;
    }
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .icon-title {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # Center-aligned header with icon
    st.markdown('<div class="icon-title">', unsafe_allow_html=True)
    st.markdown('# 📊 AI Agents - Powered Market Analysis Tool')
    st.markdown('</div>', unsafe_allow_html=True)

    colored_header(label="", description="Gain deep insights into any company using advanced AI agents",
                   color_name="blue-70")

    add_vertical_space(2)

    st.write("Enter a company name below to start a comprehensive market analysis powered by our AI agents.")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        company = st.text_input("Company Name:", placeholder="e.g. Tesla, Apple, Microsoft")
        start_analysis = st.button("Start Analysis")

    if start_analysis:
        if company:
            progress_bar = st.progress(0)
            status_placeholder = st.empty()
            log_placeholder = st.empty()

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
                    <div class="log-container">
                        {full_logs}
                    </div>
                    """, unsafe_allow_html=True)
                status_placeholder.markdown('<p class="status-text">Analysis in progress...</p>',
                                            unsafe_allow_html=True)
                progress_bar.progress(
                    min(last_position / 1000, 1.0))  # Adjust the denominator based on expected log size
                time.sleep(1)

            # Get the final result
            result = result_queue.get()

            # Restore original stdout and stderr
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            # Display the final result
            progress_bar.progress(1.0)
            status_placeholder.markdown('<p class="status-text">Analysis Complete!</p>', unsafe_allow_html=True)
            st.success("Market analysis completed successfully!")

            with st.expander("View Detailed Analysis Report", expanded=True):
                st.markdown(result)

            st.download_button(
                label="Download Full Report",
                data=result,
                file_name=f"{company}_market_analysis.txt",
                mime="text/plain"
            )
        else:
            st.warning("Please enter a company name to begin the analysis.")


if __name__ == "__main__":
    main()