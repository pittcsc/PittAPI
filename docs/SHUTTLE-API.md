> [Home](README.md) > Shuttle API
---

# Shuttle API

### **get_map_vehicle_points(api_key="8882812681")**

#### **Parameters**:
  - `api_key`: API Key for Ride Systems | Example: `8882812681`

#### **Returns**:
Returns a list of dictionaries containing the location information for all active vehicles.

#### **Example**:

###### **Code**:
```python
shuttle.get_map_vehicle_points()
```

###### **Sample Output**:
```python
[
  {
    "GroundSpeed": 2.9999999973178,
    "Heading": 317,
    "IsDelayed": false,
    "IsOnRoute": true,
    "Latitude": 40.44186,
    "Longitude": -79.95675,
    "Name": "51265",
    "RouteID": 21,
    "Seconds": 46,
    "TimeStamp": "\/Date(1486873994000-0700)\/",
    "VehicleID": 25
  }
]

```

---

### **get_route_stop_arrivals(api_key="8882812681", times_per_stop=1)**

#### **Parameters**:
  - `api_key`: API Key for Ride Systems | Example: `8882812681`
  - `times_per_stop`: Future times per stop | Example: `1`

#### **Returns**:
Returns stops for all routes and the given amount of times in the future.

#### **Example**:

###### **Code**:
```python
shuttle.get_route_stop_arrivals()
```

###### **Sample Output**:
```python
[
  {
    "RouteID": 21,
    "RouteStopID": 473,
    "ScheduledTimes": [
      {
        "ArrivalTimeUTC": "\/Date(1486848600000)\/",
        "AssignedVehicleId": 0,
        "DepartureTimeUTC": "\/Date(1486848600000)\/"
      }
    ],
    "VehicleEstimates": [
      {
        "OnRoute": true,
        "SecondsToStop": 332,
        "VehicleID": 25
      }
    ]
  },
  {
    "RouteID": 21,
    "RouteStopID": 480,
    "ScheduledTimes": [
      {
        "ArrivalTimeUTC": "\/Date(1486848960000)\/",
        "AssignedVehicleId": 0,
        "DepartureTimeUTC": "\/Date(1486848960000)\/"
      }
    ],
    "VehicleEstimates": [
      {
        "OnRoute": true,
        "SecondsToStop": 1322,
        "VehicleID": 25
      }
    ]
  },
  ...
]
```

---

### **get_vehicle_route_stop_estimates(vehicle_id, quantity=2)**

#### **Parameters**:
  - `vehicle_id`: Vehicle ID | Example: `25`
  - `quantity`: Quantity | Example: `2`

#### **Returns**:
Returns stop time estimates for the next `quantity` stops for `vehicle_id`.

#### **Example**:

###### **Code**:
```python
shuttle.get_vehicle_route_stop_estimates(25, quantity=3)
```

###### **Sample Output**:
```python
[
  {
    "Estimates": [
      {
        "Description": "Cathedral of Learning",
        "EstimateTime": "\/Date(1486849189764)\/",
        "IsArriving": true,
        "OnRoute": true,
        "OnTimeStatus": 0,
        "RouteStopID": 473,
        "ScheduledTime": null,
        "Seconds": 7,
        "Text": "Arriving",
        "Time": "\/Date(1486849189764)\/",
        "VehicleId": 25
      },
      {
        "Description": "Bigelow and Lytton",
        "EstimateTime": "\/Date(1486849669764)\/",
        "IsArriving": false,
        "OnRoute": true,
        "OnTimeStatus": 0,
        "RouteStopID": 474,
        "ScheduledTime": null,
        "Seconds": 487,
        "Text": "8 mins",
        "Time": "\/Date(1486849669764)\/",
        "VehicleId": 25
      }
    ],
    "VehicleID": 25
  }
]
```

---

### **get_routes(api_key="8882812681")**

#### **Parameters**:
  - `api_key`: API Key for Ride Systems | Example: `"8882812681"`

#### **Returns**:
Returns route name (eg. 10A), route ID, lat, long, and all stops (and their details) for all routes.

#### **Example**:

###### **Code**:
```python
shuttle.get_routes()
```

###### **Sample Output**:
```python
[
  {
    "Description": "10A Upper Campus",
    "IsCheckedOnMap": false,
    "IsVisibleOnMap": true,
    "Landmarks": [
      
    ],
    "MapLatitude": 40.44505,
    "MapLineColor": "#04BB84",
    "MapLongitude": -79.9574,
    "MapZoom": 14,
    "Order": 1,
    "RouteID": 21,
    "Stops": [
      {
        "AddressID": 90,
        "City": "Pittsburgh",
        "Latitude": 40.444326,
        "Line1": "Cathedral of Learning",
        "Line2": "",
        "Longitude": -79.95473,
        "State": "PA",
        "Zip": "15260",
        "Description": "Cathedral of Learning",
        "Heading": 0,
        "MapPoints": [
          {
            "Heading": 0,
            "Latitude": 40.4443501183,
            "Longitude": -79.9547195434
          },
          {
            "Heading": 0,
            "Latitude": 40.4457,
            "Longitude": -79.95638
          },
          {
            "Heading": 0,
            "Latitude": 40.44633,
            "Longitude": -79.95554
          }
        ],
        "MaxZoomLevel": 0,
        "Order": 1,
        "RouteDescription": "",
        "RouteID": 21,
        "RouteStopID": 473,
        "SecondsAtStop": 450,
        "SecondsToNextStop": 30,
        "ShowDefaultedOnMap": true,
        "ShowEstimatesOnMap": true,
        "SignVerbiage": "Cathedral of Learning",
        "TextingKey": ""
      },
      ...
    ],
    ...
  },
  ...
]
```
