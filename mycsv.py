# Provide simple read/write methods for csv files (as used by EasyChair)
# Ulle Endriss, 11 April 2024

import csv

# return list of dictionaries corresponding to rows in input csv file 
def read_csv(path_to_input_csv):
    f = open(path_to_input_csv, encoding='utf-8-sig')
    reader = csv.DictReader(f, delimiter=',')
    return [row for row in reader]

# write given list/dictionary to given csv file, using given headers
def write_csv(output, headers, path_to_output_csv):
    f = open(path_to_output_csv, 'w', newline='') 
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    for row in output:
        writer.writerow(row)
    print('> ' + str(len(output)) + ' rows written to ' +  path_to_output_csv)

# lookup values in reader
def lookup(reader, in_column, in_value, out_column):
    out_values = []
    for row in reader:
        if row[in_column] == in_value:
            out_values.append(row[out_column])
    return out_values
            
    
