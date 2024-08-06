# UNIVERSITY OF SCIENCE AND TECHNOLOGY OF HANOI
# DEPARTMENT OF INFORMATION COMMUNICATION TECHNOLOGY
![](USTH_logo/Logo-Truong-Dai-hoc-Khoa-hoc-va-Cong-nghe-Ha-Noi.png)

# INTERNSHIP PROJECT REPORT
# Web Application Reconnaissance Flow Analysis

**Supervisor**: Dr. Nguyen Minh Huong, ICT Department, USTH

**Student/Reporter**: Tran Duc Tuan, BI12-467, B3 CS, USTH

ICT Lab, May 15, 2024

## Table of Content
### 1. Executive Summary
### 2. Introduction
- #### 2.1 Project Context
	- ##### 2.1.1 Web Application
	- ##### 2.1.2 Web Application Domain
	- ##### 2.1.3 Offensive Security - Red Teaming & Penetration Testing
	- ##### 2.1.4 Reconnaissance
- #### 2.2 Project Objective
- #### 2.3 Project Scopes
	- ##### 2.3.1 Inclusion
	- ##### 2.3.2 Exclusion
### 3. Methodology 
- #### 3.1 Introduce Open-Source Reconnaissance Tool - reNginx
- #### 3.2 Breakdown Web Domain Reconnaissance Workflow Into Stages
- #### 3.3 Passive Reconnaissance
	- ##### 3.3.1 OSINT (Open Source Intelligence) Definition and Workflow
	- ##### 3.3.2 User Name
	- ##### 3.3.3 Email Address
	- ##### 3.3.4 Real Name
	- ##### 3.3.5 Phone Number And Telephone
	- ##### 3.3.6 Location
- #### 3.4 Active Reconnaissance
	- ##### 3.4.1 Verify Alive Target
	- ##### 3.4.2 Server's Technology Detection
	- ##### 3.4.3 Domain Discovery
	- ##### 3.4.4 Port Scanning
	- ##### 3.4.5 Endpoint Fuzzing
	- ##### 3.4.6 Parameter Fuzzing
	- ##### 3.4.7 Vulnerability Scanning
### 4. Implementation
- #### 4.1 Applying Reconnaissance Idea & Technology To Develop Reconnaissance Tool With Narrowed Purpose
### 5. Result
- #### 5.1 Testing Tools and Comparing Result With Using Specific Tools For Each Stage
- #### 5.2 Conclusion
### 6. References


	- method
		- analyze: in & out
	- implement
		-  analyze: in & out
	- result
		- data 
		- analyze : %CVE CWE
		- category & vitalize

## 1. Executive Summary

- My project aims to separate, research and analyze a standard reconnaissance workflow. I focus on research protocol, service and stored information of a web application and analyze the output's value stage of each stage in the workflow.
- In each stage, I demonstrate research and analyze the idea of reconnaissance\
  techniques and introduced some specific tools in that stage.
- After finish analyzing process, i would like to custom an open-source recon reconnaissance tool to center all reconnaissance technique with automatic purpose.
## 2. Introduction
### 2.1 Project Context
#### 2.1.1 Web Application

- A web application is an application program that is stored on a remote server and delivered over the internet through a browser interface.
- Structure of a Website:
![](capture/Pasted%20image%2020240531102715.png)

- Include: 
	- `Web Client`: is user's device, has role is render and display data received from server.
	- `Firewall`:A firewall is a network security device that monitors incoming and outgoing network traffic and decides whether to allow or block specific traffic based on a defined set of security rules.
	- Web Server:
		- On the hardware side, a web server is a computer that stores web server software and a website's component files. A web server connects to the Internet and supports physical data interchange with other devices connected to the web.
		- On the software side, a web server includes several parts that control how web users access hosted files. At a minimum, this is an _HTTP server_. An HTTP server is software that understands URL (web addresses) and HTTP. An HTTP server can be accessed through the domain names of the websites it stores, and it delivers the content of these hosted websites to the end user's device.
	- WebApp (Web Application): is application run on a corresponding web engine which is install inside web server, resolve incomming request from client, execute logic and response to client.
	- Database: is a service play role store and provide data for resove logic process in web applications.

#### 2.1.2 Web Application Domain

- `Web Application Domain`: Input for Reconnaissance and Pentest Processing, a web application domain is a component of a uniform resource locator (URL) used to access websites. It is also a representative name for web application's IP address. 
	![](capture/Pasted%20image%2020240528154451.png)
#### 2.1.3 Offensive Security - Red Teaming & Penetration Testing

- Red teaming is a structured process used to simulate an attack on an organization to identify vulnerabilities and improve security. Red teaming focus on deep attack in organization's server such as take control server and attack to related infrastructure and server while pentesting which present is initial access of whole red team process involves identifying vulnerabilities, exploiting them to determine their impact, and providing actionable recommendations to mitigate the discovered weaknesses. 
- Pentest typically includes a comprehensive examination of various aspects of the target environment, such as network infrastructure, web applications, and internal systems. 
- In this report, I will focus on web application testing, demonstrate detailed methodologies for identifying and exploiting vulnerabilities, and clarify the logical workflows and tools used in the pentest process.

![](capture/Pasted%20image%2020240707171822.png)

#### 2.1.4 Reconnaissance

-  Its regular name is recon for short. It is the process of gathering information about a target system, network, or organization before attempting an attack or security assessment. 
- The Reconnaissance process involves collecting extensive information about the potential targets, their vulnerabilities, and possible attack vectors. 
- In this report, I would focus on web reconnaissance, demonstrate analyze workflows and clarify analyzing of the mentioned tools in the reconnaissance process.
### 2.2 Project Objective

- My project leads to clarifying protocol and techniques which are used to searching for structure and information related to the input target domain. In each technology or protocol or some kind of researched information, I would like to determine if it is a critical data related web application target or evidence for the next stage of gathering data.
- Based on current knowledge after ending the research process, I would like to develop a recon tool to equip recon modules which are mentioned in the research part. My purpose is to actualization all the proof of concept of techniques and protocols in the research part in a use-able tool. This tool would use a domain name of a web application as into the tool's automated recon process and return raw data of the web application.
### 2.3 Project Scopes
#### 2.3.1 Inclusion

My project includes the following features:
- Breakdown the whole recon process into individual stages.
- Searching and analyze technique, protocol and workflow of each stages.
- Provide and introduce some tools specified for each stage.
- Develop a new recon tool.
#### 2.3.2 Exclusion

My project doesn’t include the following features:
- Customize an open-source recon tool for automatic purpose.
- Reserve some close-course tool to extract recon workflow.
- Define red team technique in custom recon flow
- Research and Analyze others stage in red team workflow.
## 3. Methodology
### 3.1 Introduce Open-Source Reconnaissance Tool - reNginx
#### 3.1.1 Introduction\

- reNginx is a web application reconnaissance suite was created with security experts, penetration testers, and bug bounty hunters. Its purpose is to make the reconnaissance process easier and more efficient. 
- ReNgine redefines how pentester gathering critical information about online web applications target with its highly configurable engines, data correlation capabilities, constant monitoring, database-backed reconnaissance data, and user-friendly interface.
#### 3.1.2 Why reNginx is the chosen one

- In the modern life, tools are design to calculate and execute works and tasks by centralize all the steps in a process. It make modern works easier to approach and automate. Narrow in pentester works, if I consider the target is a web application, there are a number of things have to check and test and tools centralize all the steps in protocols or works and automate it.
- While traditional reconnaissance tools often fall short in terms of configurability and efficiency. reNgine addresses these shortcomings and emerges as an excellent alternative to existing tools.
- An important reason that makes reNginx in my choice list is that reNginx is an open-source tool with a clarity design that is able to cover most category in recon process. This tool also provide a fully recon's workflow which i would like to focus on searching and analyze technique in each stages.
#### 3.1.3 Overview about reNginx workflow

![](capture/Pasted%20image%2020240710094028.png)

- reNginx also require a Web Domain or URL which point to web application to trigger the recon process. Base on the graph's workflow, I consider that OSINT process (passive recon) run parallel with active recon process. The aim of osint process is gathering several kind of information related to target such as domain whois data, register email, and employees emails and sensitive data. reNginx would collect list subdomain and active port data in active recon stage then the result's list would become input of vulnerability scanning stage.
### 3.2 Breakdown Web Domain Reconnaissance Workflow Into Stages

- I would like to separate the recon workflow into stages by techniques before digging into analysis. A recon process regularly divided into two main stages, which are passive recon and active recon. While passive recon involves gathering information without directly interacting with the target, the other one involves interacting with the target system. This can be more detectable by the target but often capture more detailed information.
- In the passive recon stage, I would like to demonstrate analyzing workflows and tactics for searching for information related to the target. This stage also has another name and is open source intelligence (OSINT). This technique focuses on searching for critical data of targets in several public databases, leaked databases, protocols and sensitive credentials.
- In the active recon stage, pentesters directly interact with the web application to extract information based on requests to and responses from the server. This process involves using protocols to transmit data. It provides pentesters with an overview of the web application's structure, including endpoints, subdomains, and parameters. At the end of the workflow, pentesters scan for potential vulnerabilities in the target using various vulnerability scanning templates.
### 3.3 Passive Reconnaissance
#### 3.3.1 OSINT (Open Source Intelligence) Definition and Workflow

- **OSINT** is an abbreviation of Open Source Intelligence. It is the process of collecting, analyzing, and utilizing information that can be gathering from the internet. Expected output of the process is critical data related to the target, such as IP address, domain information, employees' email, sensitive information, hidden endpoints, documents and social network information. Here is a standard OSINT workflow [1] applied to web application .

![](capture/Pasted%20image%2020240723163134.png)

- In order to initiate of this OSINT workflow, it requires an live web domain as an input for the process. This process covers most of OSINT's fields and there are two main parts: gathering, extracting & analyzing data. While in the collecting information part, the workflow uses a searching technique (docking) in several well-known search engines or Spiderbot's databases (Wayback Machine). In the other part, the process extracts critical information from the gathered data list and analyzes it.
##### 3.3.1.1 Search Engines and Web Cached

- In daily life, internet users usually use several search engines in computer browsers, such as Google, Firefox, Bing, ... Each browser has its own corresponding search engine or users can choose the engine which is the most suitable for them. In general, Google is the most well-known search engine, and it is also used by most of internet users.
- Indeed, using search engines to find information is searching for data of cached versions of websites matched with search's form which is stored on the servers of the entity running the spider bot, such as a search engine company.
- A cached page (cached versions of websites) is a web page that has been saved by a search engine on its servers or by a user's browser. Search engines cache pages to allow access to them even when the website's server is not accessible because it is data crawled at the latest capture time but not the data page at search time.
##### 3.3.1.2 Regular Search and Search Engine Dorking

- Because Google is the most famous search engine, and it also has the highest number of users in all over the world, so in this part and during this report, I would like to use and research about Google search engine. Indeed, search action in the browser is query data in search engine databases with searching term which is input by user but not google search engine help user search the result in the internet at the time user input the term. There are two main kinds of internet user: basic user and attacker. While the former used to use regular Google searching, the latter takes advantage of Google dorking most of the time in order to optimize searching efficacy.

- While using regular Google searching, Google interprets the search query by splitting it into individual words or terms and searches for pages that are relevant to any or all of those terms. Google uses its ranking algorithms to show the most relevant results based on factors such as relevance, popularity, user behavior, and content quality. Google might also consider synonyms, related terms, and variations of the words in the query to provide a comprehensive set of results. Google tries to understand the context and intent behind the search query to offer the most useful results.

- From a Pentesters' view, regular searching is easy to use and collects a amount of search results by input searching term. But, because regular search splits search terms into terms to make sure that it is possible to collect the most results as can - this feature can cause a critical weak point is low accuracy.
- In order to avoid is disadvantage, attackers suggest using a more advance searching technique. Google Dorking, also known as Google hacking, involves using advanced search operators to find specific information. It involves using basic search operators to find information that is publicly accessible but might not be immediately obvious. 
- Google Working sites, which are regular search, can not act. It's often used to find specific files, information, or directories on a website. Dorking is a combination between using fixed terms placed in double or single quotes and Google search operators. While regular searching is able to split search terms to collect the most possible result, advanced search with quotes makes Google search engine algorithms respect full string search to collect accurate results.
- Besides, Google Dorking is famous for using Google search engine operators. It includes the operator keyword followed by a colon and the search term. The search term can be put in quotes to increase accuracy. Here is an example of searching login endpoint with Google Dorking.

![](capture/Pasted%20image%2020240803231739.png)

- While Google Working is highly effective at searching for hidden data or data which is unable to search regularly, it is still hard to collect a set of results but only display results on page in on a search engine's browser. I would like to introduce tools which support capturing dorking results and provide more effective search operators: shodan and FOFA. Both of these tools support search engines in a better way and each of these tools has its own crawlers and databases. FOFA and there both have support documents about search operators and API, but there are a few differences in the operators and has a client version but FOFA does not.
##### 3.3.1.3 Crawler (Spiderbot) and Wayback Machine 

- Crawler (Spiderbot) is an automated program that systematically browses the web to collect, retrieve and index information from websites. Here is a general workflow of a web crawler.

![](capture/Pasted%20image%2020240721170611.png)

- The web spiderbot prepares a list of URLs (Seed URLs) as input for the crawl process. The selection of seed URLs depends on the goals of the web crawler. For each endpoint in the seed list, the crawler uses HTTP requests to fetch the HTML content of the web pages and parses it based on HTML tags. Then, the crawler extracts useful information, most of which are external links pointing to new websites. Sometimes, the crawler can detect sensitive data in the HTML content. In the view of Googlebot, for searching purposes, it prioritizes extracting content in header tags and images. After finishing the downloading process of the seed list, the crawler removes duplicates, irrelevant links, or URLs that already exist in the seed list. URLs are prioritized based on the crawler's algorithms, considering factors like page importance and update frequency while scheduling to avoid server overload. Unlike some specific-purpose spiderbots, crawlers that serve search engines like Google or Bing index URLs based on their rank (number of backlinks) and categories to enhance performance. backlinks also known as inbound links or incoming links, are links from one website to a page on another website. It is an external links place in others sites which are point to your website. Last, the crawler updates new-found URLs into the seed list in order to initialize new crawl processes.

- The Web crawler plays an important role in the OSINT process because it gives the pentesters a view of target's web structure, especially is hidden endpoint or internal documents. Indeed, most web spiderbots serve for search purposes or search engines, so it do not display old cached versions of websites in order to ensure access the URL search lists. Wayback Machine is a well-known internet archive providing a friendly search engine for older versions of the website. Wayback snapshot a website's content at specific times in the past. This provides a major advantage in collecting critical deleted information or ability (hidden API keys) of unfix vulnerability. 

![](capture/Pasted%20image%2020240722120622.png)

- Thanks to crawlers' Wayback and its data, WaybackURLs help pentesters find old subdomains and hidden endpoints by leverage the existing archived data from the Wayback Machine. Those find-able old subdomains that may have vulnerabilities are described as follows. I consider a scenario where a web developer has to shut down a service on the web application. But the developer just deletes a service's DNS record so that a basic user is unable to access the service, while the attacker may find the IP of that service and, of course, old services always contain vulnerabilities.
##### 3.3.1.4 Hidden Endpoints

- Hidden endpoints are web application URLs or paths which exist but are not documented or publicly advertised. These endpoints are not intended for general use and may serve various specific purposes, such as using in internal of companies or organizations, testing new features and serving for superusers. Indeed, hidden endpoints are latent risks of being attacked by entities outside the organization. Attackers would like to focus on the endpoints which bring value, the web application's information as endpoints are internal documents or web config files.
- Attackers have many ways to collect hidden endpoints archives, search engine dorking and webmaster files. For web archives, as I mention in the above part, Wayback's crawler downloads web content automatically but, important thing is the crawler indexes the URLs. This structures the web accidentally so the attacker can collect all the URLs which are collected by the crawler.
- Besides URLs collected from web archives, attackers also can gather hidden paths in webmaster files which optimize the way search engine crawlers interact with their websites. There are two webmaster files we should pay attention to: robots.txt and sitemap.xml. robots.txt is a file which is placed at the document root of a web application, and provides directives to web crawlers about which pages or sections of a site should not be crawled or indexed. sitemap.xml is a file contains a list of URLs on a website, along with metadata about each URL.
- Technique search engine dorking is not really directly gathering URLs as both methods above. This technique is mentions above with ability of searching endpoints which are hard to finds, low rank and can not find by regular searching. At the time when web programming templates were created, It mark an explosive growth of web applications' services. But, while all web developers focus on create services which make people's daily life become more convenient, developers usually do not concern about exist security problems. Because of ensuring development progress of the web service and reducing time for project's newbie understanding the code, developers rarely change name of various file type and folder name, especially is documents and configs folders. Attackers usually take advantage of those default name paths in order to design vulnerability dorking to search web applications which do not configs well enough to hide those sensitive endpoints.

![](capture/Pasted%20image%2020240724105739.png)
##### 3.3.1.5 Server's Config and Documents

- Web application configuration refers to the process of setting up and managing the settings and parameters that control the behavior, security, and functionality of a web application. This includes configuring server settings, database connections, environment variables, application settings. 
- In other words, a server's config can be the server's setting or instructions for initializing the server or even the server's secret key. If web crawlers provide the pentesters overview of the web's structure, the config file may contain information about services of the applications application, such as subdomain, virtual host, folder permissions, communication protocol between the application's services and cryptography secret key.

![](capture/Pasted%20image%2020240729144303.png)

- Documents may stand for images and texts, but on the pentesters usually focus on types of internal document which bring back rich information such as salary sheets or employee's sheets and documents which are created on a web server. Here is an example of using Google Dorking to search public salary sheets of government companies in Vietnam.

![](capture/Pasted%20image%2020240720161531.png)

-  Visible data from those documents can be an employee's email, real name, real name or various kinds of sensitive data. Indeed, attackers regularly demonstrate invisible data inside those files - metadata. Metadata is information that is stored within a file and used to provide context or descriptions about that file. So, metadata of files which are created on a web server is very valuable because it contains critical important information such as opera system information, file's creator software version, username of author, embed email and file path. Each gathered information above opens an attack arrow to the web server system: the attacker can search for CVE based on a version of an opera system or software, phishing email attack and reveal the web structure on file path.
- Metagoofil is a tool for extracting metadata of public documents (PDF, doc,XLS, ppt,etc.) available on the target websites. This information could be useful because you can get valid usernames, people's names, for using later in bruteforce password attacks (vpn, ftp, webapps), the tool will also extract interesting "paths" of the documents, where we can get shared resources names, server names, etc. The tool first performs a query in Google requesting different filetypes that can have useful metadata (PDF, doc, XLS, ppt,etc.), then will download those documents to the disk and extracts the metadata of the file using specific libraries for parsing different file types (Hachoir, Pdfminer, etc.)
##### 3.3.1.6 DNS, WHOIS Databases and Domain Information.

- nslookup (stands for “Name Server Lookup”) is a useful command for getting information from the DNS server. It is a network administration tool for querying the Domain Name System (DNS) to obtain domain name or IP address mapping or any other specific DNS record. Here is a general workflow of DNS record query, this flow is applied for both command and internet browser [2].

![](capture/Pasted%20image%2020240804095515.png)

- First, nslookup requires a web domain to initialize the work flow, then check that domain if it exists in the local cache, OS cache and router cache. 
- The local cache, also known as the browser cache, is maintained by web browsers (regular in browser://net-internals/#dns and browser stands for what browser user is using). When a user visits a website, the browser stores the DNS resolution results temporarily. 
- The OS cache, or system cache, is maintained by the operating system and is used to store DNS query results system-wide. When an application needs to resolve a domain name, the OS checks its cache. If a recent entry is found, it uses the cached IP address. This reduces the number of queries sent to the DNS resolver and speeds up network requests.
- The router cache is maintained by the router or network gateway device that connects a local network to the internet. When a device on the network makes a DNS query, the router checks its cache. If a recent entry is found, it responds with the cached IP address.
- After checking the user's device cache, the command checks host file (/etc/hosts for Linux distro), which is a static text file used by the operating system to map host-names to IP addresses. Users possibly to change content of this file in order to map domain with IP may not resolve in public DNS.
- After cache checking, client requests the DNS resolver (or recursive DNS resolver) provided by the ISP (Internet Service Provider) or a third-party service like Google Public DNS or Cloudflare. It is responsible for communicating with several other DNS servers to hunt down an IP address. This is reducing software burden on client sites by avoiding an iterative DNS query, where the client communicates directly with each DNS server involved in the lookup.
- Because DNS resolvers are provided by different organizations, they are basically different systems, so they can have their own policy and cache. So, the DNS resolver's cache is also looked up for domain information. Then, the resolver query to DNS servers in order queries are root DNS server, Top Level DNS server and Authoritative DNS server to collect the IP address of the provided domain.
- When there is a request to complete a domain name into an IP address, the client will send the request to the nearest DNS resolver. The resolver server queries a DNS root server, which is the top level in the DNS hierarchy. When the root server receives a query for the IP address for google.com Google, for example, the root server is not going to know what the IP address is.  The DNS root server manages all top level domains so the root server will direct the resolver to the TLD or top-level domain server for the **.com** domain. So the resolver will now ask the TLD server for an IP address for the domain base on instruction in response's root DNS server.
- The top-level domain server stores address information for top-level domains such as **.com**, **.net**, **.org** and so on. TLD servers store numbers DNS records, which specify the authoritative DNS servers for each level domain under the TLD. This particular TLD server manages **.com** domain which google.com is a part of. So when a TLD server receives query for IP address for google.com, TLD server is not going to know what IP addresses for google.com but they store information about the authoritative DNS servers that are responsible for providing the IP addresses for these domain names. So the TLD will direct resolver to  authoritative name servers. So once again the resolver will now ask authoritative name server for IP address for google.com. Authoritative name server or servers are responsible for knowing everything about domain which includes IP address.
- Authoritative DNS is the system that keeps official records corresponding to domain names such as IP addresses. Domain names are the human-readable names of IP addresses that direct applications such as browsers to websites such as google.com.
- The authoritative server responds with DNS record that includes the IP address and the DNS resolver server caches the IP address and sends it to the browser. So now the client or browser get the domain's IP address

- WHOIS is a public database that store the information collected when someone registers a domain name or updates their DNS settings. Every domain name that’s been registered belongs to someone, and by default, that registration information is public. WHOIS is a way of storing that information and making it available for the public to search.The information collected during the domain registration process includes your: Name, Address, Phone Number, Email Address. In draw back, it doesn’t display all of the registration information for every domain name, like **.com** and **.net** can be store more data than those domain. There are some domain doesn't require policy so its always be displayed.

![](Capture/Pasted%20image%2020240730104615.png)

- Users have to request to query WHOIS data domain's information by WHOIS protocol. When a user want to public a web application or a web service out to the internet, they first need to create a new domain with creator information then update to WHOIS, then that user is able to use that new domain to register DNS record for the web application.

- Whoisology is a web-based service that offers comprehensive WHOIS data and tools for exploring and analyzing domain registration information.
	- Whoisology collects WHOIS data from a wide range of domain registries.
	- The collected data from various` WHOIS database` is organized into a searchable database. This database allows users to query and analyze domain information efficiently.
		
		![](capture/Pasted%20image%2020240606172441.png)
	
	- Users can search the database by domain name, registrant name, email address, organization, or other WHOIS fields. Whoisology provides advanced search capabilities to filter and refine search results.
	- Links related WHOIS records based on common attributes such as registrant names, email addresses, and IP addresses. This helps users uncover relationships between different domains and identify patterns.
	- Maintains historical WHOIS records, allowing users to see changes in domain registration information over time. This is useful for tracking the history of a domain or identifying trends.
	- Below is Raw data reponse from `Whoisology` with input domain is `whoisology.com`
	

- `ViewDNS`: is an online service that provides a variety of tools for examining domain name and IP address information. It helps users gather information about domains, IP addresses, and related records. Here are some of the key services provided by ViewDNS:
	
	- `DNS Record Lookup`: Allows you to retrieve `DNS records` (such as: `A` - holds the IP address of a domain, `MX` - Directs mail to an email server, `NS` - Stores the name server for a DNS entry, `TXT` - Lets an admin store text notes in the record. These records are often used for email security) for a given domain name.
		- `DNS records` (aka zone files) provide information about a domain including what `IP address` is associated with that domain and how to handle requests for that domain. These records consist of a series of text files written in what is known as `DNS syntax`. 
			![](capture/Pasted%20image%2020240608105859.png)
		- `DNS syntax` is just a string of characters used as commands that tell the DNS server what to do. All DNS records also have a `TTL`, which stands for time-to-live - indicates how often a DNS server will refresh that record.
		
		- 
		
		- Result of searching `kenh14.vn`
		![](capture/Pasted%20image%2020240601103211.png)
	
	- `Reverse Whois Lookup`: Find domain names owned by an individual person or company. Simply provide the email address or name of the person or company to find other domains registered using those same details.
		
		![](capture/Pasted%20image%2020240601103528.png)
	
	- `Reverse DNS Lookup`: Find the reverse DNS entry (PTR) for a given IP. This is generally the server or host name.. In this case, I am using domian `example.com`, this tool automate revert it to IP for input
		
		![](capture/Pasted%20image%2020240531173350.png)
	
	- `IP History`: Shows a historical list of IP addresses a given domain name has been hosted on as well as where that IP address is geographically located, and the owner of that IP address.
		
		![](capture/Pasted%20image%2020240601111110.png)

- `WhoisMind`: Allow lookup IP address details including location, owners, ISP (internet service provider), hostname, type, proxy, blacklist status and more. Find people information by IP. So I tried to search information which is extract by `Reverse DNS Lookup` with input domain of example.com. With input IP, this tool extract full range IP. 
	![](capture/Pasted%20image%2020240609144143.png)



- `FOCA`: `FOCA` is a network infrastructure mapping tool that can be used for `OSINT`. It can analyze metadata from various files, including doc, pdf and ppt files. FOCA can also enumerate users, folders, emails, software used, operating system, and other useful information.
	- *Document Search and Download*: `FOCA` searches for and downloads documents from the target domain.
		- `FOCA` starts by crawling the target website to collect documents such as PDFs, Word documents, Excel spreadsheets, and other file types.
	- *Metadata Extraction*: Extract metadata from the downloaded documents.
		- Metadata includes information such as the document's author, creation and modification dates, software used, and other embedded data.
		- It also looks for hidden data like comments, hidden text, and previous versions within the documents.
	- *Information Gathering*: 
		- `FOCA` can determine the software and operating systems used to create the documents, which can be valuable for identifying potential vulnerabilities.
		- FOCA can gather network-related information such as IP addresses, server names, and internal network paths that might be embedded in the documents.
	- *Information Analysis*: Analyze the extracted information to identify patterns and vulnerabilities.
		- `FOCA` correlates the extracted metadata to build a profile of the organization, identifying relationships between users, systems, and software.

- This next steps focuses on tools designed to extract specific types of data directly from the domain.

- `SpyOnWeb`: identifies domains with shared `Google Analytics` or `AdSense codes`, which is a specific function that cannot be performed by general search engines.
	- `Google Analytics`: Google Analytics is used to track website performance and collect visitor insights. It can help organizations determine top sources of user traffic, gauge the success of their marketing activities and campaigns.
		
		![](capture/Pasted%20image%2020240605110120.png)
	
	- `Google Analytics IDs`: a unique identifier for a web data stream (which is a website registered within Google Analytics). The format of a measurement ID in Google Analytics 4 is 'G-' followed by a combination of numbers and letters.
		
		![](capture/Pasted%20image%2020240605152056.png)
	
	- `AdSense` is a free-of-charge, simple way to earn money by displaying ads next to your online content.
	- `AdSense IDs`: User publisher ID is the unique identifier for your `AdSense` account. To protect the security of your account and make it easier for us to find account-specific details, user may be asked to provide this ID when user communicate with Google.
		
		![](capture/Pasted%20image%2020240605105905.png)

- `NerdyData`: discovering and analyzing data on the web. It focuses on searching through the source code of websites, allowing users to find specific pieces of code, technologies, and other web assets.
	- NerdyData is a free alternative to Wappalyzer, Whatruns, and BuiltWith.
	- Search all the web which are using the same template's input code
	- Allows users to search for websites using specific technologies, such as CMS platforms (e.g., WordPress, Drupal), e-commerce solutions (e.g., Shopify, Magento), JavaScript libraries (e.g., jQuery, React), and more.
	![](capture/Pasted%20image%2020240609164639.png)
#### 3.3.2 User Name
#### 3.3.3 Email Address
#### 3.3.4 Real Name
#### 3.3.5 Phone Number And Telephone
#### 3.3.6 Location

### 3.4. Active Reconnaissance

https://pentester.land/blog/compilation-of-recon-workflows/
- Recon flow 1:
![](capture/Pasted%20image%2020240607113115.png)

- Recon 2:
![](capture/Pasted%20image%2020240607113203.png)
#### 3.4.1 Verify Alive Target

- In order to continue, we need to verify that the domain is live by looking at the live website associated with the domain.
- Use command `ping` to target's domain: is a network utility used to test the reachability of a host on an IP network and to measure the round-trip time for messages sent from the originating host to a destination computer.
	
	![](capture/Pasted%20image%2020240605225837.png)

- `ping` command uses the Internet Control Message Protocol (ICMP) to send and receive messages. The package is sent from the source host to the target host over the network using IP.The ICMP Echo Reply packet mirrors the Echo Request, changing the ICMP type to 0 (Echo Reply) and keeping the identifier, sequence number, and payload data intact.
	
	![](capture/Pasted%20image%2020240605232009.png)


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

## 4. Implementation
- #### 4.1 Applying Reconnaissance Idea & Technology and Customizing Open-Source Reconnaissance For Automatic Purpose
- 
## 5. Result
- #### 5.1 Testing Customized Tools and Comparing Result With Using Specific Tools For Each Stage
- #### 5.2 Conclusion

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