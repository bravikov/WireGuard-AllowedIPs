import dns.resolver
import glob
import sys
import socket

filenames = glob.glob('*.list')

domains = []

for filename in filenames:
    with open(filename) as file:
        for line in file.readlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                continue
            domains.append(line)

print('Domains:', domains)

ipv4s = []
ipv6s = []

for domain in domains:
    try:
        result = dns.resolver.resolve_name(domain)
    except dns.resolver.NXDOMAIN as e:
        print(e, file=sys.stderr)
    for ipv4 in result.addresses(family=socket.AF_INET):
        ipv4s.append(ipv4 + '/32')
    for ipv6 in result.addresses(family=socket.AF_INET6):
        ipv6s.append(ipv6 + '/128')

print('IPv4:')
print('\t', ', '.join(ipv4s))
print('IPv4 and IPv6:')
print('\t', ', '.join(ipv4s + ipv6s))
