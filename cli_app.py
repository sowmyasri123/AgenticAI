from crewai import Crew, LLM
from trip_agents import TripAgents
from trip_tasks import TripTasks
from datetime import datetime
import argparse
from datetime import datetime
from crewai.memory import  EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
import os
from dotenv import load_dotenv
load_dotenv()

class TripCrew:
    def __init__(self, origin, cities, date_range, interests,budget):
        self.cities = cities
        self.origin = origin
        self.interests = interests
        self.date_range = date_range
        self.budget=budget
        self.llm = LLM(model="gpt-4.1-mini")
        #self.llm = LLM(model="gemini/gemini-2.0-flash-lite")
        self.storage_path = os.getenv("CREWAI_STORAGE_DIR", "./storage")


    def run(self):
        try:
            agents = TripAgents(llm=self.llm)
            tasks = TripTasks()
            city_selector_agent = agents.city_selection_agent()
            local_expert_agent = agents.local_expert()
            travel_concierge_agent = agents.travel_concierge()

            identify_task = tasks.identify_task(
                city_selector_agent,
                self.origin,
                self.cities,
                self.interests,
                self.date_range,
                self.budget
            )

            gather_task = tasks.gather_task(
                local_expert_agent,
                self.origin,
                self.interests,
                self.date_range,
                self.budget
            )

            plan_task = tasks.plan_task(
                travel_concierge_agent,
                self.origin,
                self.interests,
                self.date_range,
                self.budget
            )

            crew = Crew(
                agents=[
                    city_selector_agent, local_expert_agent, travel_concierge_agent
                ],
                tasks=[identify_task, gather_task, plan_task],
                memory=True,
                entity_memory = EntityMemory(
                storage=RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {
                            "model": 'text-embedding-3-small'
                        }
                    },
                    type="short_term",
                    path=self.storage_path
                )
            ),                      
                output_log_file="trip_log.json",  
                verbose=True 
            )

            result = crew.kickoff()
            return result
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

def validate_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format. Please use YYYY-MM-DD")

def main():
    # Load environment variables from .env file
    load_dotenv()
    # Check if required API keys are set
    required_keys = ['OPENAI_API_KEY', 'SERPER_API_KEY', 'BROWSERLESS_API_KEY']
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        print(f"Error: Missing required environment variables: {', '.join(missing_keys)}")
        print("Please set them in your .env file or environment.")
        return

    parser = argparse.ArgumentParser(description='AI Travel Planner')
    
    parser.add_argument('--origin', '-o', 
                       type=str, 
                       required=True,
                       help='Your current location (e.g., "San Mateo, CA")')
    
    parser.add_argument('--destination', '-d', 
                       type=str, 
                       required=True,
                       help='Destination country')
    
    parser.add_argument('--start-date', '-s',
                       type=validate_date,
                       required=True,
                       help='Start date of your trip (YYYY-MM-DD)')
    
    parser.add_argument('--end-date', '-e',
                       type=validate_date,
                       required=True,
                       help='End date of your trip (YYYY-MM-DD)')
    
    parser.add_argument('--interests', '-i',
                       type=str,
                       required=True,
                       help='Your interests and trip details (e.g., "2 adults who love swimming, dancing, hiking")')
    
    parser.add_argument('--budget', '-b',
                       type=float,
                       required=True,
                       help='Budget of your trip in $USD")')

    args = parser.parse_args()

    # Validate dates
    if args.end_date <= args.start_date:
        print("Error: End date must be after start date")
        return
    


    # Format date range as string
    date_range = f"{args.start_date} to {args.end_date}"

    print("\nTravel Concierge Agent")
    print("================================")
    print(f"\nPlanning your trip...")
    print(f"From: {args.origin}")
    print(f"To: {args.destination}")
    print(f"Dates: {date_range}")
    print(f"Interests: {args.interests}")
    print(f"Budget: {args.budget}")
    print("\nThis may take a few minutes. Please wait while our AI agents work on your perfect trip...\n")

    trip_crew = TripCrew(args.origin, args.destination, date_range, args.interests,args.budget)
    result = trip_crew.run()

    if result:
        print("\n✨ Your Trip Plan ✨")
        print("===================\n")
        print(result)
    else:
        print("\n Failed to generate trip plan. Please try again.")

if __name__ == "__main__":
    main()