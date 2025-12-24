from google.adk.agents.llm_agent import Agent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.book_recommender.agent import book_recommender
from .sub_agents.news_analyst.agent import news_analyst
from .sub_agents.crypto_analyst.agent import crypto_analyst
from .tools.tools import get_current_time

root_agent = Agent(
    model='gemini-2.5-flash',
    name='manager_agent',
    description='Manager agent responsible for overseeing operations',
    instruction="""
    You are a manager agent responsible for overseeing and delegating work to appropriate specialized sub-agents.

    Always delegate the user's request to the most suitable sub-agent.
    Use your best judgment to decide which agent can best accomplish the task.

    You can delegate tasks to the following sub-agents:
    - crypto_analyst: Expert in cryptocurrency market analysis and trends.
    - book_recommender: Specialist in recommending books based on user preferences.

    You also have access to the following tools:
    - news_analyst: Tool for analyzing current news articles and extracting relevant information.
    - get_current_time: Tool to fetch the current date and time.
    """,
    sub_agents=[crypto_analyst, book_recommender],
    tools=[AgentTool(news_analyst), get_current_time],
)
