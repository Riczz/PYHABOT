import discord
import integrations.Parent as IntegrationsParent
import classes.pyhabot as pyhabot


class Client(discord.Client):
    integration = False

    def __init__(self, token, integration):
        self.token       = token
        self.integration = integration
        super().__init__()

    async def on_message(self, message):
        if not message.author.bot:
            await pyhabot.bot.onMessage(integration=self.integration, ctx=message, text=message.content)


class Integration(IntegrationsParent.Parent):
    client = False
    type_  = "Discord"

    def __init__(self, token):
        super().__init__("Discord")
        self.client = Client(token, self)
        
        @self.client.event
        async def on_ready():
            print(f"Invite link: https://discord.com/oauth2/authorize?client_id={self.client.user.id}&scope=bot&permissions=8")
            pyhabot.bot.startScrapeTask()
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="HardverApró"))
            
    def run(self):
        return self.client.run( self.client.token )

    async def sendMessage(self, ctx, text):
        for chunk in self.splitToChunks(text, 2000):
            await ctx.channel.send(chunk)

    async def reply(self, ctx, text):
        for chunk in self.splitToChunks(text, 2000):
            await ctx.reply(chunk, mention_author=True)

    def getMessageChannelID(self, ctx):
        return ctx.channel.id

    async def sendMessageToChannelByID(self, id_, text):
        channel = self.client.get_channel(id_)
        
        if channel:
            for chunk in self.splitToChunks(text, 2000):
                await channel.send(chunk)

def init(token):
    pyhabot.bot.setIntegration( Integration(token) )