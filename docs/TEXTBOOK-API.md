> [Home](README.md) > Textbook API
---

# Textbook API

### **get_book(department_code,course_name, instructor,term)**

#### **Parameters**:
  - `department_code`: Code for department | Example: `CS` or `LATIN`
  - `course_name` : Department_code followed by 4-digit course number | Example: `CS0447` or `LATIN0021`
  - `instructor` : Class instructor (uppercase last name) | Example `CHILDERS`, `NEWELL`
  - `term` : ID for class term | Example `2600`
    - Default value is `2600` for Spring 2017

#### **Returns**:
Returns a dictionary with book Title, Author, ISBN, Status, Edition, Copyright,
as well as url to the Pitt University Store site to order book

#### **Example**:

###### **Code**:
```python
textbook.get_book('CS', 'CS0447', 'CHILDERS')
```
###### **Sample Output**:
```python
   [
     {
       'isbn': 9780133957051,
       'title': 'Starting Out W/Java:From... W/Access',
       'author': 'Gaddis',
       'edition': ' 6th Edition'
      }
    ]
```

### **get_books_data(course_ids)**


### **get_many_books(list_of_course_info)**
