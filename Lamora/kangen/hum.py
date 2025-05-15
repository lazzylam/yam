def chunk_list(lst, size):
    return [lst[i:i + size] for i in range(0, len(lst), size)]

async def is_admin(client, event):
    try:
        chat = await event.get_chat()
        user = await event.get_sender()
        perms = await client.get_permissions(chat, user)
        return perms.is_admin or perms.is_creator
    except:
        return False
