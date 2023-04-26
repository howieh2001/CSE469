#!/usr/bin/env python3
import datetime
import hashlib
import os
import pickle
import argparse
'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Authors:        MinhHien Luong
    File Name:      blockchain.py
    Description:    Chain of custody stored in binary blocks 
                    with the design as a blockchain.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

# case's data
class Case:
    def __init__(self, case_id):
        self.case_id = case_id
        self.items = []


    def add(self, i):
        a = False
        print(f"Case: {case_id}")
        time = datetime.datetime.now().isoformat()
        for block in bl.get_chain():
            if isinstance(block.data, Case):
                case = block.data
                for item in case.get_items():
                    if (item['item_id'] == i):
                        print("VERIFY ISSUE: duplicate block added")
                        a = True
                    if a:
                        break
        self.items.append({
        'item_id': i,
        'status': 'CHECKEDIN',
        'time': time,})
        print(f"Added item: {i}")
        print(f"Status: CHECKEDIN")
        print(f"Time of action: {time}")

    def get_items(self):
        return self.items

# Hashed as a blockchain system
class ChainOfCustody:
    def __init__(self, data, previous_hash):
        self.timestamp = datetime.datetime.now()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

# each block's properties set up
class Blockchain:
    def __init__(self):
        self.blocks_file = 'blocks.bin'
        if os.path.exists(self.blocks_file):
            with open(self.blocks_file, 'rb') as f:
                self.chain = pickle.load(f)
        else:
            self.chain = [self.create_genesis_block()]
            with open(self.blocks_file, 'wb') as f:
                pickle.dump(self.chain, f)

    def create_genesis_block(self):
        return ChainOfCustody("Genesis Block", "0")

    def add_block(self, new_data):
        previous_hash = self.chain[-1].hash
        new_block = ChainOfCustody(new_data, previous_hash)
        self.chain.append(new_block)
        with open(self.blocks_file, 'wb') as f:
            pickle.dump(self.chain, f)

    def get_chain(self):
        return self.chain

    def get_cases(self):
        cases = {}
        for block in self.chain:
            if isinstance(block.data, Case):
                cases[block.data.case_id] = block.data
        return cases

    def get_case(self, case_id):
        for block in self.chain:
            if isinstance(block.data, Case) and block.data.case_id == case_id:
                return block.data
        return None
    
    def log(self, item_id=None, reverse=False, num_entries=None):
        blocks = self.chain
        if item_id:
            blocks=[block for block in self.chain 
                    if isinstance(block.data, Case) and any(item['item_id'] == item_id for item in block.data_items)]
        if reverse:
            blocks = reversed(blocks)
        if num_entries is not None:
            blocks = list(blocks)[:num_entries]
        for block in blocks:
            data = block.data
            if isinstance(data, Case):
                for item in data.items:
                    if item_id is None or item['item_id'] == item_id:
                        print(f"Case: {data.case_id}\nItem: {item['item_id']}\nAction: {item['status']}\nTime: {item['time']}\n")

# commands parser
def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    # create the parser for the "init" command
    parser_init = subparsers.add_parser('init', help='initialize the blockchain')
    #parser_init.add_argument('filename', help='the filename of the blockchain')

    # create the parser for the "add" command
    parser_add = subparsers.add_parser('add', help='add a new block to the blockchain')
    parser_add.add_argument('-c', '--case-id', required=True, help='the ID of the case to add the evidence to')
    parser_add.add_argument('-i', '--item-id', required=True, help='the ID of the evidence item being added')

    # create the parser for the "log" command
    parser_log = subparsers.add_parser('log', help='display the blockchain entries')
    parser_log.add_argument('-i', '--item-id', help='the ID of the evidence item being displayed')
    parser_log.add_argument('-r', '--reverse', action='store_true', help='reverse the order of the block entries')
    parser_log.add_argument('-n', '--num-entries', type=int, help='number of block entries to show')

    return parser

# main driver
if __name__ == '__main__':
    
    # initialization and local objs
    bl = Blockchain()

    # parser
    parser = get_parser()
    args = parser.parse_args()

    # 'init' command
    if args.command == "init":
        if os.path.exists('blocks.bin'):
            print('Blockchain file found with INITIAL block.')
        else:
            bl.create_genesis_block()
            print('Blockchain file not found. Created INITIAL block.')

    # 'add' command
    if args.command == 'add':
        if args.case_id and args.item_id:
            case = bl.get_case(args.case_id)
            if case:
                for item_id in args.item_id:
                    case.add(item_id)
                    

    # 'log' command
    if args.command == 'log':
        cases = bl.get_cases()
        item_id = args.item_id
        reverse = args.reverse
        num_entries = args.num_entries
        if item_id:
            for case_id in cases:
                case = cases[case_id]
                items = case.get_items()
                for item in items:
                    if item['item_id'] == item_id:
                        print(f"Case: {case.case_id}\nItem: {item_id}\nAction: {item['status']}\nTime: {item['time']}\n")
                        break
                else:
                    continue
                break
        else:
            blocks = bl.get_chain()
            if reverse:
                blocks.reverse()
            if num_entries:
                blocks = blocks[-num_entries:]
            for block in blocks:
                if isinstance(block.data, Case):
                    print(f"Case: {block.data.case_id}\n")
                else:
                    print(f"Item: {block.data}\n")

    # example use
