import discord
import random
from discord import app_commands
from discord.ext import commands


intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    # Sync commands to Discord
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(e)

# Slash command: /sendmessage <message> <channel>
@tree.command(name="sendmessage", description="Send a message to a selected channel")
@app_commands.describe(
    message="Enter the message to send",
    channel="The channel to send it to"
)
async def send_message(interaction: discord.Interaction, message: str, channel: discord.TextChannel):
    try:
        await channel.send(message)
        await interaction.response.send_message(f"✅ Success dude. Message sent to {channel.mention}", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Oh no. Failed to send message: {e}", ephemeral=True)




# /roll command
@tree.command(name="roll", description="Roll a dice")
@app_commands.describe(
    sides="Number of sides on the dice (default is 6)"
)
async def roll(interaction: discord.Interaction, sides: int = 6):
    import random
    result = random.randint(1, sides)
    await interaction.response.send_message(f"🎲 You rolled a **{result}** (1–{sides})")



# /rps command
@tree.command(name="rps", description="Play Rock Paper Scissors")
@app_commands.describe(choice="Your move. Type: rock,paper or scissors)")
async def rps(interaction: discord.Interaction, choice: str):
    options = ["rock", "paper", "scissors"]
    bot_choice = random.choice(options)
    choice = choice.lower()

    if choice not in options:
        await interaction.response.send_message("❌ Invalid choice! Choose rock, paper, or scissors.")
        return

    result = "🤝 It's a tie!"
    if (choice == "rock" and bot_choice == "scissors") or \
       (choice == "paper" and bot_choice == "rock") or \
       (choice == "scissors" and bot_choice == "paper"):
        result = "🎉 You win!"
    elif choice != bot_choice:
        result = "😢 You lose!"

    await interaction.response.send_message(f"You chose **{choice}**,\n I chose **{bot_choice}**.\n {result}")






# Run the bot

bot.run("token_here")
