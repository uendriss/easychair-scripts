# Collusion detection
# Ulle Endriss, 15 May 2024 (cleaned up on 27 November 2024)

# Perform simplistic checks for collusion:
# - two-cycles: two people reviewing each others' papers
# - papers where most reviewers assigned are from the same country as most authors
# Any hits found should be inspected but are by no means proof of collusion.

from mycsv import *

# headers: #, person #, first name, last name, email, country, affiliation, Web page, role
committee_csv = 'csv-in/committee.csv'
committee = read_csv(committee_csv)

# headers: submission #, first name, last name, email, country, affiliation, Web page, person #, corresponding?
author_csv = 'csv-in/author.csv'
author = read_csv(author_csv)

# headers: #, title, authors, submitted, last updated, form fields, keywords, decision, notified, reviews sent, abstract, deleted?
submission_csv = 'csv-in/submission.csv'
submission = read_csv(submission_csv)

# headers: member #, member name, submission #
assignment_csv = 'csv-in/assignment.csv'
assignment = read_csv(assignment_csv)

# collect person ID of each "reviewer" (= PC/SPC/AC/chair)
reviewers = [int(row['person #']) for row in committee]
    
# collect person ID of each author
authors = list(set([int(row['person #']) for row in author]))

# collect person ID of each person who has both roles
author_reviewers = [x for x in reviewers if x in authors]

# collect paper IDs occuring in assignment
papers = [int(row['#']) for row in submission]

# Report basic stats
print('Found ' + str(len(papers)) + ' papers.')
print('Found ' + str(len(reviewers)) + ' reviewers (meaning: PC/SPC/AC/chairs).')
print('Found ' + str(len(authors)) + ' authors.')
print('Found ' + str(len(author_reviewers)) + ' individuals who are both.')

# Recover person ID from member ID
person_id = dict()
for row in committee:
    m = int(row['#']) 
    p = int(row['person #'])
    person_id[m] = p

# Retrieve name, country, and role from person ID (the latter only for committee members)
name = dict()
country = dict()
role = dict()
for row in committee:
    r = int(row['person #'])
    name[r] = row['first name'] + ' ' + row['last name']
    country[r] = row['country']
    if row['role']=='PC member': role[r] = 'PC'
    if row['role']=='senior PC member': role[r] = 'SPC'
    if row['role']=='associate chair': role[r] = 'AC'
for row in author:
    a = int(row['person #'])
    name[a] = row['first name'] + ' ' + row['last name']
    country[a] = row['country']
    
# Dictionaries: reviewers/papers
reviewer_papers = dict()
paper_reviewers = dict()
for r in reviewers:
    reviewer_papers[r] = set()
for p in papers:
    paper_reviewers[p] = set()
for row in assignment:
    m = int(row['member #'])
    r = person_id[m]
    p = int(row['submission #'])
    reviewer_papers[r].add(p)
    paper_reviewers[p].add(r)

# Dictionaries: authors/papers
paper_authors = dict()
author_papers = dict()
for p in papers:
    paper_authors[p] = set()
for a in authors:
    author_papers[a] = set()
for row in author:
    a = int(row['person #'])
    p = int(row['submission #'])
    if p in papers:
        paper_authors[p].add(a)
        author_papers[a].add(p)

# Construct reviewing graph
reviews = dict()
for r in reviewers:
    reviews[r] = set()
    for p in reviewer_papers[r]:
        reviews[r] = reviews[r].union(paper_authors[p])
reviewed_by = dict()
for a in authors:
    reviewed_by[a] = set()
    for p in author_papers[a]:
        reviewed_by[a] = reviewed_by[a].union(paper_reviewers[p])
print('Reviewing graph constructed successfully.')    

# find the paper(s) "between" two given people (reviewer and author)
def papers_between(r, a):
    return reviewer_papers[r].intersection(author_papers[a])

# display a given 2-cycle:
def display_two_cycle(r1, r2):
    output = name[r1] + '/' + role[r1] + ' reviews ' + str(papers_between(r1,r2))
    output = output + ' authored by ' + name[r2] + '/' + role[r2]
    output = output + ' reviews ' + str(papers_between(r2,r1))
    output = output + ' authored by ' + name[r1] + '/' + role[r1]
    print('> ' + output)

# helper function to rank reviewers in terms of seniority 
def role_score(r):
    if role[r]=='AC':
        return 3
    elif role[r]=='SPC':
        return 1
    else:
        return 0
    
# find all 2-cycles in the review assignment
pairs = []
for i in author_reviewers:
    hits = [x for x in reviews[i] if x in reviewed_by[i] and x > i]
    for x in hits:
        pairs.append((i,x))
print('Found ' + str(len(pairs)) + ' two-cycles in the reviewing graph:')
pairs.sort(key = lambda x : role_score(x[0]) + role_score(x[1]))
for pair in pairs:
    display_two_cycle(pair[0], pair[1])

# get proportion to which a given paper belongs to a given country in terms of authors
def author_country_weight(p, c):
    cs = lookup(author, 'submission #', str(p), 'country')
    return cs.count(c) / len(cs)

# get proportion to which a given paper belongs to a given country in terms of authors
def reviewer_country_weight(p, c):
    cs = [country[r] for r in paper_reviewers[p]]
    if len(cs) > 0:
        return cs.count(c) / len(cs)
    else:
        return 0

# look for papers where more at least 50% of authors and reviewers are from the same country
matches = []
for p in papers:
    cs = list(set(lookup(author, 'submission #', str(p), 'country')))
    for c in cs:
        if author_country_weight(p,c) >= 0.5 and reviewer_country_weight(p,c) >= 0.5:
            matches.append((p,c))
print('Found ' + str(len(matches)) + ' papers where at least half of authors and reviewers are from the same country.')
for match in matches:
    p = match[0]
    c = match[1]
    rp = str(round(100 * reviewer_country_weight(p,c))) + '%'
    ap = str(round(100 * author_country_weight(p,c))) + '%'
    people = [name[i] + '/' + role[i] for i in paper_reviewers[p] if country[i]==c]
    people = people + [name[i] for i in paper_authors[p]  if country[i]==c]
    print('> ' + str(p) + ' - ' + c + ' (' + rp + ',' + ap + ') - ' + ', '.join(people))
involved_reviewers =[]
for match in matches:
    p = match[0]
    involved_reviewers = involved_reviewers + list(paper_reviewers[p])
frequent_reviewers = []
for r in involved_reviewers:
    frequent_reviewers.append((r,involved_reviewers.count(r)))
frequent_reviewers = list(set(frequent_reviewers))
frequent_reviewers.sort(key = lambda x : x[1], reverse = True)
print('List of reviewers involved in more than one of these cases:')
for pair in frequent_reviewers:
    r = pair[0]
    f = pair[1]
    if f > 1:
        print('> ' + name[r] + '/' + role[r] + ' - ' + str(f) + ' papers')
