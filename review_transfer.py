# Review transfer
# Ulle Endriss, 11 July 2024 (cleaned up on 27 November 2024)

# Create list of anonymised review for each workshop upon request of authors.
# Requires list of review transfer requests on top of EasyChair files.

from mycsv import *
import re

# headers: #, title, authors, submitted, last updated, form fields, keywords, decision, notified, reviews sent, abstract, deleted?
submission_csv = 'csv-in/submission.csv'
submission_rows = read_csv(submission_csv)

# headers: #, submission #, member #, member name, number, version, text, scores, reviewer first name, reviewer last name, reviewer email, reviewer person #, date, time, attachment?
review_csv = 'csv-in/review.csv'
review = read_csv(review_csv)

# headers: submission #, member #, member name, recommendation, text, PC-only part, date, time
metareview_csv = 'csv-in/metareview.csv'
metareview = read_csv(metareview_csv)

# headers: Submission Number, Authors, Title, Workshop
transfer_request_csv = 'csv-in/review_transfer_request.csv'
transfer_request = read_csv(transfer_request_csv)

# base address for output
base = 'csv-out/review_transfer_'

# read requests
submissions = []
claimed_title = dict()
claimed_authors = dict()
workshop = dict()
for row in transfer_request:
    s = int(row['Submission Number'])
    if s in submissions:
        print('* Attention: repeated request for submission ' + str(s) + ' (overwriting earlier requests)')
    else:    
        submissions.append(s)
    claimed_title[s] = row['Title']
    claimed_authors[s] = row['Authors']
    workshop[s] = row['Workshop'].split(':')[0]
print('Found ' + str(len(submissions)) + ' unique review requests')

# print list of workshops with requests
workshops = list(set(workshop.values()))
workshops.sort()
print('Found requests for ' + str(len(workshops)) + ' workshops: ' + ', '.join(workshops))

# get eligible submissions (those that were rejected) and official titles/authors
title = dict()
authors = dict()
for row in submission_rows:
    s = int(row['#'])
    if s in submissions:
        if row['decision'] != 'reject':
            print('* Attention: request for non-rejected submission ' + str(s) + ' (ignored from here on)')
        else:
            title[s] = row['title']
            if title[s].strip() != claimed_title[s].strip():
                print('* Attention: difference in title for submission ' + str(s))
                print('  > ' + title[s]) 
                print('  > ' + claimed_title[s]) 
            authors[s] = row['authors']
            if authors[s].strip() != claimed_authors[s].strip():
                print('* Attention: difference in authors for submission ' + str(s))
                print('  > ' + authors[s]) 
                print('  > ' + claimed_authors[s]) 
            
# prepare output
headers = ['workshop', 'submission', 'title', 'authors', 'review', 'score', 'text']
info = dict()
for ws in workshops:
    info[ws] = []
for row in metareview:
    s = int(row['submission #'])
    if s in submissions:
        ws = workshop[s]
        info[ws].append({
            'workshop': ws,
            'submission': str(s),
            'title': title[s],
            'authors': authors[s],
            'review': 'metareview',
            'score': 'n/a',
            'text': '(METAREVIEW) ' + row['text']
            })
for row in review:
    s = int(row['submission #'])
    if s in submissions:
        ws = workshop[s]
        parts = row['text'].split('(CONFIDENTIAL REMARKS FOR THE PROGRAMME COMMITTEE)')
        if len(parts) == 1:
            text = parts[0]
        else:
            text = parts[0]
            parts = parts[1].split('(COMMENTS ADDED AFTER REBUTTAL)')
            if len(parts) == 2:
                text = text + '(COMMENTS ADDED AFTER REBUTTAL)' + parts[1]
        info[ws].append({
            'workshop': ws,
            'submission': str(s),
            'title': title[s],
            'authors': authors[s],
            'review': '#' + row['number'],
            'score': re.findall(r'\d+', row['scores'])[0] + '/10',
            'text': text
            })
for ws in workshops:
    info[ws].sort(key = lambda x : int(x['submission']))
    write_csv(info[ws], headers, base + ws + '.csv')



