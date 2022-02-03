from cx_Freeze import setup, Executable

setup(
    name = "mythDrive",
    version = "0.1",
    description = "My Sync Drive whitout install.",
    executables = [Executable("main.py", base="Win32GUI")]
)