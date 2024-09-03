#!/bin/bash

# sudo ./nmap_scanner.sh [IP] [RATE] [FILENAME]
ip=$1
rate=$2
fileName=$3

for sub in $(cat ~/HTB/SecLists/Discovery/DNS/subdomains-top1million-20000.txt);do dig $sub.internal.inlanefreight.htb @10.129.96.14 | grep -v ';\|SOA' | sed -r '/^\s*$/d' | grep $sub | tee -a subdomains.txt;done


echo "Executing nmap scans on IP address "$ip" at a rate of T"$rate" and storing into files labelled"$fileName


nmap_syn_command="nmap -T"$rate" -p- -sS -oN "$fileName"_syn_scan "$ip
nmap_ack_command="nmap -T"$rate" -p- -sA -oN "$fileName"_ack_scan "$ip
nmap_tcp_command="nmap -T"$rate" -p- -sT -oN "$fileName"_tcp_scan "$ip

echo $nmap_syn_command
$nmap_syn_command &

echo $nmap_ack_command
$nmap_ack_command &

echo $nmap_tcp_command
$nmap_tcp_command &
