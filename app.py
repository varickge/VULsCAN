import gradio as gr

from agency_swarm import Agency
from agency.ReportGenerator import ReportGenerator
from agency.CodeAnalyzer import CodeAnalyzer
from agency.CEO import CEO
from agency.threadLocal import thread_local_data, init_thread_local_data
from gradio.components import HTML
from dotenv import load_dotenv
load_dotenv()

ceo = CEO()
code_analyzer = CodeAnalyzer()
report_generator = ReportGenerator()

agency = Agency([ceo, [ceo, code_analyzer],
                 [code_analyzer, report_generator]],
                shared_instructions='./agency_manifesto.md')

def analyze_code(repo_link, code_type):
    init_thread_local_data()
    thread_local_data.repo_link = repo_link
    thread_local_data.file_extension = code_type

    # Placeholder for your code analysis logic
    # You would typically clone the repo and analyze files based on code_type here
    message = agency.get_completion(f"Please analyze the code and generate a report.Repo URL: {repo_link}",
                                yield_messages=False)
    
    # Dummy data for demonstration
    result_summary = f"<h3>Analysis Summary</h3>Analysis completed for {code_type} files in {repo_link}.<br><b>Results:</b><br>{message}"

    return result_summary, thread_local_data.report_path

# Define the dropdown options for code types
code_types = [("Python", ".py"), ("C++", ".cpp"), ("C", ".c"), ("Java", ".java"), ("JavaScript", ".js")]

# Setup the Gradio interface
iface = gr.Interface(
    fn=analyze_code,
    inputs=[
        gr.Textbox(label="GitHub Repository Link", placeholder="Enter GitHub repo URL here"),
        gr.Dropdown(label="Select Code Type", choices=code_types)
    ],
    outputs=[
        HTML(label="Result Summary"),
        gr.File(label="Download Report")
    ],
    title="VULsCAN Code Analysis Tool",
)

iface.launch()
