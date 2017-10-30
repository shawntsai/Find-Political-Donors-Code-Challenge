# Find Political Donors Code Challenge
This is solution to the challenge for insight data engineer

We are asked to do two tasks
* Calculate sum of contributions, number transactions and median donation for recipient from the contributor's zipcode[Task1]
* Calculate sum of contributions, number transactions and median donation received by recipient on that date[Task2].


## Approach
* Parse each line and filter out any invalid record
* Find median with data structure max heap and min heap, n is the length of amount of donations, the complexitiy in get median and insert value per transaction is O(log(n))
* Using two HashMap data structure to store cumulated sum of contribution, and median donation,  number of transactions of particular tuple (recipient id, zip code) and tuple (recipient id, date)
* For scalibitity, I stream in the data by 20 mega per chunk, execute per chunk and append output to the result medianvals_by_date.txt. It is capable to handle big amount of data. 
* When stream in the data, I also update the nessesary infomation for task2, and write to medianvals_by_date at the end of program
* I test my program for 3.8 GB data and it takes about 13 mins to complete on a single machine.


## Requirements and dependencies
python 2.7
using module heapq, sys, os, datetime, unnittest


## Run Instructions

In FindPoliticalDonorsCodeChallenge folder, run this command will generate two following output file under output folder 
output/medianvals_by_date.txt
output/medianvals_by_zip.txt

```
./run.sh
```

Run 10 unit tests

```
python src/test_find_political_donors.py

```

I have also added test under ./insight_testsuite/tests/test_2
You could run this two tests by this command in insight_testsuite folder

```
./run_tests.sh

```

## Author
Yu Hsiang Tsai
