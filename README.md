### Pitt API

```python
from pittAPI import CourseAPI, LaundryAPI

course = CourseAPI()
laundry = LaundryAPI()

# Will return a list of dictionaries containing courses in subject
big_dict = course.get_courses(term="2161", subject="CS")

# Will return a list of dictionaries containing courses that fulfill req
big_dict = course.get_courses_by_req(term="2161", req="Q")

# Will return a string, which is the description of the course
description = course.get_class_description(class_number="10163", term="2161")

# Will return a dictionary with amount of washers and dryers
# in use vs. total washers and dryers at building
small_dict = laundry.get_status_simple(loc="TOWERS")
```
