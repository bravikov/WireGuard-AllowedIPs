import dns.resolver
import glob
import sys
import socket
import re


def read_lists(template):
    filenames = glob.glob(template)
    lines = []
    for filename in filenames:
        with open(filename) as file:
            for line in file.readlines():
                line = line.strip()
                if not line:
                    continue
                if line.startswith('#'):
                    continue
                lines.append(line)
    return lines


domains = read_lists('*.domain_list')

print('Domains:', domains)

ipv4s = []
ipv6s = []

my_resolver = dns.resolver.Resolver()

# 8.8.8.8 is Google's public DNS server
my_resolver.nameservers = ['8.8.8.8']

for domain in domains:
    try:
        result = my_resolver.resolve_name(domain)
    except dns.resolver.NXDOMAIN as e:
        print(e, file=sys.stderr)
        exit(1)
    for ipv4 in result.addresses(family=socket.AF_INET):
        ipv4s.append(ipv4 + '/32')
    for ipv6 in result.addresses(family=socket.AF_INET6):
        ipv6s.append(ipv6 + '/128')

ipv4s += read_lists('*.ipv4_list')
ipv6s += read_lists('*.ipv6_list')

print('IPv4:')
print('\t', ', '.join(ipv4s))
print('IPv4 and IPv6:')
print('\t', ', '.join(ipv4s + ipv6s))
