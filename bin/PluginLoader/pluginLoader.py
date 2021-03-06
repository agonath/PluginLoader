#
# - Updated function "normalizeModuleName", replaced if-statements with lookup in "importlib.machinery" for known file extensions. - Agonath - 08.12.2018
# - Added "unload_Module" and "reload_ModuleByPath" - both needs to be tested - Agonath - 02.12.2018 -
# 
#


import importlib
from importlib import machinery
import sys
import os
from os import path
#import marshal


# Directory separator
SEP=os.sep

class PluginLoader(object):

    #
    # Helper: Remove file format endings if needed.
    #
    def normalizeModuleName(self, _moduleName):
        if(0 < len(_moduleName)):
            extension_list = importlib.machinery.all_suffixes() # "all_suffixes" returns a list with all known python module file extensions
            extension_list.append('.pyo') # old extension is missing?
            for item in extension_list:
                if(True == _moduleName.endswith(item)):
                    return _moduleName[:-(len(item))]
            return _moduleName
                
            

    #
    # Load a class from module in given path.
    #
    # Module parameter must be a "*.py", "*.pyc" or "*.pyo" file.
    # Path parameter points to the local directory by default.
    # Class name must be a class within the module.
    #
    # Example:  " loadModuleByPath(_path="..\\Programs\\Plugins", _moduleName="test", _className="myClass") "
    #           OR " loadModuleByPath(_moduleName="test.pyc", _className="myClass") "
    #
    def load_ModuleAndGetClass(self, *, _className, _moduleName, _path=str(".\\" + SEP)):
        try:
            moduleABC= self.load_ModuleByPath(_path=_path, _moduleName = _moduleName)
            classABC = self.load_ClassFromModule(_className = _className, _module=moduleABC)
            return classABC
        except Exception as e:
            print(e)
        

    #
    # Load module by path.
    # Module must be a "*.py", "*.pyc" or "*.pyo" file.
    # 
    # Example: loadModuleByPath(_path="..\\Programs\\Plugins", _moduleName="test")
    #
    def load_ModuleByPath(self, *, _path=str(".\\" + SEP), _moduleName):
        if(len(_moduleName) > 0):            
            if(len(_path) > 0):
                # add path to list of known system paths
                if(_path not in sys.path):
                    sys.path.append(_path)
            # try to load module
            try:
                name = self.normalizeModuleName(_moduleName)
                module = importlib.import_module(name)
                sys.modules[name] = module
                return module
            except Exception as e:
                print(e)


    #
    # Reload a previously loaded module by path.
    # Module must be a "*.py", "*.pyc" or "*.pyo" file.
    # 
    # Example: reloadModuleByPath(_path="..\\Programs\\Plugins", _moduleName="test")
    #
    def reload_ModuleByPath(self, *, _path=str(".\\" + SEP), _moduleName):
        if(len(_moduleName) > 0):
            mod = self.normalizeModuleName(_moduleName)
            
            if(len(_path) > 0):
                # add path to list of known system paths
                if(_path not in sys.path):
                    sys.path.append(_path)
            # try to reload module
            try:
                return importlib.reload(mod)
            except Exception as e:
                print(e)


    #
    # Unload a previously loaded module.
    # Module must be previously loaded.
    # 
    # Example: unload_Module(_moduleName="test")
    #
    def unload_Module(self, *, _moduleName):
        if(len(_moduleName) > 0):
            mod = self.normalizeModuleName(_moduleName)
            
            # try to unload the module
            try:
                return importlib.sys.modules.pop(mod)
            except Exception as e:
                print(e)



    #
    # Load a class from a given module.
    # Module must be an instance of <class, module>.
    #
    def load_ClassFromModule(self, *, _className, _module):
        if(len(_className) > 0 and None != _module):
            try:
                # try to find the class
                return (getattr(_module, _className))
            except Exception as e:
                print(e)

