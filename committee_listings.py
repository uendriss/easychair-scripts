# Script to generate lists of committee members for website and proceedings
# Also collects names of PC members who should possibly be removed
# Ulle Endriss, 19 June 2024 (cleaned up on 28 November 2024)

from mycsv import *
from unidecode import unidecode

# headers: #, person #, first name, last name, email, country, affiliation, Web page, role
committee_csv = 'csv-in/committee.csv'
committee = read_csv(committee_csv)

# headers: #, submission #, member #, member name, number, version, text, scores, reviewer first name, reviewer last name, reviewer email, reviewer person #, date, time, attachment?
review_csv = 'csv-in/review.csv'
review = read_csv(review_csv)

# headers: member #, name, email, num_bids
emergency_reviewers_csv = 'csv-in/emergency_reviewer.csv'
emergency_reviewers = read_csv(emergency_reviewers_csv)

# path to directory where output should be saved
path = 'csv-out/'

# store committee files of a given type
def store(type, names):
    csv_output = path + 'listing_' + type + '.csv'
    txt_output = path + 'listing_' + type + '.txt'
    f = open(csv_output, 'w', newline='')
    for name in names:
        f.write(name + '\n')
    f.close()
    f = open(txt_output, 'w', newline='')
    f.write(', '.join(names))
    f.close()
    print('> ' + str(len(names)) + ' names written to ' + csv_output + ' and ' + txt_output)
    
# build and store list for given type
def build(type, easychair_type):
    listing = [row['first name'] + ' ' + row['last name'] for row in committee if row['role']==easychair_type]
    listing.sort(key = lambda x : unidecode(x))
    store(type, listing)

# build lists for PC/SPC/AC
print('\nPreparing lists of committee members ...')
build('pc', 'PC member')
build('spc', 'senior PC member')
build('ac', 'associate chair')

# Subreviewers with at least one submitted review
# Note: in case there are two people with the same name it will print the name just once
# Note: subreviewers who also have another role will get removed
subreviewers = [row['reviewer first name'] + ' ' + row['reviewer last name'] for row in review if row['reviewer person #']]
subreviewers = list(set(subreviewers))
for row in committee:
    name = row['first name'] + ' ' + row['last name']
    if name in subreviewers:
        subreviewers.remove(name)
subreviewers.sort(key = lambda x : unidecode(x))
store('subreviewers', subreviewers)

# build dictionaries for PC members
person_name = dict()
member_person = dict()
for row in committee:
    m = int(row['#'])
    p = int(row['person #'])
    person_name[p] = row['first name'] + ' ' + row['last name']
    member_person[m] = p

# PC members who are candidates for removal
print('\nPC members with no reviews who are not in the emergency reviewer pool (candidates for removal):')
pc = [int(row['person #']) for row in committee if row['role']=='PC member']
active = [member_person[int(row['member #'])] for row in review]
emergency_names = [row['name'] for row in emergency_reviewers]
removal = []
for id in pc:
    name = person_name[id]
    if id not in active and name not in emergency_names:
        removal.append(name)
removal.sort(key = lambda x : unidecode(x))
if len(removal) > 100:
    print('[more than 100 names]')
else:
    print(', '.join(removal))
        
    

