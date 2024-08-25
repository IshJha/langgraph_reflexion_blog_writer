**LangChain - Conditional Tool Execution Bot with Groq Integration**
**Author: Ish Jha
Contact Info: ishjha1929@gmail.com / jha.13@alumni.iitj.ac.in**
(Please feel free to contact for any doubts or collaborative projects!)

This project demonstrates a sophisticated chatbot that leverages LangChain, Groq, and Tavily Search to perform conditional tool execution
and iterative revisions based on user input. The bot can draft a response, invoke tools to gather additional information, and revise its responses using a conditional event loop.

**Requirements**
Python 3.8+
LangChain
LangGraph
LangChain Community (for Tavily Search)
dotenv


**Installation**
Clone the repository:
git clone https://github.com/yourusername/conditional-tool-execution-bot.git
cd conditional-tool-execution-bot

**Install the required packages using Pipenv:**
pipenv install
Activate the Pipenv shell:
pipenv shell

**Set up your environment variables:**
Create a .env file in the root directory.
Add your Groq and Google API keys:
GOOGLE_API_KEY=your-google-api-key
GROQ_API_KEY=your-groq-api-key

**Usage**
To run the bot and execute tool invocations:
Ensure the setup of Tavily Search API is configured in the code.
Run the main script:
python main.py

**How It Works**
Message Graph Construction: A MessageGraph is built, defining nodes and edges for drafting, tool execution, and revision.

Conditional Event Loop: The event loop is designed to allow multiple iterations of tool execution, revising the response until the maximum number of iterations is reached.

Tool Invocation and Execution: Tools are invoked based on parsed AI messages, and results are processed and returned as ToolMessage objects.

Iterative Revisions: The response is iteratively revised based on the output of the tools until a satisfactory answer is generated.

Integration with Groq
This project integrates with the Groq API to leverage various large language models, such as Gemma2-9b-It and others, to generate responses and revise them using structured prompts.

**Example**
To generate a response about "India" using the bot, the following code is executed:

human_message = HumanMessage(content="Write about India.")
chain = (
    first_responder_prompt_template
    | llm.bind_tools(tools=[AnswerQuestion], tool_choice="AnswerQuestion")
    | parser_pydantic
)

res = chain.invoke(input={"messages": [human_message]})
print(res)

**Author: Ish Jha
Contact Info: ishjha1929@gmail.com / jha.13@alumni.iitj.ac.in
(Please feel free to contact for any doubts or collaborative projects!)**
