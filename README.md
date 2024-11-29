# EasyChair Scripts

This repository includes a number of simple Python scripts a PC chair of a large conference might use to analyse and manipulate data downloaded from [EasyChair](https://easychair.org/). I wrote them when I was PC chair of [ECAI-2024](https://www.ecai2024.eu/), the 27th European Conference of Artificial Intelligence (a conference with over 2,300 paper submissions). These scripts are provided here in the hope that others might find them useful.

All scripts have been tested with Python 3.12.1 on a Mac.

For more ambitious development projects to build tools for conference management, you might instead want to take the [EasyChair-Extra](https://github.com/COMSOC-Community/easychair-extra) package developed by Simon Rey as a starting point.

## Various Listings

There are two script for generating various listings, which you might need for the conference website or the production of the proceedings:

+ `committee_listings.py`: Separate lists of regular PC members, SPC members, and area chairs. Also shows list of inactive committee members, who you might want to remove from your committee.

+ `accepted_listing.py`: List of accepted papers and contact details of authors of accepted papers.

## Anonymised Submission List for Dual Submission Check

Submitting the same paper, or a very similar paper, to two conferences with overlapping reviewing periods is unethical. Large AI conferences routinely exchange anonymised lists of submissions to detect such cases of _dual submission_. The script `anonymous_submissions.py` can be used to generate such a list for your conference.

## Detecting Placeholder Abstracts

For large conferences, there usually is an abstract deadline a few days before the final submission deadline. Authors usually are required to submit a proper abstract by the first deadline: small updates later on are permissible, but the abstract should give a clear idea of what kind of paper they plan to submit. Submitting a "placeholder abstract" is not allowed.

The script `short_abstracts.py` will order the submissions by abstract length, meaning that a typical placeholder abstract will show up near the top of the list and thus can be easily detected.

## Identifying (Overly) Prolific Authors

It is good practice to set a limit for the number of papers any one author is allowed to submit.

And should you be short of reviewers, you might want to require (some) authors to serve as reviewers. In this case, it makes sense to start by looking through the list of authors with a particularly large number of submissions as possible candidates.

The script `frequent_authors.py` generates a list of authors ordered by number of submissions, annotated with information on whether the author in question is also a PC member.

## Bidding Statistics

To get a good review assignment, it is a good idea to ask PC members to bid for papers they would like to review.

The script `bid_size.py` will display basic statistics on the sizes of bids submitted by PC members. This can be useful while monitoring the bidding process. This data can also be helpful in identifying inactive PC members (who you might want to remove from the committee) and especially flexible PC members (who might be good candidates for the _emergency reviewer pool_).

## Analysis of the Review Assignment

The script `assignment_analysis.py` will report some basic indicators to help you assess the quality of the current review assignment:

+ Proportion of the assignment based on positive bids. It can be useful to report this information to PC members. (My own anecdotal evidence suggests that PC members often have a more pessimistic subjective view on the quality of review assignments than what the objective data would suggest.)

+ List of "unhappy" PC members (with more than one paper assigned to them that they did not bid for). Typically but not always this will be individuals who only bid for a very small number of papers.

+ List of "problematic" papers (with more than one PC member assigned who did not bid for the paper). Such papers should receive some extra attention from you.

The script will also split the assignment file into three separate assignments (PC, SPC, AC), which could be edited separately and then uploaded into EasyChair. This can be useful in case you want to run your own assignment algorithm for some of the three assignment problems.

## Analysis of Incoming Reviews

You will need to monitor the reviewing process as reviews come in and try to spot problems early. Doing so directly on the EasyChair platform can be difficult for a large conference.

The script `review_analysis.py` can help with some basic monitoring activities:

+ Displaying the number of reviews still missing. (Note that this count might not be entirely accurate once a few extra reviews have been submitted, by individuals who were not required to submit a review for a given paper.)

+ Generating a list of PC members with missing reviews, ordered by number of missing reviews. This allows you to tailor your reminder emails to the gravity of the problem caused by a given PC member. (You should definitely avoid sending redundant reminders to those PC members who delivered everything on time.)

+ Generating a list of reviews ordered by length. The very shortest reviews almost always are unprofessional reviews, and in some cases you will have to intervene.

+ Generating a list of all confidential comments submitted by PC members. While you won't be able to read all reviews, you should at least try to skim through all confidential comments, as this is where the most serious problems will get signalled and as this might be a way in which PC members try to reach you. It's a good idea to search the file for terms such as "plagiarism", "ethics", or "unprofessional".

+ Displaying simple statistics on review scores. Probably too many reviewers will use borderline scores and you can use this data to estimate the severity of the problem. Towards the end of the reviewing period, this data can be useful when formulating advice for PC members under which circumstances a given paper might be a good candidate for acceptance.

## Simple Collusion Detection

For major AI conferences there have been increasing reports of _collusion_ between reviewers and authors: people writing overly favourable reviews for one another, sometimes in exchange for money. This is very difficult to detect, particularly when the collusion ring extends over multiple conferences.

The script `collusion_detection.py` performs two basic checks:

+ Check for _two-cycles_, i.e., cases of pairs of people who have been assigned to review each others' papers. Any two-cycles found should be inspected but are by no means a proof of wrong-doing (two-cycles can naturally arise for papers in a relatively narrow research area).

+ Check for submissions where a majority of authors and reviewers are all from the same country. Any such case should be inspected but again by no means constitutes a proof of wrong-doing.

## Submission and Acceptance Statistics

The script `paper_stats.py` will produce basic statistics about the submissions (number of submissions, number of submissions by country, number of submissions per area, number of submissions and number of PC members per submission topic, acceptance statistics by area).

As an example, here are the acceptance statistics for ECAI-2024:

```
Fairness, Ethics, and Trust -- sub-share 9.9% -- acc-rate 24% -- acc-share 10.2%
Computer Vision -- sub-share 14.2% -- acc-rate 21% -- acc-share 12.6%
Constraints and Satisfiability -- sub-share 1.6% -- acc-rate 29% -- acc-share 2.0%
Data Mining -- sub-share 4.7% -- acc-rate 19% -- acc-share 3.9%
Humans and AI -- sub-share 2.8% -- acc-rate 20% -- acc-share 2.4%
Knowledge Representation and Reasoning -- sub-share 4.2% -- acc-rate 26% -- acc-share 4.7%
Machine Learning -- sub-share 29.1% -- acc-rate 23% -- acc-share 29.0%
Multiagent Systems -- sub-share 6.5% -- acc-rate 29% -- acc-share 8.0%
Natural Language Processing -- sub-share 11.7% -- acc-rate 23% -- acc-share 11.4%
Planning and Search -- sub-share 4.8% -- acc-rate 31% -- acc-share 6.4%
Robotics -- sub-share 1.5% -- acc-rate 25% -- acc-share 1.6%
Uncertainty in AI -- sub-share 2.8% -- acc-rate 23% -- acc-share 2.8%
Multidisciplinary Topics -- sub-share 6.1% -- acc-rate 20% -- acc-share 5.2%
```

Here the submission share of an area is the percentage of submissions that belong to that area, and the acceptance share is the corresponding percentage of accepted submissions. 

## Review Transfer to Satellite Workshops

For ECAI-2024, our satellite workshops had the option to allow the authors of papers rejected from the main conference to have their reviews transferred to a specific workshop, so the organisers of that workshop could decide on acceptance based on those reviews rather than having to solicit their own reviews.

The script `review_transfer.py` will take a list of review transfer requests by authors and produce one list of anonymised reviews per workshop, which can then be sent to the workshop organisers.

## Sample Data

The `csv-in` folder includes sample data of the kind you can download from EasyChair (if you are the PC chair and if you have the right license). This includes lists of PC members, lists of authors, lists of topics that can be used to classify submissions, lists of submissions, lists of bids by PC members for submissions to review, lists of reviews, and the review assignment.

The EasyChair file format is fairly intuitive and has been stable over several years (here we assume the format of 2024). The main difficulty of working with EasyChair data is that every PC member has both a "person id" and a "member id", which can be confusing.

Besides the types of files you can download from EasyChair, the `csv-in` folder contains two further files:

+ `emergency_reviewer.csv`: It can be useful to reserve some PC members as _emergency reviewers_, not assigning them any papers at the start. This is a list of such emergency reviewers.

+ `review_transfer_request.csv`:  This is a list of review transfer requests by authors of rejected papers who wish their paper to be considered by a specific workshop. For ECAI-2024, we used a simple Google form to invite authors to submit such requests.

The `csv-out` file includes all the output files generated by the scripts provided when applied to the data in `csv-in`.
