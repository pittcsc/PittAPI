> [Home](README.md) > Course API
---

# Course API

### **get_classes(term, code)**

#### **Parameters**:
  - `term`: Term number | Example: `2171`
  - `code`: Subject\Program\Requirement abbreviation | Example: `CS`

#### **Returns**:
Returns a list of dictionaries containing the data for all SUBJECT classes in TERM

#### **Example**:

###### **Code**:
```python
course.get_courses(term='2171', code='cs')
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

### **get_class(class_number, term)**

#### **Parameters**:
  - `term`: Term number | Example: `"2174"`
  - `class_number`: Class Number | Example: `"23138"`

#### **Returns**:
Returns the details for `class_number` in `term`.

#### **Example**:

###### **Code**:
```python
course.get_class(term='2174', class_number='23138')
```

###### **Sample Output**:
```python
{'class_number': '23138',
 'classroom': '05502 SENSQ',
 'days': 'MoWe',
 'description': 'This course covers a broad range of the most commonly used '
                'algorithms. Some examples include algorithms for sorting, '
                'searching, encryption, compression and local search. The '
                'students will implement and test several algorithms. The '
                'course is programming intensive.Please note that each CS '
                'section has a WRIT and non-WRIT option. Please enroll '
                'carefully.',
 'enroll_limit': '20',
 'instructor': 'Farnan,Nicholas Leo',
 'section': 'AT',
 'special_indicators': ['WRIT'],
 'term': '2174',
 'time': ['09:30 AM', '10:45 AM']}
```

---

### Deprecated

### **get_courses(term, code)**

#### **Parameters**:
  - `term`: Term number | Example: `2171`
  - `code`: Subject\Program\Requirement abbreviation | Example: `CS`

#### **Returns**:
Returns a list of dictionaries containing the data for all SUBJECT classes in TERM

#### **Example**:

###### **Code**:
```python
course.get_courses(term='2171', code='cs')
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