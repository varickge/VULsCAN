import json
import os

from agency_swarm.tools import BaseTool
from pydantic import Field
from git import Repo
import requests
import shutil 

from dotenv import load_dotenv

load_dotenv()

class GitHubPullRequester(BaseTool):
    """
    Fetches source code from GitHub repository.
    """

    def run(self):
        res = {}
        self.repo_url = get
        self.file_extensions = get

        temp_clone_folder = 'temp_repo'
        if os.path.exists(temp_clone_folder):
            shutil.rmtree(temp_clone_folder)
        Repo.clone_from(self.repo_url, temp_clone_folder)

        for root, _, files in os.walk(temp_clone_folder):
            for file in files:
                if any(file.endswith(ext) for ext in self.file_extensions):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        res['file'] = f.read()
                    os.remove(file_path)

        return res



if __name__ == "__main__":
    tool = GitHubPullRequester()
    print(tool.run())