> [Home](README.md) > LAB API
---

# Lab API

### **Location Codes:**
  - Alumni Hall: `"ALUMNI"`
  - Benedum Hall: `"BENEDUM"`
  - Cathedral G26: `"CATH_G27"`
  - Cathedral G27: `"CATH_G62"`
  - David Lawrence Hall: `"LAWRENCE"`
  - Hillman Library: `"HILLMAN"`
  - Sutherland Hall: `"SUTH"`

---

### **get_status(lab_name)**

#### **Parameters**:
  - `lab_name`: Lab name (comes from LabAPI's **LOCATION**)

#### **Returns**:
Returns a dictionary with status and amount of OS machines.

#### **Example**:

###### **Code**:
```python
get_status(lab_name='ALUMNI')
get_status(lab_name='CATH_G62')
```

###### **Sample Output**:
```python
{'status': 'closed', 'windows': 0, 'mac': 0, 'linux': 0}
{'status': 'open', 'windows': 96, 'mac': 29, 'linux': 2}
```
