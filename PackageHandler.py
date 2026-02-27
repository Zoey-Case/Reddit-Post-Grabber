import sys
import subprocess

def ensure_installed(package_name):
    try:
        __import__(package_name)
        print(f"Package '{package_name}' is already installed.")
    except ModuleNotFoundError:
        print(f"Package '{package_name}' is NOT installed.")
        print(f"Attempting to install '{package_name}' using pip...")
    
    try:
        # Get the path to the current Python executable
        python_executable = sys.executable
        # Run pip install command
        # Use check_call to raise an error if install fails
        # Use DEVNULL to suppress pip's output (optional)
        subprocess.check_call(
            [python_executable, '-m', 'pip', 'install', package_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL # Suppress errors too if desired
        )
        print(f"Successfully installed '{package_name}'.")
        # You might want to re-attempt the import here if needed immediately,
        # though sometimes restarting the script might be necessary for Python
        # to fully recognize the new package path.
        # __import__(package_name) # Re-try import
    
    except subprocess.CalledProcessError as e:
        print(f"Failed to install '{package_name}'. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during installation: {e}")