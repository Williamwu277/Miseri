# miseri
A for-fun discord bot

Created for no whatever reason, miseri can do a few fun tricks such as data generation for competitive programming :D

Call ``$help`` for a list of commands

The command ``$miseri-$`` can be used to do some cool stuff with miseri :) Just follow up with two \`\`\` and whatever commands you want executed in between 
them for the interpreter to run them.

If you are having trouble with ``$miseri-$``, ``$example`` can provide an example of its use: such as

**$miseri-$**
```
OUT->":D"
```

which outputs ``:D`` into the channel stream

For a more extensive explanation of the syntax of each command, simply call ``$syntax <command>``

___

**So far, miseri supports the keywords:**

| **keyword** | **action** | **keyword** | **action** |
| - | - | - | - |
| ``SET`` | set variables or change them | ``ADD`` | add things together |
| ``OUT`` | output things | ``SUB`` | subtract things from each other |
| ``IF`` | complete conditional statements | ``MULT`` | multiply things together |
| ``LOOP`` | repeat actions | ``DIV`` | divide things from each other |
| ``TREE`` | data generation of a tree | ``INT`` | convert to integer |
| ``DFS`` | perform depth first search on said tree | ``STR`` | convert to string |
| ``TYPE`` | find the type of something | ``APPEND`` | add things to a list |
| ``POP`` | pop an index from a list | ``REMOVE`` | remove something from a list |
| ``RAND`` | generate random numbers | ``DRAW`` | send the image of a tree generated |
| ``MIN`` | find the minimum number | ``MAX`` | find the maximum number |
| ``BSL`` | lower bound binary search | ``BSU`` | upper bound binary search |
| ``SORT`` | sort a list | | |

___

**Not to mention, there are also a few sub-commands:**

| **sub-command** | **action** | **sub_command** | **action** |
| - | - | - | - |
| ``ENDL`` | create a newline | ``LIST`` | initialize a list |
| ``READ`` | read input | | |

___

With danger of near infinite loops, giant trees or errors in syntax from the command, miseri also has error messages when a command has gone awry

messages such as
```
SyntaxError
```
or
```
TimeoutError
```
indicate when something has gone wrong

___
## Have fun :P
