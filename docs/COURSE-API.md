> [Home](README.md) > Course API
---

# Course API

### **get_term_courses(term, subject)**

#### **Parameters**:
  - `term`: Term  | Example: `2194`
  - `subject`: Subject Code | Example: `'CS'`

#### **Returns**:
Returns a `PittSubject` object containing the information of all courses offered that semester and information about the sections for each course.

#### **Example**:

###### **Sample Usage**:
```python
>>> cs_subject = course.get_term_courses(term='2194', subject='CS')
>>> str(cs_subject)
'PittSubject(2194, CS)'
>>> cs_subject  # This string representation comes from performing cs_subject.to_dict()
{'0004': [{'days': ['Mo', 'We'],
           'end_date': '2019-04-19 00:00:00',
           'instructor': 'Michael Devine',
           'number': '27865',
           'room': '5502 Sennott Square',
           'section': '1060',
           'section_type': 'LEC',
           'start_date': '2019-01-07 00:00:00',
           'subject': 'CS',
           'term': '2194',
           'times': ['9:30am', '10:45am']},
          {'days': ['Tu', 'Th'],
           'end_date': '2019-04-19 00:00:00',
           'instructor': 'Michael Devine',
           'number': '27866',
           'room': '209 Lawrence Hall',
           'section': '1100',
           'section_type': 'LEC',
           'start_date': '2019-01-07 00:00:00',
           'subject': 'CS',
           'term': '2194',
           'times': ['11:00am', '12:15pm']}],
 ...       
}
>>> cs_subject.subject
'CS'
>>> cs_subject.term
'2194'
>>> str(cs_subject['1501'])
'PittCourse(2194, CS, 1501)'
>>> cs_subject['1501'].sections
[{'days': ['Mo', 'We'],
  'end_date': '2019-04-19 00:00:00',
  'instructor': 'Nicholas Farnan',
  'number': '27740',
  'room': '5129 Sennott Square',
  'section': '1040',
  'section_type': 'LEC',
  'start_date': '2019-01-07 00:00:00',
  'subject': 'CS',
  'term': '2194',
  'times': ['9:30am', '10:45am']},
  ...       
]
>>> str(cs_subject['1501'].sections[0])
'PittSection(CS, 1501, LEC, 27740, Nicholas Farnan)'
```

---

### **get_course_sections(term, subject, course)**

#### **Parameters**:
  - `term`: Term  | Example: `2194`
  - `subject`: Subject Code | Example: `'CS'`
  - `course`: Course Number | Example: `1501`


#### **Returns**:
Returns a `PittCourse` object containing information about the course and information on all sections being offered.


#### **Example**:

###### **Sample Usage**:
```python
>>> cs_course = course.get_course_sections(term='2194', subject='CS', course='1501')
>>> str(cs_course)
'PittCourse(2194, CS, 1501)'
>>> cs_course # This string representation comes from performing cs_course.to_dict()
[{'days': ['Mo', 'We'],
  'end_date': '2019-04-19 00:00:00',
  'instructor': 'Nicholas Farnan',
  'number': '27740',
  'room': '5129 Sennott Square',
  'section': '1040',
  'section_type': 'LEC',
  'start_date': '2019-01-07 00:00:00',
  'subject': 'CS',
  'term': '2194',
  'times': ['9:30am', '10:45am']},
  ...       
]
>>> cs_course.subject
'CS'
>>> cs_course.term
'2194'
>>> cs_course.number
'1501'
>>> cs_course.sections
[{'days': ['Mo', 'We'],
  'end_date': '2019-04-19 00:00:00',
  'instructor': 'Nicholas Farnan',
  'number': '27740',
  'room': '5129 Sennott Square',
  'section': '1040',
  'section_type': 'LEC',
  'start_date': '2019-01-07 00:00:00',
  'subject': 'CS',
  'term': '2194',
  'times': ['9:30am', '10:45am']},
  ...       
]
>>> str(cs_subject['1501'].sections[0])
'PittSection(CS, 1501, LEC, 27740, Nicholas Farnan)'
```

---

### **get_section_details(term, section_number)**

#### **Parameters**:
  - `term`: Term  | Example: `2194`
  - `section_number`: Section Number | Example: `27740`

#### **Returns**:
Return a `PittSection` object containing information for a particular section

#### **Example**:

###### **Sample Usage**:
```python
>>> cs_section = course.get_section_details('2194', '27740')
>>> str(cs_section)
'PittSection(CS, 1501, LEC, 27740, Nicholas Farnan)'
>>> cs_section # This string representation comes from performing cs_section.to_dict()
{'days': ['Mo', 'We'],
 'end_date': '2019-04-19 00:00:00',
 'instructor': 'Nicholas Farnan',
 'number': '27740',
 'room': '5129 Sennott Square',
 'section': '1040',
 'section_type': 'LEC',
 'start_date': '2019-01-07 00:00:00',
 'subject': 'CS',
 'term': '2194',
 'times': ['9:30am', '10:45am']}
>>> cs_section.subject
'CS'
>>> cs_section.term
'2194'
>>> cs_section.course_number
'1501'
>>> cs_section.number
'22740'
>>> cs_section.room
'5129 Sennott Square'
>>> cs_section.extra_details
{'class_attributes': 'Writing Requirement Course',
 'description': 'The course covers a broad range of the most commonly used '
                'algorithms:  some examples include algorithms for sorting, '
                'searching, encryption, compression, and local search.  The '
                'students will implement and test several algorithms.  The '
                'course is programming intensive.',
 'preq': '(CS 0441 or CS 0406) and (CS 0445 or CS 0455 or COE 0445) ; (MIN '
         "GRADE 'C'  or Transfer FOR ALL COURSES LISTED)",
 'units': '3 units'}
>>> cs_section.to_dict(extra_details=True)
{'days': ['Mo', 'We'],
 'end_date': '2019-04-19 00:00:00',
 'extra': {'class_attributes': 'Writing Requirement Course',
           'description': 'The course covers a broad range of the most '
                          'commonly used algorithms:  some examples include '
                          'algorithms for sorting, searching, encryption, '
                          'compression, and local search.  The students will '
                          'implement and test several algorithms.  The course '
                          'is programming intensive.',
           'preq': '(CS 0441 or CS 0406) and (CS 0445 or CS 0455 or COE 0445) '
                   "; (MIN GRADE 'C'  or Transfer FOR ALL COURSES LISTED)",
           'units': '3 units'},
 'instructor': 'Nicholas Farnan',
 'number': '27740',
 'room': '5129 Sennott Square',
 'section': '1040',
 'section_type': 'LEC',
 'start_date': '2019-01-07 00:00:00',
 'subject': 'CS',
 'term': '2194',
 'times': ['9:30am', '10:45am']}
```

---

## PittAPI.course.PittSubject

## PittAPI.course.PittCourse

## PittAPI.course.PittSubject