import subprocess
import os


class ExecuteCommand:
    def block(executable: str, arguments: list, stdin=None, stdout=None, stderr=None, timeout=None) -> int:
        process = subprocess.Popen([executable] + arguments, stdin=stdin, stdout=stdout, stderr=stderr)
        try:
            process.wait(timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            # print to stderr
            print(f'Process {executable} {arguments} timed out after {timeout} seconds', file=stderr)
            return 504
        return process.returncode
        
    
    def non_block(executable: str, arguments: list, stdin=None, stdout=None, stderr=None) -> subprocess.Popen:
        process = subprocess.Popen([executable] + arguments, stdin=stdin, stdout=stdout, stderr=stderr)
        return process

class FileOperations:
    def write(path: str, content: str):
        with open(path, 'w') as file:
            file.write(content)

    def delete(*paths: str):
        for path in paths:
            os.remove(path)

def include(module: str):
    globals()[module] = __import__(module)
