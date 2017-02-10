> [Home](README.md) > Dining API
---

# Dining API

### **get_dining_locations()**

#### **Returns**:
Returns all dining locations

---

### **get_dining_locations_by_status(status=None)**

#### **Parameters**:
  - `status`: Status of locations (default is all)
    - All locations: `None` or `"all"`
    - Open locations: `"open"`
    - Closed locations: `"closed"`

#### **Returns**:
Returns dining locations based on status

---

### **get_dining_locations_by_name(location)**

#### **Parameters**:
  - `location`: Dining Location

#### **Returns**:

---

### **get_dining_locations_menu(location, date)**

#### **Parameters**:
  - `location`: Dining location
  - `date`: Date

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
