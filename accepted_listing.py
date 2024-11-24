# Extract list of accepted papers from EasyChair submission file
# Ulle Endriss, 4 July 2024 (cleaned up on 24 November 2024)

import csv

# path tho submission.csv downloaded from EasyChair
# headers: #, title, authors, submitted, last updated, form fields, keywords, decision, notified, reviews sent, abstract, deleted?
submission_csv = 'csv-in/submission.csv'

# headers: submission #, first name, last name, email, country, affiliation, Web page, person #, corresponding?
author_csv = 'csv-in/author.csv'

# path to output paper file
# headers: paper, title, authors
accepted_papers_csv = 'csv-out/accepted_papers_main_track.csv'

# path to output paper file
# headers: paper, author, email
accepted_authors_csv = 'csv-out/accepted_authors_main_track.csv'

# prefix for submission numbers (M for main track, D for demo track, etc.)
prefix = 'M'

# return list of dictionaries corresponding to rows in input csv file
def read_csv(path_to_input_csv):
    f = open(path_to_input_csv, encoding='utf-8-sig')
    reader = csv.DictReader(f, delimiter=',')
    return [row for row in reader]

# write given list/dictionary to given csv file, using given headers
def write_csv(output, headers, path_to_output_csv):
    f = open(path_to_output_csv, 'w', newline='')
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    for row in output:
        writer.writerow(row)
    print('> ' + str(len(output)) + ' rows written to ' +  path_to_output_csv)

# read submission and author files
submission_rows = read_csv(submission_csv)
author_rows = read_csv(author_csv)

# write listing of accepted papers
papers = []
paper_data = []
headers = ['paper', 'title', 'authors']
for row in submission_rows:
    if row['decision'] == 'accept':
        papers.append(row['#'])
        paper_data.append({
            'paper': prefix + row['#'],
            'title': row['title'],
            'authors': row['authors']
            })
write_csv(paper_data, headers, accepted_papers_csv)

# write listing of accepted authors
author_data = []
headers = ['paper', 'author', 'email']
for row in author_rows:
    if row['submission #'] in papers:
        author_data.append({
            'paper': prefix + row['submission #'],
            'author': row['first name'] + ' ' + row['last name'],
            'email': row['email']
            })
write_csv(author_data, headers, accepted_authors_csv)


