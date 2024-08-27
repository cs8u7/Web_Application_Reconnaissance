from pathlib import Path
import requests
import ssl
from publicsuffixlist import PublicSuffixList
import argparse
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import logging

# Directory to store PEM files (cache)
STATE_DIR = Path('state')
STATE_DIR.mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO)


def get_cert_ids(domain, args, extended=None):
    """Find all certs with 'domain' in the Identity section."""
    base_url = "https://crt.sh/"
    r_params = {'output': "json"}

    if args.exclude_expired:
        r_params['exclude'] = 'expired'

    if (extended is None or extended) and args.extended:
        r_params['q'] = f"{get_domain_private_suffix(domain)}.%.%"
    else:
        r_params['Identity'] = domain

    r_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
    req = requests.get(base_url, params=r_params, headers=r_headers)
    logging.info(f"Request URL: {req.url}")

    if req.ok:
        try:
            for cert in req.json():
                yield cert['min_cert_id']
        except ValueError:
            logging.error("Failed to parse JSON response.")
    else:
        logging.error(f"Failed to retrieve certificates for domain {domain}")
    return None


def get_cert(cert_id, args):
    """Download the PEM formatted certificate for processing."""
    pem_file = STATE_DIR.joinpath(f'{cert_id}.pem')
    if pem_file.exists() and not args.uncached:
        return pem_file

    base_url = f"https://crt.sh/?d={cert_id}"
    r_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
    req = requests.get(base_url, headers=r_headers)

    if req.ok:
        try:
            with pem_file.open('w+b') as f:
                f.write(req.content)
            return pem_file
        except IOError:
            logging.error(f"Error writing PEM file {pem_file}")
    else:
        logging.error(f"Failed to download certificate ID {cert_id}")
    return None


def get_subjectaltname(cert_path):
    """Extract subjectAltName from the certificate using cryptography."""
    if cert_path is None:
        return

    with open(cert_path, 'rb') as cert_file:
        cert_data = cert_file.read()
    
    try:
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
        for ext in cert.extensions:
            if isinstance(ext.value, x509.SubjectAlternativeName):
                for name in ext.value.get_values_for_type(x509.DNSName):
                    yield name.lower()
    except Exception as e:
        logging.error(f"Failed to extract subjectAltName: {e}")


def get_subdomains(domain, args, extended=None):
    """Extracts domain names from subjectAltName field."""
    if extended is None:
        extended = args.extended

    subdomains = set()
    count = 0

    if extended:
        priv_suffix = get_domain_private_suffix(domain)

    for crtsh_id in get_cert_ids(domain, args, extended):
        for subject in get_subjectaltname(get_cert(crtsh_id, args)):
            if not extended or priv_suffix in subject:
                subdomains.add(subject)

        new_count = len(subdomains) - count
        if new_count > 0:
            logging.info(f"New domains found: {new_count}.  Total: {count + new_count}")
        count = len(subdomains)

    return subdomains


def get_domain_private_suffix(domain):
    """Returns 'www.google' for 'www.google.com'."""
    psl = PublicSuffixList()
    tld = "." + psl.publicsuffix(domain)
    return domain.replace(tld, '')


def main(args):
    logging.info(f'Domain: {args.domain}, Extended: {args.extended}, Exclude Expired: {args.exclude_expired}, Uncached: {args.uncached}')
    for domain in args.domain:
        if args.extended:
            subdomains = get_subdomains(domain, args, extended=False).union(get_subdomains(domain, args))
        else:
            subdomains = get_subdomains(domain, args, extended=False)
        logging.info(f"Subdomains for {domain}: {subdomains}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Discover domains using crt.sh.")
    parser.add_argument('--domain', '-d', required=True, metavar='N', type=str, nargs='+',
                        help="crt.sh domain query. Specify multiple using --domain <domain>")
    parser.add_argument('--extended', required=False, default=False, action='store_true',
                        help="Include wildcard searches with domain private suffix ('google.%%.%%' for 'google.com').")
    parser.add_argument('--exclude_expired', required=False, default=False, action='store_true',
                        help="Exclude expired certificates.")
    parser.add_argument('--uncached', required=False, default=False, action='store_true',
                        help="Only return domains not previously discovered (not in PEM cache).")
    parser.set_defaults(func=main)

    try:
        args = parser.parse_args()
        args.func(args)
    except Exception as err:
        logging.error(err)
        parser.print_help()
