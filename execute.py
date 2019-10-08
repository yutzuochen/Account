import json
import sys
import datetime
from datetime import timedelta, date
import unittest
import logging
import re


class Account:
    def __init__(self, cash, startDate):
        self.startDate = startDate
        self.cash = cash
        
    # order:python3 execute.py sum 2019-01-01  
    def countDate(self, txt, date, order):
        count = 0
        for i in txt:
            if i[:10] == date:
                num = re.search(r"(,\w*,)(-?\d*)(\(\w*\))" , i)
                money = float(num.group(2))
                if order == 'sum':
                    count += money
                elif order == 'exp':
                    if money < 0:
                        count -= money
                elif order == 'earn':
                    if money > 0:
                        count += money              
        return count

    def sumDates(self, txt, start, end, order):
        count = 0
        dt = start
        # date.fromisoformat(str): the usage of the function is{string -> class date}
        countday = (date.fromisoformat(end) - date.fromisoformat(start)).days
        # the date of 'start' needs to be smaller then date of 'end'
        if countday < 0:
            return
        while countday >= 0:
            count += self.countDate(txt, dt, order)
            dt = str(date.fromisoformat(dt) + timedelta(1))
            countday -= 1
        return count

    def currentCash(self, txt):
        return self.cash + self.sumDates(
            txt, self.startDate, "2019-03-23", "sum"
            )

    def sumCategory(self, txt, cg, date):
        count = 0
        for i in txt:
            if i[:10] == date: # we can improve it
                if re.search(
                    r"(\d+-\d+-\d+,)(\w*)(,.*,)", i
                        ).group(2) == cg: # category
                    num = re.search(r"(,\w*,)(-?\d*)(\(\w*\))" , i) # amount
                    count += int(num.group(2))              
        return count

    def sumDatesCategory(self, txt, cg, startDate, endDate):
        count = 0
        #ex: dt = date.fromisoformat(startDate) # transfer string to time module
        dt = startDate
        diff = (date.fromisoformat(endDate) - date.fromisoformat(dt)).days
        print("diff")
        while diff >= 0:
            count += self.sumCategory(txt, cg, dt) # ex: str(dt) == '2019-01-01'
            diff -= 1
            dt = str(date.fromisoformat(dt) + timedelta(1))
            print("count: ", count)
        return count
    def new_data(self, txt, cg, startDate, endDate):
        res = "Date,Category,Amount\n"
        for i in range(1, len(txt)):
            match = re.search(r"(\d+-\d+-\d+)(,)(\w+)(,)(-?\d+)(\(\w+\))", txt[i])
            #print("txt", date.fromisoformat(txt[i][:10]))
            #print("endDate", date.fromisoformat(endDate))
            if date.fromisoformat(txt[i][:10]) > date.fromisoformat(endDate):
                break
            if date.fromisoformat(txt[i][:10]) < date.fromisoformat(startDate):
                continue
        # '2019-01-01,beverage,-50(NTD),coffee\n'
            if match.group(3) == cg:
                amount = int(match.group(5))
                if amount >= 0:
                    res += match.group(1) + "," + "diet" + "," + match.group(5) +"\n"
                else:
                    res += match.group(1) + "," + "diet" + "," + str(-amount) + "\n"
        f2 = open("/Users/yutzuochen/Documents/myworks/account/data_for_graph.csv", "w")
        f2.write(res)
        f2.close()
    def graph(self, txt, cg, startDate, endDate):
        import numpy as np
        from numpy.random import randn
        import matplotlib.pyplot as plt
        from datetime import datetime
        import matplotlib
        import pandas as pd
        self.new_data(txt, cg, startDate, endDate)
        #f_g = open('/Users/yutzuochen/Documents/myworks/account/for_graph.numbers', 'r')
        #new_file = f_g.readlines()
        #f_g.close()
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        data = pd.read_csv(
            '/Users/yutzuochen/Documents/myworks/account/data_for_graph.csv', index_col=0,parse_dates=True
                            )
        dj = data['Amount']
        dj.plot(ax = ax, style = 'k-')
        ax.set_title(cg + " : " + startDate + " ~ " + endDate)
        plt.savefig('visualization')
        # python3 exe Yutzuo graph diet 2019-01-01 2019-01-30
        # def graph(self, txt, cg, startDate, endDate)


class Account_l2(Account):
    def __init__(self, cash, startDate):
        super().__init__(cash, startDate)
        self.stockValue = 0
        #self.futureMargin = 0
        #self.futreRevenue = 0
        self.asset = self.cash + self.stockValue
    
    # 2019-01-02,long_nake,5478,2000,156800(NTD)  
    # 2019-01-02,long_nake,8099,1000,18500(NTD)
    def holdStock(self, txtFin, endDate):
        # 1.long_nake  2.short  3.long_fin  
        # 4.close_nake  5.close_short  6.close_fin
        # e.g. {"5478":{long_nake:2000,long_fin:1000},
        #       "1101":{long_fin,3000},2251:{short,1000}
        logging.warning("begining")
        holdStock = {}  
        # def stockInf(self, txtFin, endDate): -> dict
        infDict =  self.stockInf(txtFin, endDate)
        for i in infDict:
            for j in infDict[i]:
                match = re.search(r"(\d+-\d+-\d+,)(\w+)(,)(\d+)(,)(\d+)(,)(\d+)(\(\w+\))", j)
                if match:
                    order = match.group(2)
                    sym = match.group(4)
                    share = int(match.group(6))
                    cost = match.group(8)
                    if share == 0:
                        continue
                    if i in holdStock:
                        if order in holdStock[i]:
                            holdStock[i][order] += share
                        else:
                            holdStock[i][order] = share
                    else:
                        holdStock[i] = {order:share}

        #print(holdStock)
        self.printStock(holdStock)
        return holdStock
        
    def printStock(self, holdStock):
        print(" -Sym-", " "* 8, "-Share-", " "* 13,"-order- ")
        print("-" * 47)
        for i in holdStock:
            for j in holdStock[i]:
                print("  "+i, " :", " " * 6, holdStock[i][j]," "*5, "->", " "*5, j)
 
    # in the function "relize", we have to know how much 
    # stock we holded on the start date
    # holdCost will return a dictionary looks like:
    # {5478:[[2019-01-01,long_nake,1000,10000],
    # [2019-01-02,long_nake,5478,2000,156800(NTD) ]}
    def stockInf(self, txtFin, endDate):
        dt = self.startDate
        hold = {}
        pair = {"close_nake":"long_nake","close_short":"short","close_fin":"long_fin"}
        while date.fromisoformat(dt) <= date.fromisoformat(endDate):
            for i in txtFin:
                match = re.search(r"(\d+-\d+-\d+,)(\w+)(,)(\d+)(,)(\d+)(,)(\d+)(\(\w+\))", i)
                if match:
                    if date.fromisoformat(i[:10]) > date.fromisoformat(dt):
                        break # wrong
                    if i[:10] == dt:
                        match = re.search(r"(\d+-\d+-\d+,)(\w+)(,)(\d+)(,)(\d+)(,)(\d+)(\(\w+\))", i)
                        if match:
                            order = match.group(2)
                            sym = match.group(4)
                            share = int(match.group(6))
                            cost = match.group(8) # improve:input price
                            if order in ["long_nake", "long_fin", "short"]:
                                if sym in hold:
                                    hold[sym].append(i)
                                else:
                                    hold[sym] = [i]
                            else:
                                if not sym in hold:
                                    raise ValueError("close action is wrong")
                                else:
                                    for j in range(len(hold[sym])):
                                        # record before the date                              
                                        rec = re.search(r"(\d+-\d+-\d+,)(\w+)(,)(\d+)(,)(\d+)(,)(\d+)(\(\w+\))", hold[sym][j])
                                        order_rec = rec.group(2)
                                        sym_rec = rec.group(4)
                                        share_rec = int(rec.group(6))
                                        cost_rec = rec.group(8)
                                        if pair[order] == order_rec:
                                            diff = share - share_rec
                                            if diff > 0:
                                                share -= share_rec
                                                # share = "0"
                                                hold[sym][j] = rec.group(1)+rec.group(2)+rec.group(3)+rec.group(4)+rec.group(5)+"0"+rec.group(7)+rec.group(8)+rec.group(9)
                                            elif diff == 0:
                                                hold[sym][j] = rec.group(1)+rec.group(2)+rec.group(3)+rec.group(4)+rec.group(5)+"0"+rec.group(7)+rec.group(8)+rec.group(9)
                                                break
                                            
                                            elif diff < 0:
                                                hold[sym][j] = rec.group(1)+rec.group(2)+rec.group(3)+rec.group(4)+rec.group(5)+ str(-diff) +rec.group(7)+rec.group(8)+rec.group(9)
                                                break
            dt = str(date.fromisoformat(dt) + timedelta(1))
        return hold

    def tax_stock(self, price, taxRate): # 0.3%
        return price * taxRate
        
    def transaction_fee(self, price, feeRate): # 0.1425%
        return price * feeRate

    def interest_fin(self, interstingRate, cost_rec, date_by):
        return cost_rec * interstingRate * date_by // 365

    def relize(self, txtFin, start, end):
        # e.g. {5478:{long_nake:2000,long_fin:1000},
        #       1101:{long_fin,3000},2251:{short,1000}
        #print(Harvey.relize(txtFin, sys.argv[3], sys.argv[4]))
        # from datetime import timedelta, date #don't know
        if date.fromisoformat(start) > date.fromisoformat(end):
            raise ValueError("the date you order is wrong!")
        dt = start
        dt_before = str(date.fromisoformat(start) - timedelta(1))
        holdStock = self.stockInf(txtFin, dt_before)
        relize = 0
        profit = 0
        txtIndex = 1
        transaction_fee_rate = 0.001425
        interestRate_fin_rate = 0.065
        tax_stock_rate = 0.003
        while txtIndex <= len(txtFin)-1:
            if date.fromisoformat(txtFin[txtIndex][:10]) > date.fromisoformat(end):
                return profit
            if date.fromisoformat(dt) > date.fromisoformat(txtFin[txtIndex][:10]):
                txtIndex += 1
                continue
            if date.fromisoformat(dt) < date.fromisoformat(txtFin[txtIndex][:10]):
                dt = str(date.fromisoformat(dt) + timedelta(1))
                continue
            if date.fromisoformat(dt) == date.fromisoformat(txtFin[txtIndex][:10]):
                match = re.search(r"(\d+-\d+-\d+)(,)(\w+)(,)(\d+)(,)(\d+)(,)(\d+)(\(\w+\))", txtFin[txtIndex])
                date_txt = match.group(1)
                order = match.group(3)
                sym = match.group(5)
                share = int(match.group(7))
                price = int(match.group(9))
                pair = {"close_nake":"long_nake","close_short":"short","close_fin":"long_fin"} 
                if order in ["long_nake", "long_fin", "short"]:
                    if sym in holdStock:
                        holdStock[sym].append(txtFin[txtIndex])
                    else:
                        holdStock[sym] = [txtFin[txtIndex]]
                else:
                    if order in ["close_nake", "close_fin"]:
                        if not sym in holdStock:
                            raise ValueError("close action is wrong")
                        else:
                            cost = self.tax_stock(price, 0.003) + self.transaction_fee(price, transaction_fee_rate)
                            for j in range(len(holdStock[sym])):
                                # record before the date                              
                                rec = re.search(r"(\d+-\d+-\d+)(,)(\w+)(,)(\d+)(,)(\d+)(,)(\d+)(\(\w+\))", holdStock[sym][j])
                                date_rec = rec.group(1)
                                order_rec = rec.group(3)
                                sym_rec = rec.group(5)
                                share_rec = int(rec.group(7))
                                cost_rec = int(rec.group(9)) # buy price
                                if pair[order] == order_rec:
                                    diff = share - share_rec  # "share" is the number of stock you closed
                                    if diff > 0:
                                        share -= share_rec
                                        # share = "0"
                                        holdStock[sym][j] = rec.group(1)+rec.group(2)+rec.group(3)+rec.group(4)+rec.group(5)+rec.group(6)+"0"+rec.group(8)+"0"+rec.group(10)
                                        # cost_nake == (selling price) * (tax + selling fee) + 
                                        #              (cost_rec)*(buy fee)
                                        cost += cost_rec + self.transaction_fee(cost_rec, transaction_fee_rate)
                                        if order == "close_fin":
                                            date_by = (date.fromisoformat(date_txt) - date.fromisoformat(date_rec)).days
                                            # def interst(self, interstingRate, cost_rec, date_by):
                                            cost += self.interest_fin(interestRate_fin_rate, cost_rec, date_by)
                                           
                                    elif diff == 0:
                                        holdStock[sym][j] = rec.group(1)+rec.group(2)+rec.group(3)+rec.group(4)+rec.group(5)+rec.group(6)+ "0" +rec.group(8)+"0"+rec.group(10)
                                        cost += cost_rec + self.transaction_fee(transaction_fee_rate, cost_rec)
                                        if order == "cost_fin":
                                            interstingRate = 0.0065
                                            date_by = (date.fromisoformat(date_txt) - date.fromisoformat(date_rec)).days
                                            # def interst(self, interstingRate, cost_rec, date_by):
                                            cost += self.interest_fin(interestRate_fin_rate, cost_rec, date_by)
                                            
                                        break
                                 
                                    elif diff < 0:
                                        cost_portion = (cost_rec * share) // share_rec
                                        #print("selling cost: ", cost)
                                        #print("buy fee: ", self.fee(cost_portion))
                                        #print("cost_portion: ",cost_portion)
                                        if order == "close_fin":
                                            
                                            cost +=  self.interest_fin(interestRate_fin_rate, cost_portion, date_by)
                                        cost += cost_portion + self.transaction_fee(cost_portion, transaction_fee_rate)
                                        holdStock[sym][j] = rec.group(1)+rec.group(2)+rec.group(3)+rec.group(4)+rec.group(5)+rec.group(6)+ str(-diff) +rec.group(8)+ str(cost_rec - cost_portion) +rec.group(10)                                        
                                        break
                            profit += (price - cost)

                    elif order == "close_fin":
                        pass # not yet, just test another part
                
            txtIndex += 1
            if txtFin[txtIndex][:10] !=  dt: # maybe the user operate many time in a day
                dt = str(date.fromisoformat(dt) + timedelta(1))
        return profit
        # possible problems:
        # (1) buy same cor. in defernt price. When we close some stick,
        #     How will we recognize the profit?
        #       A: FIFO
        #{
        # 5478:[long_nake:1000:24000,long_nake:2000:49000]
        # 1101:[.......]
        # }

        # (2) We need to pay interest if we use financial way to get stock.
        # (3) pay fee and tax

    def inputMoney(self, txtFin, targetDate):
        #dt = Harvey.startDate
        inputMoney = 0
        fin_rate = 0.4
        holdStock = {}
        txtIndex = 1
        while txtIndex <= len(txtFin)-1:
            if date.fromisoformat(txtFin[txtIndex][:10]) > date.fromisoformat(targetDate):
                break
            match = re.search(r"(\d+-\d+-\d+)(,)(\w+)(,)(\d+)(,)(\d+)(,)(\d+)(\(\w+\))", txtFin[txtIndex])
            order = match.group(3)
            sym = match.group(5)
            share = int(match.group(7))
            price = int(match.group(9))
            pair = {"close_nake":"long_nake","close_short":"short","close_fin":"long_fin"} 
            if order in ["long_nake", "long_fin", "short"]:
                if sym in holdStock:
                    holdStock[sym].append(txtFin[txtIndex])
                else:
                    holdStock[sym] = [txtFin[txtIndex]]
            else:
                if order in ["close_nake", "close_fin"]:
                    if not sym in holdStock:
                        raise ValueError("close action is wrong")
                    else:
                        for j in range(len(holdStock[sym])):
                            # record before the date                              
                            rec = re.search(r"(\d+-\d+-\d+)(,)(\w+)(,)(\d+)(,)(\d+)(,)(\d+)(\(\w+\))", holdStock[sym][j])
                            date_rec = rec.group(1)
                            order_rec = rec.group(3)
                            sym_rec = rec.group(5)
                            share_rec = int(rec.group(7))
                            cost_rec = int(rec.group(9)) # buy price
                            if pair[order] == order_rec:
                                diff = share - share_rec  # "share" is the number of stock you closed
                                if diff > 0:
                                    share -= share_rec
                                    # share = "0"
                                    holdStock[sym][j] = rec.group(1)+rec.group(2)+rec.group(3)+rec.group(4)+rec.group(5)+rec.group(6)+"0"+rec.group(8)+"0"+rec.group(10)
                                elif diff == 0:
                                    holdStock[sym][j] = rec.group(1)+rec.group(2)+rec.group(3)+rec.group(4)+rec.group(5)+rec.group(6)+"0"+rec.group(8)+"0"+rec.group(10)
                                    break
                                
                                elif diff < 0:
                                    cost_portion = (cost_rec * share) // share_rec
                                    holdStock[sym][j] = rec.group(1)+rec.group(2)+rec.group(3)+rec.group(4)+rec.group(5)+rec.group(6)+ str(-diff) +rec.group(8)+ str(cost_rec - cost_portion) +rec.group(10)
                                    break              
            txtIndex += 1
        
        for i in holdStock:
            for j in holdStock[i]:
                m = re.search(r"(\d+-\d+-\d+)(,)(\w+)(,)(\d+)(,)(\d+)(,)(\d+)(\(\w+\))", j)
                order = m.group(3)
                price = int(m.group(9))
                #print("price: ", price)
                if order == "long_nake":
                    inputMoney += price
                elif order == "long_fin":
                    inputMoney += price * fin_rate
        return inputMoney
        # not yet, close 的不份有出入 10/01
    
    # initial the account 'Yutzuo'
def run_Harvey():
    Harvey = Account_l2(2000, '2019-01-01')
    f_Harvey_fin = open('/Users/yutzuochen/Documents/myworks/account/database_Harvey/database_fin.csv', 'r')
    txtFin = f_Harvey_fin.readlines()
    f_Harvey = open('/Users/yutzuochen/Documents/myworks/account/database_Harvey/database.csv', 'r')
    txt = f_Harvey.readlines()
    try:
        if sys.argv[2] in ['sum', 'exp', 'earn']:
            # database:2019-01-01,beverage,-50(NTD),coffee
            # order:python3 execute.py Harvey sum 2019-01-01 
            try:
                if sys.argv[2] == 'sum':
                    print(Harvey.sumDates(txt, sys.argv[3], sys.argv[4], 'sum'))
                elif sys.argv[2] == 'exp':
                    print(Harvey.sumDates(txt, sys.argv[3], sys.argv[4], 'exp'))
                elif sys.argv[2] == 'earn':
                    print(Harvey.sumDates(txt, sys.argv[3], sys.argv[4], 'earn'))

            except: # only 1 day
                print('the', sys.argv[3], 'you', sys.argv[2], 'is:')
                print(Harvey.countDate(txt, sys.argv[3], sys.argv[2]))
                
        elif sys.argv[2] == 'currentCash':
            print(Harvey.currentCash(txt))
            
        elif sys.argv[2] == 'sumCategory':
            logging.warning('ok_1')
            try: # at least 2 days
                logging.warning("ok_4")
                print(Harvey.sumDatesCategory(txt, sys.argv[3], sys.argv[4], sys.argv[5]))
            except: # 1day
                logging.warning("ok_5")
                print(Harvey.sumCategory(txt, sys.argv[3], sys.argv[4]))
        elif sys.argv[2] == "holdStock":
            logging.warning("hold stock up")
            Harvey.holdStock(txtFin, sys.argv[3])
            logging.warning("hold stock down")

        # python3 execute.py Harvey relize 2019-01-01 2019-01-03
        elif sys.argv[2] == "relize":
            print("profit:  ", Harvey.relize(txtFin, sys.argv[3], sys.argv[4]))
        
        # def inputMoney(self, txtFin, date)
        elif sys.argv[2] == "inputMoney":
            print(Harvey.inputMoney(txtFin, sys.argv[3]))

        elif sys.argv[2] == "stockInf": # only for test
            print(Harvey.stockInf(txtFin , sys.argv[3]))

    except IndexError:
        print('index error!')
    except ValueError:
        print('value error!')
    f_Harvey.close()
    f_Harvey_fin.close()

def run_Yutzuo():
    Yutzuo = Account(5000, '2019-01-01')
    f_Yu = open(
        '/Users/yutzuochen/Documents/myworks/account/database_Yutzuo/database.csv', 'r'
        )
    txt = f_Yu.readlines()
    try:
        if sys.argv[2] in ['sum', 'exp', 'earn']:
            # database:2019-01-01,beverage,-50(NTD),coffee
            # order:python3 execute.py sum 2019-01-01 
            try:
                if sys.argv[2] == 'sum':
                    print(Yutzuo.sumDates(txt, sys.argv[3], sys.argv[4], 'sum'))
                elif sys.argv[2] == 'exp':
                    print(Yutzuo.sumDates(txt, sys.argv[3], sys.argv[4], 'exp'))
                elif sys.argv[2] == 'earn':
                    print(Yutzuo.sumDates(txt, sys.argv[3], sys.argv[4], 'earn'))

            except: # only 1 day
                print('the', sys.argv[3], 'you', sys.argv[2], 'is:')
                print(Yutzuo.countDate(txt, sys.argv[3], sys.argv[2]))
                
        elif sys.argv[2] == 'currentCash':
            print(Yutzuo.currentCash(txt))
            
        elif sys.argv[2] == 'sumCategory':
            logging.warning('ok_1')
            try: # at least 2 days
                logging.warning("ok_4")
                print(Yutzuo.sumDatesCategory(txt, sys.argv[3], sys.argv[4], sys.argv[5]))
            except: # 1day
                logging.warning("ok_5")
                print(Yutzuo.sumCategory(txt, sys.argv[3], sys.argv[4]))
        # python3 execute.py Harvey graph diet 2019-01-01 2019-01-03 
        elif sys.argv[2] == 'graph':
            Yutzuo.graph(txt, sys.argv[3], sys.argv[4], sys.argv[5])
        # python3 exe Yutzuo graph diet 2019-01-01 2019-01-30
        # def graph(self, txt, cg, startDate, endDate)
    except IndexError:
        print('index error!')
    f_Yu.close() # not yet

# Execute the code
logging.basicConfig(filename = 'Logger')
try:
    if sys.argv[1] == "Harvey":
        run_Harvey()
    
    elif sys.argv[1] == "Yutzuo":
        run_Yutzuo()
except IndexError: # We would'n test the file without this line.
    pass

# mac_order:
# [diary]
# python3 execute.py Harvey sum 2019-01-01
# python3 execute.py Harvey sum 2019-01-01 2019-01-04
# python3 execute.py Harvey exp 2019-01-01 2019-01-04
# python3 execute.py Harvey earn 2019-01-01 2019-01-04
# python3 execute.py Harvey currentCash
# python3 execute.py Harvey sumCategory diet 2019-01-01
# python3 execute.py Harvey sumCategory diet 2019-01-01 2019-01-03
# python3 execute.py Yutzuo graph diet 2019-01-01 2019-01-30
# [stock]
# python3 execute.py Harvey holdStock 2019-01-05
# python3 execute.py Harvey holdStock market value
# python3 execute.py Harvey relize 2019-01-01 2019-01-03
# [not yet]
# python3 execute.py Harvey inputMoney 2019-01-02
# python3 execute.py Harvey unrelize 2019-01-01 2019-01-03
# python3 execute.py Harvey TotalMarketValue

# Date,Op,Symbol,Amount,total
# 2019-01-02,long_nake,8099,1000,18500(NTD)
# 2019-01-04,long_nake,5478,1000,77800(NTD)




