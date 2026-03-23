import sys
import subprocess

def EnsureInstalled(packageName):
    try:
        __import__(packageName)
        print(f"Package '{packageName}' is already installed.")
    except ModuleNotFoundError:
        print(f"Package '{packageName}' is NOT installed.")
        print(f"Attempting to install '{packageName}' using pip...")
    
        try:
            executable = sys.executable
            
            subprocess.check_call(
                [executable, '-m', 'pip', 'install', packageName],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"Successfully installed '{packageName}'.")
        
        except subprocess.CalledProcessError as e:
            print(f"Failed to install '{packageName}'. Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during installation: {e}")