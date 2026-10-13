import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from src.logger import setup_logger

load_dotenv()
logger = setup_logger("agent")

def get_hydration_feedback(total_intake_ml: float, goal_ml: float = 3000.0) -> str:
    logger.info(f"Generating AI hydration feedback for intake: {total_intake_ml}ml / goal: {goal_ml}ml")
    api_key = os.getenv("OPENAI_API_KEY")
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=api_key
    )
    
    system_prompt = (
        "You are an AI health and hydration assistant. "
        "Analyze the user's daily water intake and provide short, friendly, "
        "and encouraging feedback. Give tips if they are lagging behind."
    )
    
    user_prompt = (
        f"The user has consumed {total_intake_ml} ml of water today out of a recommended goal of {goal_ml} ml. "
        "Provide constructive feedback."
    )
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    response = llm.invoke(messages)
    logger.info("Successfully generated AI feedback.")
    return response.content