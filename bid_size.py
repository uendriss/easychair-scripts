# Generate lists of bid sizes submited by PC members
# Ulle Endriss, 4 May 2024 (cleaned up on 24 November 2024)

# This can be useful while monitoring bidding progress,
# to report statistics to PC members, to refine bidding instructions
# in future years, and to identify good candidates for the
# emergency reviewer pool.
 
from mycsv import *
import statistics

# headers: member #, member name, submission #, bid
bidding_csv = 'csv-in/bidding.csv'

# headers: #, person #, first name, last name, email, country, affiliation, Web page, role
committee_csv = 'csv-in/committee.csv'

# headers: name, total, yes, maybe, email
bid_size_ac_csv = 'csv-out/bid_size_ac.csv'

# headers: name, total, yes, maybe, email
bid_size_spc_csv = 'csv-out/bid_size_spc.csv'

# headers: name, total, yes, maybe, email
bid_size_pc_csv = 'csv-out/bid_size_pc.csv'

# read input
bidding = read_csv(bidding_csv)
committee = read_csv(committee_csv) 

# get PC status of a given committee member (specified by #, not person #)
def pc_status(id):
    status = 'none'
    for row in committee:
        if row['#'] == id:
            status = row['role']
    return status

# prepare lists
headers = ['name', 'total', 'yes', 'maybe', 'email']
bid_size_ac = []
bid_size_spc = []
bid_size_pc = []
for row in committee:
    id = row['#']
    name = row['first name'] + ' ' + row['last name']
    email = lookup(committee, '#', id, 'email')[0]
    role = pc_status(id)
    bids = lookup(bidding, 'member #', id, 'bid')
    n_total = len(bids)
    n_yes = bids.count('yes')
    n_maybe = bids.count('maybe')
    if role == 'associate chair':
        bid_size_ac.append({
            'name': name,
            'total': n_total,
            'yes': n_yes,
            'maybe': n_maybe,
            'email': email
            })
    if role == 'senior PC member':
        bid_size_spc.append({
            'name': name,
            'total': n_total,
            'yes': n_yes,
            'maybe': n_maybe,
            'email': email
            })     
    if role == 'PC member':
        bid_size_pc.append({
            'name': name,
            'total': n_total,
            'yes': n_yes,
            'maybe': n_maybe,
            'email': email
            })     
bid_size_ac.sort(key = lambda x : x['total'])    
write_csv(bid_size_ac, headers, bid_size_ac_csv)
bid_size_spc.sort(key = lambda x : x['total'])    
write_csv(bid_size_spc, headers, bid_size_spc_csv)
bid_size_pc.sort(key = lambda x : x['total'])    
write_csv(bid_size_pc, headers, bid_size_pc_csv)

# get high-level starts for given list of numbers
def stats(numbers):
    zeros = str(round(100 * numbers.count(0) / len(numbers))) + '% no bid, '
    nonzeros = [x for x in numbers if x!=0]
    median = 'median ' + str(round(statistics.median(nonzeros))) + ', '
    mean = 'mean ' + str(round(statistics.mean(nonzeros)))
    return zeros + median + mean
    
# report high-level stats
print('')
pc_totals = [row['total'] for row in bid_size_pc]
print('PC:  ' + stats(pc_totals))
spc_totals = [row['total'] for row in bid_size_spc]
print('SPC: ' + stats(spc_totals))
ac_totals = [row['total'] for row in bid_size_ac]
print('AC:  ' + stats(ac_totals))
        

 
 
