# Channels agregator bot

This is a **telegram bot** that forwards new posts from added channels 

## How to start the code?

1. Clone the repository: 
```bash
git clone https://github.com/xxxproc/channels_agregator_bot.git
```
2. Download the requirements:
```python
pip install -r requirements.txt
```
4. Rename a `.env.example` file to `.env` and enter the key:
    - `token`: token of telegram bot (from BotFather)
    - `id_of_main_channel`: id of channel where new posts will be sent to
    - `link_to_bot`: link to bot (https://t.me/bot_name)
5. Launch the main.py:
```python
python main.py
```