import os
import shutil
from termcolor import colored

from module.active.ping import ping
from module.active.tech_pro5 import technology_pro5
from module.active.endpoint_fuzzing import endpoint_fuzzing
from module.active.passive_endpoint_param_fuzzing import passive_endpoint_param_fuzzing
from module.active.subdomain_fuzzing import subdomain_fuzzing
from module.active.passive_subdomain_fuzzing import passive_subdomain_fuzzing
from module.active.param_fuzzing import parameter_fuzzing
from module.active.port_scanning import port_scanning


def active_recon(domain, folder_result, threads, port_start, port_end):
    if os.path.exists(f'{folder_result}/active') and os.path.isdir(f'{folder_result}/active'):
        shutil.rmtree(f'{folder_result}/active')
    os.makedirs(f'{folder_result}/active', exist_ok=True)
    print(colored(f'[**] Starting Active Recon', 'yellow'))

    print(colored('[+] Subdomains Fuzzing', 'cyan'))
    subdomain_fuzzing(domain, threads, folder_result)

    subdomain_fuzzing_sample = folder_result + f'/passive/subdomain.txt'
    if os.path.exists(subdomain_fuzzing_sample):
        print(colored('[+] Passive Subdomains Fuzzing', 'cyan'))
        passive_subdomain_fuzzing(threads, folder_result)

    print(colored('[+] Ping & OS Detection', 'cyan'))
    ping(domain, folder_result)

    print(colored('[+] Technology Profiling', 'cyan'))
    technology_pro5(folder_result)

    print(colored('[+] Endpoints Fuzzing', 'cyan'))
    endpoint_fuzzing(threads, folder_result)

    print(colored('[+] Parameters Fuzzing', 'cyan'))
    parameter_fuzzing(threads, folder_result)

    endpoint_fuzzing_sample = folder_result + f'/passive/endpoint.txt'
    if os.path.exists(endpoint_fuzzing_sample):
        print(
            colored('[+] Passive Endpoints And Passive Parameters Fuzzing', 'cyan'))
        passive_endpoint_param_fuzzing(threads, folder_result)

    print(colored('[+] Port Scanning    ', 'cyan'))
    port_scanning(threads, folder_result, port_start, port_end)

