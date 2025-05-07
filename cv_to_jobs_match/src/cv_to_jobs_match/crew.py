from tabnanny import verbose
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import CSVSearchTool, FileReadTool
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class CvToJobsMatch():
    """CvToJobsMatch crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def cv_reader(self) -> Agent:
        return Agent(
            config=self.agents_config['cv_reader'],
            tools=[FileReadTool()],
            verbose=True,
			allow_delegation=False
        )

    @agent
    def matcher(self) -> Agent:
        return Agent(
            config=self.agents_config["matcher"],
            tools=[FileReadTool(), CSVSearchTool()],
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
    def match_cv_task(self) -> Task:
        return Task(
            config=self.tasks_config["match_cv_task"],
            agent=self.matcher()
        )



    @crew
    def crew(self) -> Crew:
        """Creates the CvToJobsMatch crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
