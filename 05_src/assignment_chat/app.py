"""
The Gradio chat interface.
Run it with:   python app.py
Then open the local URL Gradio prints (usually http://127.0.0.1:7860).
Completion: DONE
"""

import gradio as gr
import config
from chatbot import respond

# ChatInterface builds the chat UI and manages the on-screen history.
# This Gradio version passes history as [user, bot] pairs, which chatbot.py converts.
demo = gr.ChatInterface(
    fn=respond,
    title="The Byte Bistro - Chat with Miso",
    description=(
        "Miso is your warm digital chef. Ask for cooking tips, check a city's "
        "weather to plan a meal, or get help scaling a recipe."
    ),
    examples=[
        "What's the weather in Toronto? Should I make soup?",
        "How do I make a simple dish taste special?",
        "I'm tripling a recipe with 250 g of flour, how much is that?",
    ],
)

if __name__ == "__main__":
    demo.launch()