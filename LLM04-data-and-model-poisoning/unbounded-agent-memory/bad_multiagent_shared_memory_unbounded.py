"""A crew of agents shares one memory list that grows every round.

Triggers unbounded-agent-memory: every agent, on every hand-off round,
appends its result to the shared list — there is no per-agent or
global cap on how many entries the shared memory can hold.
"""
from crewai import Agent, Crew, Task

shared_memory: list[str] = []


class LoggingAgent(Agent):
    def execute_task(self, task, context=None, tools=None):
        result = super().execute_task(task, context, tools)
        shared_memory.append(result)  # every agent, every round, forever
        return result


researcher = LoggingAgent(role="Researcher", goal="Research topics", backstory="...")
writer = LoggingAgent(role="Writer", goal="Write reports", backstory="...")
crew = Crew(
    agents=[researcher, writer],
    tasks=[Task(description="Research and write", agent=researcher)],
)
