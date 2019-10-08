# Unittest
import unittest
import execute
from execute import Account, Account_l2
import json

Harvey = execute.Account_l2(5000, '2019-01-01')

f_Harvey = open('/Users/yutzuochen/Documents/myworks/account/test_database/database.csv', 'r')
txt = f_Harvey.readlines()
f_Harvey.close()

f_fin_Harvey = open('/Users/yutzuochen/Documents/myworks/account/test_database/database_fin.csv', 'r')
txtFin = f_fin_Harvey.readlines()
f_fin_Harvey.close()

f_fin_2_Harvey = open('/Users/yutzuochen/Documents/myworks/account/test_database/database_fin_2.csv', 'r')
txtFin_2 = f_fin_2_Harvey.readlines()
f_fin_2_Harvey.close()

f_fin_3_Harvey = open('/Users/yutzuochen/Documents/myworks/account/test_database/database_fin_2.csv', 'r')
txtFin_3 = f_fin_3_Harvey.readlines()
f_fin_3_Harvey.close()

class AccountTest(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(Harvey.sumDates(txt, "2019-01-01", "2019-01-01", 'sum'), -270.0)

    def test_sum_2(self):
        self.assertEqual(Harvey.sumDates(txt, "2019-01-06", "2019-01-06", 'sum'), 1950.0)

    def test_sum_mutipleDays(self):
        self.assertEqual(Harvey.sumDates(txt, "2019-01-01", "2019-01-05", 'sum'), -1050.0)
    
    #python3 execute.py expe 2019-01-01 2019-01-04
    def test_exp(self):
        self.assertEqual(Harvey.sumDates(txt, "2019-01-01", "2019-01-05", 'exp'), 1050.0)

    #python3 execute.py earn 2019-01-01 2019-01-06
    def test_earn(self):
        self.assertEqual(Harvey.sumDates(txt, "2019-01-01", "2019-01-06", 'earn'), 2000.0)

    # python3 execute.py currentCash
    def test_currentCash(self):
        self.assertEqual(Harvey.currentCash(txt), -2170.0)

    # python3 execute.py sumCategory 2019-01-01 diet
    # def sumCategory(self, txt, date, cg):
    def test_diet(self):
        self.assertEqual(Harvey.sumCategory(txt, "diet", "2019-01-01"), -220.0)
    def test_diet_2(self):
        self.assertEqual(Harvey.sumCategory(txt, "diet", "2019-01-04"), -220.0)

    # python3 execute.py sumCategory 2019-01-01 2019-01-03 diet
    def test_diet_multi(self):
        self.assertEqual(
            Harvey.sumDatesCategory(txt, "diet", "2019-01-01", "2019-01-04"
                                    ), -530)

#-------------------fin account atart----------------------

    def test_holdStock(self):
        self.assertEqual(Harvey.holdStock(txtFin, "2019-01-05"), {'1101': {'long_nake': 4000, 'long_fin': 3000}})

    def test_holdStock_fin(self):
        self.assertEqual(Harvey.holdStock(txtFin_2, "2019-01-05"), {'1101': {'long_fin': 7000}})
        
    def test_holdStock_fin_2(self):
        self.assertEqual(Harvey.holdStock(txtFin_2, "2019-02-07"), {'1101': {'long_fin': 3000}})

    def test_inputMoney_fin(self):
        self.assertEqual(Harvey.inputMoney(txtFin, "2019-01-04"), 267900.0)

    def test_inputMoney_fin_2(self):
        self.assertEqual(Harvey.inputMoney(txtFin, "2019-02-06"), 178400.0)
    #inputMoney(self, txtFin, targetDate):
    #python3 execute.py Harvey inputMoney 2019-01-04

# python3 execute.py Harvey holdStock 2019-01-05
# python3 execute.py Harvey holdStock market value
# python3 execute.py Harvey relize 2019-01-01 2019-01-03
# python3 execute.py Harvey inputMoney 2019-01-02
# python3 execute.py Harvey TotalMarketValue



if __name__ == '__main__':
    unittest.main()
