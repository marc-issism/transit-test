import requests
import xmltodict

URL = 'https://webservices.umoiq.com/service/publicXMLFeed?command='


def print_route_list() -> None:
    """Output the list of all TTC routes."""
    response = requests.get(URL + 'routeList&a=ttc')
    data = xmltodict.parse(response.content)

    for route in data['body']['route']:
        print(route['@title'])


def get_route_list() -> str:
    """Return every route separated by a comma (,). """
    response = requests.get(URL + 'routeList&a=ttc')
    data = xmltodict.parse(response.content)
    route_list = ''

    for route in data['body']['route']:
        route_list = route_list + ',' + route['@title']
    
    return route_list[1:]


def get_num_of_vehicles(route_num: str, branch: str) -> int:
    """Return the number of buses currently serving the given route number 'route_num'.
    The 'branch' parameter refers to a specific branch of the route, leave as an empty 
    string to get all the vehicles on a route. Returns 0 if branch does not exist or if there
    are no vehicles currently on the route.
    """
    response = requests.get(URL + 'vehicleLocations&a=ttc&r=' + route_num + '&t=0')
    data = xmltodict.parse(response.content)
    count = 0
    route_num = '_' + route_num + str.upper(branch)

    # Branch not empty string
    if branch != '':
        for vehicle in data['body']['vehicle']:
            if '@dirTag' in vehicle.keys():
                if route_num in vehicle['@dirTag']:
                    count += 1
    else:
        for vehicle in data['body']['vehicle']:
            if vehicle['@predictable'] == 'true':
                count += 1  

    return count


def get_branches(route_num: str) -> str:
    """Return the branches of a given route 'route_num' separated by a commma (,)."""
    response = requests.get(URL + 'routeConfig&a=ttc&r=' + route_num + '&t=0')
    data = xmltodict.parse(response.content)   

    branch_list = ''

    for branch in data['body']['route']['direction']:
        branch_list = branch_list + ',' + branch['@title']
    
    return branch_list[1:]


def get_stop_list():
    return None


def get_prediction(stop_id: int) -> str:
    """Return the routes and the next vehicles for a given stop. Each term is separated
    by a comma (,)."""
    response = requests.get(URL + 'predictions&a=ttc&stopId=' + stop_id)
    data = xmltodict.parse(response.content)

    prediction_list = ''

    try: 
        for route in data['body']['predictions']['direction']:
            print(route['@title'])
    except: # A TypeError would have been raised because 'route' would become a string in the case of inactive routes.
        for route in data['body']['predictions']:
            if 'direction' in route.keys():
                print(route['direction']['@title'])
            else:
                print(route['@routeTitle'])
    
    return prediction_list[1:]