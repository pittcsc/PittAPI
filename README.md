# Pitt API
[![License GPLv2](https://img.shields.io/badge/license-GPLv2-blue.svg)](LICENSE)
![Python 3.4, 3.5, 3.6](https://img.shields.io/badge/python-3.4%2C%203.5%2C%203.6-green.svg)
[![Build Status](https://travis-ci.org/Pitt-CSC/PittAPI.svg?branch=master)](https://travis-ci.org/Pitt-CSC/PittAPI)

Made by Ritwik Gupta at the University of Pittsburgh in an effort to get more open data from Pitt. 

## Usage examples

```python
from PittAPI import course, laundry, lab, dining

### Courses
# Will return a list of dictionaries containing courses in subject
big_dict = course.get_courses(term="2161", subject="CS")
# Will return a list of dictionaries containing courses that fulfill req
big_dict = course.get_courses_by_req(term="2161", req="Q")
# Will return a string, which is the description of the course
description = course.get_class_description(term="2161", class_number="10163")

### Laundry
# Will return a dictionary with amount of washers and dryers
# in use vs. total washers and dryers at building
small_dict = laundry.get_status_simple(building_name="TOWERS")

### Computer Lab
# Will return a dictionary with status of the lab, and amount
# of machines with a certain OS
small_dict = lab.get_status(lab_name="ALUMNI")

### Dining
# Will return a dictionary of dictionaries containing each dining location,
# with its name, its open/closed status, and open times (if it exists)
medium_dict = dining.get_dining_locations()
medium_dict = dining.get_dining_locations_by_status(status="open")
medium_dict = dining.get_dining_locations_by_status(status="closed")
# Will return a single dictionary of a dining location,
# with its name, its open/closed status, and open times (if it exists)
one = dining.get_dining_location_by_name(u"taco_bell-schenley_cafe")
two = dining.get_dining_location_by_name(u"cup_&_chaucer-hillman")

```

## Tests
Run tests with `python3 -m "nose" --with-cov --cov PittAPI --with-timer tests/*`.  
If your `python -v` is 3+, replace `python3` with `python`.

## TODO
* [x] Make the laundry detailed method work
* [x] Test the computer lab status API and make it return a dictionary
* [ ] Working on the DiningAPI
    * [x] Have the DiningAPI return a dict instead of a list
    * [x] Have a separate method for `get_dining_locations_by_status` and `get_dining_locations`
        * [x] `get_dining_locations_by_status` is what is currently implemented
        * [x] `get_dining_locations` is the same as what is currently implemented with no arguments
            * [x] but with a good-looking dictionary
    * [x] Implement the `get_dining_location_by_name` method
    * [ ] Implement the `get_dining_location_menu` method
    * [x] Implement the helper methods `_encode_dining_location` and `_decode_dining_location`
* [x] Change all string processing to unicode (dropped Py2.7 support, fixed :smile:)

## License

This project is licensed under the terms of the [GPLv2 license](LICENSE).
