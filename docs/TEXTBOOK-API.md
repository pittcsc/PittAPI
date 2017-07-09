> [Home](README.md) > Textbook API
---

# Textbook API

### **get_textbook(term, department, course, instructor, section)**

#### **Parameters**:
  - `term`: Term number | Example: `2671`
  - `department`: Department code | Example: `CS`
  - `course`: Course number | Example: `0401`, `411`
  - `instructor`: Instructor name | Example: `GARRISON III`, `YANG`, `HOFFMAN`
  - `section`: Section number | Example: `1030`, `1060`

#### **Returns**:
Returns a list of dictionaries containing Author, ISBN, Edition, Title, and Citation

#### **Example**:

###### **Code**:
```python
get_textbook(
            term='2671,
            department='CS',
            course='445',
            instructor='GARRISON III'
)

get_textbook(
            term='2671',
            department='CS',
            course='401',
            section='1010'
)
```

###### **Sample Output**:
```python
    [
        {
            'author': 'Carrano',
            'citation': '<em>Data Struct.+Abstract.W/Java-W/Access</em> by Carrano. '
            'Pearson Education, 4th Edition, 2014. (ISBN: 9780133744057).',
            'edition': '4',
            'isbn': '9780133744057',
            'title': 'Data Struct.+Abstract.W/Java-W/Access'
        }
    ]

    [
        {
            'author': 'Gaddis',
            'citation': '<em>Starting Out W/Java:From..-W/Access</em> by Gaddis. Pearson '
            'Education, 6th Edition, 2015. (ISBN: 9780133957051).',
            'edition': '6',
            'isbn': '9780133957051',
            'title': 'Starting Out W/Java:From...-W/Access'
        }
    ]
```

### **get_textbooks(term, courses)**

#### **Parameters**:
  - `term`: Term number | Example: `2671`
  - `courses`: List of dictionaries of class info | Example: `[{'department': 'CS', 'course': '0401', 'instructor': 'HOFFMAN'}]`

#### **Returns**:
Returns a list of dictionaries containing Author, ISBN, Edition, Title, and Citation

#### **Example**:

###### **Code**:
```python
get_textbooks(
    term='2671',
    courses=[
    {'department': 'CS', 'course': '445', 'section': '1010'},
    {'department': 'STAT', 'course': '1000', 'instructor': 'REGISTER'}
    ]
)
```

###### **Sample Output**:
```python
    [
        {
            'author': 'Moore',
            'citation': '<em>Intro.To Practice Of Stat.-W/Access</em> by Moore. Freeman
                        & Company, W. H., 8th Edition, 2014. (ISBN: 9781464158933).',
            'edition': '8',
            'isbn': '9781464158933',
            'title': 'Intro.To Practice Of Stat.-W/Access'
        },
        {
            'author': 'Carrano',
            'citation': '<em>Data Struct.+Abstract.W/Java-W/Access</em> by Carrano.
                        Pearson Education, 4th Edition, 2014. (ISBN: 9780133744057).',
            'edition': '4',
            'isbn': '9780133744057',
            'title': 'Data Struct.+Abstract.W/Java-W/Access'
        }
    ]
```