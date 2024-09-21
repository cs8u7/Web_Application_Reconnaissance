import argparse
import sys
import re
from datetime import datetime
from termcolor import colored
from module.print_title import print_title
from main.active import active_recon
from main.passive import passive_recon


def main():
    print_title()

    parser = argparse.ArgumentParser(
        description="Automate Reconnaissance Tool")
    parser.add_argument('-u', type=str, help="URL of target web application.")
    parser.add_argument('-p', action='store_true',
                        help="Specific passive recon")
    parser.add_argument('-a', action='store_true',
                        help="Specific active recon")
    parser.add_argument('-ipinfo', action='store_true',
                        help="Mark IPinfo key is trail or premium")
    parser.add_argument('-cert', action='store_true',
                        help="Enable domain discover with certificate")
    parser.add_argument('-cache', action='store_true',
                        help="Only use captured SSL certificate for domain discover")
    parser.add_argument('-threads', type=int, default=10,
                        help="Define number of threads in fuzzing (default: 100)")
    parser.add_argument('-port_start', type=int, default=1,
                        help="Define start port for scanning (default: 1)")
    parser.add_argument('-port_end', type=int, default=10000,
                        help="Define end port for scanning  (default: 10000)")
    args = parser.parse_args()

    args_dict = vars(args)

    if not args.u:
        print(colored(
            "Error: The '-u' option is required. Please provide a valid URL.", "magenta"))
        sys.exit(1)

    if not (args.p or args.a):
        print("Error: You must provide either -p (passive recon) or -a (active recon).")
        sys.exit(1)

    encountered_options = []

    for option, value in args_dict.items():
        if value:
            if option in encountered_options:
                print(colored(
                    f"Error: Duplicate option detected: '{option}'. Please use each option only once.", "magenta"))
                sys.exit(1)
            else:
                encountered_options.append(option)

    url_pattern = re.compile(
        r'^((http|https):\/\/)?(?P<domain>[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,})(:\d+)?(\/\S*)?$')
    match = url_pattern.match(args.u)

    if match:
        domain = match.group('domain')
        date = datetime.now().date()
        folder_result = str(date) + '#' + args.u

        if args.p:
            passive_recon(domain, folder_result, args.cert,
                          args.cache, args.ipinfo)

        if args.a:
            active_recon(domain, folder_result, args.threads,
                         args.port_start, args.port_end)
    else:
        print(colored(
            "Error: The url has invalid form. Please provide a valid URL.", "magenta"))
        sys.exit(1)


if __name__ == '__main__':
    main()
    print(colored('[\/] DONE !!!!!!!!!!!!!!!!!!!!!!!!!!!!', 'green'))
