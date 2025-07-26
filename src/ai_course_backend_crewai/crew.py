from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class AiCourseBackendCrewai():
    """
    AiCourseBackendCrewai crew
    
    Crew class for generating AI-powered personalized mini-courses on any topic.

    This class configures all agents and task flows using the YAML-defined configurations.
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    # === AGENTS ===

    @agent
    def curriculum_designer(self) -> Agent:
        return Agent(
            config=self.agents_config["curriculum_designer"],
            verbose=True
        )

    @agent
    def content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["content_creator"],
            verbose=True
        )

    @agent
    def quiz_master(self) -> Agent:
        return Agent(
            config=self.agents_config["quiz_master"],
            verbose=True
        )

    @agent
    def content_editor(self) -> Agent:
        return Agent(
            config=self.agents_config["content_editor"],
            verbose=True
        )

    @agent
    def format_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["format_agent"],
            verbose=True
        )

    # @agent
    # def feedback_agent(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["feedback_agent"],
    #         verbose=True
    #     )

    # === TASKS ===

    @task
    def curriculum_design_task(self) -> Task:
        return Task(
            config=self.tasks_config["curriculum_design_task"]
        )

    @task
    def content_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config["content_creation_task"]
        )

    @task
    def quiz_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config["quiz_generation_task"]
        )

    @task
    def content_editing_task(self) -> Task:
        return Task(
            config=self.tasks_config["content_editing_task"]
        )

    @task
    def formatting_task(self) -> Task:
        return Task(
            config=self.tasks_config["formatting_task"],
            output_file="final_course_output.md"
        )

    # @task
    # def feedback_loop_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["feedback_loop_task"]
    #     )

    # === CREW FLOW ===

    @crew
    def crew(self) -> Crew:
        """
        Builds the complete crew with all agents and their defined tasks,
        run in a SEQUENTIAL process from outline to delivery.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,  # You may switch to .hierarchical if FeedbackAgent leads decisions
            verbose=True
        )
