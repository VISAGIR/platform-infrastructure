##
# Docker Container Entrypoint Fundamentals
##

# 1. User and Group Management
# 2. Environment Setup
# 3. Command Handling
# 4. Script Execution

##
# Entrypoint Features
##

# 1. Argument Parsing
# 2. Root Privilege Checking
# 3. Home Directory Initialization
# 4. Bashrc Validation
# 5. Command Execution (bash, help, run)

import os
import sys
import argparse
import grp
import pwd
import subprocess
from pathlib import Path

# from ros2setup import Ros2Setup

class DockerEntrypointError(Exception):
    pass

class DockerEntrypoint:
    def __init__(self):
        self.commands = ['bash', 'help', 'run', 'status']
        self.progname = 'visagirDocker'
        self.parser = self._create_argument_parser()
        self.args = self.parser.parse_args()

        # try:
            # self.ros2 = Ros2Setup(ros_distro="humble") # Inject ROS2 dependency
            # self.ros2.source_environment()
        self._check_user_context()
        # except RuntimeError as e:
        #     sys.exit(f"ROS 2 setup failed: {str(e)}")

    @property
    def in_docker(self):
        return os.path.isfile('/.dockerenv')
    
    def _check_user_context(self):
        """
            # Verify running as dockeruser
            Verify running as ubuntu
        """
        # if os.getuid() != int(os.environ.get('HOST_UID', 1000)):
        #     print("Warning: Not running as dockeruser", file=sys.stderr)

        if os.getuid() != int(os.environ.get('HOST_UID', 1000)):
            print("Warning: Not running as ubuntu", file=sys.stderr)

    def _create_argument_parser(self):
        epilog = 'Supported Commands:\n\n' + '\n'.join(self.commands)
        parser = argparse.ArgumentParser(prog=self.progname, 
            description="VISAGIR Docker Entrypoint",
            epilog=epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('command', help='VISAGIR commands to execute', nargs='?', default='help', choices=self.commands)
        parser.add_argument('args', nargs=argparse.REMAINDER, help='Arguments for the command')
        return parser

    # 2. Add Environment Verification
    def _show_env_status(self):
        """
            Display environment configuration
        """
        # status = self.ros2.verify_setup()
        # print(f"ROS 2 {status['ros_distro']} environment")
        print(f"Python: {sys.executable}")
        print(f"Venv active: {'VIRTUAL_ENV' in os.environ}")
        # print(f"User: {os.getuid()/os.getgid()} (dockeruser)")
        print(f"User: {os.getuid()/os.getgid()} (ubuntu)")

    def _run_bash(self):
        """
            Start interactive shell
        """

        try:
            cmd = ["/usr/bin/bash"]
            if self.args.args:
                cmd.extend(self.args.args)
            os.execvp(cmd[0], cmd)
        except OSError as e:
            raise DockerEntrypointError(f"Error executing bash: {str(e)}")

    # 3. Secure Command Execution
    # def _run_ros2(self):
    #     """
    #         Execute ROS 2 command via venv
    #     """
    #     cmd = [self.ros2.python_path, "-m", "ros2cli"] + self.args.args
    #     os.execvp(cmd[0], cmd)


    def _run_script(self):
        """
            Execute custom script
        """
        if not self.args.args:
            raise DockerEntrypointError("No script specified")

        script = Path(self.args.args[0]).resolve()

        if not script.exists():
            raise DockerEntrypointError(f"Script not found: {script}")
        
        try:
            if script.suffix == '.py':
                cmd = [sys.executable, str(script)] + self.args.args[1:]
            else:
                if not os.access(script, os.X_OK):
                    raise DockerEntrypointError(f"Not executable: {script}")
                cmd = [str(script)] + self.args.args[1:]

            os.execvp(cmd[0], cmd)

        except OSError as e:
            raise DockerEntrypointError(f"Error executing script: {str(e)}")

    @staticmethod
    def _eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)
    
    @staticmethod
    def _run_command(command):
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            raise DockerEntrypointError(f"Error running command '{command}': {str(e)}")
    
    def _execute_command(self):
        if self.args.command == 'bash':
            self._run_bash()
        # elif self.args.command == 'ros2':
        #     self._run_ros2()
        elif self.args.command == 'run':
            self._run_script()
        elif self.args.command == 'status':
            self._show_status()
        elif self.args.command == 'help':
            self.parser.print_help()
        else:
            self.parser.print_help()

    def run(self):
        try:
            self._execute_command()
        except DockerEntrypointError as e:
            self._eprint(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(1)
    

if __name__ == "__main__":
    entrypoint = DockerEntrypoint()
    entrypoint.run()
