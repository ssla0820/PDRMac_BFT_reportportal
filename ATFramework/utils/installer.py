import subprocess
import sys
import platform


class Pip:
    def __init__(self):
        self.current_process = 0
        self.package_name = None

    def __execute(self, cmd):
        if platform.system() == "Windows":
            cmd = [sys.executable.replace(".exe", "w.exe", -1)] + cmd
        else:
            cmd = [sys.executable] + cmd
        try:
            # print(f"{cmd=}")
            self.current_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return self.current_process
        except Exception as e:
            print(f"Install Exception: {e}")

    def install(self, package, _uninstall=False):
        self.package_name = package
        self.__execute(["-m", "pip", "install", package])
        return self

    def uninstall(self, package):
        self.__execute(["-m", "pip", "uninstall", "-y", package])
        return self

    def wait(self):
        try:
            ret = self.current_process.communicate()
            # print(f"result = {ret[0].decode('utf-8')}\n")
            return self
        except Exception as e:
            print(f"Wait Exception: {e}")
            return False

    def list(self):
        print("")
        self.__execute(["-m", "pip", "list"])
        msg = self.current_process.communicate()[0].decode("utf-8")
        print(msg)

    def apply(self, name=None, package=None):
        package = package or self.package_name
        name = name or package
        if not package: raise Exception("[Error] Package name is required")
        globals()[name] = __import__(package)


if __name__ == "__main__":
    package = "numpy"
    while option := int(input(f"0.Exit\n1.Install {package}\n2.Uninstall {package}\n"
                              f"3.List all\nYour Option:") or 0):
        if option == 1:
            p = Pip().install(package)
            print(f"installing - {package}")
            ret = p.wait()
            print(f"install completed - {ret}")
        elif option == 2:
            p = Pip().uninstall(package)
            print(f"uninstalling - {package}")
            ret = ret = p.wait()
            print(f"uninstall completed - {ret}")
        elif option == 3:
            Pip().list()
        else:
            break
