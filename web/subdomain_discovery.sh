
for sub in $(cat ~/HTB/SecLists/Discovery/DNS/subdomains-top1million-20000.txt);do dig $sub.internal.inlanefreight.htb @10.129.96.14 | grep -v ';\|SOA' | sed -r '/^\s*$/d' | grep $sub | tee -a subdomains.txt;done
