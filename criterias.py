import os
import re

global bindings

class ByteStream:
    
    def get_content(arg) -> str:
        if isinstance(arg, str):
            return arg
        elif hasattr(arg, 'read'):
            return arg.read()
        else:
            raise TypeError("Argument must be a string or file-like object.")
        
    def diff(s1, s2) -> bool:
        content1 = ByteStream.get_content(s1)
        content2 = ByteStream.get_content(s2)

        return ''.join(content1.split()) == ''.join(content2.split())
    
    def wc(s) -> int:
        content = ByteStream.get_content(s)
        return len(content.split())

    def lc(s) -> int:
        content = ByteStream.get_content(s)
        return len(content.splitlines())
    
    def contains(s, substr, ignore_ws=False) -> bool:
        content = ByteStream.get_content(s)
        if ignore_ws:
            content = re.sub(r'\s+', '', content)
            substr = re.sub(r'\s+', '', substr)
        return substr in content
    
    def contains_all(s, substrs, ignore_ws=False) -> bool:
        content = ByteStream.get_content(s)
        if ignore_ws:
            content = re.sub(r'\s+', '', content)
            substrs = [re.sub(r'\s+', '', substr) for substr in substrs]
        return all(substr in content for substr in substrs)
    
    def missing_n(s, substrs, ignore_ws=False) -> int:
        content = ByteStream.get_content(s)
        if ignore_ws:
            content = re.sub(r'\s+', '', content)
            substrs = [re.sub(r'\s+', '', substr) for substr in substrs]
        return len([substr for substr in substrs if substr not in content])
    
    def count(s, substr, ignore_ws=False) -> int:
        content = ByteStream.get_content(s)
        if ignore_ws:
            content = re.sub(r'\s+', '', content)
            substr = re.sub(r'\s+', '', substr)
        return content.count(substr)
    
    def read_int(s) -> int:
        content = ByteStream.get_content(s)
        return int(content)
    
    def match(s, pattern) -> bool:
        content = ByteStream.get_content(s)
        return re.match(pattern, content) is not None

class AssertFile:

    def exists(path: str) -> bool:
        try:
            with open(path, 'r') as file:
                return True
        except FileNotFoundError:
            return False

    def is_empty(path: str) -> bool:
        with open(path, 'r') as file:
            return len(file.read()) == 0

    def is_dir(path: str) -> bool:
        return os.path.isdir(path)

    def is_file(path: str) -> bool:
        return os.path.isfile(path)

    def is_executable(path: str) -> bool:
        return os.access(path, os.X_OK)

    def is_readable(path: str) -> bool:
        return os.access(path, os.R_OK)

    def is_writable(path: str) -> bool:
        return os.access(path, os.W_OK)

    def is_symlink(path: str) -> bool:
        return os.path.islink(path)

    def is_pipe(path: str) -> bool:
        return os.path.isfifo(path)

    def is_socket(path: str) -> bool:
        return os.path.isscoket(path)

    def is_block_device(path: str) -> bool:
        return os.path.isblock(path)

    def is_char_device(path: str) -> bool:
        return os.path.ischar(path)

    def is_mount_point(path: str) -> bool:
        return os.path.ismount(path)

    def is_absolute(path: str) -> bool:
        return os.path.isabs(path)

    def is_relative(path: str) -> bool:
        return not os.path.isabs(path)

    def is_readable(path: str) -> bool:
        return os.access(path, os.R_OK)

    def is_writable(path: str) -> bool:
        return os.access(path, os.W_OK)

    def is_executable(path: str) -> bool:
        return os.access(path, os.X_OK)

    def is_hidden(path: str) -> bool:
        return path.startswith('.')

    def is_empty(path: str) -> bool:
        return os.path.getsize(path) == 0

    def is_empty_dir(path: str) -> bool:
        return len(os.listdir(path)) == 0

    def is_same_file(path1: str, path2: str) -> bool:
        return os.path.samefile(path1, path2)

    def is_same_file_descriptor(fd1: int, fd2: int) -> bool:
        return os.path.sameopenfile(fd1, fd2)

class AssertBinding:

    def exists(name: str) -> bool:
        return name in bindings
    
    def get(name: str):
        if AssertBinding.exists(name):
            return bindings[name]
        else:
            return None
    
    def eq(name: str, value) -> bool:
        return AssertBinding.get(name) == value
    
    def ne(name: str, value) -> bool:
        return not AssertBinding.eq(name, value)

class AssertType:
    def isinstance(obj, cls) -> bool:
        return isinstance(obj, cls)
