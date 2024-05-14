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

    try:
        for route in data['body']['predictions']:
            # Active but no predictions
            if '@dirTitleBecauseNoPredictions' in route.keys():
                print(route['@dirTitleBecauseNoPredictions'])
                prediction_list = prediction_list + ',' + route['@dirTitleBecauseNoPredictions']
            # Active with predictions
            elif 'direction' in route.keys(): 
                print(route['direction']['@title'])
                prediction_list = prediction_list + ',' + route['direction']['@title']
                # Multiple predictions
                if isinstance(route['direction']['prediction'], list):
                    for time in route['direction']['prediction']:
                        print(time['@minutes'] + ' minutes')
                        prediction_list = prediction_list + ',' + time['@minutes'] + ' minutes'
                # Only one prediction
                else:
                    print(route['direction']['prediction']['@minutes'] + ' minutes')
                    prediction_list = prediction_list + ',' + route['direction']['prediction']['@minutes'] + ' minutes'
            # Inactive
            else: 
                print(route['@routeTitle'])
                prediction_list = prediction_list + ',' + route['@routeTitle']
    except AttributeError: # Stop has only active routes
        print(data['body']['predictions']['direction']['@title'])
        for route in data['body']['predictions']['direction']['prediction']:
            print(route['@minutes'] + ' minutes')
            prediction_list = prediction_list + ',' + route['@minutes'] + ' minutes'

    return prediction_list[1:]


def get_frequency(route_num: str, branch: str) -> int:
    return -1


