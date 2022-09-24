> [Home](README.md) > Course API
---

# Course API

### **get_subject_courses(subject)**

#### **Parameters**:
  - `subject`: Subject Code | Example: `'CS'`

#### **Returns**:
Returns a `Subject` object containing the information of all courses underneath that subject.
#### **Example**:

###### **Sample Usage**:
```python
>>> cs_subject = course.get_subject_courses(term='2194', subject='CS')
>>> str(cs_subject)
Subject(
    subject_code='CS',
    courses={
        '0004': Course(
            subject_code='CS',
            course_number='0004',
            course_id='105609',
            course_title='INTRO TO COMPUTER PROGRAMMING-BASIC'
        ),
        '0007': Course(
            subject_code='CS',
            course_number='0007',
            course_id='105611',
            course_title='INTRO TO COMPUTER PROGRAMMING'
        )
        ...
    }
)

```

---

### **get_course_details(term, subject, course)**

#### **Parameters**:
  - `term`: Term  | Example: `2194`
  - `subject`: Subject Code | Example: `'CS'`
  - `course`: Course Number | Example: `1501`


#### **Returns**:
Returns a `Course` object containing information about the course and all sections offered.
#### **Example**:

###### **Sample Usage**:
```python
>>> cs_course = course.get_course_details(term='2194', subject='CS', course='1501')
>>> str(cs_course)
Course(
    subject_code='CS',
    course_number='1501',
    course_id='105761',
    course_title='ALGORITHM IMPLEMENTATION',
    course_description='The course covers a broad range...',
    credit_range=(3,3),
    requisites='PREQ: (CS 0441 or CS 0406) and (CS 0445 or CS 0455 or COE 0445) ; (MIN GRADE 'C' or Transfer FOR ALL COURSES LISTED)',
    components=[
        Component(component='Lecture', required=True), 
        Component(component='Recitation', required=True)
    ],
    attributes=None,
    sections=[
        Section(
            term='2194',
            session='Academic Term',
            section_number='1040',
            class_number='27740',
            section_type='Lecture',
            status='Open',
            instructors=[Instructor(name='Nicholas Farnan', email='')],
            meetings=[
                Meeting(
                    days='MoWe', 
                    start_time='09.30.00.000000-05:00', 
                    end_time='10.45.00.000000-05:00', 
                    start_date='01/07/2019', 
                    end_date='04/19/2019', 
                    instructors=[Instructor(name='Nicholas Farnan', email=None)]
                )
            ],
            details=None
        )
    ]
)
```

---

### **get_section_details(term, section_number)**

#### **Parameters**:
  - `term`: Term  | Example: `2194`
  - `section_number`: Section Number | Example: `27740` | Note: Potential section numbers can be determined via a call to `get_course_details`

#### **Returns**:
Return a `Section` object containing information for a particular section. 

#### **Example**:

###### **Sample Usage**:
```python
>>> cs_section = course.get_section_details('2194', '27740')
>>> str(cs_section)
Section(
    term='2194', 
    session='Academic Term', 
    section_number='1040', 
    class_number='27740', 
    section_type='LEC', 
    status='Open', 
    instructors=None, 
    meetings=[
        Meeting(
            days='MoWe', 
            start_time='9:30AM', 
            end_time='10:45AM', 
            start_date='01/07/2019',
            end_date='04/19/2019', 
            instructors=[
                Instructor(name='Nicholas Farnan', email='')
            ]
        )
    ], 
    details=SectionDetails(
        units='3 units', 
        class_capacity='26', 
        enrollment_total='25', 
        enrollment_available='1',
         wait_list_capacity='20', 
         wait_list_total='1', 
         valid_to_enroll='F', 
         combined_section_numbers=['21754', '27740', '27741']
    )
)
```

---

## PittAPI.course.Attribute
Represents a requirement or group this course can be applied to (i.e. a general education requirement)
- __attribute__
    - String name representing course attribute/requirement satisfaction
- __attribute_description__
    - More information about course attribute/requirement
- __value__
    - Specific representation of requirement being satisfied
- __value_description__
    - Description of specific representation of requirement being satisfied

## PittAPI.course.Component
Specific types of sections that a course may contain (i.e. lecture, recitation, lab, etc.)
- __component__
    - Identifier/name for the course component
- __required__
    - True if this component is required for successful course completion, false otherwise

## PittAPI.course.Course
Object meant to broadly represent a Pitt course
- __subject_code__
- __course_number__
- __course_id__
    - Pitt course ID used to uniquely represent the course
- __course_title__
- __course_description__
- __credit_range__
    - Minimum and maximum num of credits course can be taken for
- __requisites__
    - Description of course prerequisites and corequisites
- __components__
    - List of Component objects part of this course
- __attributes__
    - List of Attribute objects that can be satisfied by this course
- __sections__
    - Sections of this course for some term, if specified

## PittAPI.course.Instructor
- __name__
- __email__

## PittAPI.course.Meeting
Representation of a course meeting (lecture, recitation, lab, etc.) within a specific section
- __days__
    - Day(s) of the week this meeting occurs
- __start_time__
- __end_time__
- __start_date__
- __end_date__
- __instructors__
    - List of Instructor objects who are assigned to this meeting

## PittAPI.course.Section
A specific section offering of some Pitt course
- __term__
- __session__
    - Specific timing of this course section (i.e. Academic Term, 12 week, 6 week)
- __section_number__
    - Identifier for this specific section
- __class_number__
    - Identifier of section, unique to within course
- __section_type__
    - Type of this section (i.e. Lecutre, Recitation)
- __status__
    - Basic representation of enrollment status for this section
- __instructors__
    - List of Instructor objects who are assigned to this section
- __meetings__
    - List of Meeting objects part of this section
- __details__
    - Optional SectionDetails object providing more information about this section, as outlined below

## PittAPI.course.SectionDetails
Provides some additional, specialized details about a Section
- __units__
    - Amount of units this specific section contributes/counts for
- __class_capacity__
- __enrollment_total__
    - Students currently enrolled in the course
- __enrollment_available__
- __wait_list_capacity__
- __wait_list_total__
    - Current number of students on wait list for this section
- __valid_to_enroll__
    - Character to indicate if course is in state where enrollment is allowed/restricted
- __combined_section_numbers__
    - If not null, outlines unique section identifiers for combined sections

## PittAPI.course.Subject
- __subject_code__
    - Pitt code for a given subject (e.g. CS, MATH, PHYS)
- __courses__
    - Dictionary of course IDs mapped to their corresponding course object within this Subject