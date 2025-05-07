from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import CSVSearchTool
from match_job_role_with_many_cvs.tools.cv_reader_tool import CVReaderTool

@CrewBase
class MatchJobRoleWithManyCvs():
    """MatchJobRoleWithManyCvs crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    
    @agent
    def cv_reader(self) -> Agent:
        return Agent(
            config=self.agents_config['cv_reader'],
            tools=[CVReaderTool()],
            verbose=True,
			allow_delegation=False
        )

    @agent
    def candidate_filter(self) -> Agent:
        return Agent(
            config=self.agents_config["candidate_filter"],
            tools=[CVReaderTool(), CSVSearchTool()],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def matcher(self) -> Agent:
        return Agent(
            config=self.agents_config["matcher"],
            tools=[CVReaderTool(), CSVSearchTool()],
            verbose=True,
            allow_delegation=False
        )

    @task
    def read_cv_task(self) -> Task:
        return Task(
            config=self.tasks_config["read_cv_task"],
            agent=self.cv_reader()
        )

    @task
    def filter_candidates_task(self) -> Task:
        return Task(
            config=self.tasks_config["filter_candidates_task"],
            agent=self.candidate_filter()
        )

    @task
    def match_cv_task(self) -> Task:
        return Task(
            config=self.tasks_config["match_cv_task"],
            agent=self.matcher()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MatchJobRoleWithManyCvs crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
    
    
