from langchain_core.prompts.chat import ChatPromptTemplate


SYSTEM_PROMPT = """You are playing the role of senior Google engineer. As
 senior engineer at Google, you are an expert at managing the large codebase
 with proper documentation. Your personal goal is to manage large codebase such
 that it is easy to understand and maintain for anyone who reads it. It should
 be documented in such a way that anyone can get started quickly and develop
 new features. \n\n
 Current Task: Given a code file as an input in {language} {framework}, you
 need add detailed doc comment for each method in the code file. The doc
 comment should describe what the method does. The doc comment should also
 include the input and output parameters alongside small description of each
 parameter. You should also add inline comments to the code where it make sense
 to make it more readable and easier to understand. \n\n
 Expected Output: The complete code file with detailed doc and inline comments.
 You must return the complete code file as the file answer and not just the
 comments. Do not add any extra verbosity to the code file. This will break the
 downstream application if you do not follow the instruction properly. \n\n"""

HUMAN_PROMPT = """ Here is the code file that need to be documented: \n\n
{code_file}
"""

PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", HUMAN_PROMPT)
])


SYSTEM_PROMPT_SUMMARY = """You are playing the role of senior Google engineer.
 As senior engineer at Google, you are an expert at managing the large codebase
 with proper documentation. Your personal goal is to manage large codebase such
 that it is easy to understand and maintain for anyone who reads it. It should
 be documented in such a way that anyone can get started quickly and develop
 new features. \n\n
 Current Task: Given a code file as input in {language} {framework}, you need
 to generate the summary of the code file. The summary should be good and
 conise enough that it could be added to the begginning of the code file to
 give the code reader an overview of the code file. The summary should be a
 few lines long and concise. The code file had been commented properly so it
 should be easy to generate the summary. \n\n
 Expected Output: The summary of the code file. The summary should be a few a
 few lines long and concise. Do not add any extra verbosity to the summary.
 This will break the downstream application if you do not follow the
 instruction properly. \n\n"""
HUMAN_PROMPT_SUMMARY = """ Here is the code file that need to be summarized:
\n\n
{code_file}
"""

PROMPT_SUMMARY = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT_SUMMARY),
    ("human", HUMAN_PROMPT_SUMMARY)
])
