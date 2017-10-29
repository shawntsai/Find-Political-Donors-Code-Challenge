import sys
import os
import datetime
from heapq import *

class Median:
    """Container used to calculate median of vals
    """
    def __init__(self):
        self.small = []
        self.large = []

    def add_num(self, num):
        heappush(self.small, - heappushpop(self.large, num))
        if len(self.large) < len(self.small):
            heappush(self.large, -heappop(self.small))

    def get_median(self):
        if len(self.large) > len(self.small):
            return float(self.large[0])
        return (self.large[0] - self.small[0]) / 2.0

    def __eq__(self, other):
        return self.small == other.small and self.large == other.large

def check_float(val):
    """ check if this val is float
    Args: val string
    Returns: true if val is float
    """
    try:
        float(val)
        return True
    except ValueError:
        return False

def parse_line(line):
    """ parse line
    Args: string
    Returns: recipient id, zip code, date of transaction, amout
    """
    words = line.split("|")
    other_id = words[15]
    if other_id: return None
    cmte_id = words[0]
    if (not cmte_id): return None
    if (not check_float(words[14])): return None

    zip_code = words[10]
    transaction_dt = words[13]
    transaction_amt = float(words[14])
    return cmte_id, zip_code, transaction_dt, transaction_amt


def handle_zip(chunk, doct):
    """ cacluate statistic for (user, zip) in this chunk
    Args:
         chunk: list of tuples id, zip, date, amout
         doct: map of (id, zip) -> list(median, count, sum)
    Returns: list of id | zip | median | count | sum 
    """
    result = list()
    for line in chunk:
        cmte_id, zip_code, transaction_dt, transaction_amt = line
        zip_code_s = zip_code[:5]
        if (len(zip_code_s) < 5): continue
        key = (cmte_id, zip_code_s)
        update_statistic(key, doct, transaction_amt)
        med = int(round(doct[key][0].get_median()))
        out = (cmte_id, zip_code_s, str(med), str(doct[key][1]), str(int(round(doct[key][2]))))
        result.append('|'.join(out))
    return result

def update_statistic(key, doct, transaction_amt):
    """ update transaction amout median
    Args: key: (id, date) or (id, zip) depend on map doct
          doct: map of (id, zip or date) -> list(median, count, sum)

    """
    if key in doct:
        temp = doct[key]
        temp[0].add_num(transaction_amt)
        temp[1] = temp[1] + 1
        temp[2] = temp[2] + transaction_amt
    else:
        med = Median()
        med.add_num(transaction_amt)
        val = list()
        val.append(med)
        val.append(1)
        val.append(transaction_amt)
        doct[key] = val

def validate_date(date):
    """validate date format for mmddyyyy
    Args: text string
    Returns: true if valid else false 
    """
    try:
        if datetime.datetime.strptime(date, '%m%d%Y').strftime('%m%d%Y') == date:
            return True
    except ValueError:
        return False


def handle_date(chunk, doct):
    """ calculate statistic in chunk, update doct
    Args: 
        chunk: list of tuples id, zip, date, amout
        doct: map of (id, date) -> list(median, count, sum)
    """
    result = list()
    for line in chunk:
        cmte_id, zip_code, transaction_dt, transaction_amt = line
        if (not validate_date(transaction_dt)): continue
        # group by recipient and zip 
        key = (cmte_id, transaction_dt)
        update_statistic(key, doct, transaction_amt)

def output_medianvals_by_date(doct):
    """ output result by sort id than date
    Arrgs: 
        doct: map of (id, date) -> list(median, count, sum)
    """
    keys = sorted(doct, key = lambda l:(l[0], l[1][4:] + l[1][0:4]))
    result = list()
    for key in keys:
        med = int(round(doct[key][0].get_median()))
        cmte_id = key[0]
        transaction_dt = key[1]
        out = (cmte_id, transaction_dt, str(med), str(doct[key][1]), str(int(round(doct[key][2]))))
        result.append('|'.join(out))
    return result

def main():
    # file_path = "../insight_testsuite/tests/test_1/input/itcont.txt"
    # out_file_path = "../output/medianvals_by_zip.txt"
    # out_file_path_by_date = "../output/medianvals_by_date.txt"
    file_path = sys.argv[1]
    out_file_path = sys.argv[2]
    out_file_path_by_date = sys.argv[3]
    doct = dict()
    try:
        os.remove(out_file_path)
        os.remove(out_file_path_by_date)
    except OSError:
        pass

    f = open(file_path, 'r')
    BUF_SIZE = 1024 * 1024 * 20
    lines = f.readlines(BUF_SIZE)
    doct_by_date = dict()

    while lines:
        chunk = list()
        for line in lines:
            temp = parse_line(line)
            if temp:
                chunk.append(temp)

        result = handle_zip(chunk, doct)
        handle_date(chunk, doct_by_date)

        lines = f.readlines(BUF_SIZE)
        with open(out_file_path, "a") as out:
            out.write('\n'.join(result))

    result_date = output_medianvals_by_date(doct_by_date)
    with open(out_file_path_by_date, "w") as out:
        out.write('\n'.join(result_date))
    # for ele in result_date: print(ele)
    
if __name__ == '__main__':
    main()
