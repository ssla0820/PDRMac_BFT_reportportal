
from .sendemail import send_mail
import os
import shutil


def summary_report_header():
    summary_report_header = '<div class=WordSection1>'
    summary_report_header += '<table class=MsoTableGrid border=1 cellspacing=0 cellpadding=0 style=\'border-collapse:collapse;border:none\'>'
    summary_report_header += '<tr style=\'height:19.75pt\'>'
    summary_report_header += '<td width=89 style=\'width:67.1pt;border:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:19.75pt\'><p class=MsoNormal align=center style=\'text-align:center\'><b><span style=\'font-size:12.0pt;color:#1F497D\'>Name<o:p></o:p></span></b></p></td>'
    summary_report_header += '<td width=96 style=\'width:1.0in;border:solid windowtext 1.0pt;border-left:none;padding:0in 5.4pt 0in 5.4pt;height:19.75pt\'><p class=MsoNormal align=center style=\'text-align:center\'><b><span style=\'font-size:12.0pt;color:#1F497D\'>Date<o:p></o:p></span></b></p></td>'
    summary_report_header += '<td width=78 style=\'width:58.5pt;border:solid windowtext 1.0pt;border-left:none;padding:0in 5.4pt 0in 5.4pt;height:19.75pt\'><p class=MsoNormal align=center style=\'text-align:center\'><b><span style=\'font-size:12.0pt;color:#1F497D\'>Time<o:p></o:p></span></b></p></td>'
    summary_report_header += '<td width=114 style=\'width:85.5pt;border:solid windowtext 1.0pt;border-left:none;padding:0in 5.4pt 0in 5.4pt;height:19.75pt\'><p class=MsoNormal align=center style=\'text-align:center\'><b><span style=\'font-size:12.0pt;color:#1F497D\'>Server<o:p></o:p></span></b></p></td>'
    summary_report_header += '<td width=84 style=\'width:63.0pt;border:solid windowtext 1.0pt;border-left:none;padding:0in 5.4pt 0in 5.4pt;height:19.75pt\'><p class=MsoNormal align=center style=\'text-align:center\'><b><span style=\'font-size:12.0pt;color:#1F497D\'>OS<o:p></o:p></span></b></p></td>'
    summary_report_header += '<td width=162 style=\'width:121.5pt;border:solid windowtext 1.0pt;border-left:none;padding:0in 5.4pt 0in 5.4pt;height:19.75pt\'><p class=MsoNormal align=center style=\'text-align:center\'><b><span style=\'font-size:12.0pt;color:#1F497D\'>Device<o:p></o:p></span></b></p></td>'
    summary_report_header += '<td width=102 style=\'width:76.5pt;border:solid windowtext 1.0pt;border-left:none;padding:0in 5.4pt 0in 5.4pt;height:19.75pt\'><p class=MsoNormal align=center style=\'text-align:center\'><b><span style=\'font-size:12.0pt;color:#1F497D\'>Version<o:p></o:p></span></b></p></td>'
    summary_report_header += '<td width=60 style=\'width:45.0pt;border:solid windowtext 1.0pt;border-left:none;padding:0in 5.4pt 0in 5.4pt;height:19.75pt\'><p class=MsoNormal align=center style=\'text-align:center\'><b><span style=\'font-size:12.0pt;color:#1F497D\'>Pass<o:p></o:p></span></b></p></td>'
    summary_report_header += '<td width=60 style=\'width:45.0pt;border:solid windowtext 1.0pt;border-left:none;padding:0in 5.4pt 0in 5.4pt;height:19.75pt\'><p class=MsoNormal align=center style=\'text-align:center\'><b><span style=\'font-size:12.0pt;color:#1F497D\'>Fail<o:p></o:p></span></b></p></td>'
    summary_report_header += '<td width=60 style=\'width:45.0pt;border:solid windowtext 1.0pt;border-left:none;padding:0in 5.4pt 0in 5.4pt;height:19.75pt\'><p class=MsoNormal align=center style=\'text-align:center\'><b><span style=\'font-size:12.0pt;color:#1F497D\'>N/A<o:p></o:p></span></b></p></td>'
    summary_report_header += '<td width=66 style=\'width:49.5pt;border:solid windowtext 1.0pt;border-left:none;padding:0in 5.4pt 0in 5.4pt;height:19.75pt\'><p class=MsoNormal align=center style=\'text-align:center\'><b><span style=\'font-size:12.0pt;color:#1F497D\'>Skip<o:p></o:p></span></b></p></td>'
    summary_report_header += '<td width=150 style=\'width:112.5pt;border:solid windowtext 1.0pt;border-left:none;padding:0in 5.4pt 0in 5.4pt;height:19.75pt\'><p class=MsoNormal align=center style=\'text-align:center\'><b><span style=\'font-size:12.0pt;color:#1F497D\'>Total Time<o:p></o:p></span></b></p></td></tr>'
    return summary_report_header


def summary_report_add_row(col_name, col_date, col_time, col_server, col_os, col_device, col_ver, col_pass, col_fail, col_na, col_skip, col_total_time):
    row_content = '<tr style=\'height:26.5pt\'>'
    row_content += '<td width=89 style=\'width:67.1pt;border:solid windowtext 1.0pt;border-top:none;padding:0in 5.4pt 0in 5.4pt;height:26.5pt\'><p class=MsoNormal align=center style=\'text-align:center\'><span style=\'font-size:12.0pt;color:#1F497D\'>{}<o:p></o:p></span></p></td>'.format(col_name)
    row_content += '<td width=96 style=\'width:1.0in;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:26.5pt\'><p class=MsoNormal align=center style=\'text-align:center\'><span style=\'font-size:12.0pt;color:#1F497D\'>{}<o:p></o:p></span></p></td>'.format(col_date)
    row_content += '<td width=78 style=\'width:58.5pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:26.5pt\'><p class=MsoNormal align=center style=\'text-align:center\'><span style=\'font-size:12.0pt;color:#1F497D\'>{}<o:p></o:p></span></p></td>'.format(col_time)
    row_content += '<td width=114 style=\'width:85.5pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:26.5pt\'><p class=MsoNormal align=center style=\'text-align:center\'><span style=\'font-size:12.0pt;color:#1F497D\'>{}<o:p></o:p></span></p></td>'.format(col_server)
    row_content += '<td width=84 style=\'width:63.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:26.5pt\'><p class=MsoNormal align=center style=\'text-align:center\'><span style=\'font-size:12.0pt;color:#1F497D\'>{}<o:p></o:p></span></p></td>'.format(col_os)
    row_content += '<td width=162 style=\'width:121.5pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:26.5pt\'><p class=MsoNormal align=center style=\'text-align:center\'><span style=\'font-size:12.0pt;color:#1F497D\'>{}<o:p></o:p></span></p></td>'.format(col_device)
    row_content += '<td width=102 style=\'width:76.5pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:26.5pt\'><p class=MsoNormal align=center style=\'text-align:center\'><span style=\'font-size:12.0pt;color:#1F497D\'>{}<o:p></o:p></span></p></td>'.format(col_ver)
    row_content += '<td width=60 style=\'width:45.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:26.5pt\'><p class=MsoNormal align=center style=\'text-align:center\'><span style=\'font-size:12.0pt;color:#1F497D\'>{}<o:p></o:p></span></p></td>'.format(col_pass)
    row_content += '<td width=60 style=\'width:45.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:26.5pt\'><p class=MsoNormal align=center style=\'text-align:center\'><span style=\'font-size:12.0pt;color:#1F497D\'>{}<o:p></o:p></span></p></td>'.format(col_fail)
    row_content += '<td width=60 style=\'width:45.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:26.5pt\'><p class=MsoNormal align=center style=\'text-align:center\'><span style=\'font-size:12.0pt;color:#1F497D\'>{}<o:p></o:p></span></p></td>'.format(col_na)
    row_content += '<td width=66 style=\'width:49.5pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:26.5pt\'><p class=MsoNormal align=center style=\'text-align:center\'><span style=\'font-size:12.0pt;color:#1F497D\'>{}<o:p></o:p></span></p></td>'.format(col_skip)
    row_content += '<td width=150 style=\'width:112.5pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:26.5pt\'><p class=MsoNormal align=center style=\'text-align:center\'><span style=\'font-size:12.0pt;color:#1F497D\'>{}<o:p></o:p></span></p></td>'.format(col_total_time)
    return row_content


def summary_report_tail():
    summary_report_tail = '</tr></table><p class=MsoNormal><span style=\'color:#1F497D\'><o:p>&nbsp;</o:p></span></p></div>'
    return summary_report_tail


def copy_rename(old_file_name, new_file_name, test_case_path, device_id):
    print(os.curdir)
    src_dir = os.path.join(test_case_path, "report/{}".format(device_id))
    #dst_dir = os.path.join(os.curdir, "dest")
    dst_dir = os.path.dirname(__file__)
    src_file = os.path.join(src_dir, old_file_name)
    dst_file = os.path.join(dst_dir, old_file_name)
    try:
        os.remove(dst_file)
    except OSError as e:
        print(e)
    shutil.copy(src_file, dst_dir)
    new_dst_file_name = os.path.join(dst_dir, new_file_name)
    try:
        os.remove(new_dst_file_name)
    except OSError as e:
        print(e)
    os.rename(dst_file, new_dst_file_name)
    return True


def remove_attachment_file(att_list):
    dst_dir = os.path.dirname(__file__)
    for f in att_list:
        try:
            os.remove(os.path.join(dst_dir, f))
        except OSError as e:
            print(e)
        else:
            print("File {} is deleted successfully".format(os.path.join(dst_dir, f)))


def read_summary_to_dict(proj_path, device_id):
    src_file = os.path.join(proj_path, "report/{}/summary.txt".format(device_id))
    f = open(src_file, 'r')
    content = f.read()
    f.close()
    d = eval(content)
    return d


def send_report(title_project, udid_list, test_case_path, receiver_list):

    fail_count = 0
    pass_count = 0
    na_count = 0
    result = '[PASS]'

    opts = {'account': 'cyberlinkqamc@gmail.com', 'password': 'qamc1234',
            'to': '', 'subject': f'QAAT_{title_project} Mobile Auto Testing Report',
            'from': 'ATServer', 'text': 'txt_content', 'html': 'html_content',
            'attachment': []}
    html_report_header = '<html><head><meta http-equiv=""Content-Type"" content=""text/html; charset=ANSI""></head><body style=font-family:Calibri>'
    html_report_tail = '</body></html>'

    mail_body = html_report_header + summary_report_header()
    for device_id in udid_list:
        if os.path.isfile('{}/report/{}/SFT_Report.html'.format(test_case_path, device_id)):
            #backup and rename
            copy_rename("SFT_Report.html", "SFT_Report_{}.html".format(device_id), test_case_path, device_id)
            #add to attachment list
            opts['attachment'].append("SFT_Report_{}.html".format(device_id))
        if os.path.isfile('{}/report/{}/summary.txt'.format(test_case_path, device_id)):
            summary_dict = read_summary_to_dict(test_case_path, device_id)
            pass_count += int(summary_dict['pass'])
            fail_count += int(summary_dict['fail'])
            na_count += int(summary_dict['na'])
            mail_body += summary_report_add_row(summary_dict['title'], summary_dict['date'], summary_dict['time'], summary_dict['server'], summary_dict['os'], summary_dict['device'], summary_dict['version'], summary_dict['pass'], summary_dict['fail'], summary_dict['na'], summary_dict['skip'], summary_dict['duration'])

    mail_body += summary_report_tail() + html_report_tail
    if fail_count > 0:
        result = '[FAIL]'
    if pass_count == 0 and fail_count == 0:
        result = '[SKIP]'
    opts['subject'] += result
    opts['to'] = receiver_list
    opts['html'] = mail_body
    send_mail(opts)
    # remove attachment files
    remove_attachment_file(opts['attachment'])
    print('compelte')
    return True
