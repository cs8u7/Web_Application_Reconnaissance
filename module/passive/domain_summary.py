import time

def domain_summary(root_domain, folder_sample):
    start_time = time.time()
    
    domain_sample = folder_sample + '/passive/subdomain.txt'
    analytic_sample = folder_sample + '/passive/analytic_domain.txt'
    cert_sample = folder_sample + '/passive/cert_domain.txt'
    
    final_subdomain = []

    with open(cert_sample, 'r') as file:
        cert_domains = file.read().splitlines()

    with open(analytic_sample, 'r') as file:
        analytic_domains = file.readlines()

    with open(domain_sample, 'r') as file:
        domains = file.readlines()

    final_subdomain = list(set(cert_domains + analytic_domains + domains))

    for domain in final_subdomain:
        with open(domain_sample, 'a') as file:
            file.writelines(f'{domain.strip()}\n')

    end_time = time.time()
    running = end_time - start_time
    print(f"[Time]: {running:.2f}s")
    print(f"[Result]: {len(final_subdomain)}")