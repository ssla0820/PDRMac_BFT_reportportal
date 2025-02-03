import os,re,glob
from os.path import exists
from os.path import basename
from os.path import dirname
from subprocess import getoutput
from subprocess import check_call
from .log import logger
import cv2

howQ3_x86inx64 = 'C:\\Program Files (x86)\\CyberLink\\HowQ 3.0\\HowQ3.exe'
howQ3_x64 = 'C:\\Program Files\\CyberLink\\HowQ 3.0(x64)\\HowQ3_x64.exe'
howQ3_x86 = 'C:\\Program Files\\CyberLink\\HowQ 3.0\\HowQ3.exe'
temp = os.environ.get("temp",os.environ.get("TMPDIR"))


def compare_video(source,target, is_delete_source=True):
    exist = lambda x,y,z : x if exists(x) else y if exists(y) else z if exists(z) else ""
    howQ3Path = exist(howQ3_x86inx64,howQ3_x64,howQ3_x86)
    fileName = basename(source)
    path = os.path.abspath(dirname(target))
    logName = '%s\\%s.info.txt'%(path,basename(target)) 

    
    if not howQ3Path:
        logger("[VerifyVideo] Can not find the HowQ3, please install in default path")
        return False
    if not exists(source):
        logger("[VerifyVideo] Sample file is not found. -> " + source)
        return False
    if not exists(target):
        logger("[VerifyVideo] Produced file is not found. -> " + target)
        return False
    
    params = ' /a evaluate /e autoclose /source "' + source + '" /output "' + target +'"'
    logger("[VerifyVideo] Runnning command: %s" % params)
    check_call('"%s" %s' % (howQ3Path,params), cwd=temp)
    
    with open(logName,"r") as f:
        file_data = f.read() 
    
    pattern = "Average PSNR=(-?\\d+\\.\\d*)[\\s\\S]*Average SSIM=(-?\\d+\\.\\d*)"
    result = re.search(pattern,file_data)
    PSNR ,SSIM = float(result.group(1)),float(result.group(2))
    
    logger("[VerifyVideo] PSNR: %s  SSIM: %s" % (PSNR,SSIM))

    if (PSNR > 40.0) & (SSIM > 0.9):
        logger("Video is the same.")
        logger("removing files")
        check_call(f'del "{os.path.abspath(logName)}"' , shell=True)
        if is_delete_source:
            check_call(f'del "{os.path.abspath(source)}"', shell=True)
        check_call(f'del "{path}\\*.csv"', shell=True)
        return True
    logger("Video is different.")
    return False

def compare_video_v2(source, target, threshold_psnr=35.0, threshold_ssim=0.9, is_delete_source=True):
    exist = lambda x, y, z: x if exists(x) else y if exists(y) else z if exists(z) else ""
    howQ3Path = exist(howQ3_x86inx64, howQ3_x64, howQ3_x86)
    fileName = basename(source)
    path = os.path.abspath(dirname(target))
    logName = '%s\\%s.info.txt' % (path, basename(target))

    if not howQ3Path:
        logger("[VerifyVideo] Can not find the HowQ3, please install in default path")
        return False
    if not exists(source):
        logger("[VerifyVideo] Sample file is not found. -> " + source)
        return False
    if not exists(target):
        logger("[VerifyVideo] Produced file is not found. -> " + target)
        return False

    params = ' /a evaluate /e autoclose /source "' + source + '" /output "' + target + '"'
    logger("[VerifyVideo] Runnning command: %s" % params)
    check_call('"%s" %s' % (howQ3Path, params), cwd=temp)

    with open(logName, "r") as f:
        file_data = f.read()

    pattern = "Average PSNR=(-?\\d+\\.\\d*)[\\s\\S]*Average SSIM=(-?\\d+\\.\\d*)"
    result = re.search(pattern, file_data)
    PSNR, SSIM = round(float(result.group(1)), 2), round(float(result.group(2)), 2)

    logger("[VerifyVideo] PSNR: %s  SSIM: %s" % (PSNR, SSIM))

    if (PSNR > threshold_psnr) & (SSIM > threshold_ssim):
        logger("Video is the same.")
        if is_delete_source:  # output file
            logger("removing files")
            check_call(f'del "{os.path.abspath(target)}"', shell=True)
        check_call(f'del "{path}\\*.csv"', shell=True)
        return True, PSNR, SSIM
    logger("Video is different.")
    return False, PSNR, SSIM
    
''' openCVTM version
def compare_image(source,target):
    openCVTMPath = "c:\\ProgramData\\OpenCVTM\\OpenCVTM.exe"
    if not os.path.isfile(openCVTMPath):
        logger("[OpenCV] XXX OpenCVTM is not found. => {}" % openCVTMPath)
        exit(-1)
    output = getoutput("{} {} {}".format(openCVTMPath,source,target))
    result = re.search("\\[(\\d*), (\\d*), (\\d*), (\\d*), (\\d*\\.\\d*)\\]",output)
    if result:
        data = result.group(0)
        logger("[OpenCV] *** image is found: {!s}".format(data))
        return True
    else:
        logger("[OpenCV] --- image is not found: {!s}".format(output))
    return False
'''

def compare_image_color(source,target,method=cv2.HISTCMP_CORREL):
    try:
        img1 = cv2.imread(source,1)
        img2 = cv2.imread(target,1)
    except Exception as e:
        print(f'Load files error: {e}')
        
    img1_hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    img2_hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    
    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]
    # hue varies from 0 to 179, saturation from 0 to 255
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges # concat lists
    # Use the 0-th and 1-st channels
    channels = [0, 1]
    
    img1_hist = cv2.calcHist([img1_hsv], channels, None, histSize, ranges, accumulate=False)
    img2_hist = cv2.calcHist([img2_hsv], channels , None, histSize, ranges, accumulate=False)
    hist_diff = cv2.compareHist(img1_hist, img2_hist, method)
   
    logger(f'{source=}')
    logger(f'{target=}')
    logger(f'color similar rate = {hist_diff}')
    return hist_diff
    
def is_same_image_color(source,target,similarity = 0.999):
    logger(f'criteria = {similarity}')
    result = True if compare_image_color(source,target) > similarity else False
    logger(f'{result=}')
    return result

def is_not_same_image_color(self,*aug):
    return not is_same_image_color(*aug)
# a = r"D:\2011 Q1-2 video test files\MPEG-2\720p\inception-720p.mpg"
# b = r"D:\2011 Q1-2 video test files\MPEG-2\720p\beastly-720p.mpg"
# print (compare_video(a,b))

# a = r"C:\Users\Miti\Desktop\temp\Untitled.png"
# b = r"C:\Users\Miti\Desktop\temp\se.png"
# print (compare_video(a,b))