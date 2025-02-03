import ecl_operation
import browser_cookie3

# 2022/02/15 updated

# input dict. keys:
# parameter: a dictionary (in 3 groups - searching/filter SRs, specified SR/TR, path specify, mail list)
#            1) Searching/Filter SRs:
#               - prod_name [MUST], prod_ver, prod_ver_type, filter_sr_keyword, custom_name, query_mode
#            2) Specified SR/TR:
#               - sr_no, tr_no
#            3) Path Specify:
#               - prog_path_sub, dest_path, work_dir
#            4) Mail List:
#               - mail_list

# output dict. keys: result, err_msg, ver_type, build, sr_no, tr_no

# for downloading TR build, should use password.py to generate credential file first.

# prod_ver_type: Essential, Ultra, Ultimate, Business essential, Standard, Upgrade to Ultimate, Subscription, Ultimate (UWP), Ultra (UWP)

para_dict = {'prod_name': 'PowerDirector', # [Must] the parameter for query eCL http service. e.g. PowerDirector
             'prod_ver': '', # [Option #1] the parameter for query eCL http service. e.g. 20.0
             'prod_ver_type': '', # [Option #2] the parameter for query eCL http service. e.g. Subscription
             'custom_name': '',  # [Option] to filter sr list by SR CustName, e.g. 'CyberLink', 'OEM' (means all SRs except for CyberLink)
             'filter_sr_keyword': 'VDE',  # [Option] to include SRs which include specified keyword (support multiple search 'VDE,PUS')
             'query_mode': 0,  # to specify the query mode: 0 (Master SR ONLY)[Default], 1(Sub-SR Only), 2(Master+Sub-SR)
             'sr_no': 'VDE220208-03', # [Option] to specified Master SR/ SubSR for get last valid TR to download build
             'tr_no': '', # [Option] to specified TR for download build
             'prog_path_sub': '', # [Option] the sub-folder of TR program path to copy e.g. Compressed, if no, keep it empty
             'dest_path': '/Users/qadf-mbp3/Desktop/Download_TRBuild', # the full path of local download build folder
             'work_dir': '', # [Option] the full path of working folder for tr_db file
             'mail_list': '' # [Option] to send the result mail
             }

ecl_operation.debug_mode = True # True: debug only, just get latest valid TR, will not download build

# Query last valid tr build by input parameter
dict_result = ecl_operation.get_latest_tr_build(para_dict)
print(f'result={dict_result}')
print('complete')