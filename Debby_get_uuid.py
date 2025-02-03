# import re
# from bs4 import BeautifulSoup

# def extract_uuids_from_file(file_path):
#     """
#     Extract UUIDs from a Python file with the pattern 'with uuid("<uuid>") as case'.
#     Returns a list of UUIDs found in the file.
#     """
#     # Regular expression to find UUIDs inside with uuid("UUID") as case
#     uuid_pattern = r'with uuid\("([a-f0-9\-]+)"\) as case'
    
#     # List to hold all found UUIDs
#     uuids = []
    
#     # Read the file content
#     with open(file_path, 'r') as file:
#         file_content = file.read()

#     # Find all matches of the pattern
#     matches = re.findall(uuid_pattern, file_content)
    
#     # Return the list of matched UUIDs
#     return matches

# def extract_uuids_from_html(html_file_path):
#     """
#     Extract all UUIDs from an HTML file, regardless of their location.
#     Returns a list of UUIDs found in the file.
#     """
#     # Regular expression to match UUIDs
#     uuid_pattern = re.compile(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', re.IGNORECASE)
    
#     # Read and parse the HTML file
#     with open(html_file_path, 'r', encoding='utf-8') as file:
#         file_content = file.read()
    
#     # Find all UUIDs in the HTML content
#     uuids = re.findall(uuid_pattern, file_content)
    
#     # Return the list of UUIDs (unique values only)
#     return list(set(uuids))

# def compare_uuids(uuid_list, html_uuid_list):
#     """
#     Compare UUIDs from the Python file and HTML file.
#     Returns two sets:
#     - UUIDs only in the HTML file (but not in Python file)
#     - UUIDs only in the Python file (but not in HTML file)
#     """
#     # Convert both lists to sets
#     html_uuids = set(html_uuid_list)
#     python_uuids = set(uuid_list)
    
#     # UUIDs in HTML but not in Python
#     html_not_in_python = html_uuids - python_uuids
    
#     # UUIDs in Python but not in HTML
#     python_not_in_html = python_uuids - html_uuids
    
#     return html_not_in_python, python_not_in_html

# # Example usage:
# if __name__ == "__main__":
#     # Path to your Python file
#     python_file_path = r'/Users/qadf_at/Desktop/AT/PDRMac_BFT/trunk/SFT/BFT_PDR22_stage1_os14.py'  # Replace with your actual Python file path
    
#     # Path to your HTML file
#     html_file_path = r'/Users/qadf_at/Desktop/AT/PDRMac_BFT/trunk/SFT/check_list/PDR22 Mac BFT_20231106.html'  # Replace with your actual HTML file path
    
#     # Step 1: Extract UUIDs from the Python file
#     found_python_uuids = extract_uuids_from_file(python_file_path)
#     print(f"Found UUIDs in Python file: {found_python_uuids}")
    
#     # Step 2: Extract UUIDs from the HTML file
#     found_html_uuids = extract_uuids_from_html(html_file_path)
#     print(f"Found UUIDs in HTML file: {found_html_uuids}")
    
#     # Step 3: Compare and get UUIDs only in one of the files
#     html_not_in_python, python_not_in_html = compare_uuids(found_python_uuids, found_html_uuids)
    
#     # Output the UUIDs unique to each file
#     print("\nUUIDs found in HTML but NOT in Python file:")
#     print(html_not_in_python)
    
#     print("\nUUIDs found in Python but NOT in HTML file:")
#     print(python_not_in_html)


# aaa = ['758e68c1-a62d-4ffb-87f0-13b98fa82f7e', 'f6068849-031c-48a0-912f-ae72071a46ad', 'da0b07b8-ab61-4351-bd85-b43caef54696', '67391393-7c99-42e4-ab81-99a1a47c4f04', '6677c5ba-305e-4742-9988-099a48d10270', 'ff239744-74cd-4b8e-91a3-9844d624a964', 'af0c9188-3a17-4cba-81c7-a229353698cb', '37eea6f6-4e58-42fb-91b3-f7c3f3511d92', 'aa965a18-7823-42e6-a6cc-7e1696500b99', '4372f92a-5da4-42ab-b8b2-db555fbc4fee', '8d9287b4-765f-43ac-b628-4a8802a14e91', 'f5aee31f-25fe-4b66-84ce-a4105113ee87', 'c07a4bfc-ce9d-401c-be8a-18a2eab602ca', '6510cb1c-17cf-47b4-8ad0-de8c15e71d48', '01bae86c-ef1b-4d49-aa1d-ecfa8ae7e70d', 'acf4e893-b714-408e-9658-566fe7060f15', '718f50b3-517d-48c2-ad6b-d067a270da1f', '798c0668-9be6-40fc-948b-5a73726e3c34', '97affa2a-c953-49a3-925c-417b95db719f', 'ee316164-79e3-40da-91a8-78ef31c1b08b', 'deeae229-a221-4738-9de1-61b0fd983374', '923f1789-4139-49aa-a2bb-509f841b4dad', '9f35ba03-1cef-4b0e-96cb-191310b2cecd', '7b066cbc-1607-4469-b677-7b8cab1b3a55', 'fdceddae-485a-447c-a89c-fef3e06326bf', '1f0fbbb2-a77d-459b-bb90-4bcbff2c9b86', '7cae4f2a-fa01-4d3b-8c06-71f2158091c9', '8145aec8-8fc1-4a62-a17b-ae8cfaad39cf', '662d72bf-19e7-4200-8bec-14a7c97b34b4', '22b24c83-bff2-48af-9fe5-afe866158399', '55aa8d43-0d80-465f-bad7-c14a7104f9a6', '22fdea74-6a4a-475d-b8aa-953ec9987fab', '01f08c96-e7ec-4ca7-b86f-4c6c7205287e', '77f85454-ae23-4306-954a-1b6c33c960ee', '838697fb-5e4e-4d77-bd72-6780e588b3c2', 'd666e85a-ea54-4c2a-82f2-d06e07b2cd8a', '302a858b-f48c-4094-9ae0-bd37e6d542e1', '461a78c6-9db8-43fe-94c8-6a1f3ab16182', 'fe0d0793-f9d3-4dd5-850f-26914dcb14c1', 'd9079e1c-b8a5-4d27-94e6-d9dd71ccb90c', 'd0f8f9c2-3ea7-4e1b-b88d-1fa88c5bb2fd', '85b38734-3f9a-4bf0-ae0a-a2701628dccf', '0811b795-5fa4-42bf-8a57-22f389e9f6f7', '98ea0e05-c63e-4be7-8c32-7055b526a850', 'b75b3f6d-1f3c-4431-a1b4-06999c7d3598', '999ef8a7-3db0-414e-b2b6-602b1670ad37', '7ac86abb-4b66-498b-9857-e09eb6d176f2', '8d69ec14-dbed-4ed9-877a-9c58de1a9bc5', 'ad8f3229-129f-45c5-a9c4-e8c490be438c', '32b3fc79-6dfb-4ff5-9348-15e4b6d6dce1', '96ee5e10-47e1-4c84-b13c-2e6ddc5fdc48', 'dd55a4de-e286-462c-bf18-990daed490d9', 'a93a1fe6-78f0-48a2-958e-251f3d95bf1e', '9a90ab51-c059-4084-a1f1-b3c1f5ae5553', 'bb2184bb-47cf-45d5-931f-cd20daccf879', '13a760bb-7e1c-401a-8ace-fdba828c3fb8', '475fcf12-b238-405c-8e37-6cd246afd396']

# uuid_string = "\n".join(aaa)
# print(uuid_string)

import pyautogui
import time

time.sleep(3)
print(pyautogui.position()) 


center_x=800.777786, center_y=425.656234, rotation_value='0'
(center_x, center_y-radius)=(800.777786, 235.65623399999998), (center_x+radius, center_y)=(990.777786, 425.656234)

f 2_1_1: 94a884-f71d-4111-bc9d-fafab5c034b ==> not problem if run single
f 3_1_3: c6ddcb5-e490-4fd7-85df-cbf4571c490==> not problem if run single

e 4_1_12: a30f3ff-290d-4179-9e15-06a92a2e3a4 ==> not problem if run single
f 4_1_13: f19ce26-268c-4255-9467-033156ceb53 ==> post in profile, keep tracking why profile in it
f 4_1_13: 0fb947c2-c718-4b81-8bed-7e0a78a84c3 ==> not problem if run single

e 4_1_14: ==> not problem if run single
e 4_1_15: 071a716-a769-4153-9d27-98d183a98f3 ==> not problem if run single
e 4_1_16: 8589cce-cb99-4c02-8edd-bb81daf8660==> not problem if run single
e 4_1_17: 941636d-0f13-4fbf-baa8-e2725af12a==> not problem if run single
e 4_1_20: ==> not problem if run single
f 4_1_21: d2e8c7e-3108-4cfa-bcf8-bb37446caa2==> not problem if run single
f 4_1_21: 8960b0f-b0f8-4451-b163-12501bca2c9==> not problem if run single


e 8_1_1: 9e063e9-d7e6-405a-9853-77c7fe598db ==> AI cutout

f 9_1_4: e4e9e98-13b0-4aa8-9e9c-aef8dbf4db47 ==> AI cutout
e 9_1_4: 6ca106d-5040-4e05-99f6-09f331eb4b9 ==> AI cutout

f 10_1_23: 1b7c7c1-017d-4915-a6a0-f0b224a967d3 ==> Not rotate the object correctly, change coordinate			
f 10_1_23: e0c915bc-66a2-4b11-bda4-206127c3dcc6 ==> Pass after solved previous
e 10_1_33: 5c5187a-9740-43ad-9fb5-3c3594a4e72 ==> ai module failed in 10_1_32

L362




