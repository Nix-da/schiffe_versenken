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

    # Create DMG for macOS
    if os.name == 'posix':
        app_name = 'YourAppName'  # Replace with your app's name
        dmg_name = 'YourAppName'  # Replace with the desired name of your DMG file
        dmg_path = os.path.join('dist', f'{dmg_name}.dmg')
        app_path = os.path.join('dist', f'{app_name}.app')

        # hdiutil command
        hdiutil_command = f'hdiutil create -volname {app_name} -srcfolder {app_path} -ov -format UDZO {dmg_path}'

        # Execute the command
        process = subprocess.Popen(hdiutil_command, shell=True, stdout=subprocess.PIPE)
        process.wait()

        print(f'DMG created at {dmg_path}.')

# Call the function
create_exe_with_pyinstaller()