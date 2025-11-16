
#Author:
#Date:
#Student ID:20240454

import csv
from collections import defaultdict
from datetime import datetime, timedelta

# Task A: Input Validation
def validate_date_input():
#prompt the year
    while True:
        try:
            year=int(input("Please enter the year of the survey in the format YYYY:"))
            if 2000<=year<=2024:
                if (year%4==0 and year%100!=0 or year%400==0):
                    leap_year_checking=True
                    break
                else:
                    leap_year_checking=False
                    break
            else:
                print("Out of Range-values must be in the  range from 2000 to 2024")
                continue
        except ValueError:
            print("Integer required.")

#prompt the month
    while True:                
        try:
            month=int(input("Please enter the month of the survey in the format MM:"))
            if month<1 or month>12:
                print("Out of Range-values must be in the range 1 to 12")
                continue
            else:
                break
        except ValueError:
            print("Integer required.")

#prompt the date
    while True:
        try:
            day=int(input("Please enter the day of the survey in the format dd:"))
            End_in_31=[1,3,5,7,8,10,12]
            End_in_30=[4,6,9,11]
            
            if month in End_in_31:
                if day<1 or day>31:
                    print("Out of Range-values must be in the range 1 and 31")
                    continue
                else:
                    break
            elif month in End_in_30:
                if day<1 or day>30:
                    print("Out of Range-values must be in the range 1 and 30")
                    continue
                else:
                    break
            else:
                if leap_year_checking==True:
                    if 1<=day<=29:
                        break
                    else:
                        print("Out of Range-values must be in the range 1 and 29")
                else:
                    if 1<=day<=28:
                        break
                    else:
                        print("Out of Range-values must be in the range 1 and 28")
        except ValueError:
            print("Integer required.")
            
    file_name=f"traffic_data{day:02d}{month:02d}{year}.csv"
    return file_name

def validate_continue_input():
    while True:
        repetition=input('Do you want to load another data file? Y/N : ').upper().strip()
        if repetition == 'Y':
            print('Loading new dataset...')
            return "y"
        
        elif repetition == 'N':
            print('End of run')
            return "n"
        
        else:
            print('Please enter Y or N')
       


# Task B: Processed Outcomes
def process_csv_data(file_path):
    try:
        with open(file_path) as file:
            reader=csv.DictReader(file)
            data=list(reader)
    except FileNotFoundError:
        print(f"File{file_path} not found.")
        return None
    
    #Initialize a dictionary to store outcomes
    outcomes=defaultdict(int)
    
    total_vehicles=len(data)
    outcomes["Total Vehicles"]=total_vehicles

    #Calculate outcomes
    hourly_vehicles=defaultdict(int)
    peak_times=[]
    peak_hour_vehicles=0
    rain_hours=set() 

    for row in data:
        vehicle_type=row["VehicleType"]
        junction_name=row["JunctionName"]
        speed_limit=int(row["JunctionSpeedLimit"])
        vehicle_speed=int(row["VehicleSpeed"])
        travel_Direction_in=row["travel_Direction_in"]
        travel_Direction_out=row["travel_Direction_out"]
        weather_condition=row["Weather_Conditions"]
        timestamp=row["timeOfDay"]
        electric=row["elctricHybrid"]

    
        
        #Total number of trucks
        if vehicle_type=="Truck":
            outcomes["Total Trucks"]+=1

        #Total number of electrical vehicles
        if electric.strip().upper()=="TRUE":
            outcomes["Total Electrical Vehicles"]+=1
            

        #Total number of two-wheeled vehicles
        if vehicle_type in ["Bicycle","Motorcycle","Scooter"]:
            outcomes["Total of two-wheeled vehicles"]+=1
            
        # Total number of busses leaving through the Elm Avenue junction
        if junction_name=='Elm Avenue/Rabbit Road' and vehicle_type =="Buss" and travel_Direction_out=="N" :
            outcomes["Elm Ave buses"]+=1 

        #Total number of bicycles
        if vehicle_type=="Bicycle":
            outcomes["Total Bicycles"]+=1

        #Total number of straight moving vehicles
        if travel_Direction_in == travel_Direction_out:
            outcomes["Straight Moving Vehicles"]=outcomes["Straight Moving Vehicles"]+1

        #Vehicles exceeding the speed limit 
        if vehicle_speed > speed_limit:
            outcomes["Over Speeding Vehicles"]+=1
            
        #Total vehicles recorded at Elm Avenue/Rabbit Road Junction  
        if junction_name=="Elm Avenue/Rabbit Road":
            outcomes["Elm Ave Vehicles"]+=1

        #Total vehicles recorded at Hanley Highway/Westway junction
        if junction_name=="Hanley Highway/Westway":
            outcomes["Hanley Hwy Vehicles"]+=1

        #Percentage of scooters passing through Elm Avenue/Rabbit Road
        if vehicle_type=="Scooter" and junction_name=="Elm Avenue/Rabbit Road":
            outcomes["Elm Ave scooters"]+=1

        #Check if the weather condition
        if weather_condition in ["Light Rain","Heavy Rain"]:
            rain_hours.add(timestamp[:2])
        

        #add hourly vechicle count into dict
        if junction_name == "Hanley Highway/Westway":
            hour = timestamp.split(":")[0]
            hourly_vehicles[hour] +=1

    #Calculate the percentage of trucks among all vehicles
    if total_vehicles>0:
            outcomes["Trucks Percentage"]=round((outcomes["Total Trucks"]/total_vehicles)*100)

    #Calculate the percentage of scooters at Elm Avenue/Rabbit Road junction
    if outcomes["Elm Ave Vehicles"]>0:
            outcomes["Scooter Percentage in Elm Ave"]=round((outcomes["Elm Ave scooters"]/outcomes["Elm Ave Vehicles"])*100)

    #Calculate the average number of bicycles per hour
    if outcomes["Total Bicycles"]>0:
            outcomes["The average number of bicycles per hour"]=round(outcomes["Total Bicycles"]/24)

    #Peak hour calculations
    peak_hour_vehicles=max(hourly_vehicles.values())
    peak_times=[f"Between {hour}:00 and {int(hour)+1}:00"
                for hour,count in hourly_vehicles.items() if count==peak_hour_vehicles]
    
    #caculate rain hours
    totalRainHours = len(rain_hours)
        
    #store results in outcomes
    outcomes = [
        '***************************************************************',
        f'Data file selected: {file_path}',
        '***************************************************************',
        
        f'The total number of vehicles recorded for this data is {outcomes["Total Vehicles"]}',
        f'The total number of trucks recorded for this data is {outcomes["Total Trucks"]}',
        f'The total number of electric vehicles recorded for this data is {outcomes["Total Electrical Vehicles"]}',
        f'The total number of two-wheeled vehicles recorded for this data is {outcomes["Total of two-wheeled vehicles"]}',
        f'The total number of busses leaving Elm Avenue/Rabbit Road heading North is {outcomes["Elm Ave buses"]}',
        f'The total number of vehicles through both junctions not turning left or right is {outcomes["Straight Moving Vehicles"]}',
        f'The percentage of total vehicles recorded that are trucks for this data is {outcomes["Trucks Percentage"]}%',
        f'The average number of bicycles per hour for this data  is {outcomes["The average number of bicycles per hour"]}',
        '',
        f'The total number of vehicles recorded as over the speed limit for this date is {outcomes["Over Speeding Vehicles"]}',
        f'The total number of trucks recorded through Elm Avenue/Rabbit Road junction is {outcomes["Elm Ave Vehicles"]}',
        f'The total number of trucks recorded through Hanley Highway/Westway junction is {outcomes["Hanley Hwy Vehicles"]}',
        f'{outcomes["Scooter Percentage in Elm Ave"]}% of the vehicles recorded through Elm Avenue/Rabbit Road are scooters',
        '',
        f'Peak Hour Vehicles at  Hanley Highway/westway is {peak_hour_vehicles}',
        f'Peak Traffic Time(s) is {",".join(peak_times)}',
        f'Total Rain Hours is {totalRainHours}'
    ]
        
    return outcomes

#Function to display calculated outcomes   
def display_outcomes(outcomes):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    print("\nCalculated Outcomes:")

    for line in outcomes:

        print(line)

    print("\n")



# Task C: Save Results to Text File
def save_results_to_file(outcomes, file_name="results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    try:
        with open(file_name,"a")as file:
            for outcome in outcomes:
                file.write(outcome + '\n')
        
    except Exception as e:
       # print(f"Error saving results to file : {e}")
        print(e)



while True:
    File_Name=validate_date_input()
    outcomes=process_csv_data(File_Name)

    if outcomes:
        display_outcomes(outcomes)
        save_results_to_file(outcomes)
    
    status=validate_continue_input()
    if status == "n":
        break

    

