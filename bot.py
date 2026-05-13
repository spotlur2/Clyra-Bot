# bot.py
# python bot.py

import discord
from discord.ext import commands
from main import run_pipeline
from collections import defaultdict
from dotenv import load_dotenv
load_dotenv()

# setup
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# context
channel_context = defaultdict(list)
CONTEXT_WINDOW = 3  # currently set to 3 messages for context

@bot.event
async def on_ready():
    print(f"✅ Clyra Bot is online as {bot.user}")
    print(f"Connected to {len(bot.guilds)} server(s)")

@bot.event
async def on_message(message):
    # ignore bot
    if message.author == bot.user:
        return
    
    #ignore commands
    if message.content.startswith("!"):
        await bot.process_commands(message)
        return
    
    context = channel_context[message.channel.id].copy()

    # run pipeline
    user_id = str(message.author.name)
    result = run_pipeline(user_id, message.content, context)
    decision = result["decision"]
    action = decision["action"]
    risk_score = decision["risk_score"]
    reason = decision["reason"]

    # update context
    channel_context[message.channel.id].append(message.content)
    if len(channel_context[message.channel.id]) > CONTEXT_WINDOW:
        channel_context[message.channel.id].pop(0)

    # actions based on decision
    if action == "allow":
        pass

    elif action == "warn":
        await message.channel.send(
            f"⚠️ **Warning** {message.author.mention}: {reason} "
        )

    elif action == "warn":
        await message.channel.send(
            f"⚠️ **Warning** {message.author.mention}: Please keep the conversation respectful."
        )

    elif action == "delete":
        try:
            await message.delete()
            await message.channel.send(
                f"🗑️ **Message deleted** — {message.author.mention}: Your message violated our server rules."
            )
        except discord.Forbidden:
            print("Missing permission to delete messages")

    elif action == "mute":
        try:
            await message.delete()
            await message.author.timeout(
                discord.utils.utcnow() + __import__("datetime").timedelta(minutes=5),
                reason=reason
            )
            await message.channel.send(
                f"🔇 **{message.author.mention} has been muted for 5 minutes** — Repeated or serious violation."
            )
        except discord.Forbidden:
            print("Missing permission to timeout members")

    elif action == "ban":
        try:
            await message.delete()
            await message.author.ban(reason=reason)
            await message.channel.send(
                f"🔨 **{message.author.mention} has been banned** — Severe violation of server rules."
            )
        except discord.Forbidden:
            print("Missing permission to ban members")

        await bot.process_commands(message)


# bot commands
@bot.command()
async def check(ctx, *, text):
    """Manually check a message: !check <message>"""
    result = run_pipeline(str(ctx.author.name), text, [])
    decision = result["decision"]
    await ctx.send(
        f"**Message:** `{text}`\n"
        f"**Action:** `{decision['action']}`\n"
        f"**Risk Score:** `{decision['risk_score']}`\n"
        f"**Reason:** {decision['reason']}"
    )

@bot.command()
async def ping(ctx):
    """Check if the bot is alive: !ping"""
    await ctx.send("🟢 Clyra Bot is online and watching!")


# main
if __name__ == "__main__":
    import os
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("DISCORD_TOKEN environment variable not set!")
    bot.run(token)