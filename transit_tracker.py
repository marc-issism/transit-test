import requests
import xmltodict

#TODO: add int, string guard asserters to function calls

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
    string to get all the vehicles on a route. If 'route_num' is 0, all routes will be counted.
    Returns 0 if branch does not exist or if there are no vehicles currently on the route, 
    otherwise return -1 if route is not active.
    """

    if route_num == '0':
        response = requests.get(URL + 'vehicleLocations&a=ttc')
        branch = ''
    else:
        response = requests.get(URL + 'vehicleLocations&a=ttc&r=' + route_num + '&t=0')
    data = xmltodict.parse(response.content)
    count = 0
    route_num = '_' + route_num + str.upper(branch)

    try:
        # Branch is specified
        if branch != '':
            for vehicle in data['body']['vehicle']:
                if '@dirTag' in vehicle.keys():
                    if route_num in vehicle['@dirTag']:
                        count += 1
        # Branch is not specified
        else:
            for vehicle in data['body']['vehicle']:
                if vehicle['@predictable'] == 'true':
                    count += 1 
    except KeyError:
        #print("Route " + route_num[1:] + " is not currently active.")
        return -1

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
        stop_title = data['body']
        print(stop_title['predictions'][0]['@stopTitle'])
        prediction_list = prediction_list + ',' + stop_title['predictions'][0]['@stopTitle']
    except KeyError:
        print(stop_title['predictions']['@stopTitle'])
        prediction_list = prediction_list + ',' + stop_title['predictions']['@stopTitle']

    info = data['body']['predictions']

    if isinstance(info, list): # Multiple Routes
        for route in info:
            if '@dirTitleBecauseNoPredictions' in route.keys():
                print(route['@dirTitleBecauseNoPredictions'])
            else:
                if '@dirTitleBecauseNoPredictions' in route.keys():
                    print(route['@dirTitleBecauseNoPredictions'])
                elif isinstance(route['direction'], list):
                    for direction in route['direction']:
                        print(direction['@title'])
                        if isinstance(direction['prediction'], dict):
                            print(direction['prediction']['@minutes'] + ' minutes')
                        if isinstance(direction['prediction'], list):
                            for prediction in direction['prediction']:
                                print(prediction['@minutes'] + ' minutes')
                elif isinstance(route['direction'], dict): 
                    print(route['direction']['@title'])
                    for prediction in route['direction']['prediction']:
                        print(prediction['@minutes'] + ' minutes') 

    try: # One route w/o branches
        if isinstance(info, dict):
            if '@dirTitleBecauseNoPredictions' in info.keys():
                print(info['@dirTitleBecauseNoPredictions'])
            else:
                print(info['direction']['@title'])
                for prediction in info['direction']['prediction']:
                    print(prediction['@minutes'] + ' minutes')
    
    except: # One route w/ Branches
        for route in info['direction']:
            if '@dirTitleBecauseNoPredictions' in route.keys():
                print(route['@dirTitleBecauseNoPredictions'])
            else:
                print(route['@title'])
                if isinstance(route['prediction'], dict):
                    print(route['prediction']['@minutes'] + ' minutes')
                if isinstance(route['prediction'], list):
                    for prediction in route['prediction']:
                        print(prediction['@minutes'] + ' minutes')

    return prediction_list[1:]

def branch_route(route: dict):
    print(route['@title'])
    if isinstance(route['prediction'], dict):
        print(route['prediction']['@minutes'] + ' minutes')
    if isinstance(route['prediction'], list):
        for prediction in route['prediction']:
            print(prediction['@minutes'] + ' minutes')

def no_branch_route(route: dict):
    print(route['direction']['@title'])
    for prediction in route['direction']['prediction']:
        print(prediction['@minutes'] + ' minutes')

def get_frequency(route_num: str, branch: str) -> int:
    return -1


