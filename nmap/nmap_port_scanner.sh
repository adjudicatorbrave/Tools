#!/bin/bash

# sudo ./nmap_scanner.sh [IP] [RATE] [FILENAME]
ip=$1
rate=$2
fileName=$3
port=$4

echo "Executing nmap scans on IP address "$ip" port(s)"$port" at a rate of T"$rate" and storing into files labelled"$fileName


nmap_sc_sv_command="nmap -T"$rate" -p "$port" -sC -sV -oN "$fileName"_sc_sv_scan "$ip
nmap_script_vuln_command="nmap -T"$rate" -p "$port" -script vuln -oN "$fileName"_script_vuln_scan "$ip
nmap_script_auth_command="nmap -T"$rate" -p "$port" -script auth -oN "$fileName"_script_auth_scan "$ip

echo $nmap_sc_sv_command
$nmap_sc_sv_command &

echo $nmap_script_vuln_command
$nmap_script_vuln_command &

echo $nmap_script_auth_command
$nmap_script_auth_command &

