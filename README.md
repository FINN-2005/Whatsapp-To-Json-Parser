# Whatsapp-To-Json-Parser

This is a simple but quite decent whatsapp chat parser (media ommited)

## Setup
```bash
git clone https://github.com/FINN-2005/Whatsapp-To-Json-Parser.git
```

## Usage
```bash
cd ./Whatsapp-To-Json-Parser
python parse.py your-chat.txt       # Replace your-chat.txt with your exported data file
```

## json template

```json
[
    {
        "id": 0,
        "type": "text",
        "user": "username_or_whatsapp",
        "content": "message content with multiline if needed",
        "time": "10/01/2022 10:31"
    }
]
```
- `id`: Unique message ID or type indicator.
- `type`: Message type such as "text", "media", "info", etc.
- `user`: Sender username or `"whatsapp"` for system messages.
- `content`: Message text content.
- `time`: Timestamp of the message.
