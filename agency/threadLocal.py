import threading

thread_local_data = threading.local()

def init_thread_local_data():
    thread_local_data.repo_link = ''
    thread_local_data.file_extension = ''
    thread_local_data.report_path = ''