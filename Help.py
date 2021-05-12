help_list = {
    "$help": 
    """
    ```\n
    Miseri's list of commands:\n\n
    $help - print out a list of commands\n
    $miseri-$ - use the miseri interpreter\n
    Allows commands such as: SET, LOOP, IF, OUT, TREE, DFS, ADD, SUB, MULT, DIV, INT, STR, TYPE, APPEND, POP and REMOVE\n
    There are also sub-commands: ENDL, READ and LIST\n
    $syntax <insert_command> - can be used to find out about the syntax of a specific command\n
    NOTE: The syntax for the interpreter is extremely strict. Things such as spaces can create an error\n
    ```
    """,
    "SET":
    """
    ```\n
    SET->insert_variable<-value\n
    SET sets a variable to the value given. The value can be either a command, a string, a number, or another variable. Variable names must be lowercase and not a number.\n
    E.g. SET->n<-"hello world"\n
    ```
    """,
    "LOOP":
    """
    ```\n
    LOOP->value\ncommands\n<-FIN\n
    LOOP runs the commands inbetween itself and FIN a number of times the value specifies. The value can be a variable or a number. Nested loops/ifs are also possible although there are no indents so the inner loops/ifs end before the outer loops/ifs.\n
    E.g.\n
    LOOP->6\n
    OUT->"hello world"\n
    <-FIN\n
    ```
    """,
    "IF":
    """
    ```\n
    IF->(value_1,comparator from: "<,>,==,<=,>=",value_2)\ncommands\n<-FIN\n
    The IF compares value_1 with value_2 with the comparator given. Since syntax is strict, spaces are not allowed. Value_1 and value_2 can be strings, numbers or variables, meaning that commands are not allowed. If the statement is true, the commands are run. Nested loop/ifs are also possible although there are no indents so the inner loops/ifs end before the outer loops/ifs.\n
    E.g.\n
    IF->(1,<,5)\n
    OUT->"hello world"\n
    <-FIN\n
    ```
    """,
    "OUT":
    """
    ```\n
    OUT->value\n
    OUT outputs the value that is given. This value can be a command, a number, a string or a variable. It should be noted that spaces are not tolerated.\n
    E.g. OUT->"hello world"\n
    ```
    """,
    "TREE":
    """
    ```\n
    TREE->(num, weight, type, chance)\n
    This generates a tree using the parameters. Num is the number of nodes. Weight makes sure that edges are generated with a weight from 1 to weight. The type can be "RANDOM", "LINE", or "STAR". Chance denotes the chance of an edge being connected randomly. This chance is 1/chance and should be noted that this value does not affect "RANDOM" trees. When printed, returns the number of nodes, follwed by n-1 lines each containing one edge.\n
    E.g. SET->n<-TREE->(7,1,"RANDOM",5)\n
    ```
    """,
    "DFS":
    """
    ```\n
    DFS->tree<-start\n
    Run depth first search from the start node to every single other node in the tree. This returns a list of distances 1 indexed.\n
    E.g. DFS->n<-1\n
    ```
    """,
    "ADD":
    """
    ```\n
    ADD->(val1, val2, ... , val_X)\n
    Returns the value of val1 + val2 + ... + val_X. This applies for both strings and integers.\n
    E.g. ADD->(1,2,3,4,5)\n
    ```
    """,
    "SUB":
    """
    ```\n
    SUB->(val1, val2)\n
    Returns the value of val1 - val2. Not applicable for strings.\n
    E.g. SUB->(7,1)\n
    ```
    """,
    "MULT":
    """
    ```\n
    MULT->(val1, val2, ... , val_X)\n
    Returns the value of val1 * val2 * ... * val_X. Not applicable for strings. One string can be multiplied by one integer.\n
    E.g. MULT->(1,2,3,4,5)\n
    ```
    """,
    "DIV":
    """
    ```\n
    DIV->(val1, val2)\n
    Returns the value of val1 / val2 in float form. Not applicable for strings.\n
    E.g. DIV->(7,2)\n
    ```
    """,
    "INT":
    """
    ```\n
    INT->val\n
    Returns the integer value of val\n
    E.g. INT->n\n
    ```
    """,
    "STR":
    """
    ```\n
    STR->val\n
    Returns the string value of val\n
    E.g. STR->n\n
    ```
    """,
    "TYPE":
    """
    ```\n
    TYPE->val\n
    Returns the type of val\n
    E.g. TYPE->n\n
    ```
    """,
    "APPEND":
    """
    ```\n
    APPEND->val<-(val1, val2, ... , val_X)\n
    Adds [val1, val2, ... val_X] to val. The code used in this case is val += [val1, val2, ... val_X].\n
    E.g. APPEND->n<-(1,2,3,4,5)\n
    ```
    """,
    "POP":
    """
    ```\n
    POP->var<-idx\n
    From the list var, this pops the index idx.\n
    E.g. POP->n<-3\n
    ```
    """,
    "REMOVE":
    """
    ```\n
    REMOVE->var<-val\n
    From the list var, this removes the value val once\n
    E.g. REMOVE->n<-5\n
    ```
    """,
    "ENDL":
    """
    ```\n
    ENDL\n
    ENDL can be substituted for a new line\n
    E.g. ADD->("hello",ENDL,"world")\n
    ```
    """,
    "READ":
    """
    ```\n
    READ\n
    Asks for and returns input\n
    E.g. SET->n<-READ\n
    ```
    """,
    "LIST":
    """
    ```\n
    LIST\n
    This can be substituted for []. Can be used to initialize a list. Indexes can be accessed by doing list->index although index has to be a number.\n
    E.g. SET->n<-LIST\n
    ```
    """
}