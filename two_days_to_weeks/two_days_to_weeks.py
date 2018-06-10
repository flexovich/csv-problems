from statistics import mean
from functools import reduce
import csv


def to7(l):
    if len(l) < 7:
        return []
    else:
        return [l[0:7]] + to7(l[7:])


def all_to_averages(l):
    return reduce(lambda x, y: x + y, map(list_to_average, l), [])

def list_to_average(l):
    return [mean(l[0:4]), mean(l[3:7])]

with open("data/bitcoin_price.csv", 'r', newline="") as csv_inp, \
     open("data/bitcoin_price_out.csv", "w", newline="") as csv_out,\
     open("data/bitcoin_request.csv", 'r', newline="") as csv_req:

    reader_price = csv.reader(csv_inp)
    reader_req = csv.reader(csv_req)
    writer_price = csv.writer(csv_out)

    prices = [row[1] for row in reader_price]

    grouped_string_prices = to7(prices)   # after execution of this line of code 'grouped_prices' represents to list
                                                                                               # of lists of strings

    grouped_prices = [list(map(float, value_list)) for value_list in grouped_string_prices]   # now all the values are
                                                                                                      # integer values
    average_prices = all_to_averages(grouped_prices)

    request_dates = [row[0] for row in reader_req][:-1]

    for i in range(len(request_dates)):
        writer_price.writerow([request_dates[i], average_prices[i]])