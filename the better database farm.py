import pymongo

client = pymongo.MongoClient("127.0.0.1", 27017) #create database
db = client.get_database("FoodSecurity")
locations = db.get_collection("Locations")
plants = db.get_collection("Plants")
db.drop_collection("Locations")
db.drop_collection("Plants")

with open('location.csv') as csv_file: #inserting location data into Locations collection
    for line in csv_file:
        lst = line.strip().split(',')
        locations.insert_one({"location":lst[0].upper(), "temperature":lst[1],
                         "humidity":lst[2], "wind speed":lst[3],
                         "area":lst[4]})

with open('Plants.csv') as csv_file: #inserting plant data into Plants collection
    for line in csv_file:
        lst = line.strip().split(',')
        plants.insert_one({"veg_name":lst[0].upper(), "min_temp":lst[1],
                         "max_temp":lst[2]})

result_plant = [] #plant data as list
plant_pointer = plants.find()
for i in plant_pointer:
    result_plant.append(i)

def verdict(result): #Algorithm to determine if land is suitable for specific vegetables
      plantable = []
      for item in result_plant:
            if float(result["temperature"]) > float(item["min_temp"]) and float(result["temperature"]) < float(item["max_temp"]) and int(result["humidity"]) > 50 and int(result["wind speed"]) < 30 and int(result["area"]) > 51:
                  plantable.append(item["veg_name"])
      return plantable



print("Farmable area Database \n\
--------------------------")

result = locations.find() #Listing available locations in database
for i in result:
    print(i["location"])
print(" ")

#this input will be from the website
place = input("Please enter chosen location: ") #input user chosen location
place = place.replace(" ","")

while place != "stop": #while loop till input is stop

    while not place.isalpha(): #Data validation
        print("Invalid input")
        place = input("Please enter chosen location again: ")
    place = place.replace(" ","")

    result = locations.find_one({"location":place.upper()}) #finding chosen location
   
    if result == None: #If location does not exist
        print("Location does not exist")
        place = input("Please enter another location: ")
        place = place.replace(" ","")

        while not place.isalpha(): #data validation
            print("Invalid input")
            place = input("Please enter chosen location again: ")
            place = place.replace(" ","")
       
    else: #printing of data
        print(" ")
        print("Plants that can be planted: ", verdict(result))
        print("Location: ", result["location"])
        print("Temperature (°C): ", result["temperature"])
        print("Humidity (%): ", result["humidity"])
        print("Wind Speed (km/h): ", result["wind speed"])
        print("Land Area useable: ", result["area"])
        print(" ")

        place = input("Please enter another location: ") #ask for another location
        place = place.replace(" ","")

        while not place.isalpha(): #Data validation
            print("Invalid input")
            place = input("Please enter chosen location again: ")
            place = place.replace(" ","")

print("end")
