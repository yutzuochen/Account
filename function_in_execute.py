class Account:

    def __init__(self, cash, startDate):
        self.startDate = startDate
        self.cash = cash

    def countDate(self, txt, date, order):  -> int          
        return count

    def sumDates(self, txt, start, end, order): -> int
        return count

    def currentCash(self, txt): -> int        

    def sumCategory(self, txt, cg, date): -> int            
        return count

    def sumDatesCategory(self, txt, cg, startDate, endDate): -> int
        
    def new_data(self, txt, cg, startDate, endDate): -> None
        Eliminate some category data from original file except specific category data.
        Then put the result into another file.
    
    def graph(self, txt, cg, startDate, endDate): -> None
        chose one category data and printout the graph 

class Account_l2(Account):

    def __init__(self, cash, startDate):
        super().__init__(cash, startDate)
        self.stockValue = 0

    def holdStock(self, txtFin, endDate): -> dict
        dict ->  {'1101': {'long_nake': 4000, 'long_fin': 3000}}
        call:
            [stockInf,    printStock]
    def printStock(self, holdStock): -> None
        printout the result of the function, holdStock, withthe specific format.
 
    def stockInf(self, txtFin, endDate): -> dict
        terminal order:
            python3 execute.py Harvey stockInf 2019-02-04
        finally we get:            
            {'1101': ['2019-01-02,long_nake,1101,2000,156800(NTD)  \n', '2019-01-02,long_nake,1101,1000,18500(NTD)\n', '2019-01-03,long_fin,1101,0,18500(NTD)', '2019-01-03,long_fin,1101,1000,18500(NTD)', '2019-01-04,long_nake,1101,1000,77800(NTD)\n']}
    Note: 
        I think the holdStock could call this function to simplize its code.

    def tax_stock(self, price, taxRate): -> float
    def transaction_fee(self, price, feeRate): -> float
    def interest_fin(self, interstingRate, cost_rec, date_by): -> float
        
    def relize(self, txtFin, start, end): -> float
        call:
            [tax_stock(), transaction_fee(), interest_fin()]

    def inputMoney(self, txtFin, targetDate): -> float
