import stoat


async def check_bot_owner(context):
    """Check if the user is the bot owner. Expects context dict with 'EVENT' and 'CLIENT' keys."""
    event: stoat.MessageCreateEvent = context["EVENT"]
    client: stoat.Client = context["CLIENT"]

    if event is None or client.user is None or client.user.get_bot_owner()[0] is None:
        print("No event provided in context for check_owner. Skipping owner check.")
        return False

    author = event.message.author
    if type(author) is not stoat.Member:
        print("Author is not a Member. Skipping owner check.")
        return False

    if author.id != client.user.get_bot_owner()[1]:
        await event.message.reply("Only the bot owner can use this command.")
        return False

    return True


async def check_server_owner(context):
    """Check if the user is the server owner. Expects context dict with 'EVENT' key."""
    event: stoat.MessageCreateEvent = context["EVENT"]

    if event is None:
        print(
            "No event provided in context for check_server_owner. Skipping server owner check."
        )
        return False

    author = event.message.author
    server = event.message.get_server()[0]

    if type(author) is not stoat.Member or server is None:
        print("Author is not a Member. Skipping server owner check.")
        return False

    if author.id != server.owner_id:
        await event.message.reply("Only the server owner can use this command.")
        return False

    return True
