import unittest
from find_political_donors import parse_line
from find_political_donors import update_statistic
from find_political_donors import handle_zip
from find_political_donors import handle_date
from find_political_donors import validate_date
from find_political_donors import Median


class TestFindPoliticalStatistic(unittest.TestCase):

    def test_no_cmte_id(self):
        line = '|N|TER|P|201701230300133512|15C|IND|PEREZ, JOHN A|LOS ANGELES|CA|90017|PRINCIPAL|DOUBLE NICKEL ADVISORS|01032017|40|H6CA34245|SA01251735122|1141239|||2012520171368850783'
        self.assertEqual(None, parse_line(line))

    def test_parse_line_contians_otherid(self):
        line = 'C00629618|N|TER|P|201701230300133512|15C|IND|PEREZ, JOHN A|LOS ANGELES|CA|90017|PRINCIPAL|DOUBLE NICKEL ADVISORS|01032017|40|H6CA34245|SA01251735122|1141239|||2012520171368850783'
        self.assertEqual(None, parse_line(line))
        
    def test_parse_line_amout_empty(self):
        line = 'C00177436|N|M2|P|201702039042410894|15|IND|DEEHAN, WILLIAM N|ALPHARETTA|GA|300047357|UNUM|SVP, SALES, CL|01312017|||PR2283873845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029337'
        self.assertEqual(None, parse_line(line))

    def test_valid_date(self):
        date = '11052015'
        self.assertTrue(validate_date(date))
        self.assertFalse(validate_date(''))
        self.assertFalse(validate_date('13022015'))
        self.assertFalse(validate_date('22000'))

    def test_transaction_amt_empty(self):
        line = 'C00177436|N|M2|P|201702039042410894|15|IND|DEEHAN, WILLIAM N|ALPHARETTA|GA|300047357|UNUM|SVP, SALES, CL|01312017|||PR2283873845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029337'
        self.assertEqual(None, parse_line(line))

    def test_median_one_val(self):
        med = Median()
        med.add_num(3)
        self.assertEqual(3, med.get_median())

    def test_median_more_than_one_val(self):
        med = Median()
        med.add_num(1)
        med.add_num(2)
        med.add_num(3)
        self.assertEqual(2, med.get_median())

    def test_median_double_vals(self):
        med = Median()
        med.add_num(1)
        med.add_num(2)
        self.assertEqual(1.5, med.get_median())

    def test_handle_zip_median_round(self):
        chunk = list()
        chunk.append(('a', '90007', '022017', 2.6))
        chunk.append(('a', '90007', '02142017', 2.6))
        doct = dict()
        result = list()
        result.append('a|90007|3|1|3')
        result.append('a|90007|3|2|5')
        self.assertListEqual(handle_zip(chunk, doct), result)

    def test_handle_date(self):
        chunk = list()
        chunk.append(('a', '90007', '02142017', 2.4))
        chunk.append(('a', '90007', '02142017', 2.6))

        doct = dict()
        result_doct = dict()
        med = Median()
        med.add_num(2.4)
        med.add_num(2.6)
        temp = list()
        temp.append(med)
        temp.append(2)
        temp.append(5.0)
        result_doct[('a', '02142017')] = temp
        handle_date(chunk, doct)
        self.assertDictEqual(result_doct, doct)


if __name__ == '__main__':
    unittest.main()
