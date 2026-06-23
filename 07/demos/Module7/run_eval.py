from langsmith import evaluate
from job_screening import run_job_screening

# Simple evaluator: checks if output exists
def has_output(outputs: dict, reference_outputs: dict):
    screening_report = outputs.get("screening_report", "")
    return 1 if screening_report.strip() else 0

# Checks whether the output length roughly matches the reference
def similar_length(outputs: dict, reference_outputs: dict):
    actual = outputs.get("screening_report", "")
    expected = reference_outputs.get("screening_report", "")
    return 1 if abs(len(actual) - len(expected)) < 500 else 0


evaluate(
    run_job_screening,
    data="candidate-dataset", 
    evaluators=[has_output,similar_length],
    experiment_prefix="job-screening-v1"
)
