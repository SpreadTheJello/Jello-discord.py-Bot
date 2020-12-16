from random import choice, randint
from datetime import datetime
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hello", aliases=["hi"])
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello', 'Hi', 'Yo', 'Hey', 'Sup'))} {ctx.author.mention}!")

    @command(name="dice", aliases=["roll", "d"])
    async def roll_dice(self, ctx, die_string: str):
        dice, value = (int(term) for term in die_string.split("d"))
        rolls = [randint(1, value) for i in range(dice)]

        #await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")

        title = (f"Rolling {dice} dice")

        embed = Embed(title=title, description="", color=0x00ff00, timestamp=datetime.utcnow())
        fields = [("Rolls", rolls, False),
        ("Total:", sum(rolls), True),
        ("Average:", sum(rolls)/dice, True)]
        dices = ["https://upload.wikimedia.org/wikipedia/commons/2/2c/Alea_1.png", "https://upload.wikimedia.org/wikipedia/commons/b/b8/Alea_2.png", "https://upload.wikimedia.org/wikipedia/commons/2/2f/Alea_3.png", "https://upload.wikimedia.org/wikipedia/commons/8/8d/Alea_4.png", "https://upload.wikimedia.org/wikipedia/commons/5/55/Alea_5.png", "https://upload.wikimedia.org/wikipedia/commons/f/f4/Alea_6.png"]
        
        image = ""

        if (value == 1):
            image = dices[0]
        elif (value == 2):
            image = dices[1]
        elif (value == 3):
            image = dices[2]
        elif (value == 4):
            image = dices[3]
        elif (value == 5):
            image = dices[4]
        elif (value == 6):
            image = dices[5]
        else:
            image = ""

        embed.set_thumbnail(url=image)
        
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)
        


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")

def setup(bot):
    bot.add_cog(Fun(bot))