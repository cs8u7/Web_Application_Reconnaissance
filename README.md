
#### 3.4.1 Verify Alive Target

- In order to continue, we need to verify that the domain is live by looking at the live website associated with the domain.
- Use command `ping` to target's domain: is a network utility used to test the reachability of a host on an IP network and to measure the round-trip time for messages sent from the originating host to a destination computer.
	

- `ping` command uses the Internet Control Message Protocol (ICMP) to send and receive messages. The package is sent from the source host to the target host over the network using IP.The ICMP Echo Reply packet mirrors the Echo Request, changing the ICMP type to 0 (Echo Reply) and keeping the identifier, sequence number, and payload data intact.



- Access the domain in browser, there are some possibilities can occur:
	- Error 404: DNS record for the domain is delete
	- Taken by another Entity 
	- Redirect request from web server turn user to lastest version

#### 3.4.2 Server's Technology Detection
#### 3.4.3 Domain Discovery
- Domain name structure
##### 3.4.2.1 Domain Enumeration

- `Subdomain Enumeration`: Identify subdomains using `Amass enum` in both active mode and passive mode
##### 3.4.2.1 Vitural Host Fuzzing

- Vitual Host: There are many websites are hosted in a same web server
	- Reduce cost & utilize resource

| Name-base Hosting                                               | Ip-base Hosting                                      |
| --------------------------------------------------------------- | ---------------------------------------------------- |
| Multiple domains to share a single IP address.                  | Unique IP address for each domain                    |
| Header "Host" determine which virtual host configuration to use | Uses IP address to determine which website to serve. |
- Name-base example:
```PHP
<VirtualHost *:80>
    ServerName example.com
    DocumentRoot /var/www/example.com
</VirtualHost>

<VirtualHost *:80>
    ServerName example.org
    DocumentRoot /var/www/example.org
</VirtualHost>
```

- IP-base example:
```PHP
<VirtualHost 192.168.1.1:80>
    ServerName example.com
    DocumentRoot /var/www/example.com
</VirtualHost>

<VirtualHost 192.168.1.2:80>
    ServerName example.org
    DocumentRoot /var/www/example.org
</VirtualHost>

```

- Subdomain example:
```PHP
<VirtualHost *:80>
    ServerName blog.example.com
    DocumentRoot /var/www/blog
</VirtualHost>

<VirtualHost *:80>
    ServerName shop.example.com
    DocumentRoot /var/www/shop
</VirtualHost>
```
#### 3.4.4 Port Scanning
    
    [](https://github.com/cs8u7/ICT-Lab_Internship-Project#342-port-scanning)

- `Port Scanning`: Use tools like Nmap to identify open ports and running services on the target.
    - Example: `nmap -sS -sV example.com`
- `Service Fingerprinting`: Determine the versions of the services running on the open ports.

#### 3.4.5 Endpoint Fuzzing
#### 3.4.6 Parameter Fuzzing

#### 3.4.7 Vulnerability Scanning

- `Automated Scanners`: Use tools like `Nuclei`, `Acunetix`, `Nessus`, `OpenVAS`, or `Burp Suite's scanner` to identify known vulnerabilities.
- `Manual Testing`: Manually test for common web vulnerabilities such as SQL injection (`sqlmap`), XSS (`fuzzing`), LFI (`lfimap`), and others.

## 6. References
https://github.com/willc/OSINT-flowcharts
https://praveendandu24.medium.com/a-beginners-guide-to-how-dns-works-making-sense-of-the-internet-s-phonebook-cd90e2054f85
https://github.com/Lissy93/web-check
https://github.com/The-Osint-Toolbox/Website-OSINT
https://github.com/yogeshojha/rengine
https://github.com/six2dez/reconftw
https://github.com/sakibulalikhan/reconx
https://github.com/samhaxr/recox
https://blog.projectdiscovery.io/secret-token-scanning-with-nuclei/