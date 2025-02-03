import contextlib
import inspect
import platform
import re
import shlex
import threading
from subprocess import check_output, PIPE, Popen
import os, time, uuid, tempfile, glob
from types import SimpleNamespace
from ctypes import c_bool
from multiprocessing import Process, Pool, Value

from ..utils import logger
from ..utils import Pip

from Quartz import *
import cv2
from pynput.mouse import Button as mouse_btn, Controller as Mouse_ctrl
from pynput.keyboard import Key as kb_key, Controller as Kb_ctrl, KeyCode
from AppKit import NSScreen, NSBundle, NSRunningApplication as ra
from Foundation import *

import atomac
from atomac.AXClasses import NativeUIElement
from .Mac_Control import MWC

try:
    import ffmpeg_quality_metrics as ffqm
except:
    logger("Initial system, please wait")
    Pip().install("ffmpeg_quality_metrics").wait().apply("ffqm")

# from log import logger
temp_dir = os.path.abspath(tempfile.gettempdir() + "/mac_driver")
os.makedirs(temp_dir, exist_ok=True)
NSBundle.mainBundle().infoDictionary()["LSBackgroundOnly"] = "1"
nc = NSDistributedNotificationCenter.defaultCenter()

for f in glob.glob(f'{temp_dir}/*'):
    try:
        os.remove(f)
    except:
        ...  # removed by others thread
screen_w, screen_h = list(map(int, NSScreen.mainScreen().frame().size))
source_w = 1440  # captured target image
ratio = 1  # disable this feature temporarily
ACTION_DELAY = 1


def click(self):
    def performSpecifiedAction():
        try:
            self._activate()
        except:
            pass
        time.sleep(0.5)
        try:
            return self._performAction("Press")
        except:
            pass

    threading.Thread(target=performSpecifiedAction).start()


def get_center(obj):
    x, y = obj.AXPosition
    w, h = obj.AXSize
    return (int(x + w / 2), int(y + h / 2))


def _position_set(self, pos, delta=15):
    try:
        (_, _, mouse_type), mouse_button = self._drag_button.value
    except AttributeError:
        mouse_type = kCGEventMouseMoved
        mouse_button = 0
    event = CGEventCreateMouseEvent(
        None,
        mouse_type,
        pos,
        mouse_button)
    if mouse_type in [kCGEventLeftMouseDragged,
                      kCGEventRightMouseDragged,
                      kCGEventOtherMouseDragged]:
        if delta:
            delta_x, delta_y = delta, delta
        else:
            pos_org = self._position_get()
            delta_x, delta_y = pos[0] - pos_org[0], pos[1] - pos_org[1]
        CGEventSetIntegerValueField(
            event,
            kCGMouseEventDeltaX,
            delta_x)
        CGEventSetIntegerValueField(
            event,
            kCGMouseEventDeltaY,
            delta_y)
    CGEventPost(
        kCGHIDEventTap,
        event)


class Mac(MWC):

    def __init__(self, bundle_id, app_path, app_name):
        setattr(NativeUIElement, "press", click)
        setattr(NativeUIElement, "center", property(get_center))
        setattr(Mouse_ctrl, "_position_set", _position_set)
        self.bundle_id = bundle_id
        self.app_path = app_path
        self.app_name = app_name
        self.mouse = Mouse()
        self.image = Image()
        self.video = Video()
        self.keyboard = Keyboard()
        self.size = {"w": screen_w, "h": screen_h}
        self.top = None
        self.file = File()

    @property
    def pid(self):
        try:
            return ra.runningApplicationsWithBundleIdentifier_(self.bundle_id)[0].processIdentifier()
        except:
            return None

    @property
    def cpu(self):
        cmd = f'''ps xo %cpu,rss,vsz,command | awk 'NR>1 {{$2=int(($2+$3)/1024)"M"; $3=""}}{{ print ;}}' | grep ''' + self.app_path.replace(
            " ", "\\ ")
        try:
            ret = re.findall(r"(\d+\.\d+)", self.shell(cmd))
            cpu = -1 if len(ret) < 2 else float(ret[0])
            logger(f"Current CPU usage: {cpu}%")
            return cpu
        except:
            return

    @property
    def ram_v2(self):
        cmd = f'''ps xo %cpu,rss,vsz,command | awk 'NR>1 {{$2=int(($2+$3)/1024)"M"; $3=""}}{{ print ;}}' | grep ''' + self.app_path.replace(
            " ", "\\ ")
        try:
            ram = int(re.findall(" (\d+)M", self.shell(cmd))[0])
            logger(f"Current RAM uasge: {ram}M")
            return ram
        except Exception as e:
            logger(f"{e=}")
            return

    @property
    def ram(self):
        cmd = f"footprint -p {self.pid} | grep phys_footprint: | awk '{{print $2}}'"
        try:
            ram = int(self.shell(cmd) or -1)
            logger(f"Current RAM uasge: {ram}M")
            return ram
        except Exception as e:
            logger(f"{e=}")
            return

    def _get_app_ref(self, bundle_id=None, app_name=None):
        bundle_id = bundle_id or self.bundle_id
        app_name = app_name or self.app_name
        try:
            if self.bundle_id:
                return atomac.getAppRefByBundleId(bundle_id)
            elif self.app_name:
                return atomac.getAppRefByLocalizedName(app_name)
        except Exception:
            # logger(f"[Error] Unable to get app reference: {Exception}")
            return

    def notification(self, *args):
        logger(*args[:4])
        nc.postNotificationName_object_userInfo_deliverImmediately_(*args[:4])

    def backdoor(self, action, get_value=False):
        try:
            values = inspect.getargvalues(inspect.stack(2)[1][0])[3].copy()
            del values["self"]
            logger(values)
            if get_value:
                filename = self.file.get_temp()
                values["filename"] = filename
                self.notification(action, None, values, True)
                ret = eval(self.file.read(filename))
                self.file.remove(filename)
            else:
                self.notification(action, None, values, True)
                ret = True
            del values
            return ret
        except Exception as e:
            logger(f"{e=}")
            return False

    def getRunningAppByBundleId(self, bundle_id=None, get_all=False):
        bundle_id = bundle_id or self.bundle_id
        if get_all:
            return ra.runningApplicationsWithBundleIdentifier_(self.bundle_id)
        else:
            return ra.runningApplicationsWithBundleIdentifier_(self.bundle_id)[0]

    def is_active(self):
        return self.getRunningAppByBundleId().isActive()

    def activate(self):
        return self.getRunningAppByBundleId().activateWithOptions_(2)

    def getAppRefByPid(self, pid):
        return atomac.getAppRefByPid(pid)

    def getRunningAppRefsByBundleId(self, bundle_id):
        ret = []
        apps = ra.runningApplicationsWithBundleIdentifier_(bundle_id)
        for app in apps:
            ret.append(atomac.getAppRefByPid(app.processIdentifier()))
        return ret

    def get_top(self, bundle_id=None, timeout=30):
        timer = time.time()
        while not (ret := self._get_app_ref(bundle_id)) and (time.time() - timer) < timeout:
            if not ret:
                self._launch_app()
        else:
            self.top = ret
            return ret

    def get_screenshot_as_file(self, file_path):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            self.image.screenshot(file_path)
            return True
        except Exception as e:
            logger(f'Exception: ({e})')
            return False

    @staticmethod
    def shell(cmd):
        # args = shlex.split(cmd)
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        # if err: logger(f'error = {err.decode("utf-8")}')
        return out.decode("utf-8")

    def is_app_exist(self):
        """
        :return: True/False
        """
        try:
            # check if app opened(2 methods: check top element / check alive(need to use if in another full screen) )
            # method 1:
            if self.get_current_wnd(self.get_top_element()):
                return True
        except Exception as e:
            return False

    def get_top_element(self):
        """
        return Atomac_element, else False
            Get the top level element for the application with the specified
            bundle ID, such as com.vmware.fusion.
        """
        try:
            # source code: NativeUIElement.getAppRefByBundleId
            top_native_el = self._get_app_ref()
            # print(f'[{MWC.func_name()}]: Native_Element({top_native_el})')
            return top_native_el
        except:
            return False

    def get_current_wnd(self, el):
        """
        return Atomac_element, else False
        """
        try:
            cur_win = el.windows()[0]
            return cur_win
        except Exception as e:
            return False

    def _launch_app(self):
        if self.app_path:
            return atomac.launchAppByBundlePath(self.app_path)
        else:
            return atomac.launchAppByBundleId(self.bundle_id)

    def launch_app(self, timeout=15, get_main_wnd=1, skip_exist=0):
        """
        Return Top el/False/True
            Check if App is not launched and then execute,
            after that, make sure atomac get top_element & window
            for only activate window: get_main_wnd=0, only execute launch and return True
        """
        try:
            self.top = self._launch_app()
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    self.top = self.activate()
                    break
                except:
                    self.terminate_app()
                    time.sleep(ACTION_DELAY * 3)
                    self.top = self._launch_app()
            return self.top
        except Exception as e:
            print('Exception occurs')
            return False

    def terminate(self):
        for app in self.getRunningAppByBundleId(get_all=True):
            app.terminate()

    def force_terminate(self):
        for app in self.getRunningAppByBundleId(get_all=True):
            app.forceTerminate()

    def terminate_app(self, forcemode=0, timeout=15):
        """
        close success: return True, others: return False
        """
        try:
            # use force kill  (need app_bundleID)
            if forcemode == 1:
                try:
                    apps = ra.runningApplicationsWithBundleIdentifier_(self.bundle_id)
                    for app in apps:
                        os.popen(f"kill {app.processIdentifier()}")
                except Exception as e:
                    logger(f'Exception. ({e})')
                    pass
            else:
                # use atomac
                atomac.terminateAppByBundleId(self.bundle_id)
            # check if app is closed
            # wait till NOT get element & window
            wait_time = 0
            while wait_time < timeout:
                if self.get_current_wnd(self.get_top_element()) is False:
                    logger('Done')
                    return True
                else:
                    logger(f'wait... {wait_time}sec.')
                    time.sleep(1)
                    wait_time += 1
        except RuntimeError as re:
            logger(f'RuntimeError({re})')
            return False
        except Exception as e:
            logger(f'Exception2({e})')
            return False

    def get_cpu_brand(self):
        try:
            return re.search(": (.*)", self.shell("sysctl machdep.cpu.brand_string"))[1]
        except:
            return

    def is_os_version(self, version="10.16"):
        mapping_table = {
            "10.15": "Catalina",
            "10.16": "Big Sur"
        }
        current_version = ".".join(platform.mac_ver()[0].split(".")[:2])
        logger(f"Platform is {mapping_table.get(current_version, 'Unknown')}")
        logger(f"{version} / {current_version}")
        return version in current_version

    @staticmethod
    def is_os_version_greater_than_or_equal_to(version='11.0'):  # os_ver: e.g. 10.15.7 or 10.15
        try:
            curr_os_ver = platform.mac_ver()[0]
            logger(f'current version: {curr_os_ver}')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False
        return curr_os_ver >= version


def osascript(cmd=None):
    p = Popen(['osascript'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(cmd.encode("utf-8"))
    return p.returncode


code = {".": 47, ",": 43, "/": 44,
        "f1": 122,
        "f2": 120,
        "f3": 99,
        "f4": 118,
        "f5": 96,
        "f6": 97,
        "f7": 98,
        "f8": 100,
        "f9": 101,
        "f10": 109,
        "f11": 103,
        "f12": 111,
        }


class Keyboard:
    kb = Kb_ctrl()
    key = kb_key

    def send(self, text):
        for c in text:
            if c.isupper():
                with self.pressed(self.key.shift, c.lower()):
                    pass
            else:
                self.press(c)
        time.sleep(0.5)

    def tab(self):
        self.kb.tap(kb_key.tab)

    def enter(self):
        self.kb.tap(kb_key.enter)

    def press(self, key):
        key_lower = key.lower() if isinstance(key, str) else key
        self.kb.press(KeyCode(code[key_lower]) if key_lower in code else key)

    def release(self, key):
        # self.kb.release(key)
        key_lower = key.lower() if isinstance(key, str) else key
        self.kb.release(KeyCode(code[key_lower]) if key_lower in code else key)

    def tap(self, key):
        self.kb.tap(key)

    @contextlib.contextmanager
    def pressed(self, *args):
        for key in args:
            self.press(key)
        try:
            yield
        finally:
            for key in reversed(args):
                self.release(key)

    def esc(self):
        self.kb.tap(kb_key.esc)

    def right(self):
        self.kb.tap(kb_key.right)

    def left(self):
        self.kb.tap(kb_key.left)

    def up(self):
        self.kb.tap(kb_key.up)

    def down(self):
        self.kb.tap(kb_key.down)


class Mouse:
    mouse = Mouse_ctrl()

    def move(self, x, y, duration=0.5, interval=0.001, wait=0.2):
        # print(f"Move mouse to {x}, {y}")
        if 0 < x < 1: x = int(x * screen_w)
        if 0 < y < 1: y = int(y * screen_h)
        timer = time.time()
        pos = self.position()
        x_dist = x - pos[0]
        y_dist = y - pos[1]
        duration = duration - wait if duration > wait else interval
        step = duration / interval
        # print(f"{step=}")
        move_x = x_dist / step
        move_y = y_dist / step
        # print(f"{move_x=} / {move_y=}")
        # print(f"Current pos = {pos}")
        for i in range(int(step)):
            while time.time() - timer < interval:
                pass
            else:
                timer = time.time()
            tar_x = pos[0] + move_x * (i + 1)
            tar_y = pos[1] + move_y * (i + 1)
            # print(f"{tar_x=} / {tar_y=}")
            self.mouse.position = (tar_x, tar_y)
        time.sleep(wait)

    @contextlib.contextmanager
    def pressed(self, *args):
        for key in args:
            self.mouse.press(key)
        try:
            yield
        finally:
            for key in reversed(args):
                self.mouse.release(key)

    def shift(self, x=0, y=0):
        self.mouse.move(x, y)

    def position(self):
        return self.mouse.position

    def click(self, x=None, y=None, btn="left", times=1, **kwargs):
        btn_dict = {
            "left": mouse_btn.left,
            "right": mouse_btn.right,
            "middle": mouse_btn.middle,
        }
        target_btn = btn_dict[btn.lower()]

        if x is not None and y is not None: self.move(x, y, **kwargs)
        with self.mouse as mouse:
            for _ in range(times):
                mouse.press(target_btn)
                mouse.release(target_btn)

    def right_click(self, x=None, y=None, times=1):
        self.click(x, y, "right", times)

    def drag(self, src_pos, dest_pos, time_gap=0.5):  # time_gap: the time gap between opeartion
        self.move(*src_pos)
        time.sleep(time_gap)
        self.mouse.press(mouse_btn.left)
        time.sleep(time_gap)
        self.move(*dest_pos)
        time.sleep(time_gap)
        self.mouse.release(mouse_btn.left)

    def drag_directly(self,src_pos, dest_pos, time_gap=0.5):
        self.mouse._position_set(src_pos, 0)
        time.sleep(time_gap)
        self.mouse.press(mouse_btn.left)
        time.sleep(time_gap)
        self.mouse._position_set(dest_pos, 0)
        time.sleep(time_gap)
        self.mouse.release(mouse_btn.left)

    def scroll(self, direction='up', times=1):
        for x in range(times):
            if direction == 'up':
                self.mouse.scroll(0, 10)
            elif direction == 'down':
                self.mouse.scroll(0, -10)
            else:
                logger('incorrect parameter')
                return False
            time.sleep(0.3)
        time.sleep(1)
        return True


class Image:
    img_path = "./material/"
    mouse = Mouse()

    def get_file(self, name):
        for path in [os.path.abspath(name), os.path.abspath(self.img_path + name)]:
            # logger(f"{path=}")
            if os.path.isfile(path):
                return path
        return None

    def snapshot(self, file_name=None, format="png", x=0, y=0, w=screen_w - 1, h=screen_h - 1, raw=False, type=-1):
        try:
            if not file_name:
                file_fullname = f"{temp_dir}/{uuid.uuid4()}.{format}"
            else:
                file_fullname = os.path.abspath(f'{file_name}')
            os.makedirs(os.path.dirname(file_fullname), exist_ok=True)

            x, y, w, h = map(lambda n: int(max(n, 0)), [x, y, w, h])
            # logger(f'snapshot -> {file_fullname}')
            cmd = f'screencapture -x -t {format} "{file_fullname}"'
            # logger(f"{cmd=}")
            check_output(cmd, shell=True)
            img = cv2.imread(file_fullname, type)
            org_h, org_w = img.shape[:2]
            if screen_w != org_h or screen_h != org_w:
                img = cv2.resize(img, (screen_w, screen_h), interpolation=cv2.INTER_LINEAR)
            # logger(f'{y=} / {y+h=} / {x=} / {x+w=}')
            img = img[y:y + h, x:x + w]
            if raw:
                return img
            else:
                cv2.imwrite(file_fullname, img)
                return file_fullname
        except Exception as e:
            logger(f'[Error] => {e}')
            return False

    def screenshot(self, *args, **kwargs):
        return self.snapshot(*args, **kwargs)

    def search(self, source, target, center=True, color=False, screen_ratio=1, _mode=5):
        """
        cv:: IMREAD_UNCHANGED = -1，
        cv:: IMREAD_GRAYSCALE = 0，
        cv:: IMREAD_COLOR = 1，
        cv:: IMREAD_ANYDEPTH = 2，
        cv:: IMREAD_ANYCOLOR = 4，
        cv:: IMREAD_LOAD_GDAL = 8
        """
        _source = self.get_file(source)
        _target = self.get_file(target)
        # print(f"{source=}/{target=}")
        s = cv2.imread(_source, [cv2.IMREAD_GRAYSCALE, cv2.IMREAD_COLOR][color])
        t = cv2.imread(_target, [cv2.IMREAD_GRAYSCALE, cv2.IMREAD_COLOR][color])
        # s_h, s_w = s.shape[:2]
        h, w = t.shape[:2]
        # s_resize = cv2.resize(s, (int(s_w * ratio), int(s_h * ratio)), interpolation=cv2.INTER_LINEAR)

        try:
            res = cv2.matchTemplate(s, t, _mode)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val == 0:
                logger("Pure image detected, switch to advanced mode")
                ret = self.search(source, target, center, True, screen_ratio, _mode=2)
                max = ret.w * ret.h * 3 * 255 * 255
                logger(f"{ret=} / {max=}")
                ret.similarity = (max - ret.similarity) / max
                return ret
        except:
            return None

        # print(min_val, max_val, min_loc, max_loc )
        ret = {
            "x": int((max_loc[0] + w / 2) / screen_ratio) if center else 0,
            "y": int((max_loc[1] + h / 2) / screen_ratio) if center else 0,
            "similarity": (max_val + 1) / 2,
            "w": int(w / screen_ratio),
            "h": int(h / screen_ratio),
        }
        return SimpleNamespace(**ret)

    def screen_search(self, file_name, similarity=0.95):
        screen = self.snapshot()
        ret = self.search(screen, file_name, screen_ratio=ratio)
        # print(f"{screen=} / {file_name=} / sim = {ret.similarity}")
        return ret if ret.similarity > similarity else None

    def click(self, file_name, similarity=0.95):
        ret = self.screen_search(file_name, similarity)
        # print(f"click -> {ret=}")
        if ret:
            self.mouse.click(ret.x, ret.y)
        else:
            raise Exception(f"image is not found")
        return True

    def exist(self, file_name, duration=5, similarity=0.95):
        global is_found, image
        period = 0.25
        tasks = int(duration / period)
        is_found = Value(c_bool, False)
        args = [(file_name, similarity, time.time() + x * period) for x in range(tasks)]
        # print(f"{args=}")
        with Pool(initializer=init, initargs=(is_found,)) as pool:
            rets = pool.starmap_async(_exist_timed, args)
            while not is_found.value and not rets.ready():
                pass
            else:
                # print(f"{is_found.value=}")
                pool.close()
            # print("wait complete")
            pool.join()
        # print("poll completed")
        if not is_found:
            # print("not found")
            return None
        # print("="*20)
        # print(f"{rets.get()=}")
        for result in rets.get():
            if result: return result

    def is_exist(self, *args, **kwargs):
        return bool(self.exist(*args, **kwargs))

    def exist_click(self, file_name, timeout=5, similarity=0.95):
        ret = self.exist(file_name, timeout, similarity)
        # print(f"exist_click -> {ret=}")
        if ret:
            self.mouse.click(ret.x, ret.y)
            return True
        else:
            logger(f"[Warning] Image was not found - {file_name} ")
            return False

    def get_color(self, x, y):
        ret = Mac.shell(f"screencapture -R{x},{y},1,1 -t bmp $TMPDIR/test.bmp && \
                 xxd -p -l 3 -s 54 $TMPDIR/test.bmp | \
                 sed 's/\\(..\\)\\(..\\)\\(..\\)/\\3\\2\\1/'")
        return ret[:6] if len(ret) == 7 else None


class Video:
    def compare(self, source, target):
        source = os.path.abspath(source)
        target = os.path.abspath(target)
        try:
            psnr, ssim = [v for _, v in ffqm.FfmpegQualityMetrics(source, target).calc(["ssim", "psnr"]).items()]
        except FileNotFoundError:
            logger("[ERROR] " + "*" * 65)
            logger("[ERROR] ** Please install FFmpeg via 'brew install ffmpeg' in terminal **")
            logger("[ERROR] " + "*" * 65)
            raise FileNotFoundError("Please install FFmpeg via 'brew install ffmpeg' in terminal")
        ssim_avg = sum([x['ssim_avg'] for x in ssim]) / len(ssim)
        psnr_avg = sum([x['psnr_avg'] for x in psnr]) / len(ssim)
        logger(f"{psnr_avg=}, {ssim_avg=}, length = {ssim[-1]['n']} frames")
        return psnr_avg > 40.0 and ssim_avg > 0.9


class File:
    @staticmethod
    def get_temp(ext="tmp"):
        return os.path.abspath(f"{temp_dir}/{uuid.uuid4()}.{ext}")

    @staticmethod
    def remove(file):
        os.remove(file)
        return True

    @staticmethod
    def read(file, timeout=5):
        timer = time.time()
        while time.time() - timer < timeout:
            try:
                with open(file, "r", encoding="UTF-8") as f:
                    text = f.read()
                return text
            except:
                pass
        return


def init(*arg):
    global is_found
    is_found = arg[0]


def _exist_timed(file_name, similarity=0.95, schedule=0):
    global is_found
    # print(f"{file_name=} / {similarity=} / {schedule=} / {is_found.value=}")
    while time.time() - schedule < 0 and not is_found.value:
        time.sleep(0.05)
    else:
        if is_found.value: return None
    ret = image.screen_search(file_name, similarity)
    # print(f"{ret=}")
    if ret:
        is_found.value = True
        return ret
    else:
        # print("return None")
        return None


def test_screenshot():
    img = Image()
    for i in range(10):
        timer = time.time()
        for _ in range(i):
            print("x")
            img.screen_search('launcher.png')
        # print(f"result -  {img.screen_search('launcher.png')}")
        print(f"{i} Times = {time.time() - timer: 0.5f} sec")


def test_exist():
    print(f'Pytest -> {image.exist("anydesk.png", 10)}')


def test_exist_click():
    osascript('activate application "U"')
    image.exist_click("./record/signInWithEmail.png", 10)


if __name__ == "__main__":
    pass
    import atomac

    pdr = atomac.getAppRefByBundleId("com.cyberlink.powerdirector")
    # x = pdr.findAllR(AXRole='AXScrollArea')
    # print(f"{x=}")
    # image.exist_click("anydesk.png", 1)
    """
    img = Image()
    timer = time.time()
    ret = img.search("1.png","1_.png")
    print(f"time = {time.time()-timer}\n{ret=}")

    with mss() as s:
        timer = time.time()

        img = cv2.imread(s.shot(), 0)
        print(f"mss time = {time.time()-timer}")

    timer = time.time()
    print(Image.snapshot_pil("","test1.png"))
    print(f"pil time = {time.time()-timer}")

    timer = time.time()
    png = Image.snapshot("","test2.png")
    print(f"snapshot time = {time.time() - timer}")
    img = cv2.imread(png,0)
    # img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite("img_g.png",img)
    print(f"read time = {time.time()-timer}")

    timer = time.time()
    tiff = Image.snapshot("", "test2.tiff","tiff")
    print(f"snapshot time = {time.time() - timer}")
    img = cv2.imread(tiff, 0)
    # img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite("img_g.png",img)
    print(f"read time = {time.time() - timer}")
    #"""
