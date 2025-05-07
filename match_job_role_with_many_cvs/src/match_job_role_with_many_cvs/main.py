#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime
from crewai_tools import DirectoryReadTool

from match_job_role_with_many_cvs.crew import MatchJobRoleWithManyCvs

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew to match CVs against job roles.
    """
    cv_dir = './src/match_job_role_with_many_cvs/data/cvs'
    
    # Get list of CV files from the directory
    cv_files = [f for f in os.listdir(cv_dir) if f.endswith('.txt')]
    
    if len(cv_files) < 3:
        raise Exception("At least three CV files are required in the cvs directory")
    
    # Get the first three CV files
    cv1 = os.path.join(cv_dir, cv_files[0])
    cv2 = os.path.join(cv_dir, cv_files[1])
    cv3 = os.path.join(cv_dir, cv_files[2])
    
    inputs = {
        'path_to_jobs_csv': './src/match_job_role_with_many_cvs/data/jobs.csv',
        'path_to_cv': cv1,
        'path_to_cv2': cv2,
        'path_to_cv3': cv3
    }
    
    try:
        MatchJobRoleWithManyCvs().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()

