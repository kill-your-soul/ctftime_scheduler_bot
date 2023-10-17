# ctftime scheduler bot 
ctftime.org scheduler bot for sending reminders about upcoming CTFs
## Prerequisites
1. [Git](https://git-scm.com/)
2. [Python 3.8+](https://www.python.org/downloads/)
3. [Docker](https://www.docker.com/) (optional)

## Installation

1. Clone the repository
```bash
git clone https://github.com/kill-your-soul/ctftime_scheduler_bot.git
```

2. Create a virtual environment
```bash
python3 -m venv .venv
```

3. Activate the virtual environment
```bash
source .venv/bin/activate
```

4. Install the dependencies
```bash
pip install -r requirements.txt
```

5. Set environment variables
```bash
set TOKEN=<your_token>
set CHAT_ID=<your_chat_id>
set MESSAGE_THREAD_ID=<your_message_thread_id>
```

6. Run the bot
```bash
python3 ctftime_sch/main.py
```

## Run via Docker

1. Build the image
```bash
docker build -t ctftime_scheduler_bot .
```

2. Run the container
```bash
docker run --env TOKEN='<your_token>' --env CHAT_ID='<your_chat_id>' --env MESSAGE_THREAD_ID=<your_message_thread_id> ctftime_sch
```

## Run via Docker Compose

1. Copy and edit example.env
```bash
cp example.env .env
```

2. Run the container
```bash
docker-compose up -d
```