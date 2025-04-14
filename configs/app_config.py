import os.path
from os.path import expanduser, abspath
root = expanduser("~")
build_info = {
    "tr": "input_tr",
    "sr": "input_sr",
    "build_version": "input_build_ver",
}

PDR_cap = {
    'app_name': 'PowerDirector 365',
    'app_bundleID': 'com.cyberlink.powerdirector',
    'app_path': '/Applications/PowerDirector 365.app',
    'ground_truth_root': root + '/Desktop/AT/GroundTruth/ground_truth',
    'auto_ground_truth_root': root + '/Desktop/AT/GroundTruth/auto_ground_truth',
    'testing_material': root + '/Desktop/AT/BFT_Material/',
}

PDR_hardcode_cap = {
    'app_name': 'PowerDirector',
    'app_bundleID': 'com.cyberlink.powerdirector',
    'app_path': '/Applications/PowerDirector.app'
}

Chrome_cap = {
    'app_name': 'Google Chrome',
    'app_bundleID': 'com.google.Chrome',
    'app_path': '/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome'
}

Finder_cap = {
    'app_name': 'Finder',
    'app_bundleID': 'com.apple.finder',
    'app_path': '/System/Library/CoreServices/Finder.app/Contents/MacOS/Finder'
}

