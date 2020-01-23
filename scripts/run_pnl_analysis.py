""" Script for Running PnL Analysis - Ali Oskooei """
import os
from collections import deque
import argparse
from functools import wraps
from time import time
from pnl_analysis.data_structs import *
from pnl_analysis.utils import *


@timer
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_dir")
    args = parser.parse_args()
    file_dir = args.file_dir

    trades_gen = gen_clean_data(file_dir)
    _ = trades_gen.next()

    trades_queue = deque()
    pairs_queue = deque()

    buy_dict = dict()
    sell_dict = dict()
    total_pnl = 0

    for trade in trades_gen:
        current_trade = Trade(*trade)
        if current_trade.side == 'B':
            if current_trade.symb in buy_dict:
                buy_dict[current_trade.symb].push(current_trade)
            else:
                buy_dict[current_trade.symb] = Stack()
                buy_dict[current_trade.symb].push(current_trade)

        else:
            if current_trade.symb in sell_dict:
                sell_dict[current_trade.symb].push(current_trade)
            else:
                sell_dict[current_trade.symb] = Stack()
                sell_dict[current_trade.symb].push(current_trade)

            if current_trade.symb in buy_dict and buy_dict[current_trade.symb].size() >= 1:
                buy_side = buy_dict[current_trade.symb].peek()
                if current_trade.quant < buy_side.quant:
                    current_pair = Pair(buy_side, current_trade)
                    pairs_queue.append(current_pair)
                    print(current_pair)
                    total_pnl += current_pair.pnl
                    buy_side.sell(current_pair.quant)
                    sell_dict[current_trade.symb].pop()
                elif current_trade.quant == buy_side.quant:
                    current_pair = Pair(buy_side, current_trade)
                    pairs_queue.append(current_pair)
                    print(current_pair)
                    total_pnl += current_pair.pnl
                    buy_side.sell(current_trade.quant)
                    buy_dict[current_trade.symb].pop()
                    sell_dict[current_trade.symb].pop()
                else:
                    while current_trade.quant > buy_side.quant and buy_dict[current_trade.symb].size() > 1:
                        current_pair = Pair(buy_side, current_trade)
                        pairs_queue.append(current_pair)
                        print(current_pair)
                        total_pnl += current_pair.pnl
                        buy_side.sell(current_pair.quant)
                        current_trade.sell(current_pair.quant)
                        if buy_side.quant == 0:
                            buy_dict[buy_side.symb].pop()
                            buy_side = buy_dict[current_trade.symb].peek()

                    if current_trade.quant > buy_dict[current_trade.symb].peek().quant:
                        current_pair = Pair(buy_side, current_trade)
                        pairs_queue.append(current_pair)
                        print(current_pair)
                        total_pnl += current_pair.pnl
                        buy_dict[current_trade.symb].pop()
                        current_trade.sell(current_pair.quant)
                        current_trade.side = 'B'
                        flipped_trade = current_trade
                        buy_dict[flipped_trade.symb].push(flipped_trade)
                    else:
                        if current_trade.quant < buy_side.quant:
                            current_pair = Pair(buy_side, current_trade)
                            pairs_queue.append(current_pair)
                            print(current_pair)
                            total_pnl += current_pair.pnl
                            buy_side.sell(current_trade.quant)
                            sell_dict[current_trade.symb].pop()
                        elif current_trade.quant == buy_side.quant:
                            current_pair = Pair(buy_side, current_trade)
                            pairs_queue.append(current_pair)
                            print(current_pair)
                            total_pnl += current_pair.pnl
                            buy_side.sell(current_trade.quant)
                            buy_dict[current_trade.symb].pop()
                            sell_dict[current_trade.symb].pop()
    print total_pnl


if __name__ == '__main__':
    print('OPEN_TIME, CLOSE_TIME, SYMBOL, QUANTITY, PNL, OPEN_SIDE, CLOSE_SIDE, OPEN_PRICE, CLOSE_PRICE')
    main()
