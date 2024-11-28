# EasyChair Scripts

This repository includes a number of simple Python scripts a PC chair of a large conference might use to analyse and manipulate data downloaded from [EasyChair](https://easychair.org/). I wrote them when I was PC chair of [ECAI-2024](https://www.ecai2024.eu/), the 27th European Conference of Artificial Intelligence (a conference with over 2,300 paper submissions). They are provided here in the hope that others might find them useful.

For more ambitious development projects to build tools for conference management, you might instead want to take the [EasyChair-Extra](https://github.com/COMSOC-Community/easychair-extra) package developed by Simon Rey as a starting point.

## Sample Data

The `csv-in` folder includes sample data of the kind you can download from EasyChair (if you are the PC chair and if you have the right kind of license). This includes lists of PC members, lists of authors, lists of topics that can be used to classify submissions, lists of submissions, lists of bids by PC members for submissions to review, lists of reviews, and the review assignment.

The `csv-in` folder contains two further files:

+ `emergency_reviewer.csv`: It can be useful to reserve some PC members as _emergency reviewers_, not assigning them any papers at the start. This is a list of such emergency reviewers.

+ `review_transfer_request.csv`: For ECAI-2024 satellite workshops had the option to allow the authors of papers rejected from the main conference to have their reviews transferred to a specific workshop, so the organisers of that workshop could decide on acceptance based on those reviews rather than having to solicit their own reviews. This is a list of such review transfer requests.
