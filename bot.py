import discord
from discord.ext import commands
import json
import cfg

intents = discord.Intents.default()
intents.message_content=True


bot = commands.Bot(
	command_prefix=cfg.bot['prefix'],
	description=cfg.bot['description'],
	owner_id=cfg.bot['owner'],
	activity=discord.Game(name=cfg.bot['game'], type=0),
	case_insensitive=True,
	intents=intents
)

@bot.event
async def on_ready():
	print(f'Logged in as {bot.user.name}({bot.user.id}) with prefix {cfg.bot['prefix']}\n-----')

@bot.event
async def on_message(message):
	if len(message.content) <= 1:#embeds or single char
		return
	if message.content[len(cfg.bot['prefix'])] == cfg.bot['prefix'][0]:
		return
	if message.webhook_id is not None:
		message.author.bot = False
		message.author.discriminator = -1
	return await bot.process_commands(message)

@bot.event
async def on_command_error(ctx,err):
	if ('Command ' in str(err)) and (' is not found' in str(err)):
		return await ctx.message.add_reaction('❓')
	print(f'[ERROR] {err}')
	return await ctx.message.add_reaction('❗')

@bot.event
async def setup_hook():

	for cog in cfg.cogs:
		cogName = f'cogs.{cog}'
		print(f'loading: {cogName}')
		await bot.load_extension(cogName)
	




if __name__ == "__main__": bot.run(cfg.bot['token'], reconnect=True)