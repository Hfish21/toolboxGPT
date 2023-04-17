import openai
import click

api_key = "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"
openai.api_key = api_key


def send_message(message_log):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        messages=message_log,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=3800,        # The maximum number of tokens (words or subwords) in the generated response
        stop=None,              # The stopping sequence for the generated response, if any (not used here)
        temperature=0.7,        # The "creativity" of the generated response (higher temperature = more creative)
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content

@click.group()
def cli():
    pass

@click.command()
@click.option('--message', default="", help='Asks GPT API')
def ask(message):
    message_log = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]


    message_log.append({"role": "user", "content": message})

    response = send_message(message_log)
    message_log.append({"role": "assistant", "content": response})

    click.echo(f"AI assistant: {response}")





cli.add_command(ask)


if __name__ == '__main__':
    cli()