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

    for domain in analytic_domains:
        if domain.endswith(f'.{root_domain}') or domain == root_domain:
            final_subdomain.append(domain)

    for domain in cert_domains:
        if domain.endswith(f'.{root_domain}') or domain == root_domain:
            final_subdomain.append(domain)

    for domain in domains:
        if domain.endswith(f'.{root_domain}') or domain == root_domain:
            final_subdomain.append(domain)

    final_subdomain = list(set(final_subdomain))

    with open(domain_sample, 'w') as file:
        file.writelines([subdomain + '\n' for subdomain in final_subdomain])

    end_time = time.time()
    running = end_time - start_time
    print(f"[Time]: {running:.2f}s")
    print(f"[Result]: {len(final_subdomain)}")