import os
import subprocess
import shutil

def create_exe_with_pyinstaller():
    # Path to your main.py file
    main_script = 'main.py'

    # PyInstaller command
    pyinstaller_command = f'pyinstaller --onefile {main_script}'

    # Execute the command
    process = subprocess.Popen(pyinstaller_command, shell=True, stdout=subprocess.PIPE)
    process.wait()

    print(f'Executable created in the dist folder.')

    # Copy assets folder to dist folder
    shutil.copytree('../assets', './dist/assets', dirs_exist_ok=True)
    print('Assets copied to dist folder.')

# Call the function
create_exe_with_pyinstaller()
