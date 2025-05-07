#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from cv_to_jobs_match.crew import CvToJobsMatch

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'path_to_jobs_csv': './src/cv_to_jobs_match/data/jobs.csv',
        'path_to_cv': './src/cv_to_jobs_match/data/cv.txt'
    }

    try:
        CvToJobsMatch().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
