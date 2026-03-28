# -*- coding: utf-8 -*-

import requests
import asyncio
from telethon import TelegramClient, events
from datetime import datetime

# ====== TELEGRAM API ======
api_id = 33756465
api_hash = 'e87308bcb4bc1ee1b8b42bb72776097b'

# ====== OPENROUTER KEY ======
openrouter_key = "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"

# ====== TELEGRAM CLIENT ======
tg = TelegramClient('zia_session', api_id, api_hash)

last_active_time = datetime.now()

# ====== AI FUNCTION ======
def get_ai_reply(user_msg):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {openrouter_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "Reply in the same language as the user. Keep it short and natural."
            },
            {
                "role": "user",
                "content": user_msg
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "I am not available now."

    except:
        return "Connection problem."

# ====== AUTO REPLY ======
@tg.on(events.NewMessage(incoming=True))
async def handler(event):
    global last_active_time

    if event.is_private and not event.out:
        try:
            user_msg = event.text

            me = await tg.get_me()
            status = await tg.get_entity(me.id)

            # ====== IF ONLINE ======
            if hasattr(status, "status") and str(status.status) == "UserStatusOnline":
                await asyncio.sleep(30)  # wait 30 sec

                # যদি তুমি এই সময়ের মধ্যে reply দাও → bot বন্ধ
                if (datetime.now() - last_active_time).seconds < 30:
                    return

                ai_reply = get_ai_reply(user_msg)

            else:
                # ====== IF OFFLINE ======
                ai_reply = get_ai_reply(user_msg)

            final = f"{ai_reply}\n\nZIA AI 🤖 — জিয়া ভাই এখন offline। কিভাবে help করতে পারি?"

            await asyncio.sleep(1)
            await event.reply(final)

            print("Reply sent")

        except Exception as e:
            print("Error:", e)

# ====== TRACK YOUR ACTIVITY ======
@tg.on(events.NewMessage(outgoing=True))
async def track_activity(event):
    global last_active_time
    last_active_time = datetime.now()

# ====== START ======
print("Bot starting...")

tg.start()

print("Bot is running (Smart 30s Auto Reply ON)")

tg.run_until_disconnected()