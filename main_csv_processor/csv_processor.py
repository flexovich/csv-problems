import csv
import re

def schoolname_parser(schoolname):
    name = re.search(r"(?i).*?(Средняя школа|СШ|Школа|Лицей|Гимназия).*?", schoolname)
    number = re.search(r"(?i).*?(\d{1,3}|БНТУ|БГУ).*?", schoolname)
    return [name, number]

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
    return final_list


with open("data/poll.csv", "r", newline="", encoding="utf-8") as read:

    reader = csv.reader(read)

    data = [row for row in reader][1:]

    schools = [row[25] if row[25] else row[3] for row in data]