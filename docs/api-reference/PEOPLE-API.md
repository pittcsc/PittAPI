> [Home](README.md) > People API
---

# People API

### **get_person(query, max_people)**

#### **Parameters**:
  - `query`: Query to find people | Example: `smith` or `abc123`
  - `max_people`: Max number of people to return | Example: `10` or `100`
    - Default value is `10`

#### **Returns**:
Returns a dictionary with data of user profiles.

#### **Example**:

###### **Code**:
```python
people.get_person('Jane')
```

###### **Sample Output**:
```python
[
  {
    "name": "Jane Doe",
    "email": "jdoe@pitt.edu",
    "phone": "(999)999-999"
  },
  {
    "name": "Janedo Smith",
    "school": "School of Dental Medicine"
    ]
  },
  ...
]
```
