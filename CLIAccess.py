from PittAPI.pittAPI3 import CourseAPI, LaundryAPI, LabAPI

APIs = ["lab","laundry","course"]
UNDER_DEV = [3]

def init():
    return LabAPI(), LaundryAPI(), CourseAPI()

def update(API,LOC):
    if API.lower() == "lab" and LOC in LabAPI().location_dict.keys():

        return LabAPI().get_status(LOC)
    if API.lower() == "laundry" and LOC in LaundryAPI().location_dict.keys():
        return LaundryAPI().get_status_simple(LOC)


def locations(API):
    if API.lower() == "lab":
        return tuple(lab.location_dict.keys())
    if API.lower() == "laundry":
        return tuple(laundry.location_dict.keys())

lab, laundry, course = init()

n = "\n"
n2 = n*2
n3 = n*3

def Main():
    print(n,
          "Welcome to the PittAPI!",n2,
          "Here you will be able to view states of Labs and Laundry Rooms.",n,
          "If a location is open, you can see how many slots are available.",n)

    print(" ------------------")

    print(n,
          "You will be asked for what service you are looking.",n,
          "Then, you will be able to select a location.",n2,
          "You must select one of the available options, then press [return].",n3)

    TypesMenu()

    Main()
    
def TypesMenu():
    print(" Here are your service type options:",n2,
          "  1. Computer Labs",n,
          "  2. Laundry Rooms",n,
          "  3. Courses (under development",n,
          "  4. Main Menu",n)
    try:
        API = int(input(" Your selection: "))
        print(n)
        APITypes = [x for x in range(1, len(APIs)+2)]
        if API not in APITypes:
            raise ValueError(">> Selection not valid!")
        if API in UNDER_DEV:
            raise ValueError(">> Currently under construction!")
        if API == len(APITypes):
            return

    except ValueError as err:
        print("", err,n3)
        TypesMenu()

    LocationMenu(API)

    TypesMenu()
    
def LocationMenu(API):
    loc = sorted(list(locations(APIs[API-1]))) + ["Previous Menu"]
    locTypes = [x for x in range(1,len(loc)+1)]
    UNDER_DEV_LOC = []
    print(" Here are your location options:",n)
    print("","\n ".join(["  %s. %s"%(x+1,loc[x]) for x in range(len(loc))]),n)
    
    try:
        LOC = int(input(" Your selection: "))
        print(n)
        if LOC not in locTypes:
            raise ValueError(">> Selection not valid!")
        if LOC in UNDER_DEV_LOC:
            raise ValueError(">> Currently under construction!")
        if LOC == len(loc):
            return

    except ValueError as err:
        print("", err,n3)
        LocationMenu(API)

    CapacityMenu(API, loc[LOC-1])

    LocationMenu(API)

def CapacityMenu(API, LOC):
    d = update(APIs[API-1], LOC)

    if APIs[API-1] == "lab":
        print("",LOC, "is:", d["status"].upper(),n)

        comps = ["Windows", "Mac", "Linux"]

        if d["status"] == "open":
            print(" Available Computers: ","\n ".join(["  %s: %s"%(comps[x], d[comps[x].lower()]) for x in range(len(comps))]),n)

        print()

    if APIs[API-1] == "laundry":
        print("",LOC+":",n2,
              "  Free Washers:", d["free_washers"]+"/"+d["total_washers"],n,
              "  Free Dryers:", d["free_dryers"]+"/"+d["total_dryers"],n3)

    return

Main()
