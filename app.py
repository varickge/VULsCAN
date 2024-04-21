import gradio as gr

from agency_swarm import Agency
from agency.ReportGenerator import ReportGenerator
from agency.CodeAnalyzer import CodeAnalyzer
from agency.CEO import CEO

from dotenv import load_dotenv
load_dotenv()

ceo = CEO()
code_analyzer = CodeAnalyzer()
report_generator = ReportGenerator()

agency = Agency([ceo, [ceo, code_analyzer],
                 [code_analyzer, report_generator]],
                shared_instructions='./agency_manifesto.md')

def analyze_code(repo_link, code_type):
    # Placeholder for your code analysis logic
    # You would typically clone the repo and analyze files based on code_type here
    message = agency.get_completion("Please analyze the code and generate a report.",
                                yield_messages=False)
    # Dummy data for demonstration
    result_summary = f"Analysis completed for {code_type} files in {repo_link}"

    
    return message

# Define the dropdown options for code types
code_types = ["Python", "C++", "C", "Java", "JavaScript"]

# Setup the Gradio interface
iface = gr.Interface(
    fn=analyze_code,
    inputs=[
        gr.Textbox(label="GitHub Repository Link", placeholder="Enter GitHub repo URL here"),
        gr.Dropdown(label="Select Code Type", choices=code_types)
    ],
    outputs=[gr.Textbox(label="Result Summary")],
    title="VULsCAN Code Analysis Tool",
)

iface.launch()
