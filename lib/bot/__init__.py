import os
import sys

from random import choice
from datetime import datetime

from glob import glob

from asyncio import sleep
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from discord import Intents
from discord import Embed

from ..db import db

PREFIX = "?"
OWNER_IDS = [216768190984749057]
COGS = [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")]

class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)

	def ready_up(self, cog):
		setattr(self, cog, True)
		print(f"  {cog} cog ready")

	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.cogs_ready = Ready()
		self.guild = None
		self.scheduler = AsyncIOScheduler()

		db.autosave(self.scheduler)
		super().__init__(
		command_prefix=PREFIX,
		owner_ids=OWNER_IDS,
		intents=Intents.all(),
		)

	def setup(self):
		for cog in COGS:
			self.load_extension(f"lib.cogs.{cog}")
			print(f"  {cog} cog loaded")

		print("setup complete")

	def run(self, version):
		self.VERSION = version

		print("running setup...")
		self.setup()

		with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
			self.TOKEN = tf.read()

		print("running bot...")
		super().run(self.TOKEN, reconnect=True)
	
	async def rules_reminder(self):
		#channel = self.get_channel(788234381327597589)
		await self.stdout.send("Remember to follow the rules!")

	async def on_connect(self):
		print("  bot connected")
		
	async def on_disconnect(self):
		print("bot disconnected")

	async def on_error(self, err, *args, **kwargs):
		if err == "on_command_error":
			await args[0].send("Something went wrong.")
			
		#channel = self.get_channel(788234381327597589)
		await self.stdout.send("An Error occured.")
		#raise

	async def on_command_error(self, ctx, exc):
		if isinstance(exc, CommandNotFound):
			pass
		elif hasattr(exc, "original"):
			raise exc.original
		else:
			raise exc

	async def on_ready(self):
		if not self.ready:			
			self.guild = self.get_guild(788174344861646908)
			self.stdout = self.get_channel(788234381327597589)
			self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
			self.scheduler.start()

			#channel = self.get_channel(788234381327597589)
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

			while not self.cogs_ready.all_ready():
				await sleep(0.5)

			await self.stdout.send(embed=embed)
			self.ready = True
			print("  bot ready")
			

		else:
			print("bot reconnected")

	async def on_message(self, message):
		if not message.author.bot:
			await self.process_commands(message)

bot = Bot()
