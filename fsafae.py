import discord
from discord.ext import commands
import os
import asyncio
import random
import urllib
from bs4 import BeautifulSoup
from urllib.request import Request
from urllib import parse
import bs4
import time
import captcha

client = discord.Client()

@client.event
async def on_ready():
    print('봇이 로그인 하였습니다.')
    print(' ')
    print('닉네임 : {}'.format(client.user.name))
    print('아이디 : {}'.format(client.user.id))

@client.event
async def on_member_join(member):
    try:
        syscha = member.guild.system_channel
        await syscha.send(f"{member.mention} 님 어서오세요 !인증이라고 말해주세요 ! ")
    except:
        pass

@client.event
async def on_message(message):

    if message.content == '!인증':
        syscha = message.channel
        embed=discord.Embed(colour=0x85CFFF, timestamp=message.created_at)
        embed.add_field(name="캡챠 코드를 가져오는중", value="당신의", inline=True)
        embed.set_footer(text=f"{message.author}, 인증을 진행중", icon_url=message.author.avatar_url)
        await message.channel.send(embed=embed)
        time.sleep(8)       
        Image_captcha = ImageCaptcha()
        msg = ""
        a = ""
        for i in range(6):
            a += str(random.randint(0, 9))

        name = "Captcha.png"
        Image_captcha.write(a, name)

        await message.channel.send(file=discord.File(name))

        def check(msg):
            return msg.author == message.author and msg.channel == message.channel

        try:
            msg = await client.wait_for("message", timeout=10, check=check)
        except:
            await message.channel.send("**시간 초과입니다.**")
            return

        if msg.content == a:
        embed=discord.Embed(colour=0x85CFFF, timestamp=message.created_at)
        await syscha.send(f"{message.author.mention} 님 싸우지 마시구 좋은 하루 되세요 ! ")
        role = discord.utils.get(message.author.guild.roles, name='유저')
        await message.author.add_roles(role)
        else:
            await message.channel.send("**님 아쉽지만 캡챠 코드가 정확하지 않네요 다시 한번 해보시겠어요?**")

access_token = os.environ["BOT_TOKEN"]
client.run(access_token)