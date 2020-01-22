""" Module Containing Data Structures """


class Stack:
    """ Stack data structure to manage buys and sells """

    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def size(self):
        return len(self.items)


class Trade:
    """ Trade Object """

    def __init__(self, time, symb, side, price, quant):
        self.time = eval(time)
        self.symb = symb
        self.side = side
        self.price = eval(price)
        self.quant = eval(quant)

    def buy(self, quantity):
        self.quant += quantity

    def sell(self, quantity):
        self.quant -= quantity


class Pair:
    """ Pair Object """

    def __init__(self, open_trade, close_trade):
        self.otime = open_trade.time
        self.ctime = close_trade.time
        self.symb = open_trade.symb
        self.quant = min(open_trade.quant, close_trade.quant)
        self.cside = close_trade.side
        self.oside = open_trade.side
        self.oprice = open_trade.price
        self.cprice = close_trade.price
        self.pnl = self.quant*(self.cprice-self.oprice)

    def __repr__(self):
        return '{}, {}, {}, {}, {}, {}, {}, {}, {}'.format(
            self.otime, self.ctime, self.symb,
            self.quant, self.pnl, self.oside,
            self.cside, self.oprice, self.cprice
        )
