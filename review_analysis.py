# Analysis of incoming reviews
# Ulle Endriss, 11 June 2024 (cleaned up on 27 November 2024)

from mycsv import *
from math import floor
import re
import string

# headers: #, submission #, member #, member name, number, version, text, scores, reviewer first name, reviewer last name, reviewer email, reviewer person #, date, time, attachment?
review_csv = 'csv-in/review.csv'
review = read_csv(review_csv)

# headers: member #, member name, submission #
assignment_csv = 'csv-in/assignment.csv'
assignment = read_csv(assignment_csv)

# headers: #, person #, first name, last name, email, country, affiliation, Web page, role
committee_csv = 'csv-in/committee.csv'
committee = read_csv(committee_csv)

# headers: submission #, first name, last name, email, country, affiliation, Web page, person #, corresponding?
author_csv = 'csv-in/author.csv'
author = read_csv(author_csv)

# headers: #, title, authors, submitted, last updated, form fields, keywords, decision, notified, reviews sent, abstract, deleted?
submission_csv = 'csv-in/submission.csv'
submission_rows = read_csv(submission_csv)

# headers: topic, header?
topics_csv = 'csv-in/topics.csv'
topics = read_csv(topics_csv)

# headers: submission #, topic
submission_topic_csv = 'csv-in/submission_topic.csv'
submission_topic = read_csv(submission_topic_csv)

# headers: member #, name, email, num_bids
emergency_reviewers_csv = 'csv-in/emergency_reviewer.csv'
emergency_reviewers = read_csv(emergency_reviewers_csv)

# headers: submission #, name, words, score, confidence, text, confidential remarks
reviews_by_length_csv = 'csv-out/reviews_by_length.csv'

# headers: submission #, name, score, confidence, confidential remarks, timestamp
confidential_remarks_csv = 'csv-out/confidential_remarks.csv'

# headers: name, email, completed, missing, progress
progress_pc_csv = 'csv-out/progress_pc.csv'

# headers: name, available, missing, nonready papers
progress_spc_csv = 'csv-out/progress_spc.csv'

# headers: submission #, reviews, scores, remaining, title
missing_reviews_csv = 'csv-out/missing_reviews.csv'

# remove deleted submissions w/o status from database 
submissions = [int(row['#']) for row in submission_rows if row['deleted?']=='no' or row['decision']!='no decision']
active_submissions = [int(row['#']) for row in submission_rows if row['deleted?']=='no' and row['decision']=='no decision']

# collect paper titles
title = dict()
for row in submission_rows:
    s = int(row['#'])
    title[s] = row['title']

# store relevant member information in dictionaries
members = []
person_id = dict()
member_id = dict()
name = dict()
email = dict()
role = dict()
for row in committee:
    i = int(row['#'])
    pi = int(row['person #'])
    person_id[i] = pi
    member_id[pi] = i
    members.append(i)
    name[i] = row['first name'] + ' ' + row['last name']
    email[i] = row['email']
    if row['role']=='PC member': role[i] = 'PC'
    if row['role']=='senior PC member': role[i] = 'SPC'
    if row['role']=='associate chair': role[i] = 'AC'
    if row['role']=='chair': role[i] = 'chair'
pc = [i for i in members if role[i]=='PC']
spc = [i for i in members if role[i]=='SPC']

# store relevant assignment information in dictionaries
assigned = dict()
completed = dict()
for i in members:
    assigned[i] = []
    completed[i] = []
for row in assignment:
    i = int(row['member #'])
    assigned[i].append(int(row['submission #']))
n_expected = 0
for i in pc:
    n_expected = n_expected + len(assigned[i])
print('Found ' + str(n_expected) + ' review assignments to regular PC members.')
    
# store relevant review information in dictionaries
reviews = []
submission = dict()
rev_name = dict() # name by review ID rather than reviewer ID
score = dict()
confidence = dict()
text = dict()
confidential_remarks = dict()
timestamp = dict()
for row in review:
    i = int(row['#'])
    reviews.append(i)
    submission[i] = int(row['submission #'])
    rev_name[i] = row['member name'] # so subreviewer name is ignored
    scores = re.findall(r'\d+', row['scores'])
    score[i] = int(scores[0])
    confidence[i] = int(scores[1])
    timestamp[i] = row['date'] +' ' + row['time']
    part = row['text'].split('(CONFIDENTIAL REMARKS FOR THE PROGRAMME COMMITTEE)',1)
    text[i] = part[0]    
    if len(part) > 1:
        confidential_remarks[i] = part[1]
    completed[int(row['member #'])].append(int(row['submission #']))    
print('Found ' + str(len(reviews)) + ' reviews (~' + str(round(100 * len(reviews) / n_expected, 1)) + '%).')        
            
# save reviews orders by length
words = dict()
for i in reviews:
    pure_text = text[i].replace('(SUMMARY)','')
    pure_text = pure_text.replace('(STRENGTHS)','')
    pure_text = pure_text.replace('(WEAKNESSES)','')
    pure_text = pure_text.replace('(DETAILED COMMENTS)','')
    pure_text = pure_text.replace('(QUESTIONS FOR REBUTTAL)','')
    words[i] = len(pure_text.split())
headers = ['submission #', 'name', 'words', 'score', 'confidence', 'text', 'confidential remarks']    
output = []
for i in reviews:
    if i in confidential_remarks:
        cm = confidential_remarks[i]
    else:
        cm = 'NONE'
    output.append({
        'submission #': submission[i],
        'name': rev_name[i],
        'words': words[i],
        'score': str(score[i]),
        'confidence': str(confidence[i]),
        'text': text[i],
        'confidential remarks': cm
        })
output.sort(key = lambda x : int(x['words']))
write_csv(output, headers, reviews_by_length_csv)

# store list of review lengths per submissions
review_lengths = dict()
for s in submissions:
    review_lengths[s] = []
for r in reviews:
    s = submission[r]
    review_lengths[s].append(words[r])

# check to exclude irrelevant confidential remarks
def remark_relevant(remark):
    remark = remark.translate(str.maketrans('', '', string.punctuation))
    words = remark.lower().split()
    stopwords = {'no', 'none', 'nothing', 'na', 'n/a'}
    if len(words) > 3:
        return True
    else:
        if set(words).intersection(stopwords):
                return False
        elif words == []:
                return False
        else:
                return True

# save all confidential comments
output = []
headers = ['submission #', 'name', 'score', 'confidence', 'confidential remarks', 'timestamp']
for i in confidential_remarks:
    if remark_relevant(confidential_remarks[i]):
        output.append({
            'submission #': submission[i],
            'name': rev_name[i],
            'score': str(score[i]),
            'confidence': str(confidence[i]),
            'confidential remarks': confidential_remarks[i],
            'timestamp': timestamp[i]
            })
output.sort(key = lambda x : x['timestamp'], reverse = True)
write_csv(output, headers, confidential_remarks_csv)

# check progress by paper
print('Found ' + str(len(active_submissions)) + ' active submisisons.')
scores = dict()
for s in submissions:
    scores[s] = []
for r in reviews:
    s = submission[r]
    if s in submissions:
        scores[s].append(score[r])
for s in active_submissions:
    scores[s].sort()
submissions_by_review_number = dict()
for n in range(5):
    submissions_by_review_number[n] = []    
for s in active_submissions:
    n = len(scores[s])
    if n > 3:
        submissions_by_review_number[4].append(s) # papers with > 3 reviews
        n = 3
    submissions_by_review_number[n].append(s)
submissions_by_review_number[1].sort(key = lambda x : scores[x][0], reverse = True)
submissions_by_review_number[2].sort(key = lambda x : scores[x][1]-scores[x][0] - abs(11-scores[x][0]-scores[x][1])/100, reverse = True)
print('Need ' + str(2 * len(submissions_by_review_number[1]) + len(submissions_by_review_number[2])) + ' more reviews.')
er_pool = [row['name'] for row in emergency_reviewers]
remaining = dict()
for s in active_submissions:
    remaining[s] = []
for i in pc:
    for s in assigned[i]:
        if s in active_submissions and s not in completed[i]:
            reviewer_name = name[i]
            if reviewer_name in er_pool:
               reviewer_name = '***' + reviewer_name
            reviewer_name = reviewer_name + ' ' + str(len(completed[i])) + '/' + str(len(assigned[i]))  
            remaining[s].append(reviewer_name)
for s in active_submissions:
    remaining[s].sort()
headers = ['submission #', 'reviews', 'scores', 'remaining', 'title']
output = []
for s in submissions_by_review_number[1] + submissions_by_review_number[2]:
        output.append({
            'submission #': s,
            'reviews': len(scores[s]),
            'scores': ' - '.join([str(x) for x in scores[s]]),
            'remaining': ' - '.join(remaining[s]),
            'title': title[s]
            })
write_csv(output, headers, missing_reviews_csv)

# check progress per PC member
headers = ['name', 'email', 'completed', 'missing', 'progress']
output = []
for i in members:
    if role[i]=='PC' and assigned[i]:
        c = len(completed[i])
        m = len([x for x in assigned[i] if x not in completed[i]])
        p = round(100 * c / (c+m))
        output.append({
            'name': name[i],
            'email': email[i],
            'completed': c,
            'missing': m,
            'progress': p
            })
output.sort(key = lambda x : x['completed'], reverse = False)        
output.sort(key = lambda x : x['missing'], reverse = True)        
output.sort(key = lambda x : x['progress'], reverse = False)        
write_csv(output, headers, progress_pc_csv)

# check progress per SPC member
spc_in_charge = dict()
for row in assignment:
    i = int(row['member #'])
    if role[i]=='SPC':
        s = int(row['submission #'])
        spc_in_charge[s] = i
spc_assignments = dict()
spc_completed = dict()
spc_papers_not_ready = dict()
for i in spc:
    spc_assignments[i] = []
    spc_completed[i] = []
    spc_papers_not_ready[i] = []
for row in assignment:
    r = int(row['member #'])
    s = int(row['submission #'])
    if s in spc_in_charge and r in pc:
        i = spc_in_charge[s]
        spc_assignments[i].append((r,s)) 
for row in review:
    r = int(row['member #'])
    s = int(row['submission #'])
    if s in spc_in_charge:
        i = spc_in_charge[s]
        spc_completed[i].append((r,s)) 
spc_missing = dict()
for i in spc:
    spc_missing[i] = [x for x in spc_assignments[i] if x not in spc_completed[i]]
for row in assignment:
    s = int(row['submission #'])
    i = int(row['member #'])
    if i in spc and s in active_submissions and s not in submissions_by_review_number[3]:
        spc_papers_not_ready[i].append(s)
headers = ['name', 'available', 'missing', 'nonready papers']
output = []    
for i in spc:
        output.append({
            'name': name[i],
            'available': len(spc_completed[i]),
            'missing': len(spc_missing[i]),
            'nonready papers': len(spc_papers_not_ready[i])
            })
output.sort(key = lambda x : x['missing'], reverse = True)        
output.sort(key = lambda x : x['available'], reverse = False)        
output.sort(key = lambda x : x['nonready papers'], reverse = True)        
write_csv(output, headers, progress_spc_csv)

# check percentage of accept/reject/borderline scores
accept = [i for i in reviews if score[i] in [7,8,9,10]]
reject = [i for i in reviews if score[i] in [1,2,3,4]]
borderline = [i for i in reviews if score[i] in [5,6]]
p = round(100 * len(accept) / len(reviews))
print(str(p) + '% of reviews have ACCEPT scores.')
p = round(100 * len(reject) / len(reviews))
print(str(p) + '% of reviews have REJECT scores.')
p = round(100 * len(borderline) / len(reviews))
print(str(p) + '% of reviews have BORDERLINE scores.')
