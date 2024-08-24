import datetime
import os
from dotenv import load_dotenv

load_dotenv()
from langchain_groq import ChatGroq





from langchain_core.output_parsers.openai_tools import (
    JsonOutputToolsParser,
    PydanticToolsParser,
)
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

from schemas import AnswerQuestion, ReviseAnswer

# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",google_api_key=<your-api-key>)
# llm = ChatGoogleGenerativeAI(model="gemini-pro",google_api_key=<your-api-key>,convert_system_message_to_human=True)
llm=ChatGroq(groq_api_key="<your-api-key>",model_name="Gemma2-9b-It")
# llm=ChatGroq(groq_api_key="<your-api-key>",model_name="mixtral-8x7b-32768")
# llm=ChatGroq(groq_api_key="<your-api-key>",model_name="llama3-70b-8192")
parser = JsonOutputToolsParser(return_id=True)
parser_pydantic = PydanticToolsParser(tools=[AnswerQuestion])
actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert researcher.
Current time: {time}

1. {first_instruction}
2. Reflect and critique your answer. Be severe to maximize improvement.
3. Recommend 1 search queries for tavily web search  to research information and improve your answer.""",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
)



first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~50 word answer."
)

first_responder = first_responder_prompt_template | llm.bind_tools(
    tools=[AnswerQuestion], tool_choice="AnswerQuestion"
)

revise_instructions = """Use Tavily search API tool to revise your answer.
    - You should use the previous critique to add important information to your answer.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com
    - You should use the previous critique to remove superfluous information.
"""

revisor = actor_prompt_template.partial(
    first_instruction=revise_instructions
) | llm.bind_tools(tools=[ReviseAnswer], tool_choice="ReviseAnswer")

if __name__ == "__main__":
    human_message = HumanMessage(
        content="Write about india."

    )
    chain = (
        first_responder_prompt_template
        | llm.bind_tools(tools=[AnswerQuestion], tool_choice="AnswerQuestion")
        | parser_pydantic
    )

    res = chain.invoke(input={"messages": [human_message]})
    print(res)
