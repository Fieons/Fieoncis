from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, AIMessagePromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from config import *
import os

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

system_template = "Given a question, try to answer it using the content of the file extracts below, and if you cannot answer, or find " \
        "a relevant file, just output \"I couldn't find the answer to that question in your files.\".\n\n" \
        "If the answer is not contained in the files or if there are no file extracts, respond with \"I couldn't find the answer " \
        "to that question in your files.\" If the question is not actually a question, respond with \"That's not a valid question.\"\n\n" \
        "In the cases where you can find the answer, first give the answer. Then explain how you found the answer from the source or sources, " \
        "and use the exact filenames of the source files you mention. Do not make up the names of any other files other than those mentioned "\
        "in the files context. Give the answer in markdown format." \
        "Use the following format:\n\nQuestion: <question>\n\nFiles:\n<###\n\"filename 1\"\nfile text>\n<###\n\"filename 2\"\nfile text>...\n\n"\
        "Answer: <answer or \"I couldn't find the answer to that question in your files\" or \"That's not a valid question.\">\n\n" \
        "Question: {question}\n\n" \
        "File name:\n{result_file_name}\n" \
        "File text:\n{result_text}\n" \
        "Answer:"
system_prompt = SystemMessagePromptTemplate.from_template(system_template)

ai_template = ""
ai_prompt = AIMessagePromptTemplate.from_template(ai_template)

# create the chat prompt template
chat_prompt = ChatPromptTemplate.from_messages([system_prompt, ai_prompt])

def get_chain():
    llm = OpenAI(temperature=0, max_tokens=1000)
    
    return LLMChain(llm=llm, prompt=chat_prompt)


