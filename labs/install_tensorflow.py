import subprocess
import sys

wheel_file = 'tensorflow-2.7.0-cp38-cp38-manylinux2010_x86_64.whl'  # Replace with the correct wheel filename

try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', wheel_file])
    print("TensorFlow has been successfully installed.")
except subprocess.CalledProcessError as e:
    print(f"Error installing TensorFlow: {e}")
    sys.exit(1)
