import json


def get_user_details(ai_message: str):
    starting_string = '*** PDF_FILLER'
    ending_string = starting_string

    start_index = ai_message.find(starting_string)
    end_index = ai_message.find(ending_string, start_index + 1)

    if start_index == -1 or end_index == -1:
        return None
    start_json_index = ai_message.find('{')
    end_json_index = ai_message.rfind('}')

    json_text = ai_message[start_json_index:end_json_index + 1]

    data = json.load(json_text)

    return data
