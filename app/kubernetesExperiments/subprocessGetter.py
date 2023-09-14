import subprocess

try:
    result = subprocess.run(['lscpu'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("RESULT:", result.returncode)
    if result.returncode == 0:
        print("Salida:", result.stdout.decode('utf-8'))
    else:
        print("Error:", result.stderr.decode('utf-8'))
except Exception as e:
    print("Excepción:", str(e))
