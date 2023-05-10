import discord
import openai

intents = discord.Intents(messages=True, guilds=True)
intents.message_content = True
client = discord.Client(intents=intents)
openai_api = open('openaiapikey.txt')
openai.api_key = openai_api.read()


@client.event
async def on_ready():
    guild_count = 0
    for guild in client.guilds:
        print(f"Online in:\nServer ID: {guild.id} (Name: {guild.name})")
        guild_count = guild_count + 1
    print("GPT is in " + str(guild_count) + " guilds.")


def generate_response(message):
    prompt = f"{message.content}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!gpt'):
        response = generate_response(message)
        if len(response) > 2000:
            response = response[:2000]  # Truncate the response to 2000 characters
        await message.channel.send(response)

discord_api = open('discordapikey.txt')
client.run(discord_api.read())
