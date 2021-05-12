from collections import deque
from Tree import Tree


class Miseri:

    def __init__(self):
        self.line = ""
        self.wait_list = deque()
        self.output = ""
        self.variables = dict()
    
    def insert(self, inp):
        self.wait_list = self.wait_list + deque(inp)
    
    def find(self):
        return self.wait_list.popleft()

    def read(self, inp):
        self.line = deque(inp.rstrip().split("->"))
        self.parse()

    def space_check(self, line):
        cnt = 0
        for nxt in line:
            if nxt != "":
                break
            else:
                cnt += 1
        return cnt

    def check(self, give):
        if give in "==<=>=!=":
            return give
        elif give.isupper() and not (give[0] in "\"'" and give[-1] in "\"'"):
            return self.sub_func(give)
        elif not give.isdigit() and not (give[0] in "\"'" and give[-1] in "\"'"):
            return self.variables[give]
        elif give.isdigit():
            return int(give)
        else:
            return give[1:len(give)-1]

    def unpack(self, give):
        length = len(give)
        if give[0] == "(" and give[-1] == ")":
            # param = give[1:length-1].replace(" ", "").split(",")
            param = give[1:length - 1].split(",")
            for i in range(len(param)):
                param[i] = self.check(param[i])
        else:
            param = self.check(give)
        return param

    def sub_func(self, func):
        if func == "ENDL":
            return "\n"
        elif func == "READ":
            return self.find().rstrip()
        elif func == "LIST":
            return []

    def loopily(self):
        take = self.find().rstrip()
        line = []
        while take.rstrip() != "<-FIN":
            if take.startswith("LOOP"):
                val = self.loopily()
                line = line + val * self.unpack(take.split("->")[-1])
            elif take.startswith("IF"):
                val = self.iffity(take.split("->")[-1])
                if val is not None:
                    line = line + val
            else:
                line.append(take)
            take = self.find().rstrip()
        if len(line) > 200:
            raise TimeoutError
        return line

    def iffity(self, args):
        param = self.unpack(args)
        take = self.find().rstrip()
        line = []
        while take != "<-FIN":
            if take.startswith("IF"):
                val = self.iffity(take.split("->")[-1])
                if val is not None:
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
            return line
        else:
            return None

    def parse(self):
        command = self.line.popleft()
        if command.islower() and not(command[0] in "\"'" and command[-1] in "\"'"):
            action = self.unpack(self.line.popleft())
            return self.variables[command][action]
        elif command == "SET":
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
            action = self.unpack(self.line.popleft())
            take = self.find().rstrip()
            line = []
            while take != "<-FIN":
                if take.startswith("LOOP"):
                    val = self.loopily()
                    line = line + val * self.unpack(take.split("->")[-1])
                elif take.startswith("IF"):
                    val = self.iffity(take.split("->")[-1])
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
            parameters = self.unpack(self.line.popleft())
            return Tree(parameters)
        elif command == "DFS":
            action = self.line.popleft().split("<-", 1)
            self.variables[action[0]].DFS(int(action[-1]), -1, 0)
            return self.variables[action[0]].distances
        elif command == "ADD":
            parameters = self.unpack(self.line.popleft())
            if isinstance(parameters[0], int):
                ans = 0
            else:
                ans = ""
            for nxt in parameters:
                ans += nxt
            return ans
        elif command == "SUB":
            parameters = self.unpack(self.line.popleft())
            return parameters[1] - parameters[0]
        elif command == "MULT":
            parameters = self.unpack(self.line.popleft())
            val = 1
            for nxt in parameters:
                val *= nxt
            return val
        elif command == "DIV":
            parameters = self.unpack(self.line.popleft())
            return parameters[0] / parameters[1]
        elif command == "INT":
            # only takes in one arg
            parameters = self.unpack(self.line.popleft())
            return int(parameters)
        elif command == "STR":
            # only takes in one arg
            parameters = self.unpack(self.line.popleft())
            return str(parameters)
        elif command == "TYPE":
            parameters = self.unpack(self.line.popleft())
            self.output += str(type(parameters))+"\n"
            return type(parameters)
        elif command == "APPEND":
            action = self.line.popleft().split("<-", 1)
            parameters = self.unpack(action[-1])
            self.variables[action[0]] += parameters
            return self.variables[action[0]]
        elif command == "POP" or command == "REMOVE":
            action = self.line.popleft().split("<-", 1)
            # only takes in one
            parameters = self.unpack(action[-1])
            if command == "POP":
                self.variables[action[0]].pop(parameters)
            else:
                self.variables[action[0]].remove(parameters)
            return self.variables[action[0]]