import json

async def reload(context):
    """Reload facts from file. Expects context dict with 'FACTS' and 'FACTS_FILE' keys."""
    print("Reloading facts...")
    facts_file = context['FACTS_FILE']
    facts_list = context['FACTS']  # This is the actual list object from main
    event = context['EVENT']

    print(f"Loading facts from {facts_file}...")

    with open(facts_file, 'r', encoding='utf-8') as file:
        new_facts = json.load(file)
        
        # Clear and extend the existing list instead of reassigning
        facts_list.clear()
        facts_list.extend(new_facts)

        if event is not None:
            await event.message.reply(f'Reloaded {len(facts_list)} facts.')