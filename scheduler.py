from os import environ
config = environ.get('CONFIG', 'poetry.json')

from tendo import singleton
me = singleton.SingleInstance(flavor_id=config)

import schedule
import time
import subprocess

def bash_command(cmd):
    subprocess.Popen(cmd, shell=True, executable='/bin/bash')
    
def stihbot():
    subprocess.run(['timeout', '21600', 'python', 'stihbot.py'])

schedule.every(10).seconds.do(stihbot)

while True:
    schedule.run_pending()
    time.sleep(1)