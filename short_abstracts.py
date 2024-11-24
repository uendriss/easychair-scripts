# Help finding placeholder abstracts
# Ulle Endriss, 14 April 2024 (cleaned up on 24 November 2024)

# Produces csv file with abstracts ordered by length.
 
from mycsv import *

# input: #, title, authors, submitted, last updated, form fields, keywords, decision, notified, reviews sent, abstract, deleted?
submission_csv = 'csv-in/submission.csv'

# output: #, length, abstract
abstract_csv = 'csv-out/abstract.csv'

input = read_csv(submission_csv)
headers = ['#', 'length', 'abstract']
output = []
for row in input:
    if row['deleted?'] == 'no':
        paper_id = row['#']
        abstract = row['abstract']
        output.append({
            '#': paper_id,
            'length': len(abstract),
            'abstract': abstract
            })
output.sort(key = lambda x : x['length'])    
write_csv(output, headers, abstract_csv)

