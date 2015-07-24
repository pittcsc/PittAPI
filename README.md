### Pitt Course API

```python
from pittCourseAPI import CourseAPI

caller = CourseAPI()

# Will return a list of dictionaries containing courses in subject
big_dict = caller.get_courses(term="2161", subject="CS")

# Will return a list of dictionaries containing courses that fulfill req
big_dict = caller.get_courses_by_req(term="2161", req="Q")

# Will return a string, which is the description of the course
description = caller.get_class_description(class_number="10163", term="2161")
```
