import subprocess
import os

def run_docker_bake():
    # Get the directory of the current script
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Get host's UID/GID
    # NOTE: Doesn't work on MacOSX
    # HOST_UID = os.getuid()
    # HOST_GID = os.getgid()

    # Navigate up to the project root directory
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))

    # Define the relative path to r-20-entries
    ENTRIES_PATH = os.path.join(PROJECT_ROOT, 'docker', 'ezedgepipeline', 'ubuntu24_04', 'r_20_entries')

    print(f"ENTRIES_PATH = {ENTRIES_PATH}")

    # Define the path to the docker-bake.hcl file
    BAKE_DIR = os.path.join(PROJECT_ROOT, 'docker', 'ezedgepipeline', 'ubuntu24_04')
    BAKE_FILE = os.path.join(BAKE_DIR, 'docker-bake.hcl')

    # Change working directory to where docker-bake.hcl is located
    os.chdir(BAKE_DIR)

    # Clean up before build
        # Prune build cache to remove intermediate layers
        # Remove dangling images after each build
        # Force overwrite existing tags during build
    subprocess.run(["docker", "builder", "prune", "-f"], check=False)
    subprocess.run(["docker", "image", "prune", "-f"], check=False)


    # Define the command with the --allow flag to avoid confirmation prompts
    command = [
        "docker", "buildx", "bake", 
        # "--no-cache", # Prevent layer reuse issues
        "--pull", # Ensure fresh base images
        # "--set", f"*.args.HOST_UID={HOST_UID}",
        # "--set", f"*.args.HOST_GID={HOST_GID}",
        f"--allow=fs.read={ENTRIES_PATH}",
        "--allow=network.host",
        "-f", BAKE_FILE
    ]


    try:
        subprocess.run(command, check=True)
        print("Docker buildx bake executed successfully with host UID/GID mapping.")

        subprocess.run(["docker", "image", "prune", "-f"], check=False)
        print("Cleaned up dangling images. For ex, <none> images")

    except subprocess.CalledProcessError as e:
        print(f"Error during Docker buildx bake: {e}")
        exit(1)

if __name__ == "__main__":
    run_docker_bake()
