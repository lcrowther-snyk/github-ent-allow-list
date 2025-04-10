import shutil

if shutil.which("gh") is not None:
    print("The 'gh' command is available in the PATH.")
else:
    print("The 'gh' command is not available in the PATH.")