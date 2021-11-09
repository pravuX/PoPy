from csv import DictReader, DictWriter
import matplotlib.pyplot as plt


# For better resolution graph
plt.rcParams['figure.dpi'] = 120


def show_stats():
    """ Read the csv file and provide a list of dictionaries containing one
    key-value pair corresponding to the day and the respective no. of
    sessions."""
    with open('sample.csv') as csv_file:
        reader = DictReader(csv_file)
        session_list = [row for row in reader]

    dates = [row['Date'] for row in session_list]
    no_of_sessions = [int(row['Sessions']) for row in session_list]

    e = len(dates)
    last_5_dates = dates[e-5:e]
    last_5_sessions = no_of_sessions[e-5:e]

    # Create and show graph for last five days.
    if e >= 5:
        plt.subplot(2, 1, 1)
        plt.plot(last_5_dates, last_5_sessions)
        plt.subplot(2, 1, 2)
        plt.bar(last_5_dates, last_5_sessions)
    else:
        plt.subplot(1, 2, 1)
        plt.plot(dates, no_of_sessions)
        plt.subplot(1, 2, 2)
        plt.bar(dates, no_of_sessions)

    plt.show()


def add_row(row_arr):
    with open('sample.csv', 'a') as csv_file:
        field_names = ['Date', 'Sessions']
        writer = DictWriter(csv_file, field_names)
        for row in row_arr:
            writer.writerow(row)

show_stats()
