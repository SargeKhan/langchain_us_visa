from typing import Tuple
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)

import logging

from common_parser import get_step_completion_status
from step_1_parser import get_visa_type
from step_2_parser import get_user_details
from generate_pdf import generate_pdf


logging.basicConfig(level=logging.INFO)

chat = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')

system_setup_message: SystemMessage
system_step_1_template_str: SystemMessage
system_step_2_template_str: str

with open('step_1.txt', 'r') as file:
    system_step_1_template_str = file.read()

with open('step_2.txt', 'r') as file:
    system_step_2_template_str = file.read()

system_setup_messages = [
    system_step_1_template_str, system_step_2_template_str]


def gather_visa_type() -> Tuple[bool, str]:
    messages = [SystemMessage(content=system_step_1_template_str)]
    while True:
        user_input = input('human:')

        if user_input.lower() == 'quit':
            break

        user_reply = HumanMessage(content=user_input)

        messages.append(user_reply)

        ai_message: AIMessage = chat(messages)
        logging.debug(''.join([
            f'\n{message.type}: {message.content}'
            for message in messages
        ]))

        logging.info(f'AI-Step1:, {ai_message.content}')

        messages.append(ai_message)

        step_status = get_step_completion_status(ai_message.content)

        logging.info(f'step_status: {step_status}')
        if step_status:
            visa_type_selected, visa_type = get_visa_type(ai_message.content)
            return visa_type_selected, visa_type


def gather_user_info(visa_type: str) -> dict:
    print(f'selected visa type={visa_type}')
    system_message_template = SystemMessagePromptTemplate.from_template(
        system_step_2_template_str)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_template])
    messages = chat_prompt.format_prompt(visa_type=visa_type).to_messages()
    starting_message = HumanMessage(
        content=f'I want to fill details for visa:{visa_type}')
    messages.append(starting_message)

    while True:
        ai_message: AIMessage = chat(messages)
        logging.debug(''.join([
            f'\n{message.type}: {message.content}'
            for message in messages
        ]))

        logging.info('AI-Step2:', ai_message.content)

        messages.append(ai_message)

        user_input = input('human:')

        if user_input.lower() == 'quit':
            break

        user_reply = HumanMessage(content=user_input)

        messages.append(user_reply)

        step_status = get_step_completion_status(ai_message.content)

        if step_status:
            user_details = get_user_details(
                ai_message.content)
            return user_details


def generate_pdf_form(user_details: dict) -> None:
    generate_pdf('usman_khen', user_details)


def main() -> None:
    visa_type_selected, visa_type = gather_visa_type()
    logging.info('step 1 completed')
    user_details = gather_user_info(visa_type)
    logging.info('step 2 completed')
    generate_pdf_form(user_details)


main()

'''
generate_pdf_form({
    "name": "usman khen",
    "email": "usmankhen@gmail.com",
    "phone": "1234567890",
    "passport_number": "1234567890",
})
'''
