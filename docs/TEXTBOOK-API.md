> [Home](README.md) > Textbook API
---

# Textbook API


### **get_books_data(course_ids)**


#### **Parameters**:
  - `course_ids`: List of dictionaries of class info | Example: get_books_data([{'department_code': 'CS', 'course_name': 'CS0401', 'instructor': 'HOFFMAN'}]

#### **Returns**:
Returns a course id number corresponding to the format used by pitt.verbacompare.com

#### **Example**:

###### **Code**:
```python
get_books_data([{'department_code': 'CS', 'course_name': 'CS0401', 'instructor': 'HOFFMAN'}, {'department_code': 'CS', 'course_name': 'CS0445', 'instructor': 'GARRISON III'}])
```

###### **Sample Output**:
```python
  [
    {
    'author': 'Gaddis',
    'isbn': '9780133957051',
    'edition': '6',
    'citation': '<em>Starting Out W/Java:From.. W/Access</em> by Gaddis. Pearson Education, 6th Edition, 2015. (ISBN: 9780133957051).',
    'title': 'Starting Out W/Java:From... W/Access'
    },
    {
    'author': 'Carrano',
    'isbn': '9780133744057',
    'edition': '4',
    'citation': '<em>Data Struct.+Abstract.W/Java W/Access</em> by Carrano. Pearson Education, 4th Edition, 2014. (ISBN: 9780133744057).',
    'title': 'Data Struct.+Abstract.W/Java W/Access'
    }
  ]
```

### **get_course_id(department_code,course_name, instructor,term)**

#### **Parameters**:
  - `department_code`: Code for department | Example: `CS` or `LATIN`
  - `course_name` : Department_code followed by 4-digit course number | Example: `CS0445` or `LATIN0021`
  - `instructor` : Class instructor (uppercase last name) | Example `GARRISON III`, `NEWELL`
  - `term` : ID for class term | Example `2600`
    - Default value is `2600` for Spring 2017

#### **Returns**:
Returns a course id number corresponding to the format used by pitt.verbacompare.com

#### **Example**:

###### **Code**:
```python
textbook.get_course_id('CS', 'CS0445', 'GARRISON III')
```
###### **Sample Output**:
```python
1904869
```
