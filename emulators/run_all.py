import subprocess


processes = [
    subprocess.Popen(
        [
            "uvicorn",
            "emulators.stable_api:app",
            "--port",
            "9001"
        ]
    ),

    subprocess.Popen(
        [
            "uvicorn",
            "emulators.slow_api:app",
            "--port",
            "9002"
        ]
    ),

    subprocess.Popen(
        [
            "uvicorn",
            "emulators.unstable_api:app",
            "--port",
            "9003"
        ]
    )
]


print("All emulator APIs started.")

try:
    for process in processes:
        process.wait()

except KeyboardInterrupt:

    print("Stopping emulators...")

    for process in processes:
        process.terminate()