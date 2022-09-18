import sys
import os
from cx_Freeze import setup, Executable

# ADD FILES
files = ['space_invader_icon.ico']

# TARGET
target = Executable(
    script="matmatar.py",
    icon="space_invader_icon.ico"
)

# SETUP CX FREEZE
setup(
    name = "MatMatar",
    version = "1.0",
    description = "tests your crappy java code",
    author = "Matheus Tran",
    options = {'build_exe' : {'include_files' : files}},
    executables = [target]
)
