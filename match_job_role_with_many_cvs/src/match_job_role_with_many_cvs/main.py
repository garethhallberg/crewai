#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime
from crewai_tools import DirectoryReadTool
from PyPDF2 import PdfReader
import logging

from match_job_role_with_many_cvs.crew import MatchJobRoleWithManyCvs

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def get_cv_files(cv_dir):
    """
    Get all .txt and .pdf files from the CV directory.
    Returns a list of full paths to the CV files.
    Skips password-protected PDFs and logs them.
    """
    cv_files = []
    for file in os.listdir(cv_dir):
        file_path = os.path.join(cv_dir, file)
        if file.endswith('.txt'):
            cv_files.append(file_path)
        elif file.endswith('.pdf'):
            try:
                # Try to open the PDF to check if it's password protected
                with open(file_path, 'rb') as pdf_file:
                    reader = PdfReader(pdf_file)
                    if reader.is_encrypted:
                        logger.info(f"Skipping password-protected PDF: {file}")
                        continue
                    cv_files.append(file_path)
            except Exception as e:
                logger.warning(f"Error processing PDF {file}: {str(e)}")
                continue
    
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
    
    # Create a string with all CV file paths
    cv_files_str = "\n".join([f"CV file: {cv_file}" for cv_file in cv_files])
    
    inputs = {
        'path_to_jobs_csv': './src/match_job_role_with_many_cvs/data/jobs.csv',
        'cv_files': cv_files_str
    }
    
    try:
        MatchJobRoleWithManyCvs().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()

