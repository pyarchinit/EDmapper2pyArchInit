
import csv
def transform_data(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        col1_idx = header.index('anteriore')
        col2_idx = header.index('posteriore')
        col3_idx = header.index('contemporaneo')
        new_header = header + ['rapporti']
        rows = []
        for row in reader:
            col1_values = row[col1_idx].split('|')
            col2_values = row[col2_idx].split('|')
            col3_values = row[col3_idx].split('|')
            new_col = []
            for val in col1_values:

                if val:
                    new_col.append(['copre', val])

            for val in col2_values:

                if val:
                    new_col.append(['coperto da', val])
            for val in col3_values:

                if val:
                    new_col.append(['si lega', val])
            row.append(new_col)
            rows.append(row)
    with open('output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(new_header)
        for row in rows:
            writer.writerow(row)
file_path = 'esempio.csv'
transform_data(file_path)
print('Operazione completata.')
import pandas as pd
data = pd.read_csv('output.csv', nrows=10)
print(data.to_string(index=False))