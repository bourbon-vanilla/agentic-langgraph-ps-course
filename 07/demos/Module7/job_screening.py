# Job Application Assistant – Running Parallel Analyses

from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv
import os

load_dotenv()  
os.environ["LANGSMITH_PROJECT"] = "job-application-assistant"

class ScreeningState(TypedDict):
    cv_text: str
    job_description: str
    strengths: str
    weaknesses: str
    interview_questions: str
    screening_report: str

llm = ChatOpenAI(model="gpt-4o-mini")

def extract_strengths(state: ScreeningState) :
    response = llm.invoke(f"""
    Given the candidate CV:  {state["cv_text"]}
    And the Job Description:  {state["job_description"]}
    Extract the candidate's key strengths relevant for this role.
    """)
    return {"strengths": response.content}

def extract_weaknesses(state: ScreeningState):
    response = llm.invoke(f"""
    Given the candidate CV:{state["cv_text"]}
    And the Job Description:{state["job_description"]}
    Extract the candidate's weaknesses or skill gaps for this role.
    """)
    return {"weaknesses": response.content}

def generate_interview_questions(state: ScreeningState):
    response = llm.invoke(f"""
    Given the candidate CV: {state["cv_text"]}
    And the Job Description:{state["job_description"]}
    Suggest 5 tailored interview questions.
    """)
    return {"interview_questions": response.content}

def create_screening_report(state: ScreeningState):
    response = llm.invoke(f"""
    Combine the following into a structured screening report for the recruiter:
    Candidate Strengths: {state["strengths"]}
    Candidate Weaknesses: {state["weaknesses"]}
    Suggested Interview Questions: {state["interview_questions"]}
    """)
    return {"screening_report": response.content}

graph_builder = StateGraph(ScreeningState)

graph_builder.add_node("extract_strengths", extract_strengths)
graph_builder.add_node("extract_weaknesses", extract_weaknesses)
graph_builder.add_node("questions", generate_interview_questions)
graph_builder.add_node("merge_report", create_screening_report)

graph_builder.add_edge(START, "extract_strengths")
graph_builder.add_edge(START, "extract_weaknesses")
graph_builder.add_edge(START, "questions")
graph_builder.add_edge("extract_strengths", "merge_report")
graph_builder.add_edge("extract_weaknesses", "merge_report")
graph_builder.add_edge("questions", "merge_report")
graph_builder.add_edge("merge_report", END)

graph = graph_builder.compile()

def run_job_screening(inputs: dict) -> dict:
    """
    This function is the evaluation entry point.
    LangSmith will call this once per dataset example.
    """
    final_state = graph.invoke({
        "cv_text": inputs["cv_text"],
        "job_description": inputs["job_description"]
    })

    return {
        "screening_report": final_state["screening_report"]
    }


if __name__ == "__main__":
    result = run_job_screening({
        "cv_text": "Experienced software engineer with 5 years...",
        "job_description": "Looking for a backend developer..."
    })
    print(result["screening_report"])

