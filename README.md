### Pitt Course API

```python
from pittCourseAPI import CourseAPI

caller = CourseAPI()

# Will return a list of dictionaries containing course info
big_dict = caller.get_courses(term="2161", subject="CS")

for course in big_dict:
    if 'Thumrongsak' in course['instructor']:
        print 'Take this class: %s (%s)' % (course['title'], course['class_number'])

# Will return a string, which is the description of the course
caller.get_class_description(class_number="10163", term="2161")
```
