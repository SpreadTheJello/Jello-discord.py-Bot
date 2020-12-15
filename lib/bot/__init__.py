from discord import Intents
from discord import Embed
from random import choice
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound


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

	async def on_error(self, err, *args, **kwargs):
		if err == "on_command_error":
			await args[0].send("Something went wrong.")
			
		channel = self.get_channel(788234381327597589)
		await channel.send("An Error occured.")
		raise

	async def on_command_error(self, ctx, exc):
		if isinstance(exc, CommandNotFound):
			pass
		elif hasattr(exc, "original"):
			raise exc.original
		else:
			raise exc

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

			embed = Embed(title="Jello Bot is online!", description="?help to get a list of commands.", color=0x00ff00, timestamp=datetime.utcnow())
			fields = [("\a", quote, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			embed.set_author(name=self.guild, icon_url=self.guild.icon_url)	
			embed.set_footer(text="Quotes by Isaac")
			#embed.set_thumbnail(url=self.guild.icon_url)
			#embed.set_image(url=self.guild.icon_url)
			await channel.send(embed=embed)
			

		else:
			print("bot reconnected")

	async def on_message(self, message):
		pass

bot = Bot()