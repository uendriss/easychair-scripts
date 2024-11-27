# Analyse assignment downloaded from EasyChair, and split into three files
# Ulle Endriss, 5 May 2024 (cleaned up on 27 November 2024)

from mycsv import *

# headers: #, person #, first name, last name, email, country, affiliation, Web page, role
committee_csv = 'csv-in/committee.csv'
committee = read_csv(committee_csv)

# headers: #, title, authors, submitted, last updated, form fields, keywords, decision, notified, reviews sent, abstract, deleted?
submission_csv = 'csv-in/submission.csv'
submissions = read_csv(submission_csv)

# headers: member #, member name, submission #, bid
bidding_csv = 'csv-in/bidding.csv'
bidding = read_csv(bidding_csv)

# headers: member #, member name, submission #
assignment_csv = 'csv-in/assignment.csv'
assignment = read_csv(assignment_csv)

assignment_pc_csv = 'csv-out/assignment_pc.csv'
assignment_spc_csv = 'csv-out/assignment_spc.csv'
assignment_ac_csv = 'csv-out/assignment_ac.csv'

# report number of assignments
print('Found ' + str(len(assignment)) + ' paper/person assignments.')

# build role dictionary
role = dict()
for row in committee:
    id = row['#']
    role[id] = row['role']

# split assignment into three subassignments
print('\nSplitting assignment into three separate files.')
headers = ['member #', 'member name', 'submission #']
assignment_pc = []
assignment_spc = []
assignment_ac = []
for row in assignment:
    id = row['member #']
    if role[id] == 'PC member': assignment_pc.append(row)
    if role[id] == 'senior PC member': assignment_spc.append(row)
    if role[id] == 'associate chair': assignment_ac.append(row)
write_csv(assignment_pc, headers, assignment_pc_csv)
write_csv(assignment_spc, headers, assignment_spc_csv)
write_csv(assignment_ac, headers, assignment_ac_csv)

# build dictionaries to get lists of yes/maybe bids for each person
yes_bids = dict()
maybe_bids = dict()
for row in committee:
    id = row['#']
    yes_bids[id] = []
    maybe_bids[id] = []
for row in bidding:
    id = row['member #']
    submission = row['submission #']
    bid = row['bid']
    if bid == 'yes': yes_bids[id].append(submission)
    if bid == 'maybe': maybe_bids[id].append(submission)

# report quality of given type of assignment
def assignment_quality(type, rows):
    n = len(rows)
    count_yes = 0
    count_maybe = 0
    count_no = 0
    for row in rows:
        p = row['member #']
        s = row['submission #']
        if s in yes_bids[p]: count_yes = count_yes + 1
        elif s in maybe_bids[p]: count_maybe = count_maybe + 1
        else: count_no = count_no + 1
    output = '- ' + type + ': '        
    output = output + str(count_yes) + ' yes-bids (' + str(round(100*count_yes/n)) + '%), '       
    output = output + str(count_maybe) + ' maybe-bids (' + str(round(100*count_maybe/n)) + '%), '       
    output = output + str(count_no) + ' no-bids (' + str(round(100*count_no/n)) + '%)'       
    print(output)            

# report on quality of assignment
print('\nOverall quality of assignment:')
assignment_quality('PC', assignment_pc)
assignment_quality('SPC', assignment_spc)
assignment_quality('AC', assignment_ac)

# list regular PC members who received more than one paper they did not bid for
print('\nRegular PC members with more than 1 assigned paper they did not bid for:')
name = dict()
papers = dict()
for row in committee:
    id = row['#']
    name[id] = row['first name'] + ' ' + row['last name']
    papers[id] = []
for row in assignment_pc:
    id = row['member #']
    submission = row['submission #']
    papers[id].append(submission)
for id in name:
    if role[id] == 'PC member':
        critical = [p for p in papers[id] if p not in yes_bids[id] and p not in maybe_bids[id]]
        if len(critical) > 1:
            output = name[id] + ': ' + str(len(critical)) + ' out of '
            output = output + str(len(papers[id])) + ' papers not bid for '
            output = output + '(bid size: ' + str(len(yes_bids[id]) + len(maybe_bids[id])) + ')'
            print(output)

# get bid type for given person/paper pair (treating conflicts as 'no')
def bid_type(person, paper):
    if paper in yes_bids[person]: return 'yes'
    elif paper in maybe_bids[person]: return 'maybe'
    else: return 'no'
            
# list papers with more than one assigned PC member who did not bid for it
print('\nPapers with more than 1 assigned PC member who did not bid for it:')
reviewers = dict()
for row in assignment_pc:
    reviewer = row['member #']
    paper = row['submission #']
    if paper in reviewers:
        reviewers[paper].append(reviewer)
    else:
        reviewers[paper] = [reviewer]
problems = []
for p in reviewers:
    bids = [bid_type(r,p) for r in reviewers[p]]
    if bids.count('no') > 1:
        bids_received = len(lookup(bidding, 'submission #', p, 'bid'))
        title = lookup(submissions, '#', p, 'title')[0]
        problems.append([p, bids, bids_received, title])
problems.sort(key = lambda x : x[2])
for problem in problems:
    output = '#' + problem[0] + ': ' + '-'.join(problem[1])
    output = output + ' (' + str(problem[2]) + ' bids received) -- ' + problem[3][:50]
    print(output)

