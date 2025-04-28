
from crewai import Agent
from langchain_core.language_models.chat_models import BaseChatModel
from crewai import LLM
from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools

class TripAgents():
    def __init__(self, llm: BaseChatModel = None):
        if llm is None:
            self.llm = LLM(model="gpt-4.1-mini")
            #self.llm = LLM(model="gemini/gemini-2.0-flash-lite")
        else:
            self.llm = llm

        # Initialize tools once
        self.search_tool = SearchTools()
        self.browser_tool = BrowserTools()
        self.calculator_tool = CalculatorTools()

    def city_selection_agent(self):
        return Agent(
            role='City Selection Expert',
            goal='Select the best city based on weather, preferences, and prices',
            backstory='An expert in analyzing travel data to pick ideal destinations',
            tools=[self.search_tool, self.browser_tool],
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def local_expert(self):
        return Agent(
            role='Local Expert at this city',
            goal='Provide the BEST insights about the selected city',
            backstory="""A knowledgeable local guide with extensive information
        about the city, it's attractions and customs""",
            tools=[self.search_tool, self.browser_tool],
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def travel_concierge(self):
        return Agent(
            role='Travel Concierge Agent',
            goal="""Create the most amazing travel itineraries with budget and 
        packing suggestions for the city""",
            backstory="""Specialist in travel planning and logistics with 
        decades of experience""",
            tools=[self.search_tool, self.browser_tool, self.calculator_tool],
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )
