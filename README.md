### Pitt API  

Made by Ritwik Gupta at the University of Pittsburgh in an effort to get more open data from Pitt. 
This project is licensed under the terms of the MIT license.   

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
```

### TODO  
* ~~Make the laundry detailed method work~~  
* ~~Test the computer lab status API and make it return a dictionary~~  
* Try to get a dining API  
