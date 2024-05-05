import json
import os

from agency_swarm.tools import BaseTool
from pydantic import Field
from git import Repo
import requests
import shutil 
import traceback

from dotenv import load_dotenv
from agency.threadLocal import thread_local_data

load_dotenv()

class GitHubPullRequester(BaseTool):
    """
    Fetches source code from GitHub repository.
    """

    def run(self):
        try:
            res = {}
            repo_url = thread_local_data.repo_link
            file_extensions = thread_local_data.file_extension
            print(repo_url, file_extensions)
            temp_clone_folder = 'temp_repo'
            if os.path.exists(temp_clone_folder):
                shutil.rmtree(temp_clone_folder)
            Repo.clone_from(repo_url, temp_clone_folder)

            def read_file_with_fallback(file_path, encoding='utf-8'):
            # for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        return f.read()
                except UnicodeDecodeError:
                    pass
                # raise Exception(f"All specified encodings failed for file: {file_path}")

            for root, _, files in os.walk(temp_clone_folder):
                for file in files:
                    if any(file.endswith(ext) for ext in file_extensions):
                        file_path = os.path.join(root, file)
                        res[file] = read_file_with_fallback(file_path)
                        os.remove(file_path)

            return res
        except Exception as e:
            print(f"Error occurred: {traceback.format_exc()}")
            return f"Error occurred: {traceback.format_exc()}"

if __name__ == "__main__":
    tool = GitHubPullRequester()
    print(tool.run())