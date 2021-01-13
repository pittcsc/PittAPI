> [Home](README.md) > Rate My Professors API
---

# Rate My Professors API

### **get_rmp_by_query(query, additional_request_params)**

#### **Parameters**:
  - `query`: An [Apache Solr query](https://lucene.apache.org/solr/guide/6_6/the-standard-query-parser.html).
  - `additional_request_params`: Additional parameters to append to the Apache Solr request. Some common parameters are listed [here](https://lucene.apache.org/solr/guide/6_6/common-query-parameters.html).

#### **Returns**:
Returns a list of dictionaries containing the requested fields of the professors matching the query.

---

### **get_rmp_by_name(prof_name, num_results, school_id, response_fields)**

#### **Parameters**:
  - `prof_name`: The name of the professor to search for.
  - `num_results`: The maximum number of results to return.
  - `school_id`: The ID of the school to search for professors. This defaults to the University of Pittsburgh.
  - `response_fields`: The professor data fields to receive from the query.

#### **Returns**:
Returns a list of dictionaries containing the requested fields of the professors matching the name and from the requested school.

---

### **get_rmp_by_name_fuzzy(prof_first_name, prof_last_name, num_results, school_id, response_fields)**

#### **Parameters**:
  - `prof_first_name`: The first name of the professor to search for.
  - `prof_last_name`: The last name of the professor to search for.
  - `num_results`: The maximum number of results to return.
  - `school_id`: The ID of the school to search for professors. This defaults to the University of Pittsburgh.
  - `response_fields`: The professor data fields to receive from the query.

#### **Returns**:
Returns a list of dictionaries containing the requested fields of the professors matching the name and from the requested school.

---

### **get_rmp_by_id(prof_id, num_results, response_fields)**

#### **Parameters**:
  - `prof_id`: The Rate My Professor ID of the professor.
  - `num_results`: The maximum number of results to return.
  - `response_fields`: The professor data fields to receive from the query.

#### **Returns**:
Returns a dictionary containing the requested fields of the professor with the requested ID, or None if there is no match.
