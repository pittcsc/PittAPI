'''
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
'''



import subprocess
import re

from bs4 import BeautifulSoup
import ssl
import requests

s = requests.session()

class InvalidParameterException(Exception):
    pass



class CourseAPI:
    def __init__(self):
        pass


    @staticmethod
    def _retrieve_from_url(url):
        page = s.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        courses = soup.findAll("tr", {"class": "odd"})
        courses_even = soup.findAll("tr", {"class": "even"})
        courses.extend(courses_even)
        return courses

    def get_courses(self, term, subject):
        # type: (str, str) -> List[Dict[str, str]]
        """
        :returns: a list of dictionaries containing the data for all SUBJECT classes in TERM

        :param: term: String, term number
        :param: subject: String, course abbreviation
        """

        subject = subject.upper()

        url = 'http://www.courses.as.pitt.edu/results-subja.asp?TERM={}&SUBJ={}'.format(term, subject)
        courses = self._retrieve_from_url(url)

        course_details = []

        for course in courses:
            details = [course_detail.string.replace('&nbsp;', '').strip()
                       for course_detail in course
                       if course_detail.string is not None]

            # Only append details if the list is not empty
            # If the subject code is incorrect, details will be NoneType
            if details:
                course_details.append(
                    {
                        'subject': details[1] if details[1] else "Not Decided",
                        'catalog_number': details[3] if details[3] else "Not Decided",
                        'term': details[5].replace('\r\n\t', '') if details[5] else "Not Decided",
                        'class_number': course.find('a').contents[0] if course.find('a').contents[0] else "Not Decided",
                        'title': details[8] if details[8] else "Not Decided",
                        'instructor': details[10] if details[10] else "Not Decided",
                        'credits': details[12] if details[12] else "Not Decided"
                    }
                )

        if not course_details:
            raise InvalidParameterException("The TERM or SUBJECT is invalid")

        return course_details

    @staticmethod
    def _get_course_dict(details):

        course_details = []

        if len(details) == 6:
            course_details.append(
                {
                    'subject': details[0],
                    'catalog_number': details[1],
                    'term': details[2].replace('\r\n\t', ' '),
                    'title': details[3],
                    'instructor': details[4] if len(details[4]) > 0 else 'Not decided',
                    'credits': details[5]
                }
            )
        else:
            course_details.append(
                {
                    'subject': 'Not available',
                    'catalog_number': details[0],
                    'term': details[1].replace('\r\n\t', ' '),
                    'title': details[2].replace('\r\n\t', ' '),
                    'instructor': details[3] if len(details[3]) > 0 else 'Not decided',
                    'credits': details[4]
                }
            )

        return course_details

    def get_courses_by_req(self, term, req):
        """
        :returns: a list of dictionaries containing the data for all SUBJECT classes in TERM

        :param: term: String, term number
        :param: req: String, requirement abbreviation
        """

        req = req.upper()

        url = 'http://www.courses.as.pitt.edu/results-genedreqa.asp?REQ={}&TERM={}'.format(req, term)
        page = s.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        courses = soup.findAll("tr", {"class": "odd"})
        courses_even = soup.findAll("tr", {"class": "even"})
        courses.extend(courses_even)

        course_details = []

        for course in courses:
            temp = []
            for i in course:
                try:
                    if len(i.string.strip()) > 2:
                        temp.append(i.string.strip())
                except (TypeError, AttributeError) as e:
                    pass

            for i in range(len(temp)):
                temp[i] = temp[i].replace('&nbsp;', '')

            if len(temp) == 6:
                course_details.append(
                    {
                        'subject': temp[0].strip(),
                        'catalog_number': temp[1].strip(),
                        'term': temp[2].replace('\r\n\t', ' '),
                        'title': temp[3].strip(),
                        'instructor': 'Not decided' if len(temp[4].strip()) == 0 else temp[4].strip(),
                        'credits': temp[5].strip()
                    }
                )
            else:
                course_details.append(
                    {
                        'subject': 'Not available',
                        'catalog_number': temp[0].strip(),
                        'term': temp[1].strip().replace('\r\n\t', ' '),
                        'title': temp[2].replace('\r\n\t', ' '),
                        'instructor': 'Not decided' if len(temp[3].strip()) == 0 else temp[3].strip(),
                        'credits': temp[4].strip()
                    }
                )

        if len(course_details) == 0:
            raise InvalidParameterException("The TERM or REQ is invalid")

        return course_details

    @staticmethod
    def get_class_description(class_number, term):
        """
        :returns: a string that is the description for CLASS_NUMBER in term TERM

        :param: class_number: String, class number
        :param: term: String, term number
        """

        url = 'http://www.courses.as.pitt.edu/detail.asp?CLASSNUM={}&TERM={}'.format(class_number, term)
        page = s.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        table = soup.findChildren('table')[0]
        rows = table.findChildren('tr')

        has_description = False
        for row in rows:
            cells = row.findChildren('td')
            for cell in cells:
                if has_description:
                    return cell.string.strip()
                if len(cell.contents) > 0 and str(cell.contents[0].encode('UTF-8')) == '<strong>Description</strong>':
                    has_description = True


class LabAPI:
    location_dict = {
        'ALUMNI': 0,
        'BENEDUM': 1,
        'CATH_G26': 2,
        'CATH_G27': 3,
        'LAWRENCE': 4,
        'HILLMAN': 5,
        'SUTH': 6
    }

    def __init__(self):
        pass

    def get_status(self, lab_name):
        """
        :returns: a dictionary with status and amount of OS machines.

        :param: lab_name: Lab name
        """

        lab_name = lab_name.upper()
        url = 'http://labinformation.cssd.pitt.edu/'
        page = s.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        labs = soup.span.contents[0].strip().split("  ")

        lab = labs[self.location_dict[lab_name]].split(':')
        di = {}
        if len(lab) > 1:
            lab = [x.strip() for x in lab[1].split(',')]
            machines = [int(x[:x.index(' ')]) for x in lab]
            di = {
                'status': 'open',
                'windows': machines[0],
                'mac': machines[1],
                'linux': machines[2]
            }
        else:
            di = {
                'status': 'closed',
                'windows': 0,
                'mac': 0,
                'linux': 0
            }

        return di


class LaundryAPI:
    location_dict = {
        'TOWERS': '2430136',
        'BRACKENRIDGE': '2430119',
        'HOLLAND': '2430137',
        'LOTHROP': '2430151',
        'MCCORMICK': '2430120',
        'SUTH_EAST': '2430135',
        'SUTH_WEST': '2430134',
        'FORBES_CRAIG': '2430142'
    }

    def __init__(self):
        pass

    def get_status_simple(self, building_name):
        """
        :returns: a dictionary with free washers and dryers as well as total washers
        and dryers for given building

        :param: loc: Building name, case doesn't matter
            -> TOWERS
            -> BRACKENRIDGE
            -> HOLLAND
            -> LOTHROP
            -> MCCORMICK
            -> SUTH_EAST
            -> SUTH_WEST

        session.hash_bits_per_character = 5
        """

        building_name = building_name.upper()
        url = 'http://classic.laundryview.com/appliance_status_ajax.php?lr={}'.format(self.location_dict[building_name])
        page = s.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        re1 = ['(\\d+)', '(\\s+)', '(of)', '(\\s+)', '(\\d+)', '(\\s+)', '((?:[a-z][a-z]+))']

        rg = re.compile(''.join(re1), re.IGNORECASE | re.DOTALL)
        search = rg.findall(str(soup))

        di = {
            'building': building_name,
            'free_washers': search[0][0],
            'total_washers': search[0][4],
            'free_dryers': search[1][0],
            'total_dryers': search[1][4]
        }

        return di

    def get_status_detailed(self, building_name):

        building_name = building_name.upper()

        # Get a cookie
        cookie_cmd = "curl -I -s \"http://www.laundryview.com/laundry_room.php?view=c&lr={}\"".format(
            self.location_dict[building_name])

        response = subprocess.check_output(cookie_cmd, shell=True)
        response = response[response.index('Set-Cookie'):]
        cookie = response[response.index('=') + 1:response.index(';')]

        # Get the weird laundry data
        cmd = """
        curl -s "http://www.laundryview.com/dynamicRoomData.php?location={}" -H "Cookie: PHPSESSID={}" --compressed
        """.format(self.location_dict[building_name], cookie)

        response = subprocess.check_output(cmd, shell=True)
        resp_split = response.split('&')[3:]

        cleaned_resp = []
        for status_string in resp_split:
            machine_name = status_string[:status_string.index('=')].replace('Status', '')
            status_string = status_string[status_string.index('=') + 1:].strip()

            machine_split = status_string.split("\n")
            machine_split[0] += machine_name

            try:
                machine_split[1] += machine_name
            except IndexError:
                pass

            machine_split = map(lambda x: x.split(':'), machine_split)
            cleaned_resp.append(machine_split[0])
            try:
                cleaned_resp.append(machine_split[1])
            except IndexError:
                pass

        cleaned_resp = filter(lambda x: len(x) == 10, cleaned_resp)

        di = []
        for machine in cleaned_resp:
            time_left = -1
            machine_name = "{}_{}".format(machine[9], machine[3])
            machine_status = ""

            if machine[0] is '1':
                machine_status = 'Free'
            else:
                if machine[6] is '':
                    machine_status = 'Out of service'
                else:
                    machine_status = 'In use'

            if machine_status is 'In use':
                time_left = int(machine[1])
            else:
                time_left = -1 if machine[6] is '' else machine[6]
            di.append({
                'machine_name': machine_name,
                'machine_status': machine_status,
                'time_left': time_left
            })

        return di

class PeopleAPI:

    def __init__(self):
        pass

    def get_person(self, query, maxPeople=10):
        '''
        Doesn't work completely for now. IT WORKS
        Returns a dict with URLs of user profiles. No scraping yet.
        '''

        query = query.replace(' ', '+')
        persons_list = []
        tens = 0
        while tens < maxPeople:
            url = "https://136.142.34.69/people/search?search=Search&filter={}&_region=kgoui_Rcontent_I0_Rcontent_I0_Ritems"
            url += '&_region_index_offset=' + str(tens) + '&feed=directory&start=' + str(tens)
            cmd = 'curl -k -s ' + '"'  + url + '"'


            cmd = cmd.format(query)
            response = subprocess.check_output(cmd, shell=True)
            if not response: #no more responses, so break
                break

            results = []
            while("formatted" in response):
                response = response[response.index('"formatted"'):]
                response = response[response.index(":") + 2:]
                response_str = response[:response.index('}') - 1]
                response_str = response_str.replace('\u0026', '&')
                response_str = response_str.replace('\\', '')
                if '&start=' not in response_str:
                    results.append("https://136.142.34.69" + response_str)

                response = response[response.index('}') :]
            for url in results:
                #results is url
                personurl = str(''.join(url))

                if personurl.lower().startswith("https://") and hasattr(ssl, '_create_unverified_context'):
                    f = s.get(personurl, verify=False)
                else:
                    f = s.get(personurl)

                html = f.read()
                person_dict = {}
                soup = BeautifulSoup(html, 'html.parser')
                name = soup.find('h1', attrs={'class' :'kgoui_detail_title'})
                person_dict['name'] = str(name.get_text())
                for item in soup.find_all('div', attrs={'class': 'kgoui_list_item_textblock'}):
                    if item is not None:
                        person_dict[str(item.div.get_text())] = str(item.span.get_text())
                persons_list.append(person_dict)
            tens += 10
        return persons_list
