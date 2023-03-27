import csv

# Create empty lists to store the data
col1, col2 = [], []

# Open the CSV file and read its contents
with open('esempio.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    # Loop through each row of the CSV file and append the data to the lists
    for row in csv_reader:
        col1.append(row[4])
        col2.append(row[5])

# Combine the two columns into a list of lists
data = [[col1[i], col2[i]] for i in range(len(col1))]

# Print the result
print(data)