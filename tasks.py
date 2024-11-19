import subprocess
import os
import importlib

import criteria

global bindings

class ExecuteCommand:
    def block(executable: str, arguments: list, stdin=None, stdout=None, stderr=None, timeout=None, cwd=None) -> int:
        process = subprocess.Popen([executable] + arguments, stdin=stdin, stdout=stdout, stderr=stderr, cwd=cwd)
        try:
            process.wait(timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            # print to stderr
            print(f'Process {executable} {arguments} timed out after {timeout} seconds', file=stderr)
            return 504
        return process.returncode
        
    
    def non_block(executable: str, arguments: list, stdin=None, stdout=None, stderr=None, cwd=None) -> subprocess.Popen:
        process = subprocess.Popen([executable] + arguments, stdin=stdin, stdout=stdout, stderr=stderr, cwd=cwd)
        return process

class FileOperations:
    def write(path: str, content: str):
        with open(path, 'w') as file:
            file.write(content)

    def delete(*paths: str):
        for path in paths:
            os.remove(path)

class Debug:
    def print(*args, **kwargs):
        print(*args, **kwargs)

    def print_bindings():
        print(bindings)

def include(module: str):
    components = module.split('.')
    package_name = components[0]  # Get the top-level package
    globals()[package_name] = importlib.import_module(package_name)  # Import the top-level package
    
    # Import the full module and assign it globally
    globals()[module] = importlib.import_module(module)
