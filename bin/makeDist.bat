xcopy /Y "..\src\pluginLoader.py" "PluginLoader\"
python setup.py sdist --formats=zip,gztar
pause