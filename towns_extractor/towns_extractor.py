import csv

def remove_duplicates(data):
    preprocessed = []
    for item in data:
        if item not in preprocessed:
            preprocessed.append(item)
    return preprocessed


with open("data/source.csv", "r", newline="",  encoding="utf-8") as source, \
     open("data/towns.csv", "w", newline="", encoding="utf-8") as output:
    reader = csv.reader(source, delimiter='\t')
    writer = csv.writer(output)

    towns = [row[21] for row in reader][1:]

    capital_city_index = towns.index("Минск")  # getting index of the capital city in the list

    towns[0], towns[capital_city_index] = towns[capital_city_index], towns[0]  # setting capital city to the first
                                                                                                        # position
    processed_towns = remove_duplicates(towns)

    for i in range(len(processed_towns)):
        writer.writerow([processed_towns[i]])