> [Home](README.md) > Sports API
---

# Sports API

## Basketball Methods

### **get_basketball_record()**

#### **Returns**:
Returns a `string` containing the current record of the Men's basketball team.
#### **Example**:

###### **Sample Usage**:
```python
>>> record = get_basketball_record()
>>> print(record) # Standard usage
'5-1'
>>> offseason_record = get_basketball_record # If offseason, return this
'There's no record now'
```

---

### **get_next_basketball_game(input_parameter: str)**

#### **Parameters**:
  - `input_parameter`: Keywords of `full_name`, `short_name,` `season_name`, `week`, `court`


#### **Returns**:
Returns the full name of the event, the short name of the event, the type of game (regular season, playoffs, preseason, etc.), the week in which it occurs, and the location, respectively.
#### **Example**:

###### **Sample Usage**:
```python
>>> event_full_name = get_next_basketball_game("full_name")
>>> print(event_full_name)
'Pittsburgh Panthers at Syracuse Orange'
>>> event_short_name = get_next_basketball_game("short_name")
>>> print(event_short_name)
'PITT @ SYR'
>>> event_season_name = get_next_basketball_game("season_name")
>>> print(event_season_name)
'Regular Season'
>>> event_week = get_next_basketball_game("week")
>>> print(event_week)
'Week 19'
>>> event_court = get_next_basketball_game("court")
>>> print(event_court)
'Spectrum Center'
```

---

### **get_basketball_standings()**

#### **Returns**:
Return a `string` containing information for the current team standings of the Men's basketball team.

#### **Example**:

###### **Sample Usage**:
```python
>>> standings = get_basketball_standings()
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
'There's no record now'
```


---


### **get_next_football_game(input_parameter: str)**

#### **Parameters**:
  - `input_parameter`: Keywords of `full_name`, `short_name,` `season_name`, `week`, `field`


#### **Returns**:
Returns the full name of the event, the short name of the event, the type of game (regular season, playoffs, preseason, etc.), the week in which it occurs, and the location, respectively.
#### **Example**:

###### **Sample Usage**:
```python
>>> event_full_name = get_next_football_game("full_name")
>>> print(event_full_name)
'Pittsburgh Panthers at Penn State Nittany Lions'
>>> event_short_name = get_next_football_game("short_name")
>>> print(event_short_name)
'PITT @ PSU'
>>> event_season_name = get_next_football_game("season_name")
>>> print(event_season_name)
'Regular Season'
>>> event_week = get_next_football_game("week")
>>> print(event_week)
'Week 3'
>>> event_field = get_next_football_game("field")
>>> print(event_field)
'Beaver Stadium'
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