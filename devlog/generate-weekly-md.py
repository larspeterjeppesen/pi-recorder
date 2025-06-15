import datetime
import sys
import re
import os
import functools

def create_weekly_log_file(new_log_file_path, week_number, log_file_template):
    date = datetime.date.today().strftime("%Y/%m/%d")
    date_text = f'Log entry for week {week_number}, started on {date}'
    with open(log_file_template, 'r') as template_log_file:
        template_text = template_log_file.readlines()
        template_text = functools.reduce(lambda a,b: a+b, template_text)
        with open(new_log_file_path, 'x') as new_log_file:
            new_log_file.write(date_text)
            new_log_file.write('\n\n')
            new_log_file.write(template_text)

 
def generate_log_week(log_file_template, weekly_topics_file_name, log_file_name):
    args = sys.argv

    p = re.compile(r'week[0-9]+')
    ds = os.walk('.').__next__()[1]
    weeks_created = list(filter(lambda dir_name: p.match(dir_name) is not None, ds))
    weeks_created = list(map(lambda dir_name: int(dir_name.split(' ')[0][4:].split(':')[0]), weeks_created))
    weeks_created.sort()
    week_number = weeks_created[-1] + 1 if weeks_created != [] else 1

    with open(weekly_topics_file_name, 'r') as weekly_topics_file:
        weekly_topics = weekly_topics_file.readlines()
        log_folder_name = weekly_topics[week_number-1].replace('\n','')

    if log_folder_name not in ds:
        os.mkdir(log_folder_name)
        print(f'Created folder {log_folder_name}.')
    else:
        print(f'Folder for week {week_number} already exists.')

    log_folder_files = os.walk(log_folder_name).__next__()[2]
    if log_file_name not in log_folder_files:
        new_log_file_path = log_folder_name + '/' + log_file_name
        create_weekly_log_file(new_log_file_path, week_number, log_file_template)
        print(f'Created log file for week {week_number}.')
    else:
        print(f'Log file for week {week_number} already exists.')


log_file_template = 'log-file-template-1'
weekly_topics_file_name = 'topics-1'
log_file_name = 'log.md'
generate_log_week(log_file_template, weekly_topics_file_name, log_file_name)
