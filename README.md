<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/fertilisai/sapio-streamlit">
    <img src="assets/favicon-128x128.png" alt="Logo" width="128" height="128">
  </a>

  <h2 align="center">Sapio</h2>

  <p align="center">
    A smarter ChatGPT
  </p>
</div>

<!-- ABOUT THE PROJECT -->

## About The Project

![Sapio-screenshot](assets/chat.png)

Sapio is a simple Streamlit UI that allows you to chat with OpenAI's GPT-3 API more specifically ChatGPT. The goal is to continue adding features frequently and make the ChatGPT capabilities even more powerful.

Why not just using ChatGPT instead?

- Sapio will get new features
- LangChain support
- Always available (no busy servers)
- No login and connection timeout
- More parameters to play with
- A fraction of the cost of ChatGPT Pro

<!-- INSTALLATION -->

## Installation

1. Get an API key at [https://platform.openai.com/](https://platform.openai.com/)
2. Clone the repo
   ```sh
   git clone https://github.com/fertilisai/sapio-streamlit.git
   ```
3. cd into the directory
   ```sh
   cd sapio-streamlit
   ```
4. install requirements
   ```sh
   pip install -r requirements.txt
   ```
5. Run the app
   ```sh
    streamlit run sapio.py
   ```
6. Enter your API key in the settings menu
7. Start to chat

or see the live demo on Streamlit: [https://sapiochat.streamlit.app/](https://sapiochat.streamlit.app/)

<!-- FEATURES -->

## Features

- Settings (model, image size, temperature, max_tokens, presence_penalty)
- Chat history
- DALL-E support
- LangChain agent with tools

<!-- ROADMAP -->

## Roadmap

- [x] DALL-E support
- [x] LangChain support
- [ ] Stable Diffusion support
- [ ] Embeddings support
- [ ] Whisper support

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.
