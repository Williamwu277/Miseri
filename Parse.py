import random
import bisect
from collections import deque
from Tree import Tree

# class to interpret the commands
class Miseri:

    '''
    line -> current command to be executed
    wait_list -> pending commands
    output -> execution output
    out_image -> image output
    variables -> user variables
    '''
    def __init__(self):
        self.line = ""
        self.wait_list = deque()
        self.output = ""
        self.out_image = None
        self.variables = dict()

    # add more commands
    def insert(self, inp):
        self.wait_list = self.wait_list + deque(inp)

    # return a command
    def find(self):
        return self.wait_list.popleft()

    # execute one command
    def read(self, inp):
        self.line = deque(inp.rstrip().split("->"))
        self.parse()

    # find the index of the first space
    def space_check(self, line):
        cnt = 0
        for nxt in line:
            if nxt != "":
                break
            else:
                cnt += 1
        return cnt

    # properly convert input to correct type
    def check(self, give):
        if give in "==<=>=!=": # operation
            return give
        elif give.isupper() and not (give[0] in "\"'" and give[-1] in "\"'"): # commands
            return self.sub_func(give)
        elif not give.isdigit() and not (give[0] in "\"'" and give[-1] in "\"'"): # variable names
            return self.variables[give]
        elif give.isdigit(): # integers
            return int(give)
        else: # no matches
            return give[1:len(give)-1] 

    # unpack the values from (x,y,z,...) type statements
    def unpack(self, give):
        length = len(give)
        if give[0] == "(" and give[-1] == ")": # multi-variable
            param = give[1:length - 1].split(",")
            for i in range(len(param)):
                param[i] = self.check(param[i])
        else: # single variable
            param = self.check(give)
        return param

    # execute subfunctions
    def sub_func(self, func):
        if func == "ENDL":
            return "\n"
        elif func == "READ":
            return self.find().rstrip()
        elif func == "LIST":
            return []

    # execute a loop
    def execute_loop(self):
        take = self.find().rstrip() 
        line = []
        while take.rstrip() != "<-FIN":
            if take.startswith("LOOP"): # run a loop within this loop
                val = self.execute_loop()
                line = line + val * self.unpack(take.split("->")[-1])
            elif take.startswith("IF"): # run an if within this loop
                val = self.execute_if(take.split("->")[-1])
                if val is not None:
                    line = line + val
            else: # execute values
                line.append(take)
            take = self.find().rstrip()
        if len(line) > 200: # make sure loop doesn't end too long
            raise TimeoutError
        return line

    # execute an if statement
    def execute_if(self, args):
        param = self.unpack(args)
        take = self.find().rstrip()
        line = []
        while take != "<-FIN": # execute each line until if statement is done
            if take.startswith("IF"):
                val = self.execute_if(take.split("->")[-1])
                if val is not None:
                    line = line + val
            elif take.startswith("LOOP"):
                val = self.execute_loop()
                line = line + val * self.unpack(take.split("->")[-1])
            else:
                line.append(take)
            take = self.find().rstrip()
        if eval(str(param[0]) + " " + str(param[1]) + " " + str(param[2])): # if true, return output
            if len(line) > 200:
                raise TimeoutError
            return line
        else:
            return None

    # parse the command line
    def parse(self):
        
        command = self.line.popleft()

        if command.islower() and not(command[0] in "\"'" and command[-1] in "\"'"):
            action = self.unpack(self.line.popleft())
            return self.variables[command][action]
            
        elif command == "SET":
            # create a variable
            action = self.line.popleft().split("<-", 1)
            if action[0].isdigit():
                var = self.line.popleft().split("<-", 1)
                ret = self.variables[var[0]][int(action[0])] = self.check(var[-1])
            elif len(self.line) == 0:
                ret = self.variables[action[0]] = self.check(action[-1])
            else:
                self.line.appendleft(action[-1])
                ret = self.variables[action[0]] = self.parse()
            return ret
            
        elif command == "LOOP":
            # execute a loop
            # loops within loops will be executed by the recursive function
            action = self.unpack(self.line.popleft())
            take = self.find().rstrip()
            line = []
            while take != "<-FIN":
                if take.startswith("LOOP"):
                    val = self.execute_loop()
                    line = line + val * self.unpack(take.split("->")[-1])
                elif take.startswith("IF"):
                    val = self.execute_if(take.split("->")[-1])
                    if val is not None:
                        line = line + val
                else:
                    line.append(take)
                take = self.find().rstrip()
            line *= action
            if len(line) > 200:
                raise TimeoutError
            for nxt in line:
                self.read(nxt)
                
        elif command == "IF":
            # execute an if statement
            # if's within if's will be executed by the if recursive function
            param = self.unpack(self.line.popleft())
            take = self.find().rstrip()
            line = []
            while take != "<-FIN":
                if take.startswith("IF"):
                    val = self.iffity(take.split("->")[-1])
                    line = line + val
                elif take.startswith("LOOP"):
                    val = self.loopily()
                    line = line + val * self.unpack(take.split("->")[-1])
                else:
                    line.append(take)
                take = self.find().rstrip()
            if eval(str(param[0]) + " " + str(param[1]) + " " + str(param[2])):
                if len(line) > 200:
                    raise TimeoutError
                for nxt in line:
                    self.read(nxt)
                    
        elif command == "OUT":
            # output something
            if len(self.line) == 1:
                parameters = self.unpack(self.line.popleft())
                out = parameters
            else:
                out = self.parse()
            if isinstance(out, list):
                self.output += " ".join(map(str, out))+"\n"
            else:
                self.output += out.__str__()+"\n"
            return out
            
        elif command == "TREE":
            # create a tree
            parameters = self.unpack(self.line.popleft())
            return Tree(parameters)
            
        elif command == "DFS":
            # execute depth first search
            action = self.line.popleft().split("<-", 1)
            self.variables[action[0]].DFS(int(action[-1]), -1, 0)
            return self.variables[action[0]].distances
            
        elif command == "ADD":
            # addition
            parameters = self.unpack(self.line.popleft())
            if isinstance(parameters[0], int):
                ans = 0
            else:
                ans = ""
            for nxt in parameters:
                ans += nxt
            return ans
            
        elif command == "SUB":
            #subtraction
            parameters = self.unpack(self.line.popleft())
            return parameters[1] - parameters[0]
            
        elif command == "MULT":
            #multiplication
            parameters = self.unpack(self.line.popleft())
            val = 1
            for nxt in parameters:
                val *= nxt
            return val
            
        elif command == "DIV":
            #division
            parameters = self.unpack(self.line.popleft())
            return parameters[0] / parameters[1]
            
        elif command == "INT":
            # convert to int
            # only takes in one arg
            parameters = self.unpack(self.line.popleft())
            return int(parameters)
            
        elif command == "STR":
            # convert to string
            # only takes in one arg
            parameters = self.unpack(self.line.popleft())
            return str(parameters)
            
        elif command == "TYPE":
            # find the type
            parameters = self.unpack(self.line.popleft())
            self.output += str(type(parameters))+"\n"
            return type(parameters)
            
        elif command == "APPEND":
            # append to a list
            action = self.line.popleft().split("<-", 1)
            parameters = self.unpack(action[-1])
            self.variables[action[0]] += parameters
            return self.variables[action[0]]
            
        elif command == "POP" or command == "REMOVE":
            # pop or remove items from a list
            action = self.line.popleft().split("<-", 1)
            # only takes in one
            parameters = self.unpack(action[-1])
            if command == "POP":
                self.variables[action[0]].pop(parameters)
            else:
                self.variables[action[0]].remove(parameters)
            return self.variables[action[0]]
            
        elif command == "RAND":
            # generates random numbers with specifications
            action = self.unpack(self.line.popleft())
            #length, low, high, type
            if action[0] > 200:
                raise TimeoutError
                
            random_arr = []
            if action[3] == "OUTLIER": # create outlier values
                random_arr.append(action[2])
                for _ in range(action[0]-1):
                    random_arr.append(random.randint(action[1], min(action[1], action[2]//action[0])))
                random.shuffle(random_arr)
                
            elif action[3] == "DISTINCT": # make sure all distinct
                if action[2]-action[1]+1 < action[0]: # not enough values for all distinct
                    raise SyntaxError
                if action[2] - action[1] + 1 < 2000: # if many distinct values to choose from
                    random_arr = list(range(action[1], action[2]+1))
                    random.shuffle(random_arr)
                    random_arr = random_arr[:action[0]]
                else: # not many disinct values to choose from
                    taken = set()
                    for _ in range(action[0]):
                        take = random.randint(action[1], action[2]+1)
                        while take in taken:
                            take = random.randint(action[1], action[2]+1)
                        taken.add(take)
                        random_arr.append(take)
                        
            elif action[3] == "RAND":
                # vanilla random
                for _ in range(action[0]):
                    random_arr.append(random.randint(action[1], action[2]))
                    
            else:
                raise SyntaxError
                
            if len(random_arr) == 1:
                # length one returns an integer
                return random_arr[0]
            else:
                return random_arr
                
        elif command == "SORT":
            # sorts a list
            param = self.unpack(self.line.popleft())
            return sorted(param)
            
        elif command == "MIN":
            # finds minimum
            param = self.unpack(self.line.popleft())
            return min(param)
            
        elif command == "MAX":
            # finds maximum
            param = self.unpack(self.line.popleft())
            return max(param)
            
        elif command == "BSL" or command == "BSU":
            # binary search "bisect left" or "bisect right"
            inp = self.line.popleft().split("<-", 1)
            param = self.unpack(inp[0])
            search = self.unpack(inp[1])
            pre = param[0]-1
            for i in range(len(param)):
                if param[i] < pre:
                    raise SyntaxError
                pre = param[i]
            if command == "BSL":
                return bisect.bisect_left(param, search)
            else:
                return bisect.bisect_right(param, search)
        
        elif command == "DRAW":
            # draw and output the tree
            param = self.unpack(self.line.popleft())
            if self.out_image != None:
                raise SyntaxError
            if param.image == None:
                param.DRAW()
            param.image.save("graph.png")
            self.out_image = "graph.png"
            
        else:
            return SyntaxError
        
