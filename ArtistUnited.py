#The_Glit-ch#4859
#https://github.com/The-Glit-ch
#4/4/21
#<----->

from itertools import count
from typing import List
import discord, json, os, uuid, asyncio
from discord.abc import PrivateChannel, User
from discord.colour import Color
from discord.embeds import Embed
#<----->
from discord.ext import commands
from discord.errors import *
from discord.ext.commands.errors import NotOwner
from discord.flags import fill_with_flags
from discord.user import Profile

#Vars
Key = ""
__author__ = 557339295325880320

ProfilesDir = os.path.abspath(__file__).replace("\ArtistUnited.py","\Profiles")
CommsDir = os.path.abspath(__file__).replace("\ArtistUnited.py","\Comms")

CommsLimit = 2
pre = "*au "
rating = "0-5"
ratingLow = 0
ratingHigh = 5

bot = commands.Bot(command_prefix=pre)
bot.remove_command("help")


@bot.event
async def on_ready():
    print('Logged in as: ' + bot.user.name)
    print('Ready!\n')
    global NewCommissionsChannel
    global RatingChannel
    RatingChannel = bot.get_channel(828822238990958613) 
    NewCommissionsChannel = bot.get_channel(828705404669132871)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{pre}help"))

@bot.event
async def on_message(message):
    if message.channel.id == 828705378753445889:
        await bot.process_commands(message)

@bot.command(aliases=['newprofile','np'])
async def newProfile(ctx):
    if os.path.exists(f"{ProfilesDir}\{ctx.author.id}.json") == False:
        Embed = discord.Embed(title="Profile Creation",description = f"Hello {ctx.author}. Making a AU profile is simple, simply give yourself bio and I'll handle the rest\nEx:\n```\nHello, I'm [Name]\nI do [Thing],[Thing2],[Thing3] art\nContact me here on discord or [other contact]\n```",color = discord.Colour.red())
        await ctx.author.send(embed=Embed)
        await ctx.author.send("Please type your Bio")
        msg = await bot.wait_for("message",check=lambda message: message.author == ctx.author)
        await ctx.author.send(f"Great! If you wish to edit your profile type ``{pre}edit``")
        newProfile = open(f"{ProfilesDir}\{ctx.author.id}.json","a")
        Data = {
            "Bio":str(msg.content).replace("```",""),
            "UserRatings": [0],
            "Comms": [],
            "AcceptedComms": []
        }
        json.dump(Data,newProfile)
        newProfile.close()
        await ctx.author.send(f"Your account has been made. Type ``{pre}profile`` to check it out")
    else:
        await ctx.send(f"It looks like you already made a profile. Type ``{pre}profile`` to see your profile and ``{pre}editProfile`` to edit your profile")

@bot.command(aliases=['Profile'])
async def profile(ctx,member:discord.Member=None):
    if member != None:
        author = member
    else:
        author = ctx.author

    if member != None:
        if os.path.exists(f"{ProfilesDir}\{member.id}.json") == True:
            with open(f"{ProfilesDir}\{member.id}.json","r") as ProfileJSONFile:
                JSON = json.load(ProfileJSONFile)
                Bio = JSON["Bio"]
                CommsStr = await getComms(JSON)
                Rounded,Decimal = await calcRatings(JSON)
                if member.id != __author__:
                    Embed = discord.Embed(title=f"{author}'s profile",description = f"Bio:```\n{Bio}\n```\nUser Ratings\nRounded: ```cal\n{Rounded}\n```\nExact: ```cal\n{Decimal}\n```\nCurrent Commissions:\n```{CommsStr}```\n",color = discord.Color.red())
                    await ctx.send(embed=Embed)
                else:
                    Embed = discord.Embed(title=f"{author}'s profile",description = f"Bio:```\n{Bio}\n```\nUser Ratings\nRounded: ```cal\n{Rounded}\n```\nExact: ```cal\n{Decimal}\n```\nCurrent Commissions:\n```{CommsStr}```\n",color = discord.Color.red()).set_footer(text="Artist Unite Devloper")
                    await ctx.send(embed=Embed)
        else:
            await ctx.send(f"It appears that {member} dosent have a profile")
    else:
        if os.path.exists(f"{ProfilesDir}\{ctx.author.id}.json") == True:
            with open(f"{ProfilesDir}\{ctx.author.id}.json","r") as ProfileJSONFile:
                JSON = json.load(ProfileJSONFile)
                Bio = JSON["Bio"]
                CommsStr = await getComms(JSON)
                Rounded,Decimal = await calcRatings(JSON)
                if ctx.author.id != __author__:
                    Embed = discord.Embed(title=f"{author}'s profile",description = f"Bio:```\n{Bio}\n```\nUser Ratings\nRounded: ```cal\n{Rounded}\n```\nExact: ```cal\n{Decimal}\n```\nCurrent Commissions:\n```{CommsStr}```\n",color = discord.Color.red())
                    await ctx.send(embed=Embed)
                else:
                    Embed = discord.Embed(title=f"{author}'s profile",description = f"Bio:```\n{Bio}\n```\nUser Ratings\nRounded: ```cal\n{Rounded}\n```\nExact: ```cal\n{Decimal}\n```\nCurrent Commissions:\n```{CommsStr}```\n",color = discord.Color.red()).set_footer(text="Artist Unite Devloper")
                    await ctx.send(embed=Embed)
        else:
            await ctx.send(f"It appears that you dont have a profile. To make a profile type ``{pre}newProfile``")

@bot.command(aliases=['working'])
async def working_on(ctx,member:discord.Member=None):
    if member != None:
        author = member
    else:
        author = ctx.author

    if os.path.exists(f"{ProfilesDir}\{author.id}.json") == True:
        with open(f"{ProfilesDir}\{author.id}.json","r") as ProfileJSONFile:
            JSON = json.load(ProfileJSONFile)
            Comms = await getAcceptedComms(JSON)
            print(Comms)
            Embed = discord.Embed(title=f"{author}'s accepted commissions",description=f"```{Comms}```")
            await ctx.send(embed=Embed)
    else:
        await ctx.send(f"It appears that {member} dosent have a profile")

@bot.command(aliases=['editprofile'])
async def editProfile(ctx):
    if os.path.exists(f"{ProfilesDir}\{ctx.author.id}.json") == True:
        author = ctx.author

        Embed = discord.Embed(title="Current edit options",description="Delete -Deletes your profile\nBio -Edits your bio",color=discord.Colour.red())
        await author.send("Please select one of the options below",embed=Embed)
        RawInput = await bot.wait_for("message",check=lambda message: message.author == ctx.author)
        CleanInput = str(RawInput.content)
        
        if CleanInput.lower() == "delete":
            await author.send("Are you sure you want to delete your profile? All your commisions would be deleted. Reply with ``yes`` or ``no``")
            RawInput = await bot.wait_for("message",check=lambda message: message.author == ctx.author)
            CleanInput = str(RawInput.content)
            if CleanInput.lower() == "yes":
                with open(f"{ProfilesDir}\{author.id}.json","r") as ProfileJSONFile:
                    JSONProfile = json.load(ProfileJSONFile)
                    List = JSONProfile["Comms"]
                    Count = 0
                    if len(List) > 0:
                        if len(List) > 1:
                            for i in List:
                                Count = Count + 1
                                CommsFile = open(f"{CommsDir}\{i}","r")
                                CommsJSON = json.load(CommsFile)
                                if CommsJSON["ClaimInfo"]["IsClaimed"] != False:
                                    ID = CommsJSON["ClaimInfo"]["ClaimedOwnerID"]
                                    User = await bot.fetch_user(ID)
                                    Owner = CommsJSON["Owner"]
                                    OwnerID = CommsJSON["OwnerID"]
                                    CommsDetails = CommsJSON["CommDetails"]
                                    CommsPrice = CommsJSON["CommPrice"]
                                    await User.send(f"Your claimed commission has been removed. Reason: Commission creator account deleted\n```\nCommission Owner Details:\n    Owner: {Owner}\n     -OwnerID: {OwnerID}\n\n  Commission Details: {CommsDetails}\nCommission Price: {CommsPrice}\n```")
                                    CommsFile.close()
                                    os.remove(f"{CommsDir}\{i}")
                                else:
                                    CommsFile.close()
                                    os.remove(f"{CommsDir}\{i}")
                            ProfileJSONFile.close()
                            os.remove(f"{ProfilesDir}\{author.id}.json")
                            await author.send("Profile deleted")       
                        else:
                            CommsFile = open(f"{CommsDir}\{List[0]}","r")
                            CommsJSON = json.load(CommsFile)
                            if CommsJSON["ClaimInfo"]["IsClaimed"] != False:
                                ID = CommsJSON["ClaimInfo"]["ClaimedOwnerID"]
                                User = await bot.fetch_user(ID)
                                Owner = CommsJSON["Owner"]
                                OwnerID = CommsJSON["OwnerID"]
                                CommsDetails = CommsJSON["CommDetails"]
                                CommsPrice = CommsJSON["CommPrice"]
                                await User.send(f"Your claimed commission has been removed. Reason: Commission creator account deleted\n```\nCommission Details:\n    Owner: {Owner}\n     -OwnerID: {OwnerID}\n\n  Commission Details: {CommsDetails}\n Commission Price: {CommsPrice}\n```")
                                CommsFile.close()
                                ProfileJSONFile.close()
                                os.remove(f"{CommsDir}\{List[0]}")
                                os.remove(f"{ProfilesDir}\{author.id}.json")
                                await author.send("Profile deleted")
                            else:
                                CommsFile.close()
                                ProfileJSONFile.close()
                                os.remove(f"{CommsDir}\{List[0]}")
                                os.remove(f"{ProfilesDir}\{author.id}.json")
                                await author.send("Profile deleted")
                    else:
                        ProfileJSONFile.close()
                        os.remove(f"{ProfilesDir}\{author.id}.json")
                        await author.send("Profile deleted")
            else:
                await author.send("Cancelling")
        else:
            await author.send("Please type in a new bio")
            RawInput = await bot.wait_for("message",check=lambda message: message.author == ctx.author)
            CleanInput = str(RawInput.content).replace("```","")
            with open(f"{ProfilesDir}\{author.id}.json","r") as ProfileJSONFile:
                JSON = json.load(ProfileJSONFile)
                ProfileJSONFile.close()
                with open(f"{ProfilesDir}\{author.id}.json","w") as ProfileJSONFile:
                    JSON["Bio"] = CleanInput
                    json.dump(JSON,ProfileJSONFile)
                    ProfileJSONFile.close()
            await author.send("Your profile has been edited and saved")
    else:
        await ctx.send("You need a profile to edit your profile...duh")

@bot.command(aliases=['newcommission','newcomm'])
async def newCommission(ctx,details,price):
    if os.path.exists(f"{ProfilesDir}\{ctx.author.id}.json") == True:
        with open(f"{ProfilesDir}\{ctx.author.id}.json","r") as ProfileJSONFile:
            UserProfileJSON = json.load(ProfileJSONFile)
            ProfileJSONFile.close()
        if str(price).isdecimal() != False:
            if len(UserProfileJSON["Comms"]) <= CommsLimit:
                NewUUID = uuid.uuid4()
                Data = {
                    "Owner": str(ctx.author),
                    "OwnerID": str(ctx.author.id),
                    "CommDetails": str(details),
                    "CommPrice": str(price),
                    "CommsID": str(NewUUID),
                    "ClaimInfo": {
                        "IsClaimed": False,
                        "ClaimedOwner": None,
                        "ClaimedOwnerID": None
                    }
                }
                UserProfileJSON["Comms"].append(f"{NewUUID}.json")
                open(f"{CommsDir}\{NewUUID}.json","a").close()
                with open(f"{ProfilesDir}\{ctx.author.id}.json","w") as ProfileJSONFile:
                    NewCommissionJSONFile = open(f"{CommsDir}\{NewUUID}.json","w")
                    json.dump(UserProfileJSON,ProfileJSONFile)
                    json.dump(Data,NewCommissionJSONFile)
                    NewCommissionJSONFile.close()
                    ProfileJSONFile.close()
                Details = Data["CommDetails"]
                Price = Data["CommPrice"]
                ID = Data["CommsID"]
                Embed = discord.Embed(title=f"New Commission by {ctx.author}",description=f"Details:```{Details}```\nPrice:```${Price}```\nID:```{ID}```", color = discord.Color.red())
                await ctx.send(f"Your commission had been made\n``ID: {NewUUID}``")
                await NewCommissionsChannel.send(embed=Embed)
            else:
                await ctx.send(f"You have made to many commisions. Type ``{pre}delcommission [commissionid]`` to delete a previous commission")
        else:
            await ctx.send('```newCommission "CommissionDetail" Price```\nArgument "Price" must be a __number__')
    else:
        await ctx.send(f"It appears that you dont have a profile. To make a profile type ``{pre}newProfile``")

@newCommission.error
async def newCommission_error(ctx, error):
    if "price" in str(error):
        await ctx.send('```newCommission "CommissionDetail" Price```\nMissing argument "Price"')
    else:
        await ctx.send('```newCommission "CommissionDetail" Price```\nMissing argument "CommissionDetail"')

@bot.command(aliases=['delcommission','delcomm'])
async def delCommission(ctx,id):
    if os.path.exists(f"{ProfilesDir}\{ctx.author.id}.json") == True:
        with open(f"{ProfilesDir}\{ctx.author.id}.json","r") as ReadOnlyProfile:
            PJSON = json.load(ReadOnlyProfile)
            ReadOnlyProfile.close()
            if len(PJSON["Comms"]) > 0:
                with open(f"{ProfilesDir}\{ctx.author.id}.json","w") as WriteOnlyProfile:
                    File = PJSON["Comms"][PJSON["Comms"].index(f"{id}.json")]
                    PJSON["Comms"].remove(f"{id}.json")
                    with open(f"{CommsDir}\{File}","r") as ReadOnlyComms:
                        CJSON = json.load(ReadOnlyComms)
                        ReadOnlyComms.close()
                        if CJSON["ClaimInfo"]["IsClaimed"] != False:
                            User = await bot.fetch_user(CJSON["ClaimInfo"]["ClaimedOwnerID"])
                            Owner = CJSON["Owner"]
                            OwnerID = CJSON["OwnerID"]
                            CommsDetails = CJSON["CommDetails"]
                            CommsPrice = CJSON["CommPrice"]
                            await User.send(f"Your claimed commission has been removed.\nReason: Commission creator deleted commission\n```\nCommission Owner Details:\n    Owner: {Owner}\n     -OwnerID: {OwnerID}\n\n  Commission Details: {CommsDetails}\nCommission Price: {CommsPrice}\n```")
                            json.dump(PJSON,WriteOnlyProfile)
                            os.remove(f"{CommsDir}\{File}")
                            WriteOnlyProfile.close()
                            await ctx.send("Commission deleted")
                        else:
                            json.dump(PJSON,WriteOnlyProfile)
                            os.remove(f"{CommsDir}\{File}")
                            WriteOnlyProfile.close()
                            await ctx.send("Commission deleted")
            else:
                await ctx.send("You don't have any commissions")
    else:
        await ctx.send(f"It appears that you dont have a profile. To make a profile type ``{pre}newProfile``")       

@delCommission.error
async def delCommission_error(ctx,error):
    if "id" in str(error):
        await ctx.send('```delCommission ID```\nMissing argument "ID"')
    else:
        await ctx.send("Invalid ID")

@bot.command(aliases=['claimcommission','claimcomm','claim'])
async def claimCommission(ctx,id):
    if os.path.exists(f"{ProfilesDir}\{ctx.author.id}.json") == True:
        with open(f"{CommsDir}\{id}.json","r") as ReadOnlyComms:
            CJSON = json.load(ReadOnlyComms)
            ReadOnlyComms.close()
            with open(f"{ProfilesDir}\{ctx.author.id}.json","r") as ReadOnlyProfile:
                PJSON = json.load(ReadOnlyProfile)
                ReadOnlyProfile.close()
                if CJSON["ClaimInfo"]["IsClaimed"] != True:
                    if CJSON["OwnerID"] != str(ctx.author.id):
                        with open(f"{CommsDir}\{id}.json","w") as WriteOnlyComms:
                            with open(f"{ProfilesDir}\{ctx.author.id}.json","w") as WriteOnlyProfile:
                                CJSON["ClaimInfo"]["IsClaimed"] = True
                                CJSON["ClaimInfo"]["ClaimedOwner"] = str(ctx.author)
                                CJSON["ClaimInfo"]["ClaimedOwnerID"] = str(ctx.author.id)
                                ID = CJSON["CommsID"]
                                OwnerID = CJSON["OwnerID"]
                                PJSON["AcceptedComms"].append(f"{ID}.json")
                                json.dump(CJSON,WriteOnlyComms)
                                json.dump(PJSON,WriteOnlyProfile)
                                User = await bot.fetch_user(OwnerID)
                                await User.send(f"Your commission(ID:{ID}) has been claimed by <@{ctx.author.id}>")
                                await ctx.send(f"<@{OwnerID}>'s commission has been claimed")
                                WriteOnlyComms.close()
                                WriteOnlyProfile.close()
                    else:
                        await ctx.send("You can't just claim your own commission lol")
                else:
                    Temp = CJSON["ClaimInfo"]["ClaimedOwnerID"]
                    await ctx.send(f"That commission had already been claimed by <@{Temp}>")
    else:
        await ctx.send(f"It appears that you dont have a profile. To make a profile type ``{pre}newProfile``")

@claimCommission.error
async def claimCommission_error(ctx,error):
    if "id" in str(error):
        await ctx.send('```claimCommission ID```\nMissing argument "ID"')
    else:
        await ctx.send("Invalid ID")

@bot.command(aliases=['leavecommission','leavecomm','leave'])
async def leaveCommission(ctx,id):
    if os.path.exists(f"{ProfilesDir}\{ctx.author.id}.json") == True:
        with open(f"{ProfilesDir}\{ctx.author.id}.json","r") as ReadOnlyProfileFile:
            PJSON = json.load(ReadOnlyProfileFile)
            File = PJSON["AcceptedComms"][PJSON["AcceptedComms"].index(f"{id}.json")]
            PJSON["AcceptedComms"].remove(f"{id}.json")
            with open(f"{CommsDir}\{File}","r") as ReadOnlyCommsFile:
                CJSON = json.load(ReadOnlyCommsFile)
                User = await bot.fetch_user(CJSON["OwnerID"])
                ID = CJSON["CommsID"]
                ClaimInfo = CJSON["ClaimInfo"]
                ClaimInfo["IsClaimed"] = False
                ClaimInfo["ClaimedOwner"] = None
                ClaimInfo["ClaimedOwnerID"] = None
                WriteOnlyProfile = open(f"{ProfilesDir}\{ctx.author.id}.json","w")
                WriteOnlyComms = open(f"{CommsDir}\{File}","w")
                json.dump(PJSON,WriteOnlyProfile)
                json.dump(CJSON,WriteOnlyComms)
                WriteOnlyProfile.close()
                WriteOnlyComms.close()
                ReadOnlyProfileFile.close()
                ReadOnlyCommsFile.close()
                await User.send(f"{ctx.author} has left your commission. Commission ID ``{ID}``")
                await ctx.send("You have left the commission")
    else:
        await ctx.send(f"It appears that you dont have a profile. To make a profile type ``{pre}newProfile``")

@leaveCommission.error
async def leaveCommission(ctx,error):
    if "id" in str(error):
        await ctx.send('```leaveCommission ID```\nMissing argument "ID"')
    else:
        await ctx.send("Invalid ID")

@bot.command(aliases=['commInfo','comminfo'])
async def CommissionInfo(ctx,id):
    if os.path.exists(f"{ProfilesDir}\{ctx.author.id}.json") == True:
        try:
            with open(f"{CommsDir}\{id}.json","r") as ReadOnlyCommissionFile:
                CJSON = json.load(ReadOnlyCommissionFile)
                ReadOnlyCommissionFile.close()
                Owner = CJSON["OwnerID"]
                Details = CJSON["CommDetails"]
                Price = CJSON["CommPrice"]

                Embed = discord.Embed(title="Commission Info",description=f"Commission Details:\nOwner: <@{Owner}>\nDetails: ```{Details}```\nPrice: ```${Price}```\n")
                await ctx.send(embed=Embed)
        except FileNotFoundError:
            await ctx.send("Invalid ID")
    else:
        await ctx.send(f"It appears that you dont have a profile. To make a profile type ``{pre}newProfile``")    

@bot.command(aliases=['rate'])
async def rate_user(ctx,member:discord.Member):
    author = ctx.author
    if os.path.exists(f"{ProfilesDir}\{ctx.author.id}.json") == True:
        if ctx.author.id != member.id:
            try:
               ReadOnly = open(f"{ProfilesDir}\{member.id}.json","r")
               PJSON = json.load(ReadOnly)
               ReadOnly.close()
               WriteOnly = open(f"{ProfilesDir}\{member.id}.json","w")
               await author.send(f"You are now rating {member}. Please enter in a value from {rating}")
               ratingRaw = await bot.wait_for("message",check=lambda message: message.author == ctx.author)
               ratingClean = str(ratingRaw.content)
               if ratingClean.isdigit != False:
                   ratingClean = await clamp(int(ratingClean),ratingLow,ratingHigh)
                   await author.send("Now type in a short message on why that person deserved that score")
                   reviewRaw = await bot.wait_for("message",check=lambda message: message.author == ctx.author)
                   reviewClean = str(reviewRaw.content)
                   PJSON["UserRatings"].append(ratingClean)
                   json.dump(PJSON,WriteOnly)
                   WriteOnly.close()
                   Embed = discord.Embed(title=f"New review and rating\nFrom {author} to {member}",description=f"Review:\n```\n{reviewClean}\n```\nRating:\n```{ratingClean} stars\n```")
                   await author.send("Your review has been sent")
                   await RatingChannel.send(embed=Embed)
                   await member.send(f"New review from {author}\nYou have been rated {ratingClean} stars")
               else:
                   WriteOnly.close()
                   await author.send("That isint a valid number")
            except FileNotFoundError:
                await ctx.send("That user dosent have a profile")
        else:
            await ctx.send("You cant just rate yourself")
    else:
        await ctx.send(f"It appears that you dont have a profile. To make a profile type ``{pre}newProfile``")

@rate_user.error
async def rate_user_error(ctx,error):
    await ctx.send('```rate_user [Memeber]```\nMissing argument "Member"')

@bot.command()
async def help(ctx):
    author = ctx.author
    Description = f"""
    ```newProfile``` Makes a new profile\n \|| Aliases: ``newprofile``, ``np``\n
    ```profile {{Discord User(Optional)}}``` Shows your profile or the select user profile\n \|| Aliases: ``Profile``\n
    ```working_on``` Shows the commissions you accepted/what you're currently working on\n \|| Aliases: ``working``\n
    ```editProfile``` Edit or Delete your profile\n \|| Aliases: ``editprofile``\n
    ```newCommission {{Commission Details}}{{Commission Price}}``` Make a new commission\n \|| Aliases: ``newcommission``, ``newcomm``\n
    ```delCommission {{Commission ID}}``` Delete a commission from the given ID\n \|| Aliases: ``delcommission``, ``delcomm``\n
    ```claimCommission {{ID}}``` Claim a commission with the given ID\n \|| Aliases: ``claimcommission``, ``claimcomm``, ``claim``\n
    ```leaveCommission {{ID}}``` Leave a commission with the given ID\n \|| Aliases: ``leavecommission``, ``leavecomm``, ``leave``\n
    ```CommissionInfo {{ID}}``` See commission info from the given ID\n \|| Aliases: ``commInfo``, ``comminfo``\n
    ```rate_user {{Discord User}}``` Rate the given discord user\n \|| Aliases: ``rate``\n
    ```help``` Shows this\n
    ----------------------\n
    My creator is <@{__author__}>\n
    If you wish to help with the bot development then check out my github __https://github.com/The-Glit-ch/Artist-Unite-Bot__\n"""
    Embed = discord.Embed(title="Help",description=Description,color=discord.Color.red())
    await author.send(embed=Embed)

async def calcRatings(JSON):
    List = JSON["UserRatings"]
    Total = List[0]
    for i in List:
        Total = Total + i
    return round(Total / len(List)),Total / len(List)

async def getComms(JSON):
    List = JSON["Comms"]
    Count = 0
    ParentStr = ""
    if len(List) > 0:
        if len(List) > 1:
            for i in List:
                Count = Count + 1
                File = open(f"{CommsDir}\{i}","r")
                CommsJSON = json.load(File)
                ID = CommsJSON["CommsID"]
                IsClaimed = CommsJSON["ClaimInfo"]["IsClaimed"]
                ParentStr = ParentStr + f"Commission {Count}:\n  ID:{ID}\n  IsClaimed:{IsClaimed}\n"
                File.close()
            return ParentStr
        else:
            File = open(f"{CommsDir}\{List[0]}","r")
            CommsJSON = json.load(File)
            ID = CommsJSON["CommsID"]
            IsClaimed = CommsJSON["ClaimInfo"]["IsClaimed"]
            File.close()
            return f"Commission 1:\n  ID:{ID}\n  IsClaimed:{IsClaimed}\n"
    else:
        return "None"

async def getAcceptedComms(JSON):
    List = JSON["AcceptedComms"]
    Count = 0
    ParentStr = ""
    if len(List) > 0:
        if len(List) > 1:
            for i in List:
               Count = Count + 1
               with open(f"{CommsDir}\{i}","r") as ReadOnlyComms:
                   CJSON = json.load(ReadOnlyComms)
                   ID = CJSON["CommsID"]
                   Owner = CJSON["Owner"]
                   OwnerID = CJSON["OwnerID"]
                   Details = CJSON["CommDetails"]
                   Price = CJSON["CommPrice"]
                   ParentStr = ParentStr + f"Commission {Count}:\n    ID:{ID}\n   Owner:{Owner}\n     OwnerID:{OwnerID}\n     Details:{Details}\n     Price:{Price}\n"
            ReadOnlyComms.close()
            return ParentStr
        else:
            with open(f"{CommsDir}\{List[0]}","r") as ReadOnlyComms:
                CJSON = json.load(ReadOnlyComms)
                ID = CJSON["CommsID"]
                Owner = CJSON["Owner"]
                OwnerID = CJSON["OwnerID"]
                Details = CJSON["CommDetails"]
                Price = CJSON["CommPrice"]
                ParentStr = ParentStr + f"Commission {Count}:\n    ID:{ID}\n    Owner:{Owner}\n     OwnerID:{OwnerID}\n     Details:{Details}\n     Price:{Price}\n"
                ReadOnlyComms.close()
            return f"Commission 1:\n    ID:{ID}\n   Owner:{Owner}\n     OwnerID:{OwnerID}\n     Details:{Details}\n     Price:{Price}\n"
    else:
        return "No accepted commissions"

async def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

bot.run(Key)