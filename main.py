import pprint

from PittAPI import course

pp = pprint.PrettyPrinter(indent=4)

v = course.get_courses(term="2171", subject="BCCC")
#w = course.get_courses_by_req(term="2171", req="Q")
#u = course.get_class_description("18047", "2171")
pp.pprint(v)

