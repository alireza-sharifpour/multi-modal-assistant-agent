import os
import json
from io import BytesIO
from PIL import Image
import requests
from dotenv import load_dotenv
from openai import OpenAI
import httpx
import gradio as gr
from pydub import AudioSegment

# Initialization
load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

if openai_api_key:
    print(f"OpenAI API Key exists and begins with: {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

MODEL = "gpt-4o-mini"

transport = httpx.HTTPTransport(retries=2)
client = httpx.Client(transport=transport)

openai = OpenAI(
    api_key=openai_api_key,
    http_client=client
)

# System message for the AI assistant
system_message = "You are a helpful assistant for an Airline called FlightAI. "
system_message += "Give short, courteous answers, no more than 1 sentence. "
system_message += "Always be accurate. If you don't know the answer, say so."


# Ticket price database, You can call API to get the price instead of hardcoding it
ticket_prices = {
    "london": "$799",
    "paris": "$899",
    "tokyo": "$1400",
    "berlin": "$499",
    "new york": "$1200",
    "los angeles": "$1100",
    "chicago": "$999",
    "houston": "$899",
    "phoenix": "$799",
    "philadelphia": "$999",
    "san antonio": "$899",
    "san diego": "$1099",
    "dallas": "$999",
    "san jose": "$1199",
    "austin": "$899",
    "jacksonville": "$999",
    "columbus": "$899",
    "charlotte": "$799",
    "seattle": "$1099",
    "denver": "$999",
    "washington": "$1199",
    "boston": "$1099",
    "nashville": "$899",
    "oklahoma city": "$799",
    "milwaukee": "$999",
    "phoenix": "$799",
    "san francisco": "$1199",
    "detroit": "$899",
}

def get_ticket_price(destination_city):
    print(f"Tool get_ticket_price called for {destination_city}")
    city = destination_city.lower()
    return ticket_prices.get(city, "Unknown")

# Function definition for the price tool
price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price, for example when a customer asks 'How much is a ticket to this city'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": price_function}]

def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    city = arguments.get('destination_city')
    price = get_ticket_price(city)
    response = {
        "role": "tool",
        "content": json.dumps({"destination_city": city,"price": price}),
        "tool_call_id": tool_call.id
    }
    return response, city

def artist(city):
    try:
        image_response = openai.images.generate(
            model="dall-e-2",
            prompt=f"An image representing a vacation in {city}, showing tourist spots and everything unique about {city}, in a vibrant pop-art style",
            size="1024x1024",
            n=1
        )

        if not image_response.data:
            raise ValueError("No image data received from the API")

        image_url = image_response.data[0].url
        if not image_url:
            raise ValueError("No image URL in the response")

        response = requests.get(image_url)
        response.raise_for_status()

        return Image.open(BytesIO(response.content))

    except Exception as e:
        print(f"Error generating image: {str(e)}")
        raise

def talker(message):
    try:
        response = openai.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=message
        )

        # Save the audio to a temporary file instead of playing directly from memory
        audio_stream = BytesIO(response.content)
        audio = AudioSegment.from_file(audio_stream, format="mp3")

        # Save to temp file and play using system audio
        temp_file = "temp_speech.mp3"
        audio.export(temp_file, format="mp3")

        # Use system command to play audio instead of pydub.playback
        if os.system(f"afplay {temp_file}") != 0:  # afplay for macOS
            print("Warning: Could not play audio")

        # Clean up
        if os.path.exists(temp_file):
            os.remove(temp_file)

    except Exception as e:
        print(f"Error in text-to-speech: {str(e)}")
        # Continue execution even if speech fails
        pass

def chat(history):
    messages = [{"role": "system", "content": system_message}] + history
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)
    image = None

    if response.choices[0].finish_reason=="tool_calls":
        message = response.choices[0].message
        tool_response, city = handle_tool_call(message)
        messages.append(message)
        messages.append(tool_response)
        image = artist(city)
        response = openai.chat.completions.create(model=MODEL, messages=messages)

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})

    talker(reply)
    return history, image

# Gradio Interface
with gr.Blocks() as ui:
    with gr.Row():
        chatbot = gr.Chatbot(height=500, type="messages")
        image_output = gr.Image(height=500)
    with gr.Row():
        entry = gr.Textbox(label="Chat with our AI Assistant:")
    with gr.Row():
        clear = gr.Button("Clear")

    def do_entry(message, history):
        if history is None:
            history = []
        history.append({"role": "user", "content": message})
        return "", history

    entry.submit(do_entry, inputs=[entry, chatbot], outputs=[entry, chatbot]).then(
        chat, inputs=chatbot, outputs=[chatbot, image_output]
    )
    clear.click(lambda: None, inputs=None, outputs=chatbot, queue=False)

if __name__ == "__main__":
    ui.launch()