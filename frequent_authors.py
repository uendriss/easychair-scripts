# Generate list of authors ordered by number of submissions
# Ulle Endriss, 26 April 2024 (cleaned up on 24 November 2024)

# Generate list of authors ordered by number of papers submitted,
# incuding information on PC-member status of each author.
# Can be used to identify authors above the submission limit.
# Can also be used to identify prolific authors to possibly invite to the PC.
 
from mycsv import *

# headers: submission #, first name, last name, email, country, affiliation, Web page, person #, corresponding?
author_csv = 'csv-in/author.csv'

# headers: #, title, authors, submitted, last updated, form fields, keywords, decision, notified, reviews sent, abstract, deleted?
submission_csv = 'csv-in/submission.csv'

# headers: #, person #, first name, last name, email, country, affiliation, Web page, role
committee_csv = 'csv-in/committee.csv'

# output: frequency, first name, last name, email, country, affiliation, Web page, person #
frequent_author_csv = 'csv-out/frequent_author.csv'

# read input
authors = read_csv(author_csv)
submissions = read_csv(submission_csv)
committee = read_csv(committee_csv)

# build list of submission ids of non-deleted submissions
submission_ids = []
for row in submissions:
    if row['deleted?'] == 'no':
        submission_id = row['#']
        submission_ids.append(submission_id)

# count frequency of given author
def count(author_id):
    n  = 0
    for row in authors:
        if row['person #'] == author_id:
            submission_id = row['submission #']
            if submission_id in submission_ids:
                n = n + 1
    return n

# get PC status of a given author
def pc_status(author_id):
    status = 'no'
    for row in committee:
        if row['person #'] == author_id:
            status = row['role']
    return status
    
# prepare output list
output = []
seen = []
headers = ['frequency', 'PC?', 'first name', 'last name', 'email', 'country', 'affiliation', 'Web page', 'person #']
for row in authors:
    author_id = row['person #']
    if author_id not in seen:
        seen.append(author_id)
        output.append({
            'frequency': count(author_id),
            'PC?': pc_status(author_id),
            'first name': row['first name'],
            'last name': row['last name'],
            'email': row['email'],
            'country': row['country'],
            'affiliation': row['affiliation'],
            'Web page': row['Web page'],
            'person #': row['person #'],
            })
output.sort(key = lambda x : x['frequency'], reverse=True)    
write_csv(output, headers, frequent_author_csv)

