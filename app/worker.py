from asyncio import events
from ipaddress import ip_address
from sys import stdout
import ansible_runner, json
import os, json, shutil, re

workdir='/home/ilya/diplom/git_repos/dip_lom-1/playbooks'

def dir_cleanup(dirs):
    for dir in dirs:
        if os.path.exists(f'{workdir}/{dir}'):
            shutil.rmtree(f'{workdir}/{dir}')

def get_facts(host_ip):

    #ip=Hosts.query(ip_address).filter_by(id=host_id)
    facts = ansible_runner.run(
        module='setup',
        inventory=f'{host_ip}',
        extravars={'ansible_user':'batman'},
        host_pattern=host_ip,
    )
    fact_output=facts.get_fact_cache(host=host_ip)
    dir_cleanup(['artifacts','inventory'])
    return fact_output

def run_playbook(host_ip, task_name):
    r = ansible_runner.run(
        private_data_dir=workdir,
        playbook=task_name,
        inventory=f'{host_ip}',
        host_pattern=host_ip,
        extravars={'ansible_user':'batman', 'ansible_sudo_pass':'qwe1'},
        rotate_artifacts=1,
        )
    task_stdout=''
    for each_host_event in r.events:
        task_stdout+=each_host_event['stdout']+"\n"
    task_stdout = re.sub(r"\[\d;\d{1,2}m", "", task_stdout)
    task_stdout = re.sub(r"\[0m", "", task_stdout)
    task_output=dict()
    task_output['stat']=r.stats
    task_output['stdout']=task_stdout
    dir_cleanup(['artifacts','inventory','env'])
    return task_output