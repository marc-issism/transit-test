import requests
import xmltodict

URL_VEHICLE_LOCATIONS = 'https://webservices.umoiq.com/service/publicXMLFeed?command=vehicleLocations&a=ttc'
URL_ROUTES = 'https://webservices.umoiq.com/service/publicXMLFeed?command=routeConfig&a=ttc&r='

class Route:

    number = 0 # The number of the route
    direction = 'NULL' # N, S, E, W ONLY
    stops = [] #Array of Stops
    num_active_vehicles = 0 # Number of active vehicles on the route currently


    def __init__(self, number:int) -> None:
        """Constructor for the class Route.

        number: Used as the ID that will refer to the route.
        """

        self.number = number


        self.num_active_vehicles = Route.count_active_vehicles(number)


    def count_active_vehicles(route_number: int) -> int:
        """Given the route number for a route, return the number of active vehicles on route.
        """

        active_vehicles = 0
        response = requests.get(URL_VEHICLE_LOCATIONS)
        data = xmltodict.parse(response.content)

        # If the route matches the vehicle, add 1 to the count
        for vehicle in data['body']['vehicle']:
            if vehicle['@routeTag'] == route_number:
                active_vehicles += 1
        return active_vehicles




    