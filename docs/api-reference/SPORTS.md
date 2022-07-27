> [Home](README.md) > Sports API
---

# Sports API

## Men's Basketball Methods

### **get_mens_basketball_record()**

#### **Returns**:
Returns a `string` containing the current record of the Men's basketball team.
#### **Example**:

###### **Sample Usage**:
```python
>>> record = get_mens_basketball_record()
>>> print(record) # Standard usage
'11-21'
>>> offseason_record = get_mens_basketball_record # If offseason, return this
>>> print(offseason_record)
'There's no record now'
```

---

### **get_next_mens_basketball_game()**

#### **Returns**:
Returns a `dictionary` containing the time and date of the game in UTC, the opponent's ESPN API ID, school name and full team name, whether Pitt is the home or away team, and information on its location. It also returns a 'Status' attribute, which identifies if the game has completed but data in the API has not updated yet.
#### **Example**:

###### **Sample Usage**:
```python
>>> next_game_details = get_next_mens_basketball_game()
>>> print(next_game_details)
{
    'Timestamp': '2022-03-08T19:00Z',
    'Opponent': {
        'id': '103',
        'school': 'Boston College',
        'name': 'Boston College Eagles'
    },
    'HomeAway': 'away',
    'Location': {
        'fullName': 'Barclays Center',
        'address': {
            'city': 'Brooklyn',
            'state': 'NY'
        }
    },
    'Status': 'GAME_COMPLETE'
}
>>> offseason_next_game_details = get_next_mens_basketball_game() # If offseason, return this
>>> print(offseason_next_game_details)
{
    'Status': 'OFFSEASON'
}
```

---

### **get_mens_basketball_standings()**

#### **Returns**:
Return a `string` containing information for the current team standings of the Men's basketball team.

#### **Example**:

###### **Sample Usage**:
```python
>>> standings = get_mens_basketball_standings()
>>> print(standings)
'12th in ACC'
```

---
## Football Methods

### **get_football_record()**

#### **Returns**:
Returns a `string` containing the current record of the football team.
#### **Example**:

###### **Sample Usage**:
```python
>>> record = get_football_record()
>>> print(record) # Standard usage
'11-3'
>>> offseason_record = get_football_record # If offseason, return this
>>> print(offseason_record)
'There's no record now'
```


---


### **get_next_football_game()**

#### **Returns**:
Returns a `dictionary` containing the time and date of the game in UTC, the opponent's ESPN API ID, school name and full team name, whether Pitt is the home or away team, and information on its location. It also returns a 'Status' attribute, which identifies if the game has completed but data in the API has not updated yet.
#### **Example**:

###### **Sample Usage**:
```python
>>> next_game_details = get_next_football_game()
>>> print(next_game_details)
{
    'Timestamp': '2021-12-05T01:00Z',
    'Opponent': {
        'id': '103',
        'school': 'Wake Forest',
        'name': 'Wake Forest Deamon Deacons'
    },
    'HomeAway': 'away',
    'Location': {
        'fullName': 'Bank of America Stadium',
        'address': {
            'city': 'Charlotte',
            'state': 'NC'
        }
    },
    'Status': 'GAME_COMPLETE'
}
>>> offseason_next_game_details = get_next_football_game() # If offseason, return this
>>> print(offseason_next_game_details)
{
    'Status': 'OFFSEASON'
}
```

---

### **get_football_standings()**

#### **Returns**:
Return a `string` containing information for the current team standings of the football team.

#### **Example**:

###### **Sample Usage**:
```python
>>> standings = get_football_standings()
>>> print(standings)
'1st in ACC - Coastal'
```

---