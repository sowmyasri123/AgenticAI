from crewai import Task
from textwrap import dedent
class TripTasks():
    def __validate_inputs(self, origin, cities, interests, date_range,budget):
        if not origin or not cities or not interests or not date_range or not budget:
            raise ValueError("All input parameters must be provided")
        return True

    def identify_task(self, agent, origin, destination, interests, range,budget):
        self.__validate_inputs(origin, destination, interests, range,budget)
        return Task(description=dedent(f"""
            Analyse and Come up with the list of cities with the added preferences in this destination.
            You must search for flight from the source location to destination location.
            Compare flight prices between different cities for the date and choose the cheap flight considering the total budget {budget}
            with direct connection preferbly morning time. Then choose the city that matches prefernces with cheap flight cost for the date.

            consider exploring nearby cities as well if time permits.

            Your final answer must be a detailed
            report on the chosen city, and everything you found out
            about it, including the actual flight costs, weather
            forecast and attractions. 
            
            Use websites like skyscaanner for flight information.


            Traveling from: {origin}
            City Options: {destination}
            Trip Date: {range}
            Traveler Interests: {interests}
          """),
            expected_output="A detailed report on the chosen city with flight costs, weather forecast, and attractions.",
            agent=agent)

    def gather_task(self, agent, origin, interests, range,budget):
        return Task(description=dedent(f"""
            As a local expert on this c-selected you must compile an
            in-depth guide for someone traveling there and wanting
            to have the best trip ever!
            Gather information about  key attractions, local customs,
            special events, and daily activity recommendations.
            Find the best spots to go to, the kind of place only a
            local would know to eat and roam.
            This guide should provide a thorough overview of what
            the c-selected has to offer, including hidden gems, cultural
            hotspots, must-visit landmarks and
            high level costs.
            use the official website of landmarks to check prices. 
            Also check if the passes are available for cheap prices than one time ticket.
                                       
            The final answer must be a comprehensive c guide,
            rich in cultural insights and practical tips,
            tailored to enhance the travel experience.


            Trip Date: {range}
            Traveling from: {origin}
            Traveler Interests: {interests}

          """),
            expected_output="A comprehensive city guide with cultural insights and practical tips.",
            agent=agent)

    def plan_task(self, agent, origin, interests, range,budget):
        return Task(description=dedent(f"""
            Expand this guide into a full travel
            itinerary for this time {range} with budget {budget}with detailed per-day plans by utilising time efficiently, including
            weather forecasts, places to eat, packing suggestions,adventure activities
            and a budget breakdown.

            You MUST suggest actual places to visit, actual hotels
            to stay and actual restaurants to go to.

            For hotels check the prices from the bookings.com for the date.

            For entry ticket prices check from their official site.

            This itinerary should cover all aspects of the trip,
            from arrival to departure, integrating the city guide
            information with practical travel logistics.

            Your final answer MUST be a complete expanded travel plan,
            formatted as markdown, encompassing a daily schedule,
            anticipated weather conditions, recommended clothing and
            items to pack, and a detailed budget, ensuring THE BEST
            TRIP EVER, Be specific and give it a reason why you picked
            #up each place, what make them special! 
            # 
            # finally display the total budget with categories like food,travel etc

            Trip Date: {range}
            Traveling from: {origin}
            Traveler Interests: {interests}
          """),
            expected_output="A complete travel plan, formatted as markdown, with a daily schedule and budget.",
            agent=agent
                )

