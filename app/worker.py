from asyncio import events
from ipaddress import ip_address
from sys import stdout
import ansible_runner, json
import os, json, shutil

workdir='/home/ilya/diplom/git_repos/dip_lom-1/playbooks'

def get_facts(host_ip):

    #ip=Hosts.query(ip_address).filter_by(id=host_id)
    facts = ansible_runner.run(
        module='setup',
        inventory=f'{host_ip}  ansible_user=batman',
        host_pattern=host_ip,
    )
    fact_output=facts.get_fact_cache(host=host_ip)
    if os.path.exists(f'{workdir}/artifacts'):
        shutil.rmtree(f'{workdir}/artifacts')
    if os.path.exists(f'{workdir}/inventory'):
        shutil.rmtree(f'{workdir}/inventory')
    return fact_output

def run_playbook(host_ip, task_name):
    r = ansible_runner.run(
        private_data_dir=workdir,
        playbook=task_name,
        inventory=f'{host_ip}  ansible_user=batman',
        host_pattern=host_ip,
        json_mode=True,
        rotate_artifacts=1,
        )
    task_output=''
    for each_host_event in r.events:
        task_output+=each_host_event['stdout']+'\n'
    if os.path.exists(f'{workdir}/artifacts'):
        shutil.rmtree(f'{workdir}/artifacts')
    if os.path.exists(f'{workdir}/inventory'):
        shutil.rmtree(f'{workdir}/inventory')
    return task_output