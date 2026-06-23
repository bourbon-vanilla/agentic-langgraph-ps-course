# Job Application Assistant – Traced LangGraph Workflow

from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv
from langsmith import traceable
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

# Helper function for identifying key interview skill areas
@traceable
def extract_focus_areas(cv_text: str, job_description: str) -> str:
    """ Identify key skill areas that interview questions should focus on. """
    prompt = f"""
    From the CV and job description below,
    identify 3 key skill areas that should be probed in an interview.
    CV: {cv_text}
    Job Description: {job_description}
    """
    response = llm.invoke(prompt)
    return response.content

# Graph Nodes
def extract_strengths(state: ScreeningState):
    response = llm.invoke(f"""
    Given the candidate CV: {state["cv_text"]}
    And the job description: {state["job_description"]}
    Extract key strengths relevant for this role.
    """)
    return {"strengths": response.content}


def extract_weaknesses(state: ScreeningState):
    response = llm.invoke(f"""
    Given the candidate CV: {state["cv_text"]}
    And the job description: {state["job_description"]}
    Identify weaknesses or skill gaps.
    """)
    return {"weaknesses": response.content}


def generate_interview_questions(state: ScreeningState):
    # Traced helper call 
    focus_areas = extract_focus_areas(
        state["cv_text"],
        state["job_description"]
    )
    response = llm.invoke(f"""
    Based on the following focus areas: {focus_areas}
    Generate 5 tailored interview questions.
    """)
    return {"interview_questions": response.content}


def create_screening_report(state: ScreeningState):
    response = llm.invoke(f"""
    Create a structured screening report using:

    Strengths: {state["strengths"]}
    Weaknesses: {state["weaknesses"]}
    Interview Questions: {state["interview_questions"]}
    """)
    return {"screening_report": response.content}


graph_builder = StateGraph(ScreeningState)

graph_builder.add_node("strengths", extract_strengths)
graph_builder.add_node("weaknesses", extract_weaknesses)
graph_builder.add_node("questions", generate_interview_questions)
graph_builder.add_node("merge_report", create_screening_report)

graph_builder.add_edge(START, "strengths")
graph_builder.add_edge(START, "weaknesses")
graph_builder.add_edge(START, "questions")

graph_builder.add_edge("strengths", "merge_report")
graph_builder.add_edge("weaknesses", "merge_report")
graph_builder.add_edge("questions", "merge_report")

graph_builder.add_edge("merge_report", END)

graph = graph_builder.compile()


cv_text = "Experienced software engineer with 5 years in backend development, Python, and cloud technologies."
job_description = "Looking for a backend developer skilled in Python, cloud platforms, and scalable system design."
initial_state = {"cv_text": cv_text, "job_description": job_description}

final_state = graph.invoke(
   initial_state,
    config={
        "run_name": "candidate_screening_preprocess",
        "tags": ["job-screening", "parallel-analysis"],
        "metadata": {
            "model": "gpt-4o-mini",
            "environment": "demo",
            "version": "v1"
        }
    }
)

print("\nScreening Report:\n")
print(final_state["screening_report"])

