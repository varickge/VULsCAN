from agency_swarm.agents import Agent
from agency_swarm.tools import CodeInterpreter

class CodeAnalyzer(Agent):
    def __init__(self):
        super().__init__(
            name="CodeAnalyzer",
            description="Specializes in retrieving the entire source code using the GitHub API, analyzing it against predefined quality and security standards. Communicates comprehensive findings to the Report Generator Agent for report compilation.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[CodeInterpreter],
            tools_folder="./tools"
        )
