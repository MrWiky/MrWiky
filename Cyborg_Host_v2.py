import time
import io
from discord.ext import commands, tasks

bot = commands.Bot('')
old_members = {''}

first_mention = '<#902820862393221140>'   # official-links channel
second_mention = '<#903729212706394163>'  # support channel

one_day_post = 902822286531395584     # general-chat channel
two_days_post = 930356346782629950    # nft-buy-sale

msg_reminder = f"""REMINDER: If you want to buy/sell NFTs, we strongly recommend using just the {first_mention}

Avoid any DMs trying to give you advice on what to do with your NFTs as, in most cases, they're coming from users with not-so-good intentions.

Remember that our staff will never DM you and if you encounter any issues you can rely on our {second_mention} !"""

comm = {
    '>help': 'Available commands are: ">web", ">mint", ">affiliate", ">twitter",'
             '">facebook", ">instagram", ">reddit", ">youtube", ">wp", ">roadmap"',
    '>web': 'https://www.cyborglegends.io/?ref=discord',
    '>mint': 'https://www.cyborglegends.io/store/?ref=discord',
    '>affiliate': 'https://www.cyborglegends.io/store/#affiliate-program-info',
    '>twitter': 'https://twitter.com/cyborglegends',
    '>facebook': 'https://www.facebook.com/cyborglegendsgame/',
    '>instagram': 'https://www.instagram.com/cyborglegendsgame/',
    '>reddit': 'https://www.reddit.com/r/CyborgLegends/',
    '>youtube': 'https://www.youtube.com/CyborgLegends',
    '>wp': 'https://www.cyborglegends.io/wp-content/uploads/2022/01/Website-WhitePaper-v1_05.pdf?fresh=1',
    '>roadmap': 'https://cdn.discordapp.com/attachments/902820936871469056/930152966273503292/roadmap.png'
}


@bot.event
async def on_message(message):
    reply = f'''Welcome to the Cyborg Army, {message.author.mention}! Take a few moments and share some details about you!

    ⏩  Which country do you come from?
    ⏩  Can you tell us for how long you have been an NFT collector?
    ⏩  How did you found out about our project?'''

    msg = str(message.content)

    if msg in comm.keys():          # check if the command exists
        await message.channel.send(comm[msg])      # if the command exists returns the value of that key

    if message.channel.name == '💬・newcomers-chat':  # Select channel

        if message.author == bot.user:  # Doesn't reply to itself
            return

        if message.author in old_members:  # Verify if the user is new
            return

        if str(message.author) not in old_members:  # If user is new sends what is in {reply}
            time.sleep(1.5)
            print(f'Message sent to {str(message.author)}')
            await message.channel.send(reply)

        async for msg in message.channel.history(limit=20000):  # Checks each old message limit=10k

            if str(msg.author) not in old_members:  # If the user is new he will be added in existing ones
                old_members.add(str(msg.author))
                print(f'User {str(msg.author)} added in old_members!')

            with io.open('old_members.txt', 'w', encoding='utf-8') as users:     # writes all members in a text file
                for member in old_members:
                    users.write(member + '\n')


# Message 1
@tasks.loop(hours=24)
async def called_once_a_day():
    message_channel = bot.get_channel(one_day_post)
    await message_channel.send(msg_reminder)
    print('Message posted after 24 hours !')


@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")


# Message 2
@tasks.loop(hours=48)
async def called_once_a_day2():
    message_channel = bot.get_channel(two_days_post)
    await message_channel.send(msg_reminder)
    print('Message posted after 48 hours !')


@called_once_a_day2.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")


called_once_a_day.start()
called_once_a_day2.start()


@bot.event
async def on_ready():
    print(f'{bot.user} is Online!')


bot.run('token')
