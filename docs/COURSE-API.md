> [Home](README.md) > Course API
---

# Course API

### **get_courses(term, subject)**

#### **Parameters**:
  - `term`: Term number | Example: `2171`
  - `subject`: Subject abbreviation | Example: `CS`

#### **Returns**:
Returns a list of dictionaries containg the data for all SUBJECT classes in TERM

#### **Example**:

###### **Code**:
```python
course.get_courses(term='2171', subject='cs')
```

###### **Sample Output**:
```python
[
  {
    'catalog_number': u'0004',
    'class_number': u'10160',
    'credits': u'3 cr.',
    'instructor': u'Not Decided',
    'subject': u'CS',
    'term': u'2171 \xa0AT',
    'title': u'Intro Computer Progrmmng-Basic' },
  {
    'catalog_number': u'1530',
    'class_number': u'11526',
    'credits': u'3 cr.',
    'instructor': u'Laboon,William J',
    'subject': u'CS',
    'term': u'2171 \xa0AT',
    'title': u'Software Engineering'
    }
]

```

---

### **get_courses_by_req(term, req)**

#### **Parameters**:
  - `term`: Term number | Example: `"2171"`
  - `req`: Requirement abbreviation | Example: `"Q"`

#### **Returns**:
Returns a list of dictionaries containing the data for all SUBJECT classes in TERM

#### **Example**:

###### **Code**:
```python
course.get_courses_by_req(term="2171", req="Q")
```

###### **Sample Output**:
```python
[
  {
    'catalog_number': u'0500',
    'credits': u'3 cr.',
    'instructor': u'Wilson, Mark',
    'subject': u'PHIL',
    'term': u'2171 \xa0AT',
    'title': u'Introduction To Logic' },
  {   
    'catalog_number': u'1000',
    'credits': u'4 cr.',
    'instructor': u'Pfenning,Nancy M.',
    'subject': u'STAT',
    'term': u'2171 \xa0AT',
    'title': u'Applied Statistical Methods'
  }
]
```

---

### **get_class_description(class_number, term)**

#### **Parameters**:
  - `class_number`: Class Number | Example: `"18047"`
  - `term`: Term number | Example: `"2171"`

#### **Returns**:
Returns the description for `class_number` in `term`.

#### **Example**:

###### **Code**:
```python
course.get_class_description(class_number="18047", term="2171")
```

###### **Sample Output**:
```python
u'This course will cover methods and strategies that are useful for the design of nonnumeric algorithms. Students are expected to design their own algorithms.'
```
