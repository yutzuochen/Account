# Unittest
import unittest
import execute
from execute import Account, Account_l2
import json

Yutzuo = execute.Account(5000, '2019-01-01')

f_Yutzuo = open('/Users/yutzuochen/Documents/myworks/account/database_Yutzuo/database.csv', 'r')
txt = f_Yutzuo.readlines()
f_Yutzuo.close()

class AccountTest(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(Yutzuo.sumDates(txt, "2019-01-01", "2019-01-01", 'sum'), -270.0)

    def test_sum_2(self):
        self.assertEqual(Yutzuo.sumDates(txt, "2019-01-06", "2019-01-06", 'sum'), 1950.0)

    def test_sum_mutipleDays(self):
        self.assertEqual(Yutzuo.sumDates(txt, "2019-01-01", "2019-01-05", 'sum'), -1050.0)
    
    #python3 execute.py expe 2019-01-01 2019-01-04
    def test_exp(self):
        self.assertEqual(Yutzuo.sumDates(txt, "2019-01-01", "2019-01-05", 'exp'), 1050.0)

    #python3 execute.py earn 2019-01-01 2019-01-06
    def test_earn(self):
        self.assertEqual(Yutzuo.sumDates(txt, "2019-01-01", "2019-01-06", 'earn'), 2000.0)

    # python3 execute.py currentCash
    def test_currentCash(self):
        self.assertEqual(Yutzuo.currentCash(txt), -2170.0)

    # python3 execute.py sumCategory 2019-01-01 diet
    # def sumCategory(self, txt, date, cg):
    def test_diet(self):
        self.assertEqual(Yutzuo.sumCategory(txt, "diet", "2019-01-01"), -220.0)
    def test_diet_2(self):
        self.assertEqual(Yutzuo.sumCategory(txt, "diet", "2019-01-04"), -220.0)

    # python3 execute.py sumCategory 2019-01-01 2019-01-03 diet
    def test_diet_multi(self):
        self.assertEqual(
            Yutzuo.sumDatesCategory(txt, "diet", "2019-01-01", "2019-01-04"
                                    ), -530)
    #def sumDatesCategory(self, txt, startDate, endDate, cg):
        

if __name__ == '__main__':
    unittest.main()
