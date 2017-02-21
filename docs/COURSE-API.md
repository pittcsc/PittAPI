> [Home](README.md) > Course API
---

# Course API

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

---

### **get_class(class_number, term)**

#### **Parameters**:
  - `term`: Term number | Example: `"2171"`
  - `class_number`: Class Number | Example: `"18047"`

#### **Returns**:
Returns the details for `class_number` in `term`.

#### **Example**:

###### **Code**:
```python
course.get_class(term='2171', class_number='26966')
```

###### **Sample Output**:
```python
{'classroom': '05502 SENSQ',
 'days': 'TuTh',
 'description': 'This is a first course in computer science programming. It is '
                'recommended for those students intending to major in computer '
                'science who do not have the required background for CS 0401. '
                'It may also be of interest to students majoring in one of the '
                'social sciences or humanities. The focus of the course is on '
                'problem analysis and the development of algorithms and '
                'computer programs in a modern high-level language.',
 'section': 'AT',
 'time': ['01:00 PM', '02:15 PM']}
```
