import requests
import xmltodict
import datetime
import mpu
import networkx as nx
from Vehicle import Vehicle


# TTC vehicle data: https://webservices.umoiq.com/service/publicXMLFeed?command=vehicleLocations&a=ttc
# TTC stop data: https://webservices.umoiq.com/service/publicXMLFeed?command=routeConfig&a=ttc&r=905
# TTC route data: https://webservices.umoiq.com/service/publicXMLFeed?command=routeList&a=ttc
# Public XML Feed documentation: https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/8217e43a-bba2-4e6c-82f5-bf6d1a52545d/resource/84572a3e-8537-4793-8a92-61107bab85f4/download/NextBusXMLFeed.pdf

if __name__ == '__main__':
    url = "https://webservices.umoiq.com/service/publicXMLFeed?command=vehicleLocations&a=ttc"
    response = requests.get(url)
    data =xmltodict.parse(response.content) 

    #print(data["body"]["vehicle"])

    route_number = input("What route number are you looking for? ")

    route_count = 0

    vehicles = []

    for vehicle in data["body"]["vehicle"]:
        if vehicle["@routeTag"] == route_number:
            print(vehicle["@lat"], " ", vehicle["@lon"])
            route_count += 1
            new = Vehicle(vehicle["@dirTag"])
            vehicles.append(new)

    time = data["body"]["lastTime"]["@time"]

    currernt_time = datetime.datetime.fromtimestamp( int(time)/1000)
    print("Current time: ", currernt_time)
    print("Vehicle count: ", route_count, " for route ", route_number)

    for bus in vehicles:
        print(bus.compassHeading)
