import PyInstaller.__main__


PyInstaller.__main__.run([
    'main.py',
    '--clean',
    '--onefile',
    '--noconsole',
    '--icon=.\Skull-Halloween-by-Daniele-De-Santis.ico',
])
