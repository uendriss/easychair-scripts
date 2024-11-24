# Produce various statistics regarding papers
# Ulle Endriss 28 April 2024 (cleaned up on 24 November 2024)

from mycsv import *

# headers: #, title, authors, submitted, last updated, form fields, keywords, decision, notified, reviews sent, abstract, deleted?
submission_csv = 'csv-in/submission.csv'

# headers: submission #, first name, last name, email, country, affiliation, Web page, person #, corresponding?
author_csv = 'csv-in/author.csv'

# headers: topic, header?
topics_csv = 'csv-in/topics.csv'

# headers: submission #, topic
submission_topic_csv = 'csv-in/submission_topic.csv'

# headers: member #, member name, topic
committee_topic_csv = 'csv-in/committee_topic.csv'

# headers: area, submitted, desk-rejected, accepted
paper_area_stats_csv = 'csv-out/paper_area_stats.csv'

# headers: topic, papers, people, area
paper_topic_stats_csv = 'csv-out/paper_topic_stats.csv'

submissions = read_csv(submission_csv)
authors = read_csv(author_csv)
topics = read_csv(topics_csv)
submission_topic = read_csv(submission_topic_csv)
committee_topic = read_csv(committee_topic_csv)

# remove deleted submissions w/o status from database 
submissions = [row for row in submissions if row['deleted?']=='no' or row['decision']!='no decision']

# number of submissions
print('Found ' + str(len(submissions)) + ' submissions ...')

# country distribution in submissions
print('\nDistribution by country:')
print('------------------------')
country_weight = {}
for row in submissions:
    id = row['#']
    countries = lookup(authors, 'submission #', id, 'country')
    weight = 1 / len(countries)
    for c in countries:
        if c in country_weight:
            country_weight[c] = country_weight[c] + weight
        else:
            country_weight[c] = weight
country_weight_view = [[c,country_weight[c]] for c in country_weight] 
country_weight_view.sort(key = lambda row : row[1], reverse=True)
n = len(submissions)
for row in country_weight_view:
    print(row[0] + ' ' + str(round(100 * row[1]/n, 2)) + '%')
print('(' + str(len(country_weight)) + ' countries in total)')
    
# build dictionary with list of topics for each area
area_topics = dict()
topic_area = dict()
areas = []
for row in topics:
    if row['header?'] == 'yes':
        area = row['topic']
        area_topics[area] = []
        areas.append(area)
    else:
        topic = row['topic']
        area_topics[area].append(topic)
        topic_area[topic] = area

# area distribution in submissions
print('\nDistribution by topical area:')
print('-----------------------------')
area_weight = {}
for row in submissions:
    id = row['#']
    given_topics = lookup(submission_topic, 'submission #', id, 'topic')
    weight = 1 / len(given_topics)
    for t in given_topics:
        a = topic_area[t]
        if a in area_weight:
            area_weight[a] = area_weight[a] + weight
        else:
            area_weight[a] = weight
area_weight_view = [[a,area_weight[a]] for a in area_weight]            
area_weight_view.sort(key = lambda row : row[1], reverse=True)
n = len(submissions)
for row in area_weight_view:
    print(row[0] + ' ' + str(round(100 * row[1]/n, 1)) + '%')

print('')

# get totals
n_submitted = 0
n_desk_rejected = 0
n_accepted = 0
for row in submissions:
    n_submitted = n_submitted + 1
    if row['decision']=='desk reject':
        n_desk_rejected = n_desk_rejected + 1
    if row['decision']=='accept':
        n_accepted = n_accepted + 1
        
# write area stats to file
area_weight_submitted = {}
area_weight_desk_rejected = {}
area_weight_accepted = {}
headers = ['area', 'submitted', 'desk-rejected', 'accepted']
for a in areas:
    area_weight_submitted[a] = 0    
    area_weight_desk_rejected[a] = 0    
    area_weight_accepted[a] = 0    
for row in submissions:
    id = row['#']
    given_topics = lookup(submission_topic, 'submission #', id, 'topic')
    weight = 1 / len(given_topics)
    for t in given_topics:
        a = topic_area[t]
        area_weight_submitted[a] = area_weight_submitted[a] + weight
        if row['decision']=='desk reject':
            area_weight_desk_rejected[a] = area_weight_desk_rejected[a] + weight
        if row['decision']=='accept':
            area_weight_accepted[a] = area_weight_accepted[a] + weight
area_stats = [[a,area_weight_submitted[a],area_weight_desk_rejected[a],area_weight_accepted[a]] for a in area_weight_submitted]
area_stats.sort(key = lambda row : row[1], reverse=True)
output = []
output.append({
    'area': 'Total',
    'submitted': n_submitted,
    'desk-rejected': n_desk_rejected,
    'accepted': n_accepted,
    })
for row in area_stats:
    output.append({
        'area': row[0],
        'submitted': round(row[1], 1),
        'desk-rejected': round(row[2], 1),
        'accepted': round(row[3], 1)
    })
write_csv(output, headers, paper_area_stats_csv)

# write topic stats file (absolute number of submissions and pc/spc/ac choosing topic)
topic_paper_weight = {}
topic_pc_weight = {}
headers = ['topic', 'papers', 'people', 'area']
for t in topic_area:
    topic_paper_weight[t] = 0
    topic_pc_weight[t] = 0
for row in submission_topic:
    t = row['topic']
    topic_paper_weight[t] = topic_paper_weight[t] + 1
for row in committee_topic:
    t = row['topic']
    topic_pc_weight[t] = topic_pc_weight[t] + 1    
output = []
for t in topic_area:
    output.append({
        'topic': t,
        'papers': topic_paper_weight[t],
        'people': topic_pc_weight[t],
        'area': topic_area[t]
    })
write_csv(output, headers, paper_topic_stats_csv)

# print area stats for PC email on screen
print('\nAcceptance statistics by topical area:')
print('--------------------------------------')
for a in areas:
    for mylist in area_stats:
        if mylist[0]==a:
            sub_share = round(100 * mylist[1] / n_submitted, 1)
            rate = round(100 * mylist[3] / mylist[1])
            acc_share = round(100 * mylist[3] / n_accepted, 1)
            print(a + ' -- sub-share ' + str(sub_share) + '% -- acc-rate ' + str(rate) + '% -- acc-share ' + str(acc_share) + '%')
