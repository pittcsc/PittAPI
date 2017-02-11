> [Home](README.md) > LAB API
---

# Lab API

### **location_dict**
  - Alumni Hall: `"ALUMNI"`
  - Benedum Hall: `"BENEDUM"`
  - Cathedral G26: `"CATH_G26"`
  - Cathedral G27: `"CATH_G27"`
  - David Lawrence Hall: `"LAWRENCE"`
  - Hillman Library: `"HILLMAN"`
  - Sutherland Hall: `"SUTH"`

---

### **get_status(lab_name)**

#### **Parameters**:
  - `lab_name`: Lab name (comes from LabAPI's **location_dict**)

#### **Returns**:
Returns a dictionary with status and amount of OS machines.
