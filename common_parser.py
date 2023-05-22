def get_step_completion_status(ai_message: str) -> bool:
    starting_string = 'step_completed=yes'
    ending_string = ','

    start_index = ai_message.find(starting_string)
    end_index = ai_message.find(ending_string, start_index + 1)

    if start_index == -1 or end_index == -1:
        return False

    return True