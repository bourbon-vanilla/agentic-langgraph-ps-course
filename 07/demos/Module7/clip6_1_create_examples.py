from dotenv import load_dotenv
from langsmith import Client

#  Load environment variables from .env
load_dotenv()  

# Create LangSmith client
client = Client()

# Dataset ID (copied from LangSmith UI)
dataset_id = "0c4768b2-c90c-4f0d-85aa-2e79a6022ad7"

# Resume screening examples
example_inputs = [
    (
        "Backend engineer with 5 years of experience in Python, Django, REST APIs, AWS, and scalable microservices.",
        "Hiring a backend developer with strong Python skills, cloud experience, and scalable system design knowledge.",
        "The candidate shows strong alignment with Python and cloud requirements. Experience with Django and microservices suggests readiness for scalable systems, though deeper system design evaluation is recommended."
    ),
    (
        "Junior backend developer with 1 year of experience in Flask, SQLite, and basic API development.",
        "Looking for a senior backend engineer with extensive cloud and distributed systems experience.",
        "The candidate’s experience level does not meet the senior role requirements. Limited exposure to cloud infrastructure and distributed systems is a significant gap."
    ),
    (
        "Backend developer with 3 years of experience in Python, FastAPI, PostgreSQL, Docker, and AWS Lambda.",
        "Hiring a backend engineer to design and maintain cloud-native, scalable backend services.",
        "The candidate aligns well with cloud-native backend development. Additional experience in large-scale system design would strengthen the fit."
    )
]

# Prepare inputs and outputs (match dataset schema)
inputs = [
    {
        "cv_text": cv_text,
        "job_description": job_description
    }
    for cv_text, job_description, _ in example_inputs
]

outputs = [
    {
        "screening_report": screening_report
    }
    for _, _, screening_report in example_inputs
]

# Upload examples in bulk
client.create_examples(
    inputs=inputs,
    outputs=outputs,
    dataset_id=dataset_id
)

print(f"Successfully uploaded {len(inputs)} examples to LangSmith")
