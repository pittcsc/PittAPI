### Pitt API  

Made by Ritwik Gupta at the University of Pittsburgh in an effort to get more open data from Pitt. 
This project is licensed under the terms of the GPLv2 license.   

### Usage examples  

```python
from pittAPI import CourseAPI, LaundryAPI, LabAPI

### Courses
course = CourseAPI()
# Will return a list of dictionaries containing courses in subject
big_dict = course.get_courses(term="2161", subject="CS")
# Will return a list of dictionaries containing courses that fulfill req
big_dict = course.get_courses_by_req(term="2161", req="Q")
# Will return a string, which is the description of the course
description = course.get_class_description(class_number="10163", term="2161")

### Laundry
laundry = LaundryAPI()
# Will return a dictionary with amount of washers and dryers
# in use vs. total washers and dryers at building
small_dict = laundry.get_status_simple(building_name="TOWERS")

### Computer Lab
lab = LabAPI()
# Will return a dictionary with status of the lab, and amount
# of machines with a certain OS
small_dict = lab.get_status(lab_name="ALUMNI")

### Dining
dining = DiningAPI()
# Will return a list of dictionaries containing each dining location
# and its open/closed status
# (at the moment it returns a list of lists)
medium_dict = dining.get_dining_locations()
medium_dict = dining.get_dining_locations(status="open")
medium_dict = dining.get_dining_locations(status="closed")

```

### TODO  
* ~~Make the laundry detailed method work~~  
* ~~Test the computer lab status API and make it return a dictionary~~  
* Working on the DiningAPI
    * ~~Have the DiningAPI return a dict instead of a list~~
    * ~~Have a separate method for `get_dining_locations_by_status` and `get_dining_locations`~~
        * ~~`get_dining_locations_by_status` is what is currently implemented~~
        * ~~`get_dining_locations` is the same as what is currently implemented with no arguments~~
            * ~~(but with a good-looking dictionary)~~
    * Implement the `get_dining_location_by_name` method
    * Implement the `get_market_menu` method
    * ~~Implement the helper methods `_encode_dining_location` and `_decode_dining_location`~~
* Čhange all dict keys to unicode
