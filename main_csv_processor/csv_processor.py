from collections import defaultdict
import csv
import re

def schoolname_parser(schoolname):
    name = re.search(r"(?i).*?(Средняя школа|СШ|Школа|Лицей|Гимназия).*?", schoolname)
    number = re.search(r"(?i).*?(\d{1,3}|БНТУ|БГУ).*?", schoolname)
    return [name, number]

def detect_school_type(passed_schools, school_number):
    school_types = defaultdict(int)
    for school in passed_schools:
        res = schoolname_parser(school)
        if res[1][1] == school_number:
            school_types[res[0][1]] += 1
    sorted_school_types = sorted([(value, key) for (key, value) in school_types.items()])
    return sorted_school_types[-1][1] if sorted_school_types else None

def correct_schoolnames(school_list):
    final_list = []
    for i in range(len(school_list)):
        res = schoolname_parser(school_list[i])

        if res[0] and res[1]:
            if res[0][1].lower() == "средняя школа" or res[0][1].lower() == "сш":
                final_list.append("{0} {1}".format("Школа", res[1][1]))
                continue
            else:
                final_list.append("{0} {1}".format(res[0][1].capitalize(), res[1][1]))
                continue
        if res[1]:
            found_type = detect_school_type(final_list[i - 20:i], res[1][1])
            if found_type:
                final_list.append("{0} {1}".format(found_type, res[1][1].capitalize()))
                continue
    return final_list

def measure_schools(school_list):
    schools = defaultdict(int)
    for school in school_list:
        schools[school] += 1
    return schools

with open("data/poll.csv", "r", newline="", encoding="utf-8") as read:

    reader = csv.reader(read)

    data = [row for row in reader][1:]

    schools = [row[25] if row[25] else row[3] for row in data]

    schools = [school for school in schools if school != ""]

    corrected = correct_schoolnames(schools)