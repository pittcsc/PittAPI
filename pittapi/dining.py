import requests
import json
import datetime
from typing import Any, Dict, List

# pitt site id = 5e6fcc641ca48e0cacd93b04

locations = {
    'The Eatery': '610b1f78e82971147c9f8ba5',
    'The Perch': '6123ff86a9f13a2a48c2a8ed',
    'The Pierogi': '62f65fd9e45d4305a44d80d5',
    'Wicked Pie': '62f666cee45d4305a44e517d',
    # more to go here, should i add all here?
    # wrote get_all_locations() to do this as well
}


def get_location_hours(date=datetime.datetime.today()) -> Dict[str, List[Any]]:
    """
    - gets hours of all locations for entire week
        - starting from sunday to monday
    - date must in YYYY-MM-DD format
    - return format will be a dictionary
        - keys => location name
        - values => list containing info of each day of the week being a list of [date, status, open hours, close hours]
    """

    url = "https://api.dineoncampus.com/v1/locations/weekly_schedule?site_id=5e6fcc641ca48e0cacd93b04&date="
    if type(date) == datetime.datetime:
        url = url + date.strftime("%Y-%m-%d")
    else:
        url += date

    loc_hours = requests.get(url).json()

    hours = {}

    # location_name : [ [date, status, open, close], [], [], ... ]
    for i in loc_hours["the_locations"]:
        week_info = []  # week info contains list of [date, status, open time, close time]
        for j in i["week"]:
            date = j["date"]

            if j["status"] == "closed":  # to handle so locations having hours despite being closed
                start_time = 0
                end_time = 0
            else:
                start_time = datetime.time(
                    j["hours"][0]["start_hour"], j["hours"][0]["start_minutes"])
                end_time = datetime.time(
                    j["hours"][0]["end_hour"], j["hours"][0]["end_minutes"])

            week_info.append([datetime.datetime(int(date[0:4]), int(
                date[5:7]), int(date[8:])), j["status"], start_time, end_time])

        hours[i["name"]] = week_info

    return hours


def get_menu(location, date=datetime.datetime.today()):
    """
    location will be string of location name
    date must be in YYYY-MM-DD format

    Returns:
        None if location is closed
        

    Raises Exception:
        If req status is unsuccessful
        Usually occurs when no menu is found
    """
    menu = {}
    url = "https://api.dineoncampus.com/v1/location/"

    loc_id = get_all_locations()[location]

    url += loc_id
    url += "/periods?platform=0&date="

    # could probably restrict arguments
    if(type(date) == datetime.datetime):
        date = date.isoformat()
        url += date
    else:
        url += date

    req = requests.get(url).json()

    if req["status"] == "success":
        if req["closed"] == True:
            return None
    else:
        raise Exception(req["msg:"])
    
    period_food = {} # is a dictionary containing the period (all day, breakfast, lunch, dinner) as value and the menu as a list 
    for periods in req["periods"]:
        period_id = periods["id"]
        new_url = "https://api.dineoncampus.com/v1/location/" + loc_id + "/periods/" + period_id + "?platform=0&date=" + date

        new_request = requests.get(new_url).json()

        food = []
        for i in new_request["menu"]["periods"]["categories"]:
            for j in i["items"]:
                food.append(j["name"])
        
        period_food[periods["name"]] = food
    
    menu[location] = period_food #returns a dictionary with the location as the key and a dictionary (see period_food) as the value

    return menu






# arguments don't really matter
def get_all_locations(menus=True, address=False, buildings=True) -> Dict[str, str]:
    """
    gets all locations by their number and id
    in case this is needed for designing a better api 🤷
    """
    url = "https://api.dineoncampus.com/v1/locations/all_locations?platform=0&site_id=5e6fcc641ca48e0cacd93b04"

    # probably not needed
    if menus == True:
        url += "&for_menus=true"
    if address == False:
        url += "&with_address=false"
    if buildings == True:
        url += "&with_buildings=true"

    print(url)

    loc_info = requests.get(url).json()

    loc_id_dict = {}
    for i in loc_info["locations"]:
        loc_id_dict[i["name"]] = i["id"]

    return loc_id_dict


print(get_menu("The Eatery", "2023-03-01"))