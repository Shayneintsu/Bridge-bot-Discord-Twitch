import asyncio
import json
import discord
from discord.ext import commands as dcmd
from twitchio.ext import commands as tcmd
from tokens import D_TOKEN,T_TOKEN

Dchannel = 1152160366760050750
Tchannel = 'shayneintsu'

with open('db-emote.json') as file:
    emotes = json.load(file)

async def search_messages(chn: discord.TextChannel,author:str,content:str):
    content = content.replace("\s"," ")
    async for message in chn.history(limit=100):
        if message.author.display_name == author and message.embeds[0].title == content:
            return message

async def start():


    """ 
    d8888b. d888888b .d8888.  .o88b.  .d88b.  d8888b. d8888b. 
    88  `8D   `88'   88'  YP d8P  Y8 .8P  Y8. 88  `8D 88  `8D 
    88   88    88    `8bo.   8P      88    88 88oobY' 88   88 
    88   88    88      `Y8b. 8b      88    88 88`8b   88   88 
    88  .8D   .88.   db   8D Y8b  d8 `8b  d8' 88 `88. 88  .8D 
    Y8888D' Y888888P `8888Y'  `Y88P'  `Y88P'  88   YD Y8888D' 
    """                                                    


    activ = discord.Activity(type=discord.ActivityType.watching,name="testing mode 👀")

    class DBot(dcmd.Bot):
        def __init__(self):
            super().__init__(
                command_prefix='$',
                intents=discord.Intents.all()
            )

    dbot = DBot()
    
    


    """ 
 d888888b db   d8b   db d888888b d888888b  .o88b. db   db 
 `~~88~~' 88   I8I   88   `88'   `~~88~~' d8P  Y8 88   88 
    88    88   I8I   88    88       88    8P      88ooo88 
    88    Y8   I8I   88    88       88    8b      88~~~88 
    88    `8b d8'8b d8'   .88.      88    Y8b  d8 88   88 
    YP     `8b8' `8d8'  Y888888P    YP     `Y88P' YP   YP 
                                                            
    """             

    class TBot(tcmd.Bot):
        def __init__(self):
            super().__init__(
                token=T_TOKEN,
                prefix='$',
                initial_channels=[Tchannel]
            )
        
            
        async def event_ready(self):
            print("Twitch Bot Ready!")

        async def event_message(self, message):
            if message.echo:
                return
            print("twitch: "+message.content)

            chn = await dbot.fetch_channel(Dchannel)
            whs = await chn.webhooks()
            wh = None
            if whs:
                wh = whs[0]
            else:
                wh = await chn.create_webhook(name="https://www.twitch.tv/"+Tchannel)

            usr = await message.author.user()

            #lastmsg = [mm async for mm in chn.history(limit=1)].pop()

            clr = None
            if message.author.colour:
                clr = int(message.author.colour[1:],base=16)

            if 'reply-parent-display-name' in message.tags:
                dmsg:discord.WebhookMessage = await search_messages(chn, message.tags['reply-parent-display-name'], message.tags['reply-parent-msg-body'])
                

                embd = discord.Embed(colour=clr,title=message.content)
                print(dmsg.embeds[0].title)
                embd.set_author(name=dmsg.embeds[0].title[:10]+"...",url=dmsg.jump_url,icon_url=dmsg.author.avatar)

                await wh.send(embed=embd,avatar_url=usr.profile_image,username=message.author.display_name,silent=True,allowed_mentions=False)

                #whmsg = await wh.fetch_message(lastmsg.id)
                #whmsg.embeds.append(discord.Embed(colour=int(message.author.colour[1:],base=16),title=message.content))
                #await whmsg.edit(embeds=whmsg.embeds+[discord.Embed(colour=int(message.author.colour[1:],base=16),title=message.content)])
            else:
                await wh.send(embed=discord.Embed(colour=clr,title=message.content),avatar_url=usr.profile_image,username=message.author.display_name,silent=True,allowed_mentions=False)

            await self.handle_commands(message)

    tbot = TBot()



    """ 
    d8888b.  .d88b.  d888888b db   db 
    88  `8D .8P  Y8. `~~88~~' 88   88 
    88oooY' 88    88    88    88ooo88 
    88~~~b. 88    88    88    88~~~88 
    88   8D `8b  d8'    88    88   88 
    Y8888P'  `Y88P'     YP    YP   YP 
    """        

    
    @dbot.event
    async def on_ready():
        await dbot.change_presence(status=discord.Status.online,activity=activ)

        print("Discord Bot Ready!")                   
    
    @dbot.event
    async def on_message(msg:discord.Message):
        if msg.id == Dchannel:
            print("discord: "+msg.content)     

    @dbot.tree.command(name="ping",description="ping?")
    async def dping(interact:discord.Interaction):
        try:
            await tbot.get_channel(Tchannel).send("Pong")
            await interact.response.send_message("Pong",ephemeral=True)
        except Exception as e:
            await interact.response.send_message(e,ephemeral=True,delete_after=10)

    @tbot.command(name='ping')
    async def tping(ctx:tcmd.Context):
            try:
                chn = await dbot.fetch_channel(Dchannel)
                await chn.send("Pong")
                await ctx.send("Pong")
            except Exception as e:
                await ctx.reply(e)
            

    await asyncio.gather(dbot.start(D_TOKEN), tbot.start())

asyncio.run(start())                    