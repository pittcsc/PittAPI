"""
The Pitt API, to access workable data of the University of Pittsburgh
Copyright (C) 2015 Ritwik Gupta

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
import requests
from typing import Union, List, Dict, Any

RESULT_FIELDS = [
  "city_state_s",
  "pk_id",
  "region_i",
  "averagehelpfulscore_rf",
  "pageviews_i",
  "schoolcountry_s",
  "status_i",
  "averagehotscore_rf",
  "schoolstate_s",
  "rated_date_dt",
  "teacherfullname_s",
  "averageteacherrating_rf",
  "total_number_of_ratings_i",
  "content_type_s",
  "averagedifficultyrating_rf",
  "averageclarityscore_rf",
  "schoolwebpage_s",
  "hotstatus_i",
  "averageratingscore_rf",
  "tag_s_mv",
  "schoolcity_s",
  "schoolstate_full_s",
  "tag_id_s_mv",
  "pict_thumb_name_s",
  "id",
  "timestamp",
  "averageschoolrating_rf",
  "geolocation",
  "schoolname_s",
  "teachermiddlename_t",
  "numberofprofessors_i",
  "schoolphoto_s",
  "teacherdepartment_s",
  "visible_i",
  "averageeasyscore_rf",
  "schoolid_s",
  "teacherfirstname_t",
  "teacherlastname_t",
]

DEFUALT_NUM_RESULTS = 20
DEFAULT_RESPONSE_FIELDS = [
  "pk_id",
  "teacherfirstname_t",
  "teacherlastname_t",
  "total_number_of_ratings_i",
  "averageratingscore_rf",
  "averagedifficultyrating_rf"
]
PITT_SCHOOL_ID = 1247

RMP_SEARCH_URL = "https://solr-aws-elb-production.ratemyprofessors.com//solr/rmp/select/"

def get_rmp_by_query(
    query: str,additional_request_params: Dict[str, str]={}) -> List[Dict[str, Any]]:
  """Return the results of a custom Apache Solr query to RMP."""
  request_params = {
    "wt": "json",
    "q": query,
    **additional_request_params
  }

  return requests.get(RMP_SEARCH_URL, params=request_params).json()['response']['docs']

def get_rmp_by_name(
  prof_name: str,
  num_results: int = DEFUALT_NUM_RESULTS,
  school_id: int = PITT_SCHOOL_ID,
  response_fields: List[str] = DEFAULT_RESPONSE_FIELDS, 
) -> List[Dict[str, Any]]:
  """Query RMP with the name (first, last, or both) of the professor.
  This type of query is somewhat resilient to alternate versions of a name ("Nick" vs "Nicholas"),
  and will attempt to use just the first name or last name if either is inaccurate.
  If the query needs to be more resilient to input mistakes, use the much more expensive fuzzy name
  query.
  """
  return get_rmp_by_query(
    query="{prof_name} AND schoolid_s:{school_id}".format(prof_name=prof_name, school_id=school_id),
    additional_request_params={
      "defType": "edismax", # https://lucene.apache.org/solr/guide/6_6/the-extended-dismax-query-parser.html#TheExtendedDisMaxQueryParser-ThesowParameter
      "qf": "teacherfirstname_t^2000 teacherlastname_t^2000 teacherfullname_t^2000 autosuggest", # https://lucene.apache.org/solr/guide/6_6/the-dismax-query-parser.html#TheDisMaxQueryParser-Theqf_QueryFields_Parameter
      "bf": "pow(total_number_of_ratings_i,2.1)", # https://lucene.apache.org/solr/guide/6_6/the-dismax-query-parser.html#TheDisMaxQueryParser-Thebf_BoostFunctions_Parameter
      "sort": "total_number_of_ratings_i desc", # https://lucene.apache.org/solr/guide/6_6/common-query-parameters.html#CommonQueryParameters-ThesortParameter
      "fl": " ".join(response_fields), # https://lucene.apache.org/solr/guide/6_6/common-query-parameters.html#CommonQueryParameters-Thefl_FieldList_Parameter
      "rows": num_results,
    }
  )

def get_rmp_by_name_fuzzy(
  prof_first_name: str,
  prof_last_name: str,
  num_results: int = DEFUALT_NUM_RESULTS,
  school_id: int = PITT_SCHOOL_ID,
  response_fields: List[str] = DEFAULT_RESPONSE_FIELDS, 
) -> List[Dict[str, Any]]:
  """Query RMP with the approximate first and last name of the professor. A fuzzy search means that
  the query is resilient to minor input errors, however the query is much more expensive than the
  non-fuzzy alternative.
  https://lucene.apache.org/solr/guide/6_6/the-standard-query-parser.html#TheStandardQueryParser-FuzzySearches
  """
  return get_rmp_by_query(
    query= ("{prof_first_name}~ {prof_last_name}~ AND schoolid_s:{school_id}").format(
        prof_first_name=prof_first_name,
        prof_last_name=prof_last_name,
        school_id=school_id
      ),
    additional_request_params={
      "defType": "edismax", # https://lucene.apache.org/solr/guide/6_6/the-extended-dismax-query-parser.html#TheExtendedDisMaxQueryParser-ThesowParameter
      "qf": "teacherfirstname_t^2000 teacherlastname_t^2000 teacherfullname_t^2000 autosuggest", # https://lucene.apache.org/solr/guide/6_6/the-dismax-query-parser.html#TheDisMaxQueryParser-Theqf_QueryFields_Parameter
      "bf": "pow(total_number_of_ratings_i,2.1)", # https://lucene.apache.org/solr/guide/6_6/the-dismax-query-parser.html#TheDisMaxQueryParser-Thebf_BoostFunctions_Parameter
      "sort": "total_number_of_ratings_i desc", # https://lucene.apache.org/solr/guide/6_6/common-query-parameters.html#CommonQueryParameters-ThesortParameter
      "fl": " ".join(response_fields), # https://lucene.apache.org/solr/guide/6_6/common-query-parameters.html#CommonQueryParameters-Thefl_FieldList_Parameter
      "rows": num_results,
    }
  )

def get_rmp_by_id(
  prof_id: Union[str, int],
  num_results: int = DEFUALT_NUM_RESULTS,
  response_fields: List[str] = DEFAULT_RESPONSE_FIELDS, 
) -> Union[Dict[str, Any], None]:
  """Query RMP with the professor's RMP ID."""
  query_results = get_rmp_by_query(
    query="pk_id:{prof_id}".format(prof_id=prof_id),
    additional_request_params={
      "fl": " ".join(response_fields), # https://lucene.apache.org/solr/guide/6_6/common-query-parameters.html#CommonQueryParameters-Thefl_FieldList_Parameter,
    }
  )

  return query_results[0] if len(query_results) > 0 else None