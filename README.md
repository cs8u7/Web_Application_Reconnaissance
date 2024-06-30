# Web Application Reconnaissance Flow Analysis

Reporter: Tran Duc Tuan - B3 CS - BI12-467


## Table of Content
### 1. Executive Summary
### 2. Methodology 
#### 2.1 Research Web Domain Reconnaissance Stages
### 3. Implementation
#### 3.1 Applying Reconnaissance Idea & Technology in Automation 
### 3. Propose a new auto Recon tool
	- method
		- analyze: in & out
	- implement
		-  analyze: in & out
	- result
		- data 
		- analyze : %CVE CWE
		- category & vitalize

# Research and Report

## 1. Definition

- `Web Application Domain`: Input for Reconnaissance and Pentest Processing,a web application is an application program stored on a remote server and delivered over the internet through a browser interface.
	![](Pasted%20image%2020240528154451.png)
	
	- Structure of a Website:
	![](capture/Pasted%20image%2020240531102715.png)
	
	- Include: 
		- `Web Client`: is user's device, has role is render and display data received from server.
		- `Firewall`:A firewall is a network security device that monitors incoming and outgoing network traffic and decides whether to allow or block specific traffic based on a defined set of security rules.
		- Web Server:
			- On the hardware side, a web server is a computer that stores web server software and a website's component files. A web server connects to the Internet and supports physical data interchange with other devices connected to the web.
			- On the software side, a web server includes several parts that control how web users access hosted files. At a minimum, this is an _HTTP server_. An HTTP server is software that understands URL (web addresses) and HTTP. An HTTP server can be accessed through the domain names of the websites it stores, and it delivers the content of these hosted websites to the end user's device.
		- WebApp (Web Application): is application run on a corresponding web engine which is install inside web server, resolve incomming request from client, execute logic and response to client
		- Database: is a service play role store and provide data for resove logic process in web applications.
	

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

- Ip-base example:
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

- `Red teaming` is a structured process used to simulate an attack on an organization to identify vulnerabilities and improve security.
	1. Testing specific systems, processes, or overall security posture.
	2. Involves gathering information about the target organization to understand its structure, technology stack, and potential vulnerabilities.
	3. Using the information gathered during reconnaissance, the red team attempts to exploit vulnerabilities to gain initial access to the target environment.
	4. The red team seeks to establish a stable and persistent presence within the target environment.
	5. Escalate their privileges within the target environment to gain higher levels of access and control.
	6. Moving through the network to access other systems, data, and resources, expanding the red team’s control over the environment.
	7. Simulating the extraction of sensitive data from the target environment to test the effectiveness of data protection and monitoring mechanisms.
	8. Ensuring that no traces of the red team’s activities remain within the target environment, simulating what a real attacker might do to avoid detection.
	9. Documenting the findings, detailing the vulnerabilities discovered, and providing recommendations for remediation.
	10. Working with the target organization to address the identified vulnerabilities.
	![](capture/Pasted%20image%2020240602155807.png)

- `Reconnaissance`: the process of gathering information about a target system, network, or organization before attempting an attack or security assessment. The Reconnaissance process involves collecting extensive information about the potential targets, their vulnerabilities, and possible attack vectors. In this report, I would focus on web reconnaissance, demonstate on analyze workflows and clarify logic of mentioned tools in reconnaissance process
	
	![](capture/Pasted%20image%2020240528155015.png)
https://github.com/yogeshojha/rengine
- `Penestration Testing`:  or pentesting, is the process of actively evaluating the security of a target system, network, or organization by simulating an attack. This process involves identifying vulnerabilities, exploiting them to determine their impact, and providing actionable recommendations to mitigate the discovered weaknesses. Pentesting typically includes a comprehensive examination of various aspects of the target environment, such as network infrastructure, web applications, and internal systems. In this report, I will focus on web application pentesting, demonstrate detailed methodologies for identifying and exploiting vulnerabilities, and clarify the logical workflows and tools used in the pentesting process.

## 2. Research Web Pentest Processing
### 2.1 Passive Reconnaissance
- Passive reconnaissance involves gathering information without directly interacting with the target. This helps in remaining undetected

#### 2.1.1 Open Source Intelligence (OSINT)
##### 2.1.1.1 OSINT Definition and Work Flow

- `OSINT` is an abbreviation of Open Source Intelligence, it is any information can legaling garthering form the internet. Belows is an explaination of a `OSINT` work flow apply for `Web Domain`.

![](capture/Pasted%20image%2020240530094142.png)

- Intialtion of this `OSINT` work flow, is a web domain as an input for the process.

- In order to continue, we need to verfify that the domain is live by looking at the live website associated with the domain.
	- Use command `ping` to target's domain: is a network utility used to test the reachability of a host on an IP network and to measure the round-trip time for messages sent from the originating host to a destination computer.
		
		![](capture/Pasted%20image%2020240605225837.png)
		
		- `ping` command uses the Internet Control Message Protocol (ICMP) to send and receive messages. The package is sent from the source host to the target host over the network using IP.The ICMP Echo Reply packet mirrors the Echo Request, changing the ICMP type to 0 (Echo Reply) and keeping the identifier, sequence number, and payload data intact.
			
			![](capture/Pasted%20image%2020240605232009.png)
	
	- Access the domain in browser, there are some possibilities can occur:
		- Error 404: DNS record for the domain is delete
		- Taken by another Entity 
		- Redirect request from web server turn user to lastest version

- Using `search engines (Google, Bing, Yandex)` to find cached versions of the website and other related information.
	- In Google, you can use the search query `cache:example.com` to find cached pages of a website. Alternatively, you can search for `site:example.com` and click on the down arrow next to the URL in the search results, then select "Cached" to view the cached version of the page 
	- The `cache:` operator is only available on web search.
	- The `cache:` operator is a search operator that you can use to find the cached version of a page. Google generates a cached version so that users can still access the web page, for example, if the site isn't available.

- Using `Wayback Machine` to searching older version of the website, may be include critical deleted information or ability of unfix vulnerability.
	![](capture/Pasted%20image%2020240530102505.png)
	
	- Wayback Machine automatically crawls and captures snapshots of webpages at various points in time. These snapshots are then stored, attached to timestamps and made accessible to users.

- `Spiderbot, Crawler`: is an automated program that systematically browses the web to index and retrieve information from websites.
	- Googlebot starts with a list of known URLs, including frequently updated sites.
	- The crawler sends requests to these URLs, downloads the HTML content, and parses it to extract links.
	- Extract useful information and discover new links. The crawler identifies hyperlinks (`<a>` tags), scripts, images, and other resources linked from the page.
	- The extracted URLs are filtered to remove duplicates, irrelevant links, or links that point to already visited pages.
	- URLs are prioritized based on Google's algorithms, considering factors like page importance and update frequency.
	- Googlebot schedules visits to avoid server overload, respecting the `robots.txt` directives.
	- The content is indexed, and metadata is stored for efficient retrieval and ranking.
	- Periodically, Googlebot revisits pages to detect changes and update the index accordingly.
	- Googlebot manages errors and dynamic content effectively, ensuring comprehensive coverage of the web.
	![](capture/Pasted%20image%2020240603153739.png)

- Verifying `Googlebot` and other Google crawlers. You can verify if a web crawler accessing your server really is a `Google crawler`, such as `Googlebot`. This is useful if you're concerned that spammers or other troublemakers are accessing your site while claiming to be `Googlebot`. There are two methods for verifying Google's crawlers:
	- *Manually*: For one-off lookups, use command line tools. This method is sufficient for most use cases.
	- *Automatically*: For large scale lookups, use an automatic solution to match a crawler's IP address against the list of published Googlebot IP addresses.

- Use command line tools
	- Run a reverse DNS lookup on the accessing IP address from your logs, using the `host` command.
	- Verify that the domain name is either `googlebot.com`, `google.com`, or `googleusercontent.com`.
	- Run a forward DNS lookup on the domain name retrieved in step 1 using the `host` command on the retrieved domain name.
	- Verify that it's the same as the original accessing IP address from your logs.
	![](capture/Pasted%20image%2020240606115718.png)

- `Google's crawlers` fall into three categories:

| Type                    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Reverse DNS mask                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Googlebot               | The main crawler for Google's search products. Always respects robots.txt rules.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `crawl-***-***-***-***.googlebot.com` or `geo-crawl-***-***-***-***.geo.googlebot.com`   |
| Special-case crawlers   | Crawlers that perform specific functions (such as AdsBot), which may or may not respect robots.txt rules.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | rate-limited-proxy-`***-***`-`***-***`.google.com                                        |
| User-Triggered fetchers | Tools and product functions where the end user triggers a fetch. For example, [Google Site Verifier](https://support.google.com/webmasters/answer/9008080) acts on the request of a user. Because the fetch was requested by a user, these fetchers ignore robots.txt rules.  <br>Fetchers controlled by Google originate from IPs in the `user-triggered-fetchers-google.json` object and resolve to a `google.com` hostname. IPs in the `user-triggered-fetchers.json` object resolve to `gae.googleusercontent.com` hostnames. These IPs are used, for example, if a site running on Google Cloud (GCP) has a feature that requires fetching external RSS feeds on the request of the user of that site. | `***-***-***-***.gae.googleusercontent.com` or `google-proxy-***-***-***-***.google.com` |


| Type     | Googlebot                                                                                  | Special-case crawlers                                                                                    | User-Triggered fetchers                                                                                                                                                                                                                                         |
| -------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ip Range | [googlebot.json](https://developers.google.com/static/search/apis/ipranges/googlebot.json) | [special-crawlers.json](https://developers.google.com/static/search/apis/ipranges/special-crawlers.json) | [user-triggered-fetchers.json](https://developers.google.com/static/search/apis/ipranges/user-triggered-fetchers.json) and [user-triggered-fetchers-google.json](https://developers.google.com/static/search/apis/ipranges/user-triggered-fetchers-google.json) |

- Using `Google Docking`: involves using basic search operators to find information that is publicly accessible but might not be immediately obvious. It's often used to find specific files, information, or directories on a website. The general structure of a search operator includes the *operator keyword* followed by a *colon* and the *target term*, without any spaces between the keyword and the colon.
	- `site`: Limits the search to a specific domain or site (`site:example.com`). 
	- `intitle`: Finds pages with the specified keyword in the title ().
	- `inurl`: Searches for pages with the specified keyword in the URL (`inurl:login`).
	- `filetype`: Finds files of a specific type (`filetype:pdf`).
	- `intext`: Searches for pages containing the specified keyword in the text (`intext:"confidential"`).
	- *Basic Usage*: Using single operator.
		 ![](capture/Pasted%20image%2020240530113115.png)
	
	- *Advanced Techniques:* Combining multiple operators, using more complex queries, and employing additional tools and techniques. It is often used in a more targeted manner to identify vulnerabilities, sensitive information, and potential security risks.
		- *Combining Multiple Operators*: Creating complex queries to narrow down search results.
		    - Example: `site:example.com intitle:"index of" inurl:backup filetype:zip`
		- *Exploiting Error Messages*: Searching for specific error messages that might indicate vulnerabilities.
		    - Example: `site:example.com intext:"SQL syntax error"`
		- *Identifying Sensitive Endpoints*: Finding URLs or endpoints that might expose sensitive data.
		    - Example: `site:example.com inurl:/api/`, `site:example.com ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup

- Using `IntelTechniques.com`: Beside providing knowledge and course about `OSINT`, this website equip a tremendous amout of searching template (Google Docking). All the templates are categoried base on search engine and social media. User is redicrect to search endpoint with correspoding search template.
	![](capture/Pasted%20image%2020240531093930.png)

- `Whois`: is a public database that houses the information collected when someone registers a domain name or updates their `DNS` settings. Every domain name that’s been registered belongs to someone, and by default, that registration information is public. `WHOIS` is a way of storing that information and making it available for the public to search.The information collected during the domain registration process includes your: *Name*, *Address*, *Phone Number*, *Email Address*. In draw back, it doesn’t display all of the registration information for every domain name, like `.com` and `.net` can be store more data than `.me` and `.gov`. There are some domain doesn't require policy so its always be displayed.

- `Whoisology`: is a web-based service that offers comprehensive WHOIS data and tools for exploring and analyzing domain registration information.
	- Whoisology collects WHOIS data from a wide range of domain registries.
	- The collected data from various` WHOIS database` is organized into a searchable database. This database allows users to query and analyze domain information efficiently.
		
		![](capture/Pasted%20image%2020240606172441.png)
	
	- Users can search the database by domain name, registrant name, email address, organization, or other WHOIS fields. Whoisology provides advanced search capabilities to filter and refine search results.
	- Links related WHOIS records based on common attributes such as registrant names, email addresses, and IP addresses. This helps users uncover relationships between different domains and identify patterns.
	- Maintains historical WHOIS records, allowing users to see changes in domain registration information over time. This is useful for tracking the history of a domain or identifying trends.
	- Below is Raw data reponse from `Whoisology` with input domain is `whoisology.com`
	![](capture/Pasted%20image%2020240531152255.png)

- `ViewDNS`: is an online service that provides a variety of tools for examining domain name and IP address information. It helps users gather information about domains, IP addresses, and related records. Here are some of the key services provided by ViewDNS:
	
	- `DNS Record Lookup`: Allows you to retrieve `DNS records` (such as: `A` - holds the IP address of a domain, `MX` - Directs mail to an email server, `NS` - Stores the name server for a DNS entry, `TXT` - Lets an admin store text notes in the record. These records are often used for email security) for a given domain name.
		- `DNS records` (aka zone files) provide information about a domain including what `IP address` is associated with that domain and how to handle requests for that domain. These records consist of a series of text files written in what is known as `DNS syntax`. 
			![](capture/Pasted%20image%2020240608105859.png)
		- `DNS syntax` is just a string of characters used as commands that tell the DNS server what to do. All DNS records also have a `TTL`, which stands for time-to-live - indicates how often a DNS server will refresh that record.
		
		- Domain Name System (DNS)
		![](capture/Pasted%20image%2020240608160245.png)
		
		- User enters `www.example.com` into the browser.
		- Browser checks its cache, then the OS cache.
		- No cached record is found; the request goes to the recursive DNS server.
			- A `recursive DNS` lookup is where one DNS server communicates with several other `DNS servers` to hunt down an `IP address` and return it to the client. This is in contrast to an iterative `DNS query`, where the client communicates directly with each `DNS server` involved in the lookup.
		- The recursive server queries a root server (just a dot `.`), which refers it to the `.com` TLD servers.
			- `DNS root Server` is a root domain name resolution service. The reason it has such a name is because all domain names in the world must pass it. There are about 13 DNS root servers in the world.
			- `DNS root server` manages all Top level domains. These domain names can be mentioned as:`.com`,`.org`,`.vn`,`.net`,... When there is a request to resolve a Domain Name into an Ip address, the client will send the request to the nearest `DNS`. (`DNS ISP`). `DNS ISP` will connect to `DNS` root Server to ask for the address of a Domain Name. `DNS` root Server will base on the `Top Levels of a Domain Name` from which to provide appropriate instructions to redirect the client to the correct address it needs to query.
		- The `.com` TLD servers refer the recursive server to the `authoritative DNS` server for `example.com`.
			- Authoritative DNS is the system that keeps official records corresponding to domain names such as IP addresses. Domain names are the human-readable names of IP addresses that direct applications such as browsers to websites such as `www.example.com`.
		- The authoritative server responds with an A record that includes the IP address (e.g., `93.184.216.34`).
		- The recursive server caches the IP address and sends it to the browser.
		- The browser connects to the server at `93.184.216.34` and loads the website.
		
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

- `DNSTrails`: is a Internet service that provides you with the tools to find any domain someone owns among other things. `DNSTrails` allows users to view the history of DNS records for a domain. This includes changes to A records, MX records, NS records, and more. - This tool is dead.

- `Backlinks`: also known as inbound links or incoming links, are links from one website to a page on another website. It is an external links place in others sites which are point to your website. Numbers of backlinks affect to site's rank for SEO (search engine optimization).
    - When `Googlebot` encounters a hyperlink on a webpage, it adds that link to its list of pages to crawl next. This process helps Googlebot discover new pages and the relationships between pages through backlinks. Once Googlebot crawls a page, it processes the content and stores it in Google’s index, a massive database of web pages.
	![](capture/Pasted%20image%2020240601231048.png)

- `SharedCount`: SharedCount is a tool used to track how many times a specific URL has been shared across various social media platforms. It provides insights into the popularity and reach of a webpage by showing the total number of shares, likes, comments, and other social interactions from platforms like Facebook, Twitter, Pinterest, LinkedIn, and more.
	![](capture/Pasted%20image%2020240601232025.png)

- `Robots.txt`: is a file which is place at document root of Web application, provides directives to web crawlers about which pages or sections of a site should not be crawled or indexed.

```PHP
User-agent: *
Disallow: /admin/  # Access to the admin section is restricted.
Disallow: /private/ # Access to the admin section is restricted.
Disallow: /tmp/ # Access to the admin section is restricted.
```

- `Sitemap.xml`: is a file contains a list of URLs on a website, along with metadata about each URL
	- Typically found at `https://example.com/sitemap.xml`. Some sites might have multiple sitemaps, or an index sitemap linking to multiple sub-sitemaps.
	- Analyze the `sitemap.xml` file to find all publicly accessible pages. This is useful for uncovering hidden or less obvious sections of a website.

```XML
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2024-05-01</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  # https://example.com/: Last modified on 2024-05-01, changes daily, highest priority.
  <url>
    <loc>https://example.com/about</loc>
    <lastmod>2024-04-15</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  # https://example.com/about: Last modified on 2024-04-15, changes monthly, medium priority.
  <url>
    <loc>https://example.com/blog</loc>
    <lastmod>2024-05-20</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
	# https://example.com/blog: Last modified on 2024-05-20, changes weekly, high priority.
  </url>
  <url>
    <loc>https://example.com/contact</loc>
    <lastmod>2024-03-30</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.5</priority>
  </url>
  # https://example.com/contact: Last modified on 2024-03-30, changes yearly, low priority.
</urlset>

```

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

- `DomainCrawler`: automates the process of gathering, analyzing, and presenting information about domains on the internet, providing valuable insights for businesses, researchers, and cybersecurity professionals.
	![](capture/Pasted%20image%2020240609162732.png)

- `NerdyData`: discovering and analyzing data on the web. It focuses on searching through the source code of websites, allowing users to find specific pieces of code, technologies, and other web assets.
	- NerdyData is a free alternative to Wappalyzer, Whatruns, and BuiltWith.
	- Search all the web which are using the same template's input code
	- Allows users to search for websites using specific technologies, such as CMS platforms (e.g., WordPress, Drupal), e-commerce solutions (e.g., Shopify, Magento), JavaScript libraries (e.g., jQuery, React), and more.
	![](capture/Pasted%20image%2020240609164639.png)

- `PubDB`: PubDB, which stands for Public Database, is a platform designed to collect, organize, and provide access to publicly available information about companies, websites, technologies, and various other entities.
	![](capture/Pasted%20image%2020240609164346.png)

- `Metagoofil`: This is a free and open-source tool designed to extract all the metadata information from public documents that are available on websites. This tool uses two libraries to extract data. These are Hachoir and PdfMiner. After extracting all the data, this tool will generate a report which contains usernames, software versions, and servers or machine names that will help Penetration testers in the information-gathering phase. This tool can also extract MAC addresses from Microsoft office documents. This tool can give information about the hardware of the system by which they generated the report of the tool.
	![](capture/Pasted%20image%2020240609164505.png)

- `Small SEO tools`: Small SEO Tools is a suite of free online tools designed to assist with various aspects of search engine optimization (SEO). These tools are used to enhance website visibility, monitor performance, and improve overall SEO strategy.
	- `Plagiarism Checker`: Detects duplicate content across the web.
	- `Article Rewriter`: Helps to rewrite articles to make them unique.
	- `Backlink Checker`: Analyzes backlinks to your website.
	- `Keyword Position Checker`: Monitors the position of specific keywords in search engine results.
##### 2.1.1.2 Preventing Missing Important Information

- In order to not missing important information, we should fllow those steps

- Define and Focus on objective and scope
	- Define objective to collect data around or relate to it
	- Notice to the level of detail required

- Double check if **domain is expired**: `WHOIS` is a public database that stores information about domain names, including their expiration dates and is not affected by the deletion of DNS records. In case, an service's web is no longer in use, the lazy dev just delete the dns record but do not stop the web service. user can still access the service if they know the ip.

- Use a Variety of Sources
	- Diverse sources provide a broader view and reduce the risk of missing critical information. 
		- *News Media*: Newspapers, magazines, and online news platforms.
		- *Social Media*: Twitter, Facebook (Cyber Space), LinkedIn, and other social networks.
		- *Government Websites*: Official documents, reports, and update releases.
		- *Academic Publications*: Journals, papers, and reports.
		- *Forums and Blogs*: Suitable communities and expert blogs.
		- *Specialized Databases*: Industry-specific databases and archives.

- Advanced Search Techniques
	- *Boolean Operators*: Use AND, OR, NOT to combine or exclude keywords.
	- *Exact Phrases*: Use quotation marks `""` to search for exact phrases.
	- *Site Search*: Use `site:example.com` to search within a specific domain.
	- *File Type*: Use `filetype:pdf` or other extensions to find specific document types.
	- *Time Range*: Use tools to filter results by date range to find the most recent information.

- Automate Data Collection
	- *Web Scrapers*: Tools like `BeautifulSoup`, `Scrapy`, or `Selenium` for extracting data from websites. Extract data in title tag.
	- *APIs*: Utilize APIs from platforms like Twitter, Google, or news services. Return data usually in Json format. Large-scale, and structured data collection tasks.
		- Google APIs is a google service can signup with google cloud, then achive api_key and cse_id for automate actions
	- *Custom Search Engines*: Create a Google Custom Search Engine (CSE) tailored to your specific needs. While using default google search query just quick and only find some match result.

 - Verify and Cross-Reference Information
	- *Cross-Verification*: Check the same information across different reputable sources.
	- **Fact-Checking:** Use dedicated fact-checking websites to validate controversial or suspect claims.
	- **Original Sources:** Whenever possible, trace information back to its original source.

- Use Specialized OSINT Tools
	- *Maltego*: For link analysis and data mining.
		- Visualizing relationships between various entities such as people, companies, websites, domains, and IP addresses through detailed graphs.
		- Investigating cyber threats, mapping social networks, analyzing criminal activity, and researching corporate structures.
	- *Shodan*: For information on internet-connected devices (FOFA).
		- Indexes information about devices connected to the internet.
		- Searching vulnerability assessments, and IoT device inventory.
	- *TheHarvester*: For gathering emails, subdomains, and more.
		- Collect information related to domains, such as email addresses, subdomains, IP addresses, and employee names.
		- Gathering information for social engineering attacks, and creating contact lists.
	- *Recon-ng*: A web reconnaissance framework.
		- Includes numerous modules that can be used to perform various tasks such as domain reconnaissance, email harvesting, and vulnerability analysis.
		- Gathering information for red teaming exercises.

- Stay Updated on OSINT Techniques
	- *Training and Courses*: Participate in OSINT training programs and courses.
	- *Communities and Forums*: Join OSINT communities and forums to exchange knowledge.
	- *Publications and Blogs*: Follow OSINT blogs and publications for the latest updates.

#### 2.1.3 Website Analysis

- `HTML Source Code`: Inspect the website’s HTML source code for comments, hidden fields, and other clues.

### 2.2 Active Reconnaissance

Active reconnaissance involves interacting with the target system to gather information. This can be more detectable but often yields more detailed information.

https://pentester.land/blog/compilation-of-recon-workflows/
- Recon flow 1:
![](capture/Pasted%20image%2020240607113115.png)

- Recon 2:
![](capture/Pasted%20image%2020240607113203.png)
#### 2.2.1 DNS Enumeration

- `Subdomain Enumeration`: Identify subdomains using `Amass enum` in both active mode and passive mode
- 

#### 2.2.2 Network Scanning

- `Port Scanning`: Use tools like Nmap to identify open ports and running services on the target.
    - Example: `nmap -sS -sV example.com`
- `Service Fingerprinting`: Determine the versions of the services running on the open ports.

#### 2.2.3 Web Application Analysis

- `Content Discovery`: Use tools like `DirBuster`, `Gobuster`, or `Burp Suite` (Intruder) to find hidden directories and files.
- `Web Server Information`: Identify the web server and its version (`Apache`, `Nginx`, `IIS`, etc.) with tools like [`Wappalyzer`](https://github.com/tunetheweb/wappalyzer)
- `Application Frameworks`: Detect the frameworks and technologies used by the application (`PHP`, `ASP.NET`, `Django`, ...).

#### 2.2.4. Spidering and Crawling

- `Web Crawlers`: Use tools like `Burp Suite`, `OWASP ZAP`, or custom scripts to crawl the website and map its structure.
- `Identify Input Fields`: Locate all forms and input fields for potential injection points. Scan params with `arjun`. 

### 2.3 Vulnerability Identification

- `Automated Scanners`: Use tools like `Nuclei`, `Acunetix`, `Nessus`, `OpenVAS`, or `Burp Suite's scanner` to identify known vulnerabilities.
	- https://blog.projectdiscovery.io/secret-token-scanning-with-nuclei/
- `Manual Testing`: Manually test for common web vulnerabilities such as SQL injection (`sqlmap`), XSS (`fuzzing`), LFI (`lfimap`), and others.

## 3. Applying Acunetix in Automatic Pentesting
### 3.1 Acunetrix introduction and usage

https://viblo.asia/p/gioi-thieu-cong-cu-do-quet-lo-hong-acunetix-ORNZqjDbl0n
### 3.2 Practice with Acunetix

## 4. Propose a new auto Recon & Scan Vuln tool or Burp extension
### 4.1 Tool's design and logic
https://github.com/yogeshojha/rengine
### 4.2 Comparing to Current Acunetrix 