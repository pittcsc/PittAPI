from BeautifulSoup import BeautifulSoup
import urllib2

class InvalidParameterException(Exception):
    pass

class CourseAPI:

    def __init__(self):
        pass

    def get_courses(self, term, subject):
        '''
        Returns a list of dictionaries containing the data for all SUBJECT classes in TERM

        Keyword arguments
        term -- String, term number
        subject -- String, course abbreviation
        '''

        url= 'http://www.courses.as.pitt.edu/results-subja.asp?TERM=%s&SUBJ=%s' % (term, subject)
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())
        courses = soup.findAll("tr", {"class": "odd"})
        courses_even = soup.findAll("tr", {"class": "even"})
        courses.extend(courses_even)

        course_details = []

        for course in courses:
            temp = []
            for i in course:
                try:
                    if len(i.string.strip()) > 2:
                        temp.append(i.string)
                except (TypeError, AttributeError) as e:
                    pass

            for i in range(len(temp)):
                temp[i] = temp[i].replace('&nbsp;', '')

            course_details.append(
                {
                    'catalog_number': temp[0].strip(),
                    'term': temp[1].replace('\r\n\t', ''),
                    'title': temp[2].strip(),
                    'class_number': course.find('a').contents[0].strip(),
                    'instructor': 'Not decided' if len(temp[3].strip()) == 0 else temp[3].strip(),
                    'credits': temp[4].strip()
                }
            )

        if len(course_details) == 0:
            raise InvalidParameterException("The TERM or SUBJECT is invalid")

        return course_details

    def get_courses_by_req(self, term, req):
        '''
        Returns a list of dictionaries containing the data for all SUBJECT classes in TERM

        Keyword arguments
        term -- String, term number
        req -- string, requirement abbreviation
        '''

        req = req.upper()

        url= 'http://www.courses.as.pitt.edu/results-genedreqa.asp?REQ=%s&TERM=%s' % (req, term)
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())
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

    def get_class_description(self, class_number, term):
        '''
        Returns a string that is the description for CLASS_NUMBER in term TERM

        Keyword arguments
        class_number -- String, class number
        term -- String, term number
        '''

        url= 'http://www.courses.as.pitt.edu/detail.asp?CLASSNUM=%s&TERM=%s' % (class_number, term)
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

    def __init__(self):
        pass

    def get_status(self):
        '''
        Doesn't do much for now, but it does return the status of the
        labs if they're all closed. Untested when a single lab is open.
        '''

        url= 'http://www.ewi-ssl.pitt.edu/labstats_txtmsg/'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())
        labs = soup.span.contents[0].strip().split(".")
        labs = map(lambda x: x.strip(), labs)
        labs = filter(lambda x: len(x) > 0, labs)

        return labs

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
        '''
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
        '''

        import re

        url = 'http://classic.laundryview.com/appliance_status_ajax.php?lr=%s' % self.location_dict[loc]
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())

        re1 = ['(\\d+)','(\\s+)','(of)','(\\s+)','(\\d+)','(\\s+)','((?:[a-z][a-z]+))']

        rg = re.compile(''.join(re1),re.IGNORECASE|re.DOTALL)
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
        '''
        Doesn't work for now
        '''

        url = 'http://classic.laundryview.com/classic_laundry_room_ajax.php?lr=%s' % self.location_dict[loc]
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())

        print soup
