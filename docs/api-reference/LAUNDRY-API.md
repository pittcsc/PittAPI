> [Home](README.md) > Laundry API
---

# Laundry API

### **location_dict**
- Litchfield Towers: `"TOWERS"`
- Brackenridge Hall: `"BRACKENRIDGE"`
- Holland Hall: `"HOLLAND"`
- Lothrop Hall: `"LOTHROP"`
- McCormick Hall: `"MCCORMICK"`
- Sutherland Hall: `"SUTH_WEST"`
- Sutherland Hall: `"SUTH_EAST"`
- Forbes Hall: `"FORBES_CRAIG"`

---

### **get_status_simple(building_name)**

#### **Parameters**:
  - `building_name`: Building name (comes from LaundryAPI's **location_dict**)


#### **Returns**:
Returns a dictionary with free washers and dryers as well as total washers and dryers for a given building.

---

### **get_status_detailed(building_name)**

#### **Parameters**:
  - `building_name`: Building name (comes from LaundryAPI's **location_dict**)

#### **Returns**:

