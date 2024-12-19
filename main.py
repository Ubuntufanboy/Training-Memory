import discord, time, asyncio, random, datetime, os, cv2, shutil, sqlite3, json
from games.visual import Visual
from games.maze import Maze
from discord.ext import commands
from PIL import Image, ImageDraw

# this code fucking sucks balls but have fun with it

TOKEN = "put your token here fucking"

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
activeusers, vuserpoints, vuserindex, muserpoints, muserindex, needtotest, eligiblefortest, takingtest, tuserpoints, iuserpoints, iuserindex, waitingresponse, rooms = {}, {}, {}, {}, {}, [], [], {}, {}, {}, {}, {}, []
acceptable = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "exit", "1 exit", "2 exit", "3 exit", "4 exit", "5 exit", "6 exit", "7 exit", "8 exit", "9 exit", "10 exit", "11 exit", "12 exit", "13 exit", "14 exit", "15 exit", "16 exit", "17 exit", "18 exit", "19 exit", "20 exit"]

def make_img(image_paths, user_id):
    images = [Image.open(img) for img in image_paths]
    small_size = (50, 50)
    large_size = (100, 100)
    resized_images = []
    for i, img in enumerate(images):
        if "correct" in image_paths[i]:
            resized_images.append(img.resize(large_size))
        else:
            resized_images.append(img.resize(small_size))
    total_width = sum(img.size[0] for img in resized_images)
    max_height = max(img.size[1] for img in resized_images)
    new_image = Image.new('RGB', (total_width, max_height), (255, 255, 255))
    x_offset = 0
    for img in resized_images:
        new_image.paste(img, (x_offset, (max_height - img.size[1]) // 2))
        x_offset += img.size[0]
    draw = ImageDraw.Draw(new_image)
    correct_index = image_paths.index("correct.png")
    x_correct = sum(img.size[0] for img in resized_images[:correct_index])
    draw.rectangle([x_correct, 0, x_correct + large_size[0], large_size[1]], outline="blue", width=3)
    new_image.save(f"final_image{user_id}.png")

class Client(discord.Client):
    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.get_channel(1274948535569223763)
        message = await channel.fetch_message(1274952474658082858)
        await message.add_reaction("👍")
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global needtotest, rooms
        if payload.message_id == 1274952474658082858:
            guild = self.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if not member: return
            channel_name = f"{member.name}'s room"
            if channel_name not in rooms:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    member: discord.PermissionOverwrite(view_channel=True)
                }
                new_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
                members_with_visual = [m for m in guild.members if guild.get_role(1274997621441822730) in m.roles]
                members_with_id = [m for m in guild.members if guild.get_role(1274997676018110464) in m.roles]
                members_with_puzzle = [m for m in guild.members if guild.get_role(1274997790673473596) in m.roles]
                members_with_combine = [m for m in guild.members if guild.get_role(1274997818540560417) in m.roles]
                minimum = min(len(members_with_visual), len(members_with_id), len(members_with_puzzle), len(members_with_combine))
                neededgroup = 1274997621441822730 if minimum == len(members_with_visual) else 1274997676018110464 if minimum == len(members_with_id) else 1274997790673473596 if minimum == len(members_with_puzzle) else 1274997818540560417
                await member.add_roles(guild.get_role(neededgroup))
                rooms.append(channel_name)
                if neededgroup == 1274997621441822730: await new_channel.send(embed = discord.Embed(title=f"**Welcome to the Experiment {member.mention}**", description=f'* **You were placed in the {guild.get_role(neededgroup)}**\n * which means your main means of practicing is done with a visual game\n * every day during september come in this channel and say "play" to do a practice\n * the more you practice the more you help out the experiment\n * after some games youll be asked to take a test by saying "test". this is to track your general memory progress\n * PLEASE DONT CHEAT, this experiment is much more fun if everyone plays fairly \n * use "leaderboard" to see if youre one of the top contenders or "stats" to view how well youve been preforming in your games and tests\n * more information could be found by saying "about"', color=discord.Color.yellow()))
                if neededgroup == 1274997676018110464: await new_channel.send(embed = discord.Embed(title=f"**Welcome to the Experiment {member.mention}**", description=f'* **You were placed in the {guild.get_role(neededgroup)}**\n * which means your main means of practicing is done with a sequence game\n * every day during september come in this channel and say "play" to do a practice\n * the more you practice the more you help out the experiment\n * after some games youll be asked to take a test by saying "test". this is to track your general memory progress\n * PLEASE DONT CHEAT, this experiment is much more fun if everyone plays fairly \n * use "leaderboard" to see if youre one of the top contenders or "stats" to view how well youve been preforming in your games and tests\n * more information could be found by saying "about"', color=discord.Color.yellow()))
                if neededgroup == 1274997790673473596: await new_channel.send(embed = discord.Embed(title=f"**Welcome to the Experiment {member.mention}**", description=f'* **You were placed in the {guild.get_role(neededgroup)}**\n * which means your main means of practicing is done with a mental maze game\n * every day during september come in this channel and say "play" to do a practice\n * the more you practice the more you help out the experiment\n * after some games youll be asked to take a test by saying "test". this is to track your general memory progress\n * PLEASE DONT CHEAT, this experiment is much more fun if everyone plays fairly \n * use "leaderboard" to see if youre one of the top contenders or "stats" to view how well youve been preforming in your games and tests\n * more information could be found by saying "about"', color=discord.Color.yellow()))
                if neededgroup == 1274997818540560417: await new_channel.send(embed = discord.Embed(title=f"**Welcome to the Experiment {member.mention}**", description=f'* **You were placed in the {guild.get_role(neededgroup)}**\n * which means you can play any game you want to help improve your memory\n * every day during september come in this channel and say "play " then visual, id or puzzle to do a practice\n * the more you practice the more you help out the experiment\n * after some games youll be asked to take a test by saying "test". this is to track your general memory progress\n * PLEASE DONT CHEAT, this experiment is much more fun if everyone plays fairly \n * use "leaderboard" to see if youre one of the top contenders or "stats" to view how well youve been preforming in your games and tests\n * more information could be found by saying "about"', color=discord.Color.yellow()))
                await self.sqlsave()
            else:
                await member.send(f"you already have a private channel, if you don't actually dm KiddyKene because that's an issue lmao")
            if payload.user_id != 755685201073537065:
                channel = self.get_channel(1274948535569223763)
                if channel:
                    message = await channel.fetch_message(1274952474658082858)
                    await message.remove_reaction(payload.emoji, member)
    async def visualmemory(self, message, user_id, level):
        global activeusers, vuserpoints, vuserindex, needtotest, eligiblefortest, takingtest
        activeusers[user_id] = "visual"
        if user_id not in vuserpoints:
            with open('assets/visualtutorial.gif', 'rb') as file:
                embed = discord.Embed(title='**Welcome to Visual Memory**', description="* **you will be shown 2 photos**\n *  there's a 50% chance there's an alteration\n * your job is to spot it and see how long you last\n * here's an example:", color=discord.Color.green())
                embed.set_image(url="attachment://visualtutorial.gif")
                first_msg = await message.channel.send(file=discord.File(file, filename='visualtutorial.gif'), embed=embed)
                vuserpoints[user_id] = [[datetime.datetime.now().strftime("%Y-%m-%d %H"), 1]]
                await asyncio.sleep(10)
                await first_msg.edit(embed=discord.Embed(title=f"Level **{level}**", color=discord.Color.green()), attachments=[])
        else: first_msg = await message.channel.send(embed=discord.Embed(title=f"Level **{level}**", color=discord.Color.green()))
        if user_id not in activeusers: return
        await asyncio.sleep(1)
        vuserindex[user_id] = [random.randint(1, 2) == 2, level]
        Visual.arrange_fruits_on_shelves(vuserindex[user_id][0], f'shelves_with_fruits1{user_id}.png', f'shelves_with_fruits2{user_id}.png', level)
        image1 = f'shelves_with_fruits1{user_id}.png'
        image2 = f'shelves_with_fruits2{user_id}.png'
        if user_id not in activeusers: return
        with open(image1, 'rb') as file:
                embed = discord.Embed(title='**Memorize This Picture** *(use "exit" to quit)*', color=discord.Color.green())
                embed.set_image(url=f"attachment://{image1}")
                await first_msg.edit(content=None, embed=embed, attachments=[discord.File(file, filename=image1)])
        if level < 40: await asyncio.sleep(4)
        else: await asyncio.sleep(3)
        if user_id not in activeusers: return
        await first_msg.edit(embed=discord.Embed(title='**Remember that photo...**', color=discord.Color.green()), attachments=[])
        await asyncio.sleep(3)
        if user_id not in activeusers: return
        with open(image2, 'rb') as file:
            embed = discord.Embed(title='**Second Photo** *(use "exit" to quit)*', color=discord.Color.green())
            embed.set_image(url=f"attachment://{image2}")
            await first_msg.edit(content=None, embed=embed, attachments=[discord.File(file, filename=image2)])
        yes_button = discord.ui.Button(label="Yes", style=discord.ButtonStyle.green)
        no_button = discord.ui.Button(label="No", style=discord.ButtonStyle.red)
        async def yes_button_callback(interaction):
            if interaction.user.id != user_id:
                await interaction.response.send_message("this isn't your game")
                return
            if vuserindex[user_id][0]:
                await interaction.response.send_message("**You are Correct, it was altered**\n *don't click the 'yes' 'no' buttons anymore*")
                view.clear_items()
                await interaction.message.edit(view=view)
                await asyncio.sleep(1)
                if user_id in activeusers: await self.visualmemory(message, message.author.id, level + 1)
            else:
                await interaction.response.send_message("**You are Wrong, nothing changed**\n *don't click the 'yes' 'no' buttons anymore*")
                view.clear_items()
                vuserpoints[user_id].append([datetime.datetime.now().strftime("%Y-%m-%d %H"), level])
                await self.sqlsave()
                highscore = max(entry[1] for entry in vuserpoints[user_id])
                await asyncio.sleep(1)
                if level == highscore: await message.channel.send(f"**THAT'S A NEW HIGHSCORE: {level}**")
                else: await message.channel.send(f"You got a score of **{level}**, try beating your highscore of: **{highscore}**")
                await asyncio.sleep(1)
                if user_id in takingtest:
                    takingtest[user_id].append(level)
                    await message.channel.send(embed = discord.Embed(title=f"**That's 1/3 games and you scored {level}**\n Now moving onto game 2", color=discord.Color.yellow()))
                    await asyncio.sleep(2.5)
                    if user_id in activeusers: await self.idgame(message, message.author.id, True, 1)
                else:
                    if user_id not in needtotest:
                        eligiblefortest.append(user_id)
                        await message.channel.send(embed = discord.Embed(title=f'**Now that youve done some practice today, type "test" to see if youve imporved overall**', color=discord.Color.yellow()))
                        await asyncio.sleep(6)
                    await asyncio.sleep(3)
                    if user_id in activeusers: await self.visualmemory(message, message.author.id, 1)
        async def no_button_callback(interaction):
            if interaction.user.id != user_id:
                await interaction.response.send_message("this isn't your game")
                return
            if vuserindex[user_id][0]:
                await interaction.response.send_message("**You are Wrong, something changed**\n *don't click the 'yes' 'no' buttons anymore*")
                view.clear_items()
                vuserpoints[user_id].append([datetime.datetime.now().strftime("%Y-%m-%d %H"), level])
                await self.sqlsave()
                highscore = max(entry[1] for entry in vuserpoints[user_id])
                await asyncio.sleep(1)
                if level == highscore: await message.channel.send(f"That's A New High Score: **{level}**")
                else: await message.channel.send(f"You got a score of **{level}**, try beating your highscore of: **{highscore}**")
                await asyncio.sleep(1)
                if user_id in takingtest:
                    takingtest[user_id].append(level)
                    await message.channel.send(embed = discord.Embed(title=f"**That's 1/3 games and you scored {level}**\n Now moving onto game 2", color=discord.Color.yellow()))
                    await asyncio.sleep(4)
                    await self.idgame(message, message.author.id, True, 1)
                else:
                    if user_id not in needtotest:
                        eligiblefortest.append(user_id)
                        await message.channel.send(embed = discord.Embed(title=f'**Now that youve done some practice today, type "test" to see if youve imporved overall**', color=discord.Color.yellow()))
                        await asyncio.sleep(6)
                    await asyncio.sleep(3)
                    if user_id in activeusers: await self.visualmemory(message, message.author.id, 1)
            else:
                await interaction.response.send_message("**You are Correct, nothing changed**\n *don't click the 'yes' 'no' buttons anymore*")
                view.clear_items()
                await interaction.message.edit(view=view)
                await asyncio.sleep(1)
                if user_id in activeusers: await self.visualmemory(message, message.author.id, level + 1)
        yes_button.callback = yes_button_callback
        no_button.callback = no_button_callback
        view = discord.ui.View()
        view.add_item(yes_button)
        view.add_item(no_button)
        await message.channel.send(embed=discord.Embed(title="Did anything change?", color=discord.Color.green()), view=view)
    async def puzzlememory(self, message, user_id, testlevel):
        global activeusers, muserpoints, muserindex, needtotest, eligiblefortest, takingtest, tuserpoints
        activeusers[user_id] = "maze"
        if ((user_id in muserpoints) or (user_id in tuserpoints)) or (testlevel >= 2):
            if testlevel >= 1: level = testlevel
            else: level = muserpoints[user_id][-1][1]
            first_msg = await message.channel.send(embed=discord.Embed(title=f"Level **{level}**", color=discord.Color.orange()))
        else:
            with open('assets/mazetutorial.gif', 'rb') as file:
                embed = discord.Embed(title='**Welcome to Puzzle Memory**', description="* **You will be shown a maze**\n *  Green indicates the start, Red is the end\n * use the buttons to mentally navigate the maze \n * here's an example:", color=discord.Color.orange())
                embed.set_image(url="attachment://mazetutorial.gif")
                first_msg = await message.channel.send(file=discord.File(file, filename='mazetutorial.gif'), embed=embed)
                level = 1
                if (any(role.id in {1274997818540560417, 1274997790673473596} for role in message.author.roles)): muserpoints[user_id] = [[datetime.datetime.now().strftime("%Y-%m-%d %H"), 1]]
                await asyncio.sleep(9)
                await first_msg.edit(embed=discord.Embed(title=f"Level **{level}**", color=discord.Color.orange()), attachments=[])
        await asyncio.sleep(1)
        muserindex[user_id] = [Maze.save_mazes(user_id, level), 0]
        with open(f'maze{user_id}.png', 'rb') as file:
            embed = discord.Embed(title=f'Level **{level}**\n**Memorize This Maze** *(use "exit" to quit)*', color=discord.Color.orange())
            embed.set_image(url=f"attachment://maze{user_id}.png")
            await first_msg.edit(content=None, embed=embed, attachments=[discord.File(file, filename=f'maze{user_id}.png')])
            view = discord.ui.View()
            up_button = discord.ui.Button(label="↑", style=discord.ButtonStyle.green)
            down_button = discord.ui.Button(label="↓", style=discord.ButtonStyle.green)
            right_button = discord.ui.Button(label="→", style=discord.ButtonStyle.green)
            left_button = discord.ui.Button(label="←", style=discord.ButtonStyle.green)
            async def getscorrect(interaction, emoji):
                muserindex[user_id] = (muserindex[user_id][0], muserindex[user_id][1] + 1)
                if len(muserindex[user_id][0]) != muserindex[user_id][1]: await interaction.response.edit_message(embed=discord.Embed(title="Navigate the maze now", description=f"{emoji}", color=discord.Color.green()), view=view)
                else:
                    activeusers[user_id] = "free"
                    await interaction.response.edit_message(embed=discord.Embed(title="🎉You Made it🎉", description=f"**Level {level} --> {level + 1}**\n DON'T CLICK THESE BUTTONS ANYMORE", color=discord.Color.green()))
                    await asyncio.sleep(4)
                    if testlevel >= 1: await self.puzzlememory(message, user_id, testlevel+1)
                    else: 
                        if user_id in muserpoints: 
                            muserpoints[user_id].append([datetime.datetime.now().strftime("%Y-%m-%d %H"), level + 1])
                            await self.sqlsave()
                        if user_id in activeusers: await self.puzzlememory(message, user_id, 0)
            async def getswrong(interaction):
                activeusers[user_id] = "free"
                await interaction.response.edit_message(embed=discord.Embed(title="❌You went the wrong way❌", description=f"**Level {level} --> {max((level - 1), 1)}**\n DON'T CLICK THESE BUTTONS ANYMORE", color=discord.Color.green()))
                view.clear_items()
                await asyncio.sleep(1)
                if user_id in takingtest:
                    takingtest[user_id].append(level)
                    if len(takingtest) > 4:
                        await message.channel.send(embed = discord.Embed(title=f"The scores are a lil screwed up because you clicked on a past game's button, don't do that in the future pls", color=discord.Color.yellow()))
                        try: average = round((takingtest[user_id][0] + takingtest[user_id][1] + takingtest[user_id][3])/3)
                        except: pass
                    else: average = round(sum(takingtest[user_id]) / len(takingtest[user_id]))
                    if user_id in tuserpoints: 
                        tuserpoints[user_id].append([datetime.datetime.now().strftime("%Y-%m-%d %H"), average])
                        await self.sqlsave()
                    else: tuserpoints[user_id] = [[datetime.datetime.now().strftime("%Y-%m-%d %H"), average]]
                    await message.channel.send(embed = discord.Embed(title=f"YOUR FINAL SCORE IS {average}", description=f"* Because you scored **{takingtest[user_id]}** on the three games\n * go to **<#1273716188840591413>** to FLEX your score\n * **Practice More and come back tomorrow to take another test**", color=discord.Color.yellow()))
                    if user_id in takingtest: del takingtest[user_id]
                    if user_id in activeusers: del activeusers[user_id]
                else:
                    if user_id in muserpoints: 
                        muserpoints[user_id].append([datetime.datetime.now().strftime("%Y-%m-%d %H"), max(level - 1 , 1)])
                        await self.sqlsave()
                    if user_id not in needtotest:
                        eligiblefortest.append(user_id)
                        await message.channel.send(embed = discord.Embed(title=f'**Now that youve done some practice today, type "test" to see if youve imporved overall**', color=discord.Color.yellow()))
                        await asyncio.sleep(6)
                    await asyncio.sleep(3)
                    if user_id in activeusers: await self.puzzlememory(message, user_id, 0)
            async def up_button_callback(interaction: discord.Interaction):
                if activeusers[user_id] != "free":
                    try:
                        if muserindex[user_id][0][muserindex[user_id][1]] == "up": await getscorrect(interaction, "↑")
                        else: raise ValueError
                    except: await getswrong(interaction)
            async def down_button_callback(interaction: discord.Interaction):
                if activeusers[user_id] != "free":
                    try:
                        if muserindex[user_id][0][muserindex[user_id][1]] == "down": await getscorrect(interaction, "↓")
                        else: raise ValueError
                    except: await getswrong(interaction)
            async def right_button_callback(interaction: discord.Interaction):
                if activeusers[user_id] != "free":
                    try:
                        if muserindex[user_id][0][muserindex[user_id][1]] == "right": await getscorrect(interaction, "→")
                        else: raise ValueError
                    except: await getswrong(interaction)
            async def left_button_callback(interaction: discord.Interaction):
                if activeusers[user_id] != "free":
                    try:
                        if muserindex[user_id][0][muserindex[user_id][1]] == "left": await getscorrect(interaction, "←")
                        else: raise ValueError
                    except: await getswrong(interaction)
            up_button.callback = up_button_callback
            down_button.callback = down_button_callback
            right_button.callback = right_button_callback
            left_button.callback = left_button_callback
            went = await message.channel.send(embed=discord.Embed(title="Prepear to solve it...", description="-", color=discord.Color.green()), view=view)
            await asyncio.sleep(4)
            for i in range(3, 0, -1):
                if user_id not in activeusers: return
                await went.edit(embed=discord.Embed(title="Prepear to solve it...", description=f"**{i}..**", color=discord.Color.green()), view=view)
                await asyncio.sleep(0.9)
        if user_id not in activeusers: return
        with open(f'mazebordered{user_id}.png', 'rb') as file:
            embed = discord.Embed(title='**Navigate the maze** *(use "exit" to quit)*', color=discord.Color.orange())
            embed.set_image(url=f"attachment://mazebordered{user_id}.png")
            await first_msg.edit(content=None, embed=embed, attachments=[discord.File(file, filename=f'mazebordered{user_id}.png')])
        view.add_item(left_button)
        view.add_item(up_button)
        view.add_item(down_button)
        view.add_item(right_button)
        await went.edit(embed=discord.Embed(title="Solve it", description=f"~", color=discord.Color.green()), view=view)
    def get_highest_score(self, user_data):
            return max(user_data, key=lambda point: point[1])[1]
    async def leaderboard(self, message):
        global vuserpoints, iuserpoints, muserpoints, tuserpoints
        highest_scores = {user_id: self.get_highest_score(user_data) for user_id, user_data in vuserpoints.items()}
        sorted_users = sorted(highest_scores.items(), key=lambda item: item[1], reverse=True)[:10]
        leaderboard_embed = discord.Embed(title="Visual Group's Leaderboard", color=discord.Color.green())
        for rank in range(1, 11):
            try:
                if rank <= len(sorted_users):
                    user_id, score = sorted_users[rank - 1]
                    user = message.guild.get_member(user_id) or await message.guild.fetch_member(user_id)
                    username = user.display_name if user else "Unknown"
                    if rank == 1: leaderboard_embed.add_field(name=f"🥇{rank}: {username} Level {score}", value="", inline=False)
                    elif rank == 2: leaderboard_embed.add_field(name=f"🥈{rank}: {username} Level {score}", value="", inline=False)
                    elif rank == 3: leaderboard_embed.add_field(name=f"🥉{rank}: {username} Level {score}", value="", inline=False)
                    else: leaderboard_embed.add_field(name=f"**{rank}: {username}** Level **{score}**", value="", inline=False)
                else:
                    if rank == 1: leaderboard_embed.add_field(name=f"🥇{rank}: Unclaimed spot", value="", inline=False)
                    elif rank == 2: leaderboard_embed.add_field(name=f"🥈{rank}: Unclaimed spot", value="", inline=False)
                    elif rank == 3: leaderboard_embed.add_field(name=f"🥉{rank}: Unclaimed spot", value="", inline=False)
                    else: leaderboard_embed.add_field(name=f"{rank}: Unclaimed spot", value="", inline=False)
            except: continue
        await message.channel.send(embed=leaderboard_embed)
        highest_scores = {user_id: self.get_highest_score(user_data) for user_id, user_data in iuserpoints.items()}
        sorted_users = sorted(highest_scores.items(), key=lambda item: item[1], reverse=True)[:10]
        leaderboard_embed = discord.Embed(title="Identification Group's Leaderboard", color=discord.Color.blue())
        for rank in range(1, 11):
            try:
                if rank <= len(sorted_users):
                    user_id, score = sorted_users[rank - 1]
                    user = message.guild.get_member(user_id) or await message.guild.fetch_member(user_id)
                    username = user.display_name if user else "Unknown"
                    if rank == 1: leaderboard_embed.add_field(name=f"🥇{rank}: {username} Level {score}", value="", inline=False)
                    elif rank == 2: leaderboard_embed.add_field(name=f"🥈{rank}: {username} Level {score}", value="", inline=False)
                    elif rank == 3: leaderboard_embed.add_field(name=f"🥉{rank}: {username} Level {score}", value="", inline=False)
                    else: leaderboard_embed.add_field(name=f"**{rank}: {username}** Level **{score}**", value="", inline=False)
                else:
                    if rank == 1: leaderboard_embed.add_field(name=f"🥇{rank}: Unclaimed spot", value="", inline=False)
                    elif rank == 2: leaderboard_embed.add_field(name=f"🥈{rank}: Unclaimed spot", value="", inline=False)
                    elif rank == 3: leaderboard_embed.add_field(name=f"🥉{rank}: Unclaimed spot", value="", inline=False)
                    else: leaderboard_embed.add_field(name=f"{rank}: Unclaimed spot", value="", inline=False)
            except: continue
        await message.channel.send(embed=leaderboard_embed)
        highest_scores = {user_id: self.get_highest_score(user_data) for user_id, user_data in muserpoints.items()}
        sorted_users = sorted(highest_scores.items(), key=lambda item: item[1], reverse=True)[:10]
        leaderboard_embed = discord.Embed(title="Puzzle Group's Leaderboard", color=discord.Color.orange())
        for rank in range(1, 11):
            try:
                if rank <= len(sorted_users):
                    user_id, score = sorted_users[rank - 1]
                    user = message.guild.get_member(user_id) or await message.guild.fetch_member(user_id)
                    username = user.display_name if user else "Unknown"
                    if rank == 1: leaderboard_embed.add_field(name=f"🥇{rank}: {username} Level {score}", value="", inline=False)
                    elif rank == 2: leaderboard_embed.add_field(name=f"🥈{rank}: {username} Level {score}", value="", inline=False)
                    elif rank == 3: leaderboard_embed.add_field(name=f"🥉{rank}: {username} Level {score}", value="", inline=False)
                    else: leaderboard_embed.add_field(name=f"**{rank}: {username}** Level **{score}**", value="", inline=False)
                else:
                    if rank == 1: leaderboard_embed.add_field(name=f"🥇{rank}: Unclaimed spot", value="", inline=False)
                    elif rank == 2: leaderboard_embed.add_field(name=f"🥈{rank}: Unclaimed spot", value="", inline=False)
                    elif rank == 3: leaderboard_embed.add_field(name=f"🥉{rank}: Unclaimed spot", value="", inline=False)
                    else: leaderboard_embed.add_field(name=f"{rank}: Unclaimed spot", value="", inline=False)
            except: continue
        await message.channel.send(embed=leaderboard_embed)
        highest_scores = {user_id: self.get_highest_score(user_data) for user_id, user_data in tuserpoints.items()}
        sorted_users = sorted(highest_scores.items(), key=lambda item: item[1], reverse=True)[:10]
        leaderboard_embed = discord.Embed(title="Standardized Test's Leaderboard", color=discord.Color.light_gray())
        for rank in range(1, 11):
            try:
                if rank <= len(sorted_users):
                    user_id, score = sorted_users[rank - 1]
                    try: user = message.guild.get_member(user_id) or await message.guild.fetch_member(user_id)
                    except:
                        if rank == 1: leaderboard_embed.add_field(name=f"🥇{rank}: Unclaimed spot", value="", inline=False)
                        elif rank == 2: leaderboard_embed.add_field(name=f"🥈{rank}: Unclaimed spot", value="", inline=False)
                        elif rank == 3: leaderboard_embed.add_field(name=f"🥉{rank}: Unclaimed spot", value="", inline=False)
                        else: leaderboard_embed.add_field(name=f"{rank}: Unclaimed spot", value="", inline=False)
                    username = user.display_name if user else "Unknown"
                    if rank == 1: leaderboard_embed.add_field(name=f"🥇{rank}: {username} Scored {score}", value="", inline=False)
                    elif rank == 2: leaderboard_embed.add_field(name=f"🥈{rank}: {username} Scored {score}", value="", inline=False)
                    elif rank == 3: leaderboard_embed.add_field(name=f"🥉{rank}: {username} Scored {score}", value="", inline=False)
                    else: leaderboard_embed.add_field(name=f"{rank}: {username} Scored {score}", value="", inline=False)
                else:
                    if rank == 1: leaderboard_embed.add_field(name=f"🥇{rank}: Unclaimed spot", value="", inline=False)
                    elif rank == 2: leaderboard_embed.add_field(name=f"🥈{rank}: Unclaimed spot", value="", inline=False)
                    elif rank == 3: leaderboard_embed.add_field(name=f"🥉{rank}: Unclaimed spot", value="", inline=False)
                    else: leaderboard_embed.add_field(name=f"{rank}: Unclaimed spot", value="", inline=False)
            except: continue
        await message.channel.send(embed=leaderboard_embed)
    async def display_profile(self, message):
        global vuserpoints, iuserpoints, muserpoints, tuserpoints
        user_id = message.author.id
        if (any(role.id in {1274997621441822730, 1274997818540560417} for role in message.author.roles)) or (user_id in vuserpoints):
            highest_scores = {user_id: self.get_highest_score(user_data) for user_id, user_data in vuserpoints.items()}
            embed = discord.Embed(title=f"{message.author.display_name}'s Visual Group Profile", color=discord.Color.green())
            if user_id in vuserpoints:
                user_score = max(entry[1] for entry in vuserpoints[user_id]) 
                embed.set_thumbnail(url=message.author.avatar.url)
                embed.add_field(name="Games Played", value=str(len(vuserpoints[user_id]) - 1), inline=True)
                embed.add_field(name="Current HighScore", value=str(user_score), inline=True)
                embed.add_field(name="Percentile", value=f"{(100-(sum(1 for score in highest_scores.values() if score > user_score) / len(highest_scores) * 100)):.2f}%", inline=True)
            else:
                embed.set_thumbnail(url=message.author.avatar.url)
                embed.add_field(name="Games Played", value="0", inline=True)
                embed.add_field(name="Current HighScore", value="1", inline=True)
                embed.add_field(name="Percentile", value="N/A%", inline=True)
            await message.channel.send(embed=embed)
        if (any(role.id in {1274997676018110464, 1274997818540560417} for role in message.author.roles)) or (user_id in iuserpoints):
            embed = discord.Embed(title=f"{message.author.display_name}'s Profile",color=discord.Color.blue())
            highest_scores = {user_id: self.get_highest_score(user_data) for user_id, user_data in iuserpoints.items()}
            if user_id in iuserpoints:
                user_score = max(entry[1] for entry in iuserpoints[user_id])
                embed.set_thumbnail(url=message.author.avatar.url)
                embed.add_field(name="Level", value=str(iuserpoints[user_id][-1][1]), inline=True)
                embed.add_field(name="Games Played", value=str(len(iuserpoints[user_id])), inline=True)
                embed.add_field(name="Max Level Achieved", value=str(user_score), inline=True)
                embed.add_field(name="Percentile", value=f"{(100-(sum(1 for score in highest_scores.values() if score > user_score) / len(highest_scores) * 100)):.2f}%", inline=True)
            else:
                embed.set_thumbnail(url=message.author.avatar.url)
                embed.add_field(name="Level", value="1", inline=True)
                embed.add_field(name="Games Played", value="0", inline=True)
                embed.add_field(name="Max Level Achieved", value="0", inline=True)
                embed.add_field(name="Percentile", value=f"N/A%", inline=True)
            embed.set_footer(text="Game created by Apolloiscool. Github: https://github.com/Ubuntufanboy")
            await message.channel.send(embed=embed)
        if (any(role.id in {1274997790673473596, 1274997818540560417} for role in message.author.roles)) or (user_id in muserpoints):
            highest_scores = {user_id: self.get_highest_score(user_data) for user_id, user_data in muserpoints.items()}
            embed = discord.Embed(title=f"{message.author.display_name}'s Puzzle Group Profile", color=discord.Color.orange())
            if user_id in muserpoints:
                user_score = max(entry[1] for entry in muserpoints[user_id])
                embed.set_thumbnail(url=message.author.avatar.url)
                embed.add_field(name="Games Played", value=str(len(muserpoints[user_id])-1), inline=True)
                embed.add_field(name="Highest Level Achieved", value=str(max(entry[1] for entry in muserpoints[user_id])), inline=True)
                embed.add_field(name="Current Level", value=str(muserpoints[user_id][-1][1]), inline=True)
                embed.add_field(name="Percentile", value=f"{(100-(sum(1 for score in highest_scores.values() if score > user_score) / len(highest_scores) * 100)):.2f}%", inline=True)
            else:
                embed.set_thumbnail(url=message.author.avatar.url)
                embed.add_field(name="Games Played", value="0", inline=True)
                embed.add_field(name="Highest Level Achieved", value="0", inline=True)
                embed.add_field(name="Current Level", value="1", inline=True)
                embed.add_field(name="Percentile", value=f"N/A%", inline=True)
            embed.set_footer(text="Play more games to improve your Stats")
            await message.channel.send(embed=embed)
        highest_scores = {user_id: self.get_highest_score(user_data) for user_id, user_data in tuserpoints.items()}
        embed = discord.Embed(title=f"{message.author.display_name}'s Standardized Test Profile", color=discord.Color.light_gray())
        if user_id in tuserpoints:
            user_score = max(entry[1] for entry in tuserpoints[user_id])
            embed.set_thumbnail(url=message.author.avatar.url)
            embed.add_field(name="Tests Taken", value=str(len(tuserpoints[user_id])-1), inline=True)
            embed.add_field(name="Highest Score Achieved", value=str(max(entry[1] for entry in tuserpoints[user_id])), inline=True)
            embed.add_field(name="Percentile", value=f"{(100-(sum(1 for score in highest_scores.values() if score > user_score) / len(highest_scores) * 100)):.2f}%", inline=True)
        else:
            embed.set_thumbnail(url=message.author.avatar.url)
            embed.add_field(name="Games Played", value="0", inline=True)
            embed.add_field(name="Highest Level Achieved", value="0", inline=True)
            embed.add_field(name="Percentile", value=f"N/A%", inline=True)
        embed.set_footer(text="Play more games to improve your Stats")
        await message.channel.send(embed=embed)
    async def runtest(self, message, user_id):
        global takingtest
        await message.channel.send(embed = discord.Embed(title="**Starting Test**", description=f"* **Here's how it'll work**\n * you will play all 3 games (Visual, Identification, and Puzzle)\n * If you fail once in any game it'll be onto the next\n * your scores will be averaged and that'll be how you've preformed\n **GOOD LUCK**", color=discord.Color.yellow()))
        await asyncio.sleep(10)
        needtotest.append(user_id)
        eligiblefortest.remove(user_id)
        takingtest[user_id] = []
        activeusers[user_id] = "test"
        await self.visualmemory(message, message.author.id, 1)
    async def idgame(self, message, user_id, route, testlevel):
        global activeusers, needtotest, eligiblefortest, takingtest, iuserindex, waitingresponse, iuserpoints
        activeusers[user_id] = "id"
        if route:
            if (user_id in iuserpoints) or (user_id in tuserpoints) or (testlevel >= 2):
                if user_id in takingtest:
                    level_num = testlevel
                else:
                    try:
                        level_num = iuserpoints[user_id][-1][1]
                    except: 
                        iuserpoints[user_id] = [[datetime.datetime.now().strftime("%Y-%m-%d %H"), 1]]
                        level_num = iuserpoints[user_id][-1][1]
            else:
                await tutorial(message)
                level_num = 1
                if (any(role.id in {1274997818540560417, 1274997676018110464} for role in message.author.roles)): iuserpoints[user_id] = [[datetime.datetime.now().strftime("%Y-%m-%d %H"), 1]]
            if user_id not in activeusers: return
            if user_id in takingtest: embed = discord.Embed(title="Game Start! (Test mode)", description=f"You are on level **{level_num}**", color=discord.Color.blue())
            else: embed = discord.Embed(title="Game Start! (Elo mode)", description=f"You are on level **{level_num}**", color=discord.Color.blue())
            await message.channel.send(embed=embed)
            await asyncio.sleep(1)
            if user_id not in activeusers: return
            filenames = make_gif(level_num, user_id)
            embed = discord.Embed(title=f"Identification Game! level **{level_num}**", description="Watch the GIF and remember the order of images!", color=discord.Color.blue())
            embed.set_image(url=f"attachment://output{user_id}.gif")
            gif_message = await message.channel.send(embed=embed, file=discord.File(f'output{user_id}.gif'))
            await asyncio.sleep(3 + (2 + level_num // 3) / 2 + 3)
            if user_id not in activeusers: return
            await gif_message.delete()
            filenames = filenames[6:-8]
            correct = random.choice(filenames)
            shutil.copy(correct, "correct.png")
            newfilenames = filenames.copy()
            newfilenames[newfilenames.index(correct)] = "correct.png"
            make_img(newfilenames, user_id)
            waitingresponse[user_id] = [level_num, testlevel, filenames.index(correct) + 1]
            embed = discord.Embed(title="Question", description='What order did this image appear in? *(use "exit" to quit)*', color=discord.Color.blue())
            embed.set_image(url="attachment://correct.png")
            if user_id not in activeusers: return
            await message.channel.send(embed=embed, file=discord.File(correct, filename="correct.png"))
        else:
            testlevel2 = waitingresponse[user_id][1]
            if testlevel2 >= 1: level_num = testlevel2
            else: level_num = waitingresponse[user_id][0]
            try:
                correct_guess = waitingresponse[user_id][2] == int(message.content)
                result_text = "Correct!" if correct_guess else f"Incorrect! The correct position was {waitingresponse[user_id][2]}."
                extra = "" if correct_guess else f"**Level {level_num} --> {max(1, level_num - 1)}**"
                embed = discord.Embed(title="Result", description=f"User guessed {message.content}! {result_text} {extra}", color=discord.Color.blue())
                embed.set_image(url=f"attachment://final_image{user_id}.png")
                activeusers[user_id] = "free"
                del waitingresponse[user_id]
                await message.channel.send(embed=embed, file=discord.File(f"final_image{user_id}.png", filename=f"final_image{user_id}.png"))
                await asyncio.sleep(3)
                if correct_guess:
                    if testlevel2 >= 1:
                        await self.idgame(message, user_id, True, testlevel2+1)
                    else:
                        if user_id in iuserpoints: 
                            iuserpoints[user_id].append([datetime.datetime.now().strftime("%Y-%m-%d %H"), level_num+1])
                            await self.sqlsave()
                        await self.idgame(message, user_id, True, 0)
                else:
                    if testlevel2 >= 1:
                        takingtest[user_id].append(testlevel2)
                        await message.channel.send(embed = discord.Embed(title=f"**That's 2/3 games and you scored {level_num}**\n Now moving onto game 3", color=discord.Color.yellow()))
                        await asyncio.sleep(4)
                        await self.puzzlememory(message, message.author.id, 1)
                    else:
                        if user_id in iuserpoints: 
                            iuserpoints[user_id].append([datetime.datetime.now().strftime("%Y-%m-%d %H"), max(level_num-1, 1)])
                            await self.sqlsave()
                        if user_id not in needtotest:
                            eligiblefortest.append(user_id)
                            await message.channel.send(embed = discord.Embed(title=f'**Now that youve done some practice today, type "test" to see if youve imporved overall**', color=discord.Color.yellow()))
                            await asyncio.sleep(6)
                        await asyncio.sleep(3)
                        if user_id in activeusers: await self.idgame(message, user_id, True, 0)
            except: pass
    async def sqlsave(self):
        global conn, cursor, activeusers, vuserpoints, muserpoints, tuserpoints, iuserpoints, rooms
        for key, value in vuserpoints.items():
            cursor.execute('INSERT OR REPLACE INTO vuserpoints (key, value) VALUES (?, ?)', (key, json.dumps(value)))
        for key, value in iuserpoints.items():
            cursor.execute('INSERT OR REPLACE INTO iuserpoints (key, value) VALUES (?, ?)', (key, json.dumps(value)))
        for key, value in muserpoints.items():
            cursor.execute('INSERT OR REPLACE INTO muserpoints (key, value) VALUES (?, ?)', (key, json.dumps(value)))
        for key, value in tuserpoints.items():
            cursor.execute('INSERT OR REPLACE INTO tuserpoints (key, value) VALUES (?, ?)', (key, json.dumps(value)))
        for item in rooms:
            cursor.execute('INSERT OR REPLACE INTO rooms (item) VALUES (?)', (json.dumps(item),))
        conn.commit()
    @commands.Cog.listener()
    async def on_message(self, message):
        global activeusers, needtotest, eligiblefortest, waitingresponse, vuserpoints, muserpoints, rooms, iuserpoints, tuserpoints, takingtest
        content = message.content.lower()
        if (content in {"play", "play vis", "play visual", "play puzzle", "play maze", "play id", "play identification"}) and (message.author.id in activeusers) and (message.channel.id != 1273716188840591413):
            await message.channel.send(embed=discord.Embed(title="Error", description="You're already playing a game", color=discord.Color.red()))
        if (message.content == "resettest") and (any(role.id == 1274954632346468362 for role in message.author.roles)):
            needtotest = []
            await message.channel.send(embed=discord.Embed(title="Now asking all users to take a Test", color=discord.Color.yellow()))
        if (content in {"test", "play test"}) and (message.author.id not in eligiblefortest):
            await message.channel.send(embed=discord.Embed(title="**You haven't fit todays requirements to run a test**", description=f'**This is fine**, just play a single game to practice then once you lose do "test" again to play one', color=discord.Color.yellow()))
        if (content in {"test", "play test"}) and (message.author.id in eligiblefortest):
            if message.author.id in activeusers: del activeusers[message.author.id]
            if message.author.id in takingtest: del takingtest[message.author.id]
            await self.runtest(message, message.author.id)
        if (content in {"play visual", "play", "play vis"}) and (any(role.id == 1274997621441822730 for role in message.author.roles)) and (message.author.id not in activeusers) and (message.channel.id != 1273716188840591413):
            await self.visualmemory(message, message.author.id, 1)
        if (content in {"play puzzle", "play maze", "play"}) and (any(role.id == 1274997790673473596 for role in message.author.roles)) and (message.author.id not in activeusers) and (message.channel.id != 1273716188840591413):
            await self.puzzlememory(message, message.author.id, 0)
        if (content in acceptable) and (message.author.id in waitingresponse):
            await self.idgame(message, message.author.id, False, 0)
        if (content in {"play id", "play identification", "play"}) and (any(role.id == 1274997676018110464 for role in message.author.roles)) and (message.author.id not in activeusers) and (message.channel.id != 1273716188840591413):
            await self.idgame(message, message.author.id, True, 0)
        if (content in {"play visual", "play vis"}) and (any(role.id == 1274997818540560417 for role in message.author.roles)) and (message.author.id not in activeusers) and (message.channel.id != 1273716188840591413):
            await self.visualmemory(message, message.author.id, 1)
        if (content in {"play id", "play identification"}) and (any(role.id == 1274997818540560417 for role in message.author.roles)) and (message.author.id not in activeusers) and (message.channel.id != 1273716188840591413):
            await self.idgame(message, message.author.id, True, 0)
        if (content in {"play puzzle", "play maze"}) and (any(role.id == 1274997818540560417 for role in message.author.roles)) and (message.author.id not in activeusers) and (message.channel.id != 1273716188840591413):
            await self.puzzlememory(message, message.author.id, 0)
        if (content == "play") and (any(role.id == 1274997818540560417 for role in message.author.roles)) and (message.author.id not in activeusers) and (message.channel.id != 1273716188840591413):
            await message.channel.send(embed=discord.Embed(title="Specify Game", description='**type "play" then "visual" or "id" or "maze" to practice any game of your choosing**', color=discord.Color.purple()))
        if (content in {"exit", "leave", "quit", "stop"}) and (message.author.id in activeusers):
            if message.author.id in takingtest: 
                del takingtest[message.author.id]
                await message.channel.send(embed=discord.Embed(title="Exited Game", description="Be careful when leaving inside a game, your scores may drop or not be recorded", color=discord.Color.red()))
            elif (activeusers[message.author.id] == "id") and (message.author.id in iuserpoints): 
                iuserpoints[message.author.id].append([datetime.datetime.now().strftime("%Y-%m-%d %H"), max(iuserpoints[message.author.id][-1][1]-1, 1)])
                await message.channel.send(embed=discord.Embed(title="Exited Game", description="Be careful when leaving inside a game, your scores may drop or not be recorded", color=discord.Color.red()))
            elif (activeusers[message.author.id] == "maze") and (message.author.id in muserpoints): 
                muserpoints[message.author.id].append([datetime.datetime.now().strftime("%Y-%m-%d %H"), max(muserpoints[message.author.id][-1][1]-1, 1)])
                await message.channel.send(embed=discord.Embed(title="Exited Game", description="Be careful when leaving inside a game, your scores may drop or not be recorded", color=discord.Color.red()))
            else: await message.channel.send(embed=discord.Embed(title="Exited Game", description="Play again whenever", color=discord.Color.red()))
            del activeusers[message.author.id]
        if content in {"about", "info"}:
            await message.channel.send(embed=discord.Embed(title="**Here's some info about the event**", description=f'* there are 4 groups: Visual, Identification, Puzzle, and Combine. Each group can play their respective game but the Combine group can play all.\n * the goal of this experiment is to track what makes peoples memory improve using various practices. \n * every day during September, go to your channel and say "play" to play your respective game.\n * the more you practice, the more you help out the experiment.\n * after some games, you will be asked to take a test by saying "test". This is to track your general memory progress.\n * I will be giving out money for the people who place the highest in each category, view #welcome for more info * PLEASE DON\'T CHEAT, this experiment is much more fun if everyone plays fairly.\n * use the command "stats" to see how well you have been performing in your games and tests.', color=discord.Color.yellow()))
        if content in {"profile", "stats", "level"}:
            await self.display_profile(message)
        if content in {"leaderboard", "rank", "leader board", "lb", "ranking"}:
            await self.leaderboard(message)
        if (message.content.startswith('aiduser')):
            tuserpoints[616745165180108814].append([datetime.datetime.now().strftime("%Y-%m-%d %H"), 27])
            await self.sqlsave()
        if (message.content.startswith('makemaze')):
            Maze.save_mazes('test', 30)
            with open(f'mazetest.png', 'rb') as file:
                await message.channel.send(file=discord.File(file, 'mazetest.png'))
            with open(f'mazeborderedtest.png', 'rb') as file:
                await message.channel.send(file=discord.File(file, 'mazeborderedtest.png'))

async def tutorial(message):
    tutorial_embed = discord.Embed(title="Welcome to the Identification Memory Game Tutorial!", description="In this game, you'll be shown a series of images in a GIF. Your task is to remember the order in which they appear.", color=discord.Color.blue())
    tutorial_embed.set_image(url="attachment://assets\tutorial.gif")
    tutorial_message = await message.channel.send(embed=tutorial_embed, file=discord.File(r"assets\tutorial.gif", filename=r"rassets\tutorial.gif"))
    await asyncio.sleep(9)
    await tutorial_message.delete()
    await asyncio.sleep(1)

def create_video(image_files, output_file, fps=2, size=(640, 480)):
    assert len(image_files) != 0, "No images provided for video creation"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, size)
    for image_file in image_files:
        img = cv2.imread(image_file)
        if img is None:
            print(f"Error: Could not read image {image_file}")
            continue
        img_resized = cv2.resize(img, size)
        out.write(img_resized)
    out.release()
    print(f"Video saved as {output_file}")

def make_gif(level, user_id):
    selected = []
    while len(selected) < 2 + level // 3:
        num = random.randint(0, 93)
        if num not in selected:
            selected.append(num)
    count = [r"assets\count3.png", r"assets\count3.png", r"assets\count2.png", r"assets\count2.png", r"assets\count1.png", r"assets\count1.png"]
    filenames = [f"assets\\{num}.png" for num in selected]
    count.extend(filenames)
    filenames = count
    for i in range(8):
        filenames.append(r"assets\white.png")
    create_video(filenames, "video.mp4")
    if os.path.exists("video.mp4"):
        print("Video creation successful. Now converting to GIF.")
        os.system(f"ffmpeg -y -i video.mp4 -pix_fmt rgb24 output{user_id}.gif")
    else:
        print("Video creation failed.")
    return filenames

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

if __name__ == "__main__":
    table_name = 'database.db'
    conn = sqlite3.connect(table_name)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS vuserpoints (key TEXT PRIMARY KEY, value INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS iuserpoints (key TEXT PRIMARY KEY, value INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS muserpoints (key TEXT PRIMARY KEY, value INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS tuserpoints (key TEXT PRIMARY KEY, value INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS rooms (item TEXT PRIMARY KEY)')
    def query_table(table_name):
        cursor.execute(f'SELECT * FROM {table_name}')
        rows = cursor.fetchall()
        temp = {}
        for row in rows:
            temp[int(row[0])] = json.loads(row[1])
        return temp
    def query_table_as_list(table_name):
        cursor.execute(f'SELECT * FROM {table_name}')
        rows = cursor.fetchall()
        temp = []
        for row in rows:
            print(f"Row data: {row[0]!r}")
            if row[0] and row[0].strip():
                try:
                    temp.append(json.loads(row[0]))
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON for row: {row[0]} - {e}")
            else:
                print(f"Empty or invalid data found in row: {row}")
        return temp
    vuserpoints = query_table('vuserpoints')
    iuserpoints = query_table('iuserpoints')
    muserpoints = query_table('muserpoints')
    tuserpoints = query_table('tuserpoints')
    rooms = query_table_as_list('rooms')
    intents = discord.Intents.default()
    intents.message_content = True
    intents.reactions = True
    intents.guilds = True
    intents.members = True
    client = Client(intents=intents)
    client.run(TOKEN)
