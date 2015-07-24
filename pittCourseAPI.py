from BeautifulSoup import BeautifulSoup
import urllib2

class InvalidParameterException(Exception):
    pass

class CourseAPI:

    def __init__(self):
        pass

    def get_courses(self, term="2161", subject="CS"):

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

            course_details.append({'catalog_number': temp[0], 'term': temp[1], 'title': temp[2], 'class_number': course.find('a').contents[0], 'instructor': 'Not decided' if len(temp[3].strip()) == 0 else temp[3].strip(), 'credits': temp[4]})

        if len(course_details) == 0:
            raise InvalidParameterException("The TERM or SUBJECT is invalid")

        return course_details
