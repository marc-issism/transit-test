import requests
import xmltodict
import datetime
import mpu
from Vehicle import Vehicle

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
