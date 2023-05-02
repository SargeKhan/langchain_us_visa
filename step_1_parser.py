from typing import Tuple, Union


def get_visa_type_value(ai_message: str):
    starting_string = 'visa_type='
    ending_string = ','

    start_index = ai_message.find(starting_string)
    end_index = ai_message.find(ending_string, start_index + 1)

    if start_index == -1 or end_index == -1:
        raise Exception('LLM failed to respond in the expected format')

    return ai_message[start_index + len(starting_string):end_index].strip()


def get_visa_type(ai_message: str) -> Tuple[bool, Union[str, None]]:
    starting_string = 'visa_type_selected='
    ending_string = ','

    start_index = ai_message.find(starting_string)
    end_index = ai_message.find(ending_string, start_index + 1)

    if start_index == -1 or end_index == -1:
        return False, None

    is_visa_type_selected = True if ai_message[start_index:end_index].strip(
    ) == 'yes' else False

    if not is_visa_type_selected:
        return False, None

    return True, get_visa_type_value(ai_message)
