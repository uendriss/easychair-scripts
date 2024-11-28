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

The script `short_abstracts.py` will order the submissions by abstract length, meaning that a typical placeholder abstract will show up near the top of the list and this can be easily detected.

## Identifying (Overly) Prolific Authors

It is good practice to set a limit for the number of papers any one author is allowed to submit.

And should you be short of reviewers, you might want to require (some) authors to serve as reviewers. In this case, it makes sense to start by looking through the list of authors with a particularly large number of submissions as possible candidates.

The script `frequent_authors.py` generates a list of authors ordered by number of submissions, annotated with information on whether the author in question is also a PC member.

## Bidding Statistics

## Analysis of the Review Assignment

## Analysis of Incoming Reviews

## Simple Collusion Detection

For major AI conferences there have been increasing reports of _collusion_ between reviewers and authors: people writing overly favourable reviews for one another, sometimes in exchange for money. This is very difficult to detect, particularly when the collusion ring extends over multiple conferences.

The script `collusion_detection.py` performs two basic checks:

+ Check for _two-cycles_, i.e., cases of pairs of people who have been assigned to review each others' papers. Any two-cycles found should be inspected but are by no means a proof of wrong-doing (two-cycles can naturally arise for papers in a relatively narrow research area).

+ Check for submissions where a majority of authors and reviewers are all from the same country. Any such case should be inspected but again by no means constitutes a proof of wrong-doing.

## Submission and Acceptance Statistics

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
