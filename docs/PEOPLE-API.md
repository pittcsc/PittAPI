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
people.get_person('Smith')
```

###### **Sample Output**:
```python
[
  {
    'name': 'John Smith',
    'unit': 'Pittsburgh' },
  {
    'name': 'Matt Coopersmith',
    'unit': 'Pittsburgh',
    'email': 'fgi345@pitt.edu'},
  {
    'email': 'cde234@pitt.edu',
    'unit': 'Pharmacy and Therapeutics',
    'name': 'Nicole Smith',
    'phone': '(412)555-5555 ',
    'address': '123 PITT'},
  {
    'email': 'aaa123@pitt.edu',
    'name': 'Joe Blacksmith',
    'unit': 'Biological Sciences',
    'address': '0000 PITT' }
]
```
