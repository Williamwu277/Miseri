import discord
import os
import time
from Parse import Miseri
from Help import help_list
from keepalive import keep_alive

client = discord.Client()
interpreter = Miseri()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

    if message.author == client.user:
        return


    if message.content.startswith("$miseri-$"):

        try:
            mes = message.content.split("\n", 1)[1].replace("```\n", "").replace("\n```", "")
            body = mes.split("\n")
            
            interpreter.output = ""
            interpreter.insert(body)
            while len(interpreter.wait_list) > 0:
                interpreter.read(interpreter.find())
            
            if interpreter.output != "":
                await message.channel.send("```\n"+interpreter.output+"```")
        except KeyError:
            # vars are stored in dict keys
            await message.channel.send("```\nNameError\n```")
        except TimeoutError:
            # large af loops
            await message.channel.send("```\nTimeoutError\n```")
        except ZeroDivisionError:
            await message.channel.send("```\nZeroDivisionError\n```")
        except IndexError:
            await message.channel.send("```\nIndexError\n```")
        except:
            await message.channel.send("```\nSyntaxError\n```")

        time.sleep(5)
    
    elif message.content.startswith("$help"):
        
        try:
            await message.channel.send(help_list["$help"])
        except:
            await message.channel.send("```\nNameError\n```")
    
    elif message.content.startswith("$syntax"):

        try:
            body = message.content.split(" ")
            await message.channel.send(help_list[body[1]])
        except:
            await message.channel.send("```\nKeyError\n```")
    
    elif message.content.startswith("$example"):

        try:
            await message.channel.send('$miseri-$\n```\nOUT->"hi"\n```')
        except:
            await message.channel.send("```\nSyntaxError\n```")



time.sleep(1)

keep_alive()
#i have to set up the pinging stuffies oh the webserver
client.run(os.getenv('TOKEN'))
#kinda need to ... not get ratelimited though
#wait how, bruh how are you getting ratelimited :wtf:
#yep this is just straight up weird
# how am i making that many requests, tru running the program again 
# i have like one await lol
# hopefully doesnt die
# ireally don't want to get banned from using discord API lol