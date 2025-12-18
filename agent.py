from langchain.agents import create_agent

agent = create_agent(
    model="groq:llama-3.1-8b-instant",
)
