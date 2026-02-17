import stoat

async def status(context):
    """Check if the bot is online."""
    event: stoat.MessageCreateEvent | None = context['EVENT']
    if event is not None:
        print(f'Status command invoked by user {event.message.author.name}#{event.message.author.discriminator} in server {event.message.get_server()[1]}')
        await event.message.reply('Bot is online!')