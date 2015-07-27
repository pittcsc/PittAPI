import urllib2

from BeautifulSoup import BeautifulSoup


class InvalidParameterException(Exception):
    pass


class CourseAPI:
    def __init__(self):
        pass

    @staticmethod
    def _retrieve_from_url(url):
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())
        courses = soup.findAll("tr", {"class": "odd"})
        courses_even = soup.findAll("tr", {"class": "even"})
        courses.extend(courses_even)
        return courses

    def get_courses(self, term, subject):
        """
        :returns: a list of dictionaries containing the data for all SUBJECT classes in TERM

        :param: term: String, term number
        :param: subject: String, course abbreviation
        """

        url = 'http://www.courses.as.pitt.edu/results-subja.asp?TERM={}&SUBJ={}'.format(term, subject)
        courses = self._retrieve_from_url(url)

        course_details = []

        for course in courses:
            details = [course_detail.string.replace('&nbsp;', '').strip()
                       for course_detail in course
                       if course_detail.string is not None
                       and len(course_detail.string.strip()) > 2]

            course_details.append(
                {
                    'catalog_number': details[0],
                    'term': details[1].replace('\r\n\t', ''),
                    'title': details[2],
                    'class_number': course.find('a').contents[0],
                    'instructor': details[3] if len(details[3]) > 0 else 'Not decided',
                    'credits': details[4]
                }
            )

        if len(course_details) == 0:
            raise InvalidParameterException("The TERM or SUBJECT is invalid")

        return course_details

    def get_courses_by_req(self, term, req):
        """
        Returns a list of dictionaries containing the data for all SUBJECT classes in TERM

        Keyword arguments
        term -- String, term number
        req -- string, requirement abbreviation
        """

        req = req.upper()

        url = 'http://www.courses.as.pitt.edu/results-genedreqa.asp?REQ={}&TERM={}'.format(req, term)
        courses = self._retrieve_from_url(url)

        course_details = []

        for course in courses:
            temp = []
            for i in course:
                try:
                    if len(i.string.strip()) > 2:
                        temp.append(i.string.strip())
                except (TypeError, AttributeError):
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

    def get_class_description(self, class_number, term):
        """
        Returns a string that is the description for CLASS_NUMBER in term TERM

        Keyword arguments
        class_number -- String, class number
        term -- String, term number
        """

        url = 'http://www.courses.as.pitt.edu/detail.asp?CLASSNUM=%s&TERM=%s' % (class_number, term)
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())
        table = soup.findChildren('table')[0]
        rows = table.findChildren('tr')

        description_flag = False
        for row in rows:
            cells = row.findChildren('td')
            for cell in cells:
                if description_flag == True:
                    return cell.string.strip()
                if len(cell.contents) > 0 and str(cell.contents[0]) == '<strong>Description</strong>':
                    description_flag = True


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

    def get_status(self, loc):
        """
        Returns a dictionary with status and amount of OS machines.

        Keyword arguments
        loc -- Building name
        """

        loc = loc.upper()
        url = 'http://www.ewi-ssl.pitt.edu/labstats_txtmsg/'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())
        labs = soup.span.contents[0].strip().split("  ")

        lab = labs[self.location_dict[loc]].split(':')
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
        'SUTH_WEST': '2430134'
    }

    def __init__(self):
        pass

    def get_status_simple(self, loc):
        """
        Returns a dictionary with free washers and dryers as well as total washers
        and dryers for given building

        Keyword arguments
        loc -- Building name, case doesn't matter
            -> TOWERS
            -> BRACKENRIDGE
            -> HOLLAND
            -> LOTHROP
            -> MCCORMICK
            -> SUTH_EAST
            -> SUTH_WEST

        session.hash_bits_per_character = 5
        """

        import re

        loc = loc.upper()
        url = 'http://classic.laundryview.com/appliance_status_ajax.php?lr=%s' % self.location_dict[loc]
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())

        re1 = ['(\\d+)', '(\\s+)', '(of)', '(\\s+)', '(\\d+)', '(\\s+)', '((?:[a-z][a-z]+))']

        rg = re.compile(''.join(re1), re.IGNORECASE | re.DOTALL)
        search = rg.findall(str(soup))

        di = {
            'building': loc,
            'free_washers': search[0][0],
            'total_washers': search[0][4],
            'free_dryers': search[1][0],
            'total_dryers': search[1][4]
        }

        return di

    def get_status_detailed(self, loc):
        """
        Works!
        """
        import subprocess

        # Get a cookie
        cookie_cmd = "curl -I -s 'http://www.laundryview.com/laundry_room.php?view=c&lr=%s'" % self.location_dict[loc]
        response = subprocess.check_output(cookie_cmd, shell=True)
        response = response[response.index('Set-Cookie'):]
        cookie = response[response.index('=') + 1:response.index(';')]

        # Get the weird laundry data
        cmd = "curl -s 'http://www.laundryview.com/dynamicRoomData.php?location=%s' -H 'Cookie: PHPSESSID=%s' --compressed" % (
            self.location_dict[loc], cookie)
        response = subprocess.check_output(cmd, shell=True)
        resp_split = response.split('&')[3:]

        cleaned_resp = []
        for string in resp_split:
            machine_name = string[:string.index('=')].replace('Status', '')
            string = string[string.index('=') + 1:].strip()
            machine_split = string.split("\n")
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
            machine_name = "%s_%s" % (machine[9], machine[3])
            machine_status = ""
            if machine[0] == '1':
                machine_status = 'Free'
            else:
                if machine[6] == '':
                    machine_status = 'Out of service'
                else:
                    machine_status = 'In use'

            if machine_status == 'In use':
                time_left = int(machine[1])
            else:
                time_left = -1 if machine[6] == '' else machine[6]
            di.append({
                'machine_name': machine_name,
                'machine_status': machine_status,
                'time_left': time_left
            })

        return di
