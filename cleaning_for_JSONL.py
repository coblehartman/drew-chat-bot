import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

validation_path = config.get(*('path', 'validation_file_location'))
training_path = config.get(*('path', 'training_file_location'))

def process_conversation(input_file, output_file):
    # Open the input file and read the lines
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # Initialize variables
    conversation = []
    user_content = []
    assistant_content = []
    current_speaker = None
    convo_tracker = 0
    # Process each line
    for i, line in enumerate(lines):
        # Check for speaker
        if line.startswith("Drew"):
            # print(line)
            current_speaker = "assistant"
            assistant_content.append(lines[i+1].strip())  # Remove speaker name and leading/trailing whitespace
            # print(user_content)
        elif line.startswith("SPK"):
            current_speaker = "user"
            user_content.append(lines[i+1].strip())  # Remove speaker name and leading/trailing whitespace
            # print(assistant_content)
        else:
            continue  # Skip lines that don't start with a speaker
        # Add to conversation
        if user_content and assistant_content:
            conversation.append({"messages": [{"role": "user", "content": f", ".join(user_content)}, {"role": "assistant", "content": f", ".join(assistant_content)}]})
            user_content.clear()
            assistant_content.clear()
        elif not user_content and assistant_content:
            print(assistant_content)
            conversation.append({"messages": [{"role": "assistant", "content": f", ".join(assistant_content)}]})
            assistant_content.clear()
        else:
            continue
    print(conversation)
    # Write to JSONL file
    with open(output_file, 'w') as file:
        for entry in conversation:
            json.dump(entry, file)
            file.write('\n')
process_conversation(validation_path, 'validation_ouput.jsonl')
process_conversation(training_path, 'training_output.jsonl')