import logging
import asyncio
import os
from client import client
from Lamora.config import BOT_TOKEN
from Lamora.kendali import *

# Setup log
logging.basicConfig(level=logging.INFO)

async def main():
    await client.start(bot_token=BOT_TOKEN)
    register(client)  # <- mendaftarkan semua handler
    me = await client.get_me()
    logging.info(f"Bot @{me.username} berjalan.")

    # Kirim notifikasi setelah reboot
    if os.path.exists("rebooting.txt"):
        try:
            with open("rebooting.txt") as f:
                chat_id = int(f.read().strip())
            await client.send_message(chat_id, "🔥Bot berhasil diaktifkan🔥")
        except Exception as e:
            logging.warning(f"Gagal kirim notifikasi reboot: {e}")
        os.remove("rebooting.txt")

    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())