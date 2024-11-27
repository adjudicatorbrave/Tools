#!/usr/bin/env python3

# Dependencies:
# python3-dnspython

# Used Modules:
import dns.zone as dz
import dns.query as dq
import dns.resolver as dr
import argparse
import re

# Initialize Resolver-Class from dns.resolver as "NS"
NS = dr.Resolver()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--domain',type=str,required=True,help='Target Domain')
    return parser.parse_args()

def clear_url(domain):
    return re.sub('.*www\.','',domain,1).split('/')[0].strip()

def AFXR(domain, nameserver):
    DiscoveredSubdomains = [] 

    # Try zome transfer for a given domain and nameserver
    try:
        # Perform the zone transfer
        axfr = dz.from_xfr(dq.xfr(nameserver,domain))

        if axfr:
            print('[*] Successful zone transfer from {}'.format(nameserver))

            # Add found subdomains to global 'Subdomain' list
            for record in axfr:
                DiscoveredSubdomains.append(record.to_text())

    # if zone transfer fails
    except Exception as error:
        print(error)
        
    return DiscoveredSubdomains

# Fetch A records for a domain
def FetchARecords(domain):
    ARecords = [] 
    try:
        a_record = dr.resolve(domain, 'A')
        for a_record_entry in a_record:
            print('\t\t\tAdding ',a_record_entry,' to list of NS records')
            ARecords.append(str(a_record_entry))
    except dr.NoAnswer:
            print("No answer")
    return ARecords

# Fetch Nameservers for a domain
def FetchNameServers(domain):
    discovered_nameservers = []
    print('\tFetching NS records for', domain)
    ns_records = dr.resolve(domain, 'NS')
    for ns_entry in ns_records:
        ns_domain = str(ns_entry)
        ns_domain = ns_domain[:len(str(ns_domain))-1]
        print('\t\tFetching A Records for'+  ns_domain)
        discovered_nameservers.extend(FetchARecords(ns_domain))
    return discovered_nameservers

# Main
def Main():
    args = parse_args()
    domain = clear_url(args.domain)

    SubDomains = []

    print('Fetching nameservers for',domain)

    NS.nameservers = FetchNameServers(domain)

    for nameserver in NS.nameservers:
        #Try AXFR
        SubDomains.extend(AFXR(domain,nameserver))

    # Print the results

    if SubDomains is not None:
        print('------ Found subdomains:')

        # Print each subdomain
        for subdomain in SubDomains:
            print('{}'.format(subdomain))
    else:
        print('No subdomains found')


Main()
