import discord
import os
import time
from Parse import Miseri
from Help import help_list
from keepalive import keep_alive

intents = discord.Intents(messages=True, message_content=True, dm_messages = True)
client = discord.Client(intents=intents)
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
            # send the command to the parser for output
            content = message.content.split("\n", 1)[1].replace("```\n", "").replace("\n```", "")
            body = content.split("\n")
            
            interpreter.insert(body)
            while len(interpreter.wait_list) > 0:
                interpreter.read(interpreter.find())

            # output the results
            if interpreter.output != "":
                await message.channel.send("```\n"+interpreter.output+"```")
                
            if interpreter.out_image != None:
                await message.channel.send(file=discord.File(interpreter.out_image))

        # error messages
        except KeyError:
            await message.channel.send("```\nNameError\n```")
        except TimeoutError:
            await message.channel.send("```\nTimeoutError\n```")
        except ZeroDivisionError:
            await message.channel.send("```\nZeroDivisionError\n```")
        except IndexError:
            await message.channel.send("```\nIndexError\n```")
        except:
            await message.channel.send("```\nSyntaxError\n```")
        finally:
            interpreter.output = ""
            interpreter.out_image = None

        time.sleep(5)

    # send command list
    elif message.content.startswith("$help"):
        
        try:
            await message.channel.send(help_list["$help"])
        except:
            await message.channel.send("```\nNameError\n```")

    # send the syntax of a command
    elif message.content.startswith("$syntax"):

        try:
            body = message.content.split(" ")
            await message.channel.send(help_list[body[1]])
        except:
            await message.channel.send("```\nKeyError\n```")

    # send example commands
    elif message.content.startswith("$example"):

        try:
            await message.channel.send('$miseri-$\n```\nOUT->"hi"\n```')
        except:
            await message.channel.send("```\nSyntaxError\n```")



time.sleep(1)
keep_alive()
client.run(os.getenv('TOKEN'))
