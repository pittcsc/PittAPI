> [Home](README.md) > Status API
---

# Status API

### **get_status()**

#### **Returns**:
Returns the status of all Pitt services and reported incidents.

###### **Code**:
```python
status.get_status()
```

###### **Sample Output**:
```python
{
    'components': [
        {
            'description': None,
            'name': 'My Pitt',
            'status': 'operational',
            'updated_at': '2017-07-19T15:17:10.780-04:00'
        },
        {
            'description': None,
            'name': 'Pitt Passport',
            'status': 'operational',
            'updated_at': '2017-08-25T10:54:54.880-04:00'
        }
    ]
    'incidents': [
         {
            'components': [
                {
                    'description': None,
                    'name': 'PeopleSoft (Student Information System)',
                    'status': 'operational',
                    'updated_at': '2018-03-04T07:00:19.673-05:00'
                }
            ],
            'impact': 'maintenance',
            'incident_updates': [
                {
                    'affected_components': [
                        {
                            'name': 'PeopleSoft (Student Information System)',
                            'new_status': 'under_maintenance',
                            'old_status': 'under_maintenance'
                        }
                    ],
                    'body': 'The scheduled maintenance has been completed.',
                    'status': 'completed',
                    'updated_at': '2018-03-04T07:00:19.656-05:00'
                }
            ],
            'name': 'Student Information System (PeopleSoft) Extended Maintenance Scheduled for March 3–4',
            'resolved_at': '2018-03-04T07:00:19.656-05:00',
            'status': 'completed',
            'updated_at': '2018-03-04T07:00:19.722-05:00'
         }
    ]

}
```
