import requests
import xmltodict
import datetime
import mpu
import networkx as nx
from Vehicle import Vehicle
from Route import Route
import transit_tracker as tt


# TTC vehicle data: https://webservices.umoiq.com/service/publicXMLFeed?command=vehicleLocations&a=ttc
# TTC stop data: https://webservices.umoiq.com/service/publicXMLFeed?command=routeConfig&a=ttc&r=905
# TTC route data: https://webservices.umoiq.com/service/publicXMLFeed?command=routeList&a=ttc
# Public XML Feed documentation: https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/8217e43a-bba2-4e6c-82f5-bf6d1a52545d/resource/84572a3e-8537-4793-8a92-61107bab85f4/download/NextBusXMLFeed.pdf

if __name__ == '__main__':
    url = "https://webservices.umoiq.com/service/publicXMLFeed?command=vehicleLocations&a=ttc"
    response = requests.get(url)
    data =xmltodict.parse(response.content) 

    #print(data["body"]["vehicle"])



    #currernt_time = datetime.datetime.fromtimestamp( int(time)/1000)

    #tt.print_route_list()
    ##print(tt.get_num_of_vehicles_on_route('68', 'A'))
    ##print(tt.get_num_of_vehicles_on_route('68', ''))

    #print(tt.get_route_list())

    #print(tt.get_num_of_vehicles('501', 'b'))
    #print(tt.get_branches('68'))

    print(tt.get_prediction('8586'))

