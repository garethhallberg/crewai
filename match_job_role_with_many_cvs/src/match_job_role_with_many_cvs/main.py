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

def get_cv_files(cv_dir):
    """
    Get all .txt files from the CV directory.
    Returns a list of full paths to the CV files.
    """
    cv_files = []
    for file in os.listdir(cv_dir):
        if file.endswith('.txt'):
            cv_files.append(os.path.join(cv_dir, file))
    return sorted(cv_files)  # Sort to ensure consistent order

def run():
    """
    Run the crew to match CVs against job roles.
    """
    cv_dir = './src/match_job_role_with_many_cvs/data/cvs'
    
    # Get all CV files from the directory
    cv_files = get_cv_files(cv_dir)
    
    if len(cv_files) < 2:
        raise Exception("At least two CV files are required in the cvs directory")
    
    # For now, we'll still use just the first three CVs to maintain compatibility
    # with the current task configuration
    cv1 = cv_files[0]
    cv2 = cv_files[1]
    cv3 = cv_files[2] if len(cv_files) > 2 else None
    
    if not cv3:
        raise Exception("Three CV files are required in the cvs directory")
    
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

