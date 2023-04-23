import datetime
import hashlib
import os
import pickle
import sys
'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Authors:        MinhHien Luong
    File Name:      blockchain.py
    Description:    Chain of custody stored in binary blocks 
                    with the design as a blockchain.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

class Case:
    def __init__(self, case_id):
        self.case_id = case_id
        self.items = []

    def find_case(this_case):
        for block in blockchain.get_chain():
            if isinstance(block.data, Case):
                case = block.data
                for item in case.get_items():
                    if (item['item_id'] == this_case):
                        return case

    def add(self, item_ids):
        print(f"Case: {case_id}")
        time = datetime.datetime.now().isoformat()
        for item in item_ids:
            self.items.append({
            'item_id': item,
            'status': 'CHECKEDIN',
            'time': time,})
            print(f"Added item: {item}")
            print(f"Status: CHECKEDIN")
            print(f"Time of action: {time}")

            for block in blockchain.get_chain():
                if isinstance(block.data, Case):
                    case = block.data
                    for item in case.get_items():
                        if (item['item_id'] == item):
                            print("VERIFY ISSUE: duplicate block added")

    def checkout(self, input_item_id):
        print(f"Case: {case_id}")
        for block in blockchain.get_chain():
            if isinstance(block.data, Case):
                case = block.data
                for item in case.get_items():
                    if (item['item_id'] == input_item_id):
                        if (item['status'] == "CHECKEDIN"):
                            item['status'] = "CHECKEDOUT"
                            print(f"Checked out item: {item['item_id']}")
                            print(f"Status: {item['status']}")
                            print(f"Time of action: {datetime.datetime.now().isoformat()}")
                        else:
                            print("Error: Cannot check out a checked out item. Must check it in first.")

    def checkin(self, input_item_id):
        print(f"Case: {case_id}")
        for block in blockchain.get_chain():
            if isinstance(block.data, Case):
                case = block.data
                for item in case.get_items():
                    if (item['item_id'] == input_item_id):
                        if (item['status'] == "CHECKEDOUT"):
                            item['status'] = "CHECKEDIN"
                            print(f"Checked out item: {item['item_id']}")
                            print(f"Status: {item['status']}")
                            print(f"Time of action: {datetime.datetime.now().isoformat()}")
    
    def remove(self, input_item_id, reason, owner_info):
        print(f"Case: {case_id}")
        for block in blockchain.get_chain():
            if isinstance(block.data, Case):
                case = block.data
                for item in case.get_items():
                    if (item['item_id'] == input_item_id):
                        if (item['status'] == "CHECKEDIN"):
                            item['status'] = reason
                            print(f"Removed item: {item['item_id']}")
                            print(f"Status: {item['status']}")
                            if owner_info != "null":
                                print(f"Owner info: {owner_info}")
                                if reason == "RELEASED":
                                    print("VERIFY ISSUE: released but no owner given")
                            print(f"Time of action: {datetime.datetime.now().isoformat()}")
                        else:
                            print("Error: Cannot remove out a checked out item. Must check it in first.")

    def get_items(self):
        return self.items

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

#runProgram class pushed by Leon Kwong
"""
Notes: Functions still need to be coded in to do what it needs to do.
"""
class runProgram:
    #More added code below
    def add():
        print("add function")

    def checkout():
        print("checkout function")

    def checkin():
        print("checkin function")

    def log():
        print("log function")

    def remove():
        print("remove function")

    def init():
        print("init function")

    def verify():
        print("verify function")

    def run():
        #Check the second entry to ask what operation needs to be conducted based on command
        #Create switch statement here to read the commands in specificed format
        match sys.argv[2]:

            case "add":
                itemIDlist = []
                caseID = sys.argv[4]
                itemID1 = sys.argv[6]
                #For loop store every caseID after first one into a list.
                for item in range(8, len(sys.argv), 2):
                    itemIDlist.append(sys.argv[item].strip("[]"))
                print(itemIDlist)

            case "checkout":
                itemID = sys.argv[3]

            case "checkin":
                itemID = sys.argv[3]

            case "log":
                if sys.argv[3].strip("[]") == "-r":
                    runProgram.remove()

                #do something call method to do reverse #If -r is not an option
                else:
                    numEnt = sys.argv[4].strip("[]")
                    caseID = sys.argv[6].strip("[]")
                    itemID = sys.argv[8].strip("[]")

            case "remove":
                itemID = sys.argv[4]
                reason = sys.argv[6]
                owner = sys.argv[8].strip("[]")

            case "init":
                runProgram.init()

            case "verify":
                runProgram.verify()


# Example usage
if __name__ == '__main__':
    blockchain = Blockchain()

    # Add a case with a few items to the chain
    case_id = '65cc391d-6568-4dcc-a3f1-86a2f04140f3'
    case = Case(case_id)
    case.add_item(987654321)
    case.add_item(123456789)
    blockchain.add_block(case)

    # Print out the blockchain
    for block in blockchain.get_chain():
        print(f"Timestamp: {block.timestamp}")
        if isinstance(block.data, Case):
            case = block.data
            print(f"Case ID: {case.case_id}")
            for item in case.get_items():
                print(f"Item ID: {item['item_id']}")
                print(f"Status: {item['status']}")
                print(f"Time: {item['time']}")
        else:
            print(f"Data: {block.data}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Hash: {block.hash}")
        print("-----------------------------")
        

