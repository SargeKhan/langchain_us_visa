def get_step_completion_status(ai_message: str) -> bool:
    starting_string = 'step_completed='
    ending_string = ','

    start_index = ai_message.find(starting_string)
    end_index = ai_message.find(ending_string, start_index + 1)

    if start_index == -1 or end_index == -1:
        return False

    is_step_completed = True if ai_message[start_index:end_index].strip(
    ) == 'yes' else False

    if not is_step_completed:
        return False

    return True
