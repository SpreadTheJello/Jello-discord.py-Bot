from discord import Intents
from discord import Embed
from random import choice
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase


PREFIX = "?"
OWNER_IDS = [216768190984749057]

class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.guild = None
		self.scheduler = AsyncIOScheduler()

		super().__init__(
		command_prefix=PREFIX,
		owner_ids=OWNER_IDS,
		intents=Intents.all(),
		)

	def run(self, version):
		self.VERSION = version

		with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
			self.TOKEN = tf.read()

		print("running bot...")
		super().run(self.TOKEN, reconnect=True)

	async def on_connect(self):
		print("bot connected")
		
	async def on_disconnect(self):
		print("bot disconnected")

	async def on_ready(self):
		if not self.ready:
			self.ready = True
			self.guild = self.get_guild(788174344861646908)
			print("bot ready")

			channel = self.get_channel(788234381327597589)
			#await channel.send("Bad boys, bad boys, watchu gonna do, watcha gonna do when they come for you")

			quotes = ["Jump up and down like you're a pancake.",
			"A steak a day keeps the vegan away!",
			"I see you have a hat, tis a nice hat."]
			quote = (choice(quotes))

			embed = Embed(title="Jello Bot is online!", description="?help to get a list of commands.", color=0xFF0000)
			fields = [("\a", quote, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
				embed.set_footer(text="Quotes by Isaac")
			await channel.send(embed=embed)
			

		else:
			print("bot reconnected")

	async def on_message(self, message):
		pass

bot = Bot()