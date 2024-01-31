from unicodedata import name
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
import asyncio
import datetime
import mysql.connector
import json

global host_name
host_name = "hostname"
global user_name
user_name = "username"
global my_password
my_password = "password"
global my_database
my_database = "database" 

intents = discord.Intents.default()
intents.members = True
#intents.message_content = True
intents = discord.Intents().all() #remove after development
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="^", intents=intents)
global channel_id
channel_id = "channel_id"
global user_array
user_array = []

# STATS VARIABLES
global eventCount
eventCount = 0

global messageCount
messageCount = 0

global upTime # Set this one up later with datetime
upTime = None

#############################################################################

@tasks.loop(seconds=60)
async def check_for_raid_pokemon():

    mydb = mysql.connector.connect(
        host= host_name,
        user= user_name,
        password= my_password,
        database= my_database
    )

    mycursor = mydb.cursor()

    try:
        now = datetime.datetime.now()
        print(f"Checking for raid pokemon at {now}")
        # Get the current hour and minute
        current_hour, current_minute = now.hour, now.minute
        # Query database table for any raid pokemon that match the current hour and minute
        print(current_hour, current_minute)
        start_date_str = now.date().strftime('%Y-%m-%d')
        print(f"Connecting to database {my_database} on host {user_name}...")
        query = "SELECT * FROM PokeData.all_events WHERE DATE(start_date)=%s"
        #####query_event = "SELECT * FROM events WHERE DATE(start_date)=%s"
        print(query, (start_date_str))
        mycursor.execute(query, (start_date_str,))
        ####mycursor.execute(query_event(start_date_str))
        rows = mycursor.fetchall()
        print(f"{len(rows)} raid pokemon found in the database.")
        print("fetched all events!")
        for row in rows:
            print("Inside for loop")
            print(row)
            # Send an embed to the designated channel
            raid_start_time = datetime.datetime.strptime(str(row[8]), '%H:%M:%S').time().replace(second=0, microsecond=0)
            current_time = now.time().replace(second=0, microsecond=0)
            channel = bot.get_channel(channel_id)
            event = row[0]
            name = row[1]
            description = row[2]
            begin_date = row[3]
            final_date = row[4]
            begin_time = row[7]
            thumbnail_url = row[9]
            title_url = row[10]
            embed_color = row[11]
            footer_text = row[12]
            new_embed = create_embed(name, title_url, description, embed_color, thumbnail_url, begin_date, final_date, begin_time, footer_text)
            guild = bot.get_guild("guild #") 
            role = discord.utils.get(guild.roles, name='Pokevent') 
            message = f"{role.mention}, New " + event +  " Coming Soon!"
            if raid_start_time == current_time:
                await channel.send(message, embed=new_embed)
                print(f"Sent pokemon event message to channel {channel.id}")
                eventCount += 1
    except Exception as e:
        print(f"An error occurred: {e}")


    # Query your MySQL table for any reminders that match the current date

@bot.command(aliases=['start', 'sr'])
async def start_reminders(ctx):
    check_for_raid_pokemon.start()
    await ctx.send('Raid Pokemon Reminders started!')

@bot.command(aliases=['chanid'])
async def print_channel_id(ctx):
    channel = bot.get_channel(channel_id)
    if channel:
        await ctx.send(f"Channel ID: {channel.id}")
    else:
        await ctx.send("Channel not found!")

def create_embed(new_title, new_title_url, new_description, new_color, new_thumbnail_url, new_start_date, new_end_date,  new_start_time, new_footer):
    embed=discord.Embed(title=new_title, url=new_title_url, description=new_description, color=new_color)
    embed.set_author(name="Pokevent")
    embed.set_thumbnail(url=new_thumbnail_url)
    embed.add_field(name="Start Date", value=new_start_date, inline=True)
    embed.add_field(name="End Date", value=new_end_date, inline=True)
    embed.add_field(name="Start Time", value=new_start_time, inline=True)
    embed.set_footer(text=new_footer)
    return embed

@bot.command(aliases=['te'])
async def test_embed(ctx):
    new_embed = create_embed("Title", "https://twitter.com/iBairly", "Description", 0xca2b3b, "https://youtube.com", "Start Date", "End Date", "Shiny", "Start Time", "Footer" )
    await ctx.send(embed=new_embed)

#############################################################################

# IGNORE
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Pokevent be built'))
    print('Logged in as {0.user}'.format(bot))
    #print(guild.members[1])
    for guild in bot.guilds:
        guild_id = guild.id
        print(f'Bot is in guild with ID: {guild_id}')

     # Fetch member data for all servers
    for guild in bot.guilds:       
        for member in guild.members:
            user_array.append(member.id)

@bot.event
async def on_server_join(guild):
    welcome_message = f"Pokévent is here!"

    channel = guild.system_channel

    if channel is not None:
        await channel.send(welcome_message)
    else:
        print("there is no channels")


##############################################################################

@bot.command()
async def alive(message):
    bair_id = "my_id"
    channel = "channel_id"
    if message.author.id == bair_id and message.channel.id ==  channel:
        await message.channel.send("Yes, I still work :0 !")

@bot.command()
async def stats(ctx):
    await ctx.send("Events Sent: " + str(eventCount))


@bot.command()
async def pack(ctx):
    embed=discord.Embed(title="Lugia GX", description="*Legendary*", color=0xff9500)
    embed.set_image(url="https://assets.pokemon.com/assets/cms2/img/cards/web/SM8/SM8_EN_227.png")
    embed.add_field(name="", value="", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def viewRaids(ctx):
    embed=discord.Embed(title="All Current Raids", description="info via @LeekDuck", url="https://leekduck.com/boss/", color=0xffffff)
    embed.set_image(url="https://leekduck.com/assets/img/logos/logo-black.png")
    await ctx.send(embed=embed)

@bot.command()
async def inventory(message):
    file_path = "Inventory.JSON"
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        await message.send("Your inventory is empty.")
        return

    user_id = str(message.author.id)  # Get the user's ID who issued the command
    if "users" not in data or user_id not in data["users"]:
        await message.send("Your inventory is empty.")
        return

    user_inventory = data["users"][user_id]

    user_nickname = message.author.nick if message.author.nick else message.author.name

    # Format and send the inventory data as a message
    inventory_message = f"**Inventory for {user_nickname}**\n"
    inventory_message += f"Currency: {user_inventory['currency']} coins\n"
    inventory_message += "Cards:\n"
    for card in user_inventory["cards"]:
        inventory_message += f"- {card}\n"

    await message.send(inventory_message)

@bot.command()
async def pullPack(ctx, num: int):
     
    mydb = mysql.connector.connect(
        host= host_name,
        user= user_name,
        password= my_password,
        database= my_database
    )

    mycursor = mydb.cursor()
    print(f"Connecting to database {my_database} on host {user_name}...")
    query = f"SELECT * FROM PokePack.poke_cards WHERE idpoke_cards = {num}"
    mycursor.execute(query)
    rows = mycursor.fetchall()
    for row in rows:
        print(row)
        name = row[1]
        rarity = row[2]
        expansion = row[4]
        number = row[5]
        image = row[6]
        card_type = row[3]
        color = None

        if (card_type == "VMAX"):
            color = 0xefff0a

        card_embed = create_cardEmbed(name, rarity, color, expansion, number, image)
        await ctx.send(embed=card_embed)

def create_cardEmbed(card_name, card_rarity, card_color, card_expansion, card_number, card_image):
    embed=discord.Embed(title=card_name, description=card_rarity, color=card_color)
    embed.set_image(url=card_image)
    embed.add_field(name="Expansion:", value=card_expansion, inline=True)
    embed.add_field(name="Number: ", value=card_number, inline=False)
    return embed

loop = asyncio.get_event_loop()
loop.create_task(bot.start('bot.token'))
loop.run_forever()
