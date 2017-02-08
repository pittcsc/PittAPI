# PittAPI Documentation

- [Course API](#course-api)
- [Lab API](#lab-api)
- [Laundry API](#laundry-api)
- [People API](#people-api)
- [Dining API](#dining-api)

# Course API

### **get_courses(term, subject)**

#### **Parameters**:
  - `term`: Term number
  - `subject`: Course abbreviation

#### **Returns**:
A list of dictionaries containg the data for all SUBJECT classes in TERM

---

### **get_courses_by_req(term, req)**

#### **Parameters**:
  - `term`: Term number
  - `req`: Requirement abbreviation

#### **Returns**:
A list of dictionaries containing the data for all SUBJECT classes in TERM

---

### **get_class_description(class_number, term)**

#### **Parameters**:
  - `class_number`: Class Number
  - `term`: Term number

#### **Returns**:
A string that is the description for `class_number` in `term`.

---

### **_get_course_dict(details)**

#### **Parameters**:
  - `details`:

#### **Returns**:

---

### **_retrieve_from_url(url)**

#### **Parameters**:
  - `url`:

#### **Returns**:

# Lab API

### **get_status(lab_name)**

#### **Parameters**:
  - `lab_name`: Lab name

#### **Returns**:
A dictionary with status and amount of OS machines.

# Laundry API

### **get_status_simple(building_name)**

#### **Parameters**:
  - `building_name`: Building name

#### **Returns**:
A dictionary with free washers and dryers as well as total washers and dryers for a given building.

---

### **get_status_detailed(building_name)**

#### **Parameters**:
  - `building_name`: Building name

#### **Returns**:

# People API

### **get_person(query, maxPeople)**

#### **Parameters**:
  - `query`:
  - `maxPeople`:

#### **Returns**:
Returns a dictionary with URLs of user profiles

# Dining API

### **get_dining_locations()**

#### **Returns**:
Returns all dining locations

---

### **get_dining_locations_by_status(status=None)**

#### **Parameters**:
  - `status`: Status of locations (`all`, `open`, `closed`)

#### **Returns**:
Returns dining halls based on status

---

### **get_dining_locations_by_name(location)**

#### **Parameters**:
  - `location`: Dining Location

#### **Returns**:

---

### **get_dining_locations_menu(location, date)**

#### **Parameters**:
  - `location`: Dining location
  - `date`: Data

#### **Returns**:
---

### **_encode_dining_location(string)**

#### **Parameters**:
  - `string`: Text

#### **Returns**:

---

### **_decode_dining_location(string)**

#### **Parameters**:
  - `string`: Text

#### **Returns**:
