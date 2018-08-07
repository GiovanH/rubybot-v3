import discord
import random
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    print(message.content)
    if message.content.startswith('!frog'):
        print("frog")
        flist = ['https://images.discordapp.net/.eJwNx0EOwiAQAMC_cHeXBaHd3voDf2AIJRTTCoH1ZPy7TeYyX_Xph1rULtLGgriVEWvfYEjtISfIteYjhVYGxHpiEAlxP9NbBhprDM327pl5mtxVNKzZeWLvtJktEWl8lDjWLk9tb3TRQA4swatl9fsDFmMlhQ.Fnrd6BLW525QvCZUzUmePI3GjeI','http://4.bp.blogspot.com/_A5pjzTdTXfQ/TPZb5hDNB0I/AAAAAAAAAm0/yoCgcykaGgo/s1600/happy+frog.gif','https://cdn.drawception.com/images/panels/2014/5-6/Zw9RBOTYYM-10.png']
        await client.send_message(message.channel, random.choice(flist))
        
    elif message.content.startswith('!'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'haha noooooope')

client.run('MjQzMjczMDY4MTI5MTU3MTIw.C6igGw.6bN0JTRxpjLCB0e4SdR1_qW3p94')
