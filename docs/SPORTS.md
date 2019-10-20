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
'5-1'
>>> offseason_record = get_mens_basketball_record # If offseason, return this
>>> print(offseason_record)
'There's no record now'
```

---

### **get_next_mens_basketball_game()**

#### **Returns**:
Returns a dictionary containing the full name of the event, the short name of the event, the type of game (regular season, playoffs, preseason, etc.), the week in which it occurs, and the location.
#### **Example**:

###### **Sample Usage**:
```python
>>> next_game_details = get_next_mens_basketball_game()
>>> print(next_game_details)
{'full_name': 'Pittsburgh Panthers at Syracuse Orange', 'short_name': 'PITT @SYR', 'season_name': 'Regular Season', 'week': 'Week 19', 'court': 'Spectrum Center'}
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
'14th in ACC'
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
'1-1'
>>> offseason_record = get_football_record # If offseason, return this
>>> print(offseason_record)
'There's no record now'
```


---


### **get_next_football_game()**

#### **Returns**:
Returns a dictionary containing the full name of the event, the short name of the event, the type of game (regular season, playoffs, preseason, etc.), the week in which it occurs, and the location.
#### **Example**:

###### **Sample Usage**:
```python
>>> next_game_details = get_next_football_game()
>>> print(next_game_details)
{'full_name': 'Pittsburgh Panthers at Penn State Nittany Lions', 'short_name': 'PITT @ PSU', 'season_name': 'Regular Season', 'week': 'Week 3', 'field': 'Beaver Stadium'}

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
'4th in ACC - Coastal'
```

---