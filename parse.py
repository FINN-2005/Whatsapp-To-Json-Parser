# Section 1: Split raw chat text into lines
def parse_raw_lines(raw_text):
    return raw_text.splitlines()

# Section 2: Group lines belonging to the same message into message blocks
def group_message_lines(lines):
    import re
    start_pattern = re.compile(r'^(\d{1,2}/\d{1,2}/\d{4}), (\d{2}:\d{2}) - ')
    message_blocks = []
    current_message = []
    for line in lines:
        if start_pattern.match(line):
            if current_message: message_blocks.append('\n'.join(current_message))
            current_message = [line]
        else: current_message.append(line)
    if current_message: message_blocks.append('\n'.join(current_message))
    return message_blocks

# Section 3: Parse message block into structured message dict
def parse_message_block(block, msg_id):
    import re
    user_pattern = re.compile(r'^(\d{1,2}/\d{1,2}/\d{4}), (\d{2}:\d{2}) - (.+?): (.*)$', re.DOTALL)
    info_pattern = re.compile(r'^(\d{1,2}/\d{1,2}/\d{4}), (\d{2}:\d{2}) - (.+)$', re.DOTALL)
    m_user = user_pattern.match(block)
    if m_user:
        date, time, user, content = m_user.groups()
        # content = content.replace('\n', '\\n')
        content = content.replace(' <This message was edited>', '')
        if content == '<Media omitted>': msg_type = 'media'
        elif content == '<This message was edited>': msg_type = 'edited'
        else: msg_type = 'text'
        return {'id': msg_id, 'type': msg_type, 'user': user, 'content': content, 'time': f'{date} {time}'}
    m_info = info_pattern.match(block)
    if m_info:
        date, time, content = m_info.groups()
        content = content.replace('\n', '\\n')
        return {'id': msg_id, 'type': 'info', 'user': 'whatsapp', 'content': content, 'time': f'{date} {time}'}
    return None

# Section 4: Parse all message blocks into list of message dicts
def parse_all_blocks(blocks):
    messages = []
    for i, block in enumerate(blocks, start=1):
        msg = parse_message_block(block, i)
        if msg is not None: messages.append(msg)
    return messages

# Section 5: Write messages list to a JSON file
def messages_to_json(messages, filename="data.json"):
    import json
    with open(filename, 'w', encoding='utf-8') as f: json.dump(messages, f, ensure_ascii=False, indent=2)





if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python parse.py <inputfile>")
        sys.exit(1)
    input_file = sys.argv[1]
    try:
        with open(input_file, 'r', encoding='utf8') as F:
            data = F.read()
        lines = parse_raw_lines(data)
        blocks = group_message_lines(lines)
        dicts = parse_all_blocks(blocks)
        messages_to_json(dicts)
        print("Parsing Successfull")
    except Exception as e:
        import traceback
        print("Parsing Failed:")
        traceback.print_exc()
