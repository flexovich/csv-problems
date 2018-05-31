from collections import defaultdict
import csv
import re


def schoolname_parser(schoolname):
    name = re.search(r"(?i).*?(Средняя школа|СШ|Школа|Лицей|Гимназия).*?", schoolname)
    number = re.search(r"(?i).*?(\d{1,3}|БНТУ|БГУ).*?", schoolname)
    return [name, number]  # >>>[name[1], number[1]]      output:['Гимназия', '22']


def detect_school_type(passed_schools, school_number):
    school_types = defaultdict(int)
    for school in passed_schools:
        res = schoolname_parser(school[0])
        if res[1][1] == school_number:
            school_types[res[0][1]] += 1
    sorted_school_types = sorted([(value, key) for (key, value) in school_types.items()])
    return sorted_school_types[-1][1] if sorted_school_types else None


def correct_schoolnames(school_list):
    final_list = []
    for i in range(len(school_list)):
        res = schoolname_parser(school_list[i][0])
        if res[0] and res[1]:
            if res[0][1].lower() == "средняя школа" or res[0][1].lower() == "сш":
                final_list.append(("{0} {1}".format("Школа", res[1][1].upper()), school_list[i][1]))
                continue
            else:
                final_list.append(("{0} {1}".format(res[0][1].capitalize(), res[1][1].upper()), school_list[i][1]))
                continue
        if res[1]:
            found_type = detect_school_type(final_list[i - 20:i], res[1][1])
            if found_type:
                final_list.append(("{0} {1}".format(found_type, res[1][1].upper()), school_list[i][1]))
    return final_list


def measure_schools(school_list):  # school_list is list of tuples in form of (schoolname, sex)
    schools_dict = defaultdict(lambda: [0, [0, 0]])  # schools_dict is schoolname:
    for school in school_list:  # [total_number_of_answers,
        schools_dict[school[0]][0] += 1  # [number_of_male_answers, number_of_female_answers]]
        if school[1] == "М":
            schools_dict[school[0]][1][0] += 1
        else:  # means school[1] is "Ж"
            schools_dict[school[0]][1][1] += 1
    return schools_dict


# def reverse_tuples(measured_schools):
#     sorted(map(lambda (a, b): (b, a), xxx))[::-1]

def categorize_schools(measured_schools):
    enough = list(filter(lambda x: int(x[1][0]) > 19, measured_schools.items()))
    not_enough = list(filter(lambda x: int(x[1][0]) <= 19, measured_schools.items()))
    enough = [(numbers, name) for (name, numbers) in enough]  # this line and the next one are needed to
    not_enough = [(numbers, name) for (name, numbers) in not_enough]  # correctly sort the list
    return sorted(enough)[::-1], sorted(not_enough)[::-1]


def write_output(enough, not_enough):
    with open("data/output.txt", "w", encoding="utf-8") as output:
        i = 1
        output.write("              ENOUGH:             ")
        for school in enough:  # school is ([total_number_of_answers,
                                          # [number_of_male_answers, number_of_female_answers]], schoolname)
            output.write("\n{0}. {1} - {2} {{M - {3}, Ж - {4}}}".format(i, school[1], school[0][0], school[0][1][0],
                                                                        school[0][1][1]))
            i += 1
        output.write("\n\n\n")
        i = 1
        output.write("              NOT ENOUGH:             ")
        for school in not_enough:
            output.write("\n{0}. {1} - {2} {{M - {3}, Ж - {4}}}".format(i, school[1], school[0][0], school[0][1][0],
                                                                        school[0][1][1]))
            i += 1


with open("data/poll.csv", "r", newline="", encoding="utf-8") as read:
    reader = csv.reader(read)

    data = [row for row in reader][1:]  # deleting the first row because it represents columns' names

    schools = [(row[25], row[1][0]) if row[25] else (row[3], row[1][0]) for row in data]

    schools = [school for school in schools if school[0] != ""]  # deleting items where schoolname is blank

    corrected = correct_schoolnames(schools)

    measured_schools = measure_schools(corrected)

    enough, not_enough = categorize_schools(measured_schools)

    write_output(enough, not_enough)

    #  to do:
    #  1. cities categorization
    #  2. гимназия-колледж искусств
