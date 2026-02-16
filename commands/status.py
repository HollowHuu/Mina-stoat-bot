import stoat

async def status(context):
    """Check if the bot is online."""
    event: stoat.MessageCreateEvent | None = context['EVENT']
    if event is not None:
        await event.message.reply('Bot is online!')