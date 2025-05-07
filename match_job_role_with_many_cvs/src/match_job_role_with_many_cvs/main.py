#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from match_job_role_with_many_cvs.crew import MatchJobRoleWithManyCvs

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew to match two CVs against job roles.
    """
    inputs = {
        'path_to_jobs_csv': './src/match_job_role_with_many_cvs/data/jobs.csv',
        'path_to_cv': './src/match_job_role_with_many_cvs/data/cv.txt',
        'path_to_cv2': './src/match_job_role_with_many_cvs/data/cv2.txt'
    }
    
    try:
        MatchJobRoleWithManyCvs().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()

