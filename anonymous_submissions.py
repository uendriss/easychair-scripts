# Make file with anonymised submissions to share with sister conferences
# (for dual-submission detection)
# Ulle Endriss, 14 April 2024 (cleaned up on 24 November 2024)

# Needs EasyChair file submission.csv.
 
from mycsv import *

# input: #, title, authors, submitted, last updated, form fields, keywords, decision, notified, reviews sent, abstract, deleted?
submission_csv = 'csv-in/submission.csv'

# output: #, length, abstract
anonymised_csv = 'csv-out/anonymised_submissions.csv'

input = read_csv(submission_csv)
headers = ['id', 'title', 'abstract']
output = []
for row in input:
    if row['deleted?'] == 'no':
        paper_id = row['#']
        title = row['title']
        abstract = row['abstract']
        output.append({
            'id': paper_id,
            'title': title,
            'abstract': abstract
            })
write_csv(output, headers, anonymised_csv)

