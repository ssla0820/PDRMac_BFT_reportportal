import ecl_operation

# 2021/10/22 updated

# input dict. keys: prod_name, prod_ver, prod_ver_type, sr_no, tr_no, prog_path_sub, dest_path, work_dir, mail_list
# output dict. keys: result, err_msg, ver_type, build

# for downloading TR build, should use password.py to generate credential file first.

# prod_ver_type: Essential, Ultra, Ultimate, Business essential, Standard, Upgrade to Ultimate, Subscription, Ultimate (UWP), Ultra (UWP)

para_dict = {'prod_name': 'PowerDirector for Mac', # [Must] the parameter for query eCL http service. e.g. PowerDirector
             'prod_ver': '', # [Option #1] the parameter for query eCL http service. e.g. 20.0
             'prod_ver_type': '', # [Option #2] the parameter for query eCL http service. e.g. Subscription
             'sr_no': '', # [Option] to specified SR for get last valid TR to download build
             'tr_no': '', # [Option] to specified TR for download build
             'prog_path_sub': '', # [Option] the sub-folder of TR program path to copy e.g. Compressed, if no, keep it empty
             'dest_path': '/Users/qadf-mbp3/Desktop/Download_TRBuild', # the full path of local download build folder
             'work_dir': '', # [Option] the full path of working folder for tr_db file
             'mail_list': ['jim_huang@cyberlink.com'] # [Option] to send the result mail
             }

# STEP #1: Initial Ecl_Operation object and pass para_dict to query by eCL http services
# Return: JSON object of query result
oecl = ecl_operation.Ecl_Operation(para_dict)
obj_json = oecl.query_sr_by_ecl_service()

# STEP #2: Get the SR List via JSON object
filter_sr_keyword = '' # only collect sr which has the keyword
sr_list = oecl.get_sr_list(obj_json, filter_sr_keyword)
print(f'Total SR={len(sr_list)}')

# STEP #2-1: Get the "Product Version" and "Product Version Type" via JSON object with SR number
# for index in range(len(sr_list)):
#     version = oecl.get_prod_ver_by_sr(obj_json, sr_list[index])
#     version_type = oecl.get_prod_ver_type_by_sr(obj_json, sr_list[index])
#     print(f'[{index+1}] sr={sr_list[index]}, {version=}, {version_type=}')

# STEP #2-2: Filter the SR List by using Product Version and Product Version Type if needed
prod_ver = '20.0'
prod_ver_type = ['Subscription', 'Ultra']
amount = 0
for index in range(len(sr_list)):
    version = oecl.get_prod_ver_by_sr(obj_json, sr_list[index])
    version_type = oecl.get_prod_ver_type_by_sr(obj_json, sr_list[index])
    if float(version) >= float(prod_ver) and version_type in prod_ver_type:
        print(f'[{amount+1}] sr={sr_list[index]}, {version=}, {version_type=}, {index=}')
        amount += 1

# STEP #3: Get the last valid TR by pass JSON object and SR number
if oecl.get_last_valid_tr_by_sr(obj_json, sr_list[3]):
    print(f'the last tr={oecl.tr_no} of sr={sr_list[3]}')
else:
    print(f'get last valid tr of sr={sr_list[3]} FAIL.')

# STEP 4: Get the TR Information by pass the TR number
# Return: A dictionary structure of result.
dict_tr_info = oecl.retrieve_tr_info()
print(f'tr_info={dict_tr_info}')

# STEP #5: Update TR number to Database
# Return: A list of TR number - the TR is new for testing
#         An empty list - the TR has been tested before.
tr_list = oecl.update_tr_to_db(oecl.tr_no, sr_list[0]) # tr_list: empty list if the tr already exists
print(f'{tr_list=}')

# STEP #6: If new TR, download build to local
tr_num = 'TR211007-008'
oecl.download_build_by_tr(tr_num)
print('complete')