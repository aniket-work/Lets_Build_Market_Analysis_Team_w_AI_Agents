import json
from crewai import Task
from textwrap import dedent

CONFIG_FILE_PATH        = '../../../../../../config/config.json'
TIP_SECTION_KEY         = 'rewards'
TASKS_KEY               = 'tasks'
RESEARCH_KEY            = 'research'
DESCRIPTION_KEY         = 'description'
EXPECTED_OUTPUT_KEY     = 'expected_output'
FINANCIAL_ANALYSIS_KEY  = 'financial_analysis'
FILINGS_ANALYSIS_KEY    = 'filings_analysis'
RECOMMEND_KEY           = 'recommend'


class AgentGoals():
    def __init__(self):
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            self.config = json.load(config_file)

    def employee_reward(self):
        return self.config[TIP_SECTION_KEY]

    def research(self, agent, company):
        task_config = self.config[TASKS_KEY][RESEARCH_KEY]
        return Task(
            description=dedent(f"""
            {task_config[DESCRIPTION_KEY]}

            {self.employee_reward()}

            Selected company by the customer: {company}
            """),
            agent=agent,
            expected_output=task_config[EXPECTED_OUTPUT_KEY]
        )

    def analyst_employee(self, agent):
        task_config = self.config[TASKS_KEY][FINANCIAL_ANALYSIS_KEY]
        return Task(
            description=dedent(f"""
            {task_config[DESCRIPTION_KEY]}

            {self.employee_reward()}
            """),
            agent=agent,
            expected_output=task_config[EXPECTED_OUTPUT_KEY]
        )

    def research_on_filling_employee(self, agent):
        task_config = self.config[TASKS_KEY][FILINGS_ANALYSIS_KEY]
        return Task(
            description=dedent(f"""
            {task_config[DESCRIPTION_KEY]}

            {self.employee_reward()}
            """),
            agent=agent,
            expected_output=task_config[EXPECTED_OUTPUT_KEY]
        )

    def final_report_employee(self, agent):
        task_config = self.config[TASKS_KEY][RECOMMEND_KEY]
        return Task(
            description=dedent(f"""
            {task_config[DESCRIPTION_KEY]}

            {self.employee_reward()}
            """),
            agent=agent,
            expected_output=task_config[EXPECTED_OUTPUT_KEY]
        )