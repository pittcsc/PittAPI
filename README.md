### Pitt Course API

```python
from pittCourseAPI import CourseAPI

caller = CourseAPI()
caller.get_courses(term="2161", subject="CS") # These arguments are actually the defaults
                                              # Will return a list of dictionaries
                                              # containing course info
```
