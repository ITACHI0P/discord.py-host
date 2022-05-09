import os
from discord.ext import commands
import asyncio


bot = commands.Bot(command_prefix="<")
TOKEN = os.getenv("DISCORD_TOKEN")
client = bot

@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=False)
    await ctx.send( ctx.channel.mention + " ***is now in lockdown.***")

@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " ***has been unlocked.***")
    
@client.command(case_insensitive=True)
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    if reason == None:
        await ctx.send('Please write a reason!')
        return
    guild = ctx.guild
    muteRole = discord.utils.get(guild.roles, name = "Muted")

    if not muteRole:
        await ctx.send("No Mute Role found! Creating one now...")
        muteRole = await guild.create_role(name = "Muted")

        for channel in guild.channels:
            await channel.set_permissions(muteRole, speak=False, send_messages=False, read_messages=True, read_message_history=True)
        await member.add_roles(muteRole, reason=reason)
        await ctx.send(f"{member.mention} has been muted in {ctx.guild} | Reason: {reason}")
        await member.send(f"You have been muted in {ctx.guild} | Reason: {reason}")

@client.command(case_insensitive=True)
async def unmute(ctx, member: discord.Member, *, reason=None):

    guild = ctx.guild
    muteRole = discord.utils.get(guild.roles, name = "Muted")

    if not muteRole:
        await ctx.send("The Mute role can\'t be found! Please check if there is a mute role or if the user already has it!")
        return
    await member.remove_roles(muteRole, reason=reason)
    await ctx.send(f"{member.mention} has been unmuted in {ctx.guild}")
    await member.send(f"You have been unmuted in {ctx.guild}")

@client.command(aliases=['clear'])
async def purge(ctx, amount=1):
    if(not ctx.author.guild_permissions.manage_messages):
        await ctx.send('Cannot run command! Requires: ``Manage Messages``')
        return
    amount = amount
    if amount > 100:
        await ctx.send('I can\'t delete more than 100 messages at a time!')
    else:
        await ctx.message.delete() 
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'Sucessfully deleted {amount} messages!', delete_after=2.0)

@client.command()
async def typing(ctx):
    # Start typing
    async with ctx.typing():
        await asyncio.sleep(120)

    await ctx.send('Done Typing')

@bot.command()
async def invite(ctx):
	emoji = ("<:emote:967390642655346688>")
	emb = discord.Embed(color=0xFFA500)
	emb.add_field(name="INVITE ME", value="<:emote:967390642655346688> [from here](https://discord.com/api/oauth2/authorize?client_id=943912366880473148&permissions=2113268983&scope=bot)")
	await ctx.send(embed=emb)

@client.command(case_insensitive=True)
@commands.has_permissions(manage_channels= True)
async def slowmode(ctx, time:int):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('Cannot run command! Requires: ``Manage Messages``')
        return
    if time == 0:
        await ctx.send('Slowmode is currently set to `0`')
        await ctx.channel.edit(slowmode_delay = 0)
    elif time > 21600:
        await ctx.send('You cannot keep the slowmode higher than 6 hours!')
        return
    else:
        await ctx.channel.edit(slowmode_delay = time)
        await ctx.send(f"Slowmode has been set to `{time}` seconds!")

@client.command()
@commands.has_permissions(administrator=True)
async def poll(ctx, *, question=None):
    if question == None:
        await ctx.send("Please write a poll!")

    icon_url = ctx.author.avatar_url 

    pollEmbed = discord.Embed(title = "`New Poll!`", description = f"```\n{question}```")

    pollEmbed.set_footer(text = f"Poll given by {ctx.author}", icon_url = ctx.author.avatar_url)

    pollEmbed.timestamp = ctx.message.created_at 

    await ctx.message.delete()
    
#    poll_msg = await ctx.send(f"```\n NEW POLL !!\n\n{question}\n poll given by {ctx.author}```")

    poll_msg = await ctx.send(embed = pollEmbed)

    await poll_msg.add_reaction("⬆️")
    await poll_msg.add_reaction("⬇️")


@client.command()
async def avatar(ctx, member: discord.Member=None):
	if member == None:
		member = ctx.author
	
	icon_url = member.avatar_url 

	avatarEmbed = discord.Embed(title = f"{member.name}\'s Avatar", color = 0xFFA500)

	avatarEmbed.set_image(url = f"{icon_url}")

	avatarEmbed.timestamp = ctx.message.created_at 

	await ctx.send(embed = avatarEmbed)

@bot.command()
async def say(ctx, * ,text=None):
	if text is None:
		await ctx.reply("please specify a message to say.")
	else:
		await ctx.message.delete()
		await ctx.send(text)

@bot.command()
async def ping(ctx):
	embed = discord.Embed(title=f"ping pong", description=f"Bot latency : `{round(bot.latency * 1000)}ms`")
	await ctx.send(embed=embed)

@bot.command(help = "Shows the Guild the bot is in")
async def serverlist(ctx):
    ownerID = 770342748393308170
    if ctx.author.id == ownerID:
        msg = "\n".join(f"{x}" for x in bot.guilds)
        embed = discord.Embed(
            title = "",
            description = "",
            color=discord.Color.teal()
        )
        embed.add_field(name = "All Bots Guilds", value = f"```\n{msg}\n```")
        await ctx.send(embed = embed)

@commands.has_permissions(administrator=True)
@bot.command(pass_context=True)
async def dm(ctx, user: discord.User, *, message=None):
    message = message or "hello"
    await user.send(message)

@bot.command(name="whois")
async def whois(ctx,user:discord.Member=None):

    if user==None:
        user=ctx.author

    rlist = []
    for role in user.roles:
      if role.name != "@everyone":
        rlist.append(role.mention)

    b = ", ".join(rlist)


    embed = discord.Embed(colour=user.color,timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info - {user}"),
    embed.set_thumbnail(url=user.avatar_url),
    embed.set_footer(text=f'Requested by - {ctx.author}',
  icon_url=ctx.author.avatar_url)

    embed.add_field(name='ID:',value=user.id,inline=False)
    embed.add_field(name='Name:',value=user.display_name,inline=False)

    embed.add_field(name='Created at:',value=user.created_at,inline=False)
    embed.add_field(name='Joined at:',value=user.joined_at,inline=False)

  
 
    embed.add_field(name='Bot?',value=user.bot,inline=False)

    embed.add_field(name=f'Roles:({len(rlist)})',value=''.join([b]),inline=False)
    embed.add_field(name='Top Role:',value=user.top_role.mention,inline=False)

    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    embed = discord.Embed(colour=discord.Colour.teal())
    await bot.process_commands(message)
    if message.content.startswith('A card from your wishlist is dropping'):
        ownerid = 646937666251915264
        if message.author.id == ownerid:
        	await message.reply('**Wishlist drop!!!**<@&944489952153071687>')
        
    if message.content == "I'm dropping 3 cards since this server is currently active!":
    	ownerid = 646937666251915264
    	if message.author.id == ownerid:
    		await message.reply("**Server drop!!!**<@&944644788865626113>")
    	
    if message.content == "<@943912366880473148>":
    	embed.add_field(value=f'`requested by - {message.author}`''', name='**MY PREFIX IS `' + command_prefix +'` \nTYPE `' + command_prefix + 'help` FOR LIST OF COMMANDS.**',inline=False)
    	await message.channel.send(embed=embed)
    	
    if message.content.startswith("<@770342748393308170>"):
    	await message.add_reaction("<​a:Itachi_Op:962968137513435146>")
	
@bot.event
async def on_ready():
	print(bot.user.name)
	await bot.change_presence(activity=discord.Activity(name=f"<help | {len(bot.guilds)} servers | made by ~Gaurav#9643", type=1))

if __name__ == "__main__":
    bot.run(TOKEN)
