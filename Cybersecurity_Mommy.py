import os
import openai
import platform
import subprocess
import distro
import requests
import threading
import time
import random
import socket
import requests
import xml.etree.ElementTree as ET
from newspaper import Article
import getpass
import os
import base64
import json
import getpass
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding



from googleapiclient.discovery import build

# Set your OpenAI API key here
openai.api_key = ""


#History file is where the conversation history is stored, however I noticed she doesnt remember after restarting the program
history_file = "conversation_history.txt"

# Sample conversations file is where you can add sample conversations to help the AI learn
sample_conversations_file = "sample_conversations.txt"

# Guidelines file is where you can add guidelines to help the AI learn
guidelines_file = "guidelines.txt"

#Cybersecurity feed ftw
def cybersecurity_feed():
    feed_urls = [
        'https://krebsonsecurity.com/feed/',
        'https://www.schneier.com/blog/atom.xml',
        'https://feeds.feedburner.com/TheHackersNews',
        'http://www.darkreading.com/rss_simple.asp',
        'https://nakedsecurity.sophos.com/feed/',
        'https://www.csoonline.com/index.rss',
        'https://threatpost.com/feed/',
        'https://www.bleepingcomputer.com/feed/',
        'https://feeds.feedburner.com/Securityweek',
        'https://www.zdnet.com/blog/security/rss.xml',
        'https://www.technologyreview.com/feed/',
        'https://venturebeat.com/feed/',
        'https://rss.nytimes.com/services/xml/rss/nyt/AI.xml'
    ]

    def get_cybersecurity_feed(feed_url):
        response = requests.get(feed_url)
        if response.status_code == 200:
            return response.text
        else:
            return None

    def parse_feed(feed_data, start_index):
        try:
            root = ET.fromstring(feed_data)
            items = root.findall('.//item')
            if not items:
                items = root.findall('.//entry')

            if start_index >= len(items):
                print("No more articles available.")
                return

            for item in items[start_index:start_index+10]:
                title = item.find('title').text
                link = item.find('link').text or item.find('link').attrib['href']
                pub_date = item.find('pubDate') or item.find('updated')
                if pub_date is not None:
                    pub_date = pub_date.text
                summary = extract_summary(link)
                print(f'Title: {title}\nLink: {link}\nDate: {pub_date}\nSummary: {summary}\n')
        except Exception as e:
            print(f'Failed to parse feed: {e}')

    def extract_summary(url):
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            return article.summary
        except Exception as e:
            print(f'Failed to extract summary: {e}')
            return None

    def fetch_more_articles(start_index=0):
        for feed_url in feed_urls:
            print(f'Feed: {feed_url}')
            feed_data = get_cybersecurity_feed(feed_url)
            if feed_data:
                parse_feed(feed_data, start_index)
            else:
                print('Failed to fetch the feed.')
            print('-' * 80)

    start_index = 0
    fetch_more_articles(start_index)
    while True:
        more_articles = input("Do you want to fetch more unique articles? Press 'y' to continue or any other key to exit: ")
        if more_articles.lower() == 'y':
            start_index += 10
            fetch_more_articles(start_index)
        else:
            break


def load_text_file(file_name):
    try:
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                content = f.read()
            print(f"{file_name} loaded successfully.")
        else:
            content = ""
            with open(file_name, 'w') as f:
                f.write(content)
            print(f"{file_name} not found. A new file has been created.")
    except IOError as e:
        print(f"Error loading {file_name}: {e}")
        content = ""
    return content

def generate_response(prompt, history):
    model_engine = "text-davinci-002"
    
    sample_conversations = load_text_file(sample_conversations_file)
    guidelines = load_text_file(guidelines_file)
    
    prompt_with_history = f"{guidelines}{sample_conversations}{history}You: {prompt}\nMom: "
    
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt_with_history,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.8,
    )

    message = completions.choices[0].text.strip()
    return message

# Because we all know things can happen at work
def disaster_recovery_option():
    print("Ohhh noo! Mommy is so sorry to hear that! I will help you as much as I can!")
    print("1. Automated Recovery Steps")
    print("2. Disaster Recovery Plan Template")
    print("3. Business Impact Analysis (BIA) Tool")
    print("4. Risk Assessment Tool")
    print("5. Third-Party Support and Resources")
    print("6. Checklist for Regulatory Compliance")
    print("7. Post-Incident Review and Reporting")

    while True:
        choice = input("Please enter the number corresponding to your choice: ")
        if choice in ["1", "2", "3", "4", "5", "6", "7"]:
            return int(choice)
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


#Tools for Mommy's First Aid Kit (BLUE TEAM)
TOOLS = [
    ("ClamAV", "clamav", "A super cute antivirus friend that helps catch bad viruses, trojans, and other icky things."),
    ("Bleachbit", "bleachbit", "A powerful helper that cleans up your computer, making more space and keeping your secrets safe."),
    ("KeePassXC", "keepassxc", "A cozy little password manager to keep all your passwords safe and sound."),
    ("VeraCrypt", "veracrypt", "A secret-keeper that locks up your important data in encrypted treasure chests."),
    ("Wireshark", "wireshark", "A curious detective that watches and learns from your network traffic."),
    ("tcpdump", "tcpdump", "A sneaky sniffer that listens in on your network traffic for troubleshooting and analyzing."),
    ("Nmap", "nmap", "A friendly explorer that finds new friends, services, and hidey-holes on networks."),
    ("OSQuery", "osquery", "A magical translator that turns computer secrets into easy-to-understand tables."),
    ("UFW", "ufw", "A gentle but firm firewall friend that keeps your computer safe from unwanted visitors."),
    ("TestDisk", "testdisk", "A powerful rescuer that helps find lost partitions and fixes broken filesystems."),
    ("PhotoRec", "photorec", "A helpful helper that finds your lost pictures and other files."),
    ("Lynis", "lynis", "A watchful guardian that checks your computer's security and finds sneaky vulnerabilities."),
    ("YARA", "yara", "A clever pattern-matcher that helps sort and identify malware samples."),
    ("Autopsy", "autopsy", "A digital detective that digs through disk images to uncover important evidence."),
    ("Sleuth Kit", "sleuthkit", "A toolbox full of helpers for analyzing filesystems and finding deleted files."),
    ("Snort", "snort", "A sniffy snorter that alerts you to bad network traffic."),
    ("Suricata", "suricata", "A watchful protector that guards against network threats."),
    ("Bro/Zeek", "bro", "A big brother that keeps an eye on your network traffic for security and performance."),
    ("OSSEC", "ossec", "A careful watcher that looks for changes in files and logs."),
    ("Fail2ban", "fail2ban", "A tough bouncer that blocks bad IPs to protect your computer."),
    ("AIDE", "aide", "A loyal guard dog that watches your important files and barks if anything changes."),
    ("TShark", "tshark", "A fin-tastic command-line buddy for watching and learning from network traffic."),
    ("SSLyze", "sslyze", "A shiny analyzer that checks the safety of your SSL/TLS connections."),
    ("Cuckoo Sandbox", "cuckoo", "A safe playpen where you can watch suspicious files without getting hurt."),
]


#Tools for Daddy's Toolbox (RED TEAM)
DADDYS_TOOLS = [
    ("Metasploit", "metasploit-framework", "A super cool toolbox for creating and using sneaky exploits."),
    ("Nmap", "nmap", "A playful explorer that maps out networks and their hidden treasures."),
    ("Burp Suite", "burpsuite", "A bubbly buddy for testing the safety of web applications."),
    ("Wireshark", "wireshark", "A curious detective that watches and learns from your network traffic."),
    ("Aircrack-ng", "aircrack-ng", "A set of tools to play detective with wireless networks and crack their secret codes."),
    ("John the Ripper", "john", "A fast code-breaker that can crack secret passwords and help test their strength."),
    ("Hydra", "hydra", "A many-headed friend that helps crack online passwords on various protocols."),
    ("SQLmap", "sqlmap", "A smart mapper that finds secret doors in web applications and explores hidden databases."),
    ("Nikto", "nikto", "A friendly scanner that checks web servers for weak spots and outdated stuff."),
    ("Mimikatz", "mimikatz", "A sneaky kitty that can pull passwords, hashes, and tickets out of a computer's memory."),
    ("Empire", "powershell-empire", "A powerful kingdom of tools for controlling other computers using PowerShell and Python."),
    ("Cobalt Strike", "cobaltstrike", "A fancy toolkit for hackers that offers lots of cool tricks like phishing and command control."),
    ("Armitage", "armitage", "A colorful artist that helps you use Metasploit's powerful tools with a pretty interface."),
    ("Responder", "responder", "A sneaky trickster that plays pretend to capture information on local networks."),
    ("Hashcat", "hashcat", "A super-fast code-cracking kitty that can break password hashes in no time."),
    ("Gobuster", "gobuster", "A speedy explorer that searches for hidden directories and files on websites."),
    ("ZAP", "zap", "A zappy helper for finding security bugs in web applications and zapping them away."),
    ("The Harvester", "theharvester", "A friendly email collector that finds email addresses related to a domain."),
    ("OpenVAS", "openvas", "A friendly scanner that helps you find security vulnerabilities in your network."),
    ("Maltego", "maltego", "A friendly investigator that helps you find connections between people, companies, and domains."),
    ("Spiderfoot", "spiderfoot", "A friendly spider that helps you find connections between people, companies, and domains."),
    ("Sherlock", "sherlock", "A friendly detective that helps you find social media accounts associated with a username."),

]



#Mommy helps you install the tools you need
def install_package(package_name):
    if platform.system() == "Linux":
        distribution_id = distro.id().lower()
        if "debian" in distribution_id or "ubuntu" in distribution_id:
            subprocess.run(["sudo", "apt", "install", "-y", package_name], check=True)
        elif "arch" in distribution_id or "manjaro" in distribution_id:
            subprocess.run(["sudo", "pacman", "-S", "--noconfirm", package_name], check=True)
        else:
            print(f"Unsupported Linux distribution. Please install {package_name} manually.")
            return
    else:
        print("This script only supports Linux systems. Please install the packages manually.")
        return
    print(f"{package_name} installed successfully!")

def install_package2(package_name):
    if platform.system() == "Linux":
        distribution_id = distro.id().lower()
        if "debian" in distribution_id or "ubuntu" in distribution_id:
            subprocess.run(["sudo", "apt", "install", "-y", package_name], check=True)
        elif "arch" in distribution_id or "manjaro" in distribution_id:
            subprocess.run(["sudo", "pacman", "-S", "--noconfirm", package_name], check=True)
        else:
            print(f"Unsupported Linux distribution. Please install {package_name} manually.")
            return
    else:
        print("This script only supports Linux systems. Please install the packages manually.")
        return
    print(f"{package_name} installed successfully!")


# Option 1: Automated Recovery Steps
def automated_recovery_steps():
    print("Ok baby lets start from the begining ok? Remember to relax and breath everything is going to be ok:")
    steps = [
        "1. Isolate the affected systems to prevent the spread of the breach. Disconnect them from the network, disable Wi-Fi and Bluetooth connections, and shut down non-essential services.",
        "2. Inform the relevant stakeholders, including employees, customers, and partners. Notify them about the breach, its potential impact, and the actions being taken to address it.",
        "3. Gather and preserve evidence of the breach for further analysis. Collect logs, network traffic data, and any other relevant artifacts for forensic investigation.",
        "4. Identify the root cause of the breach and take steps to address it. Investigate how the breach occurred, whether it was due to a technical vulnerability or human error, and implement measures to fix the issue.",
        "5. Implement measures to prevent future breaches, such as stronger passwords, multi-factor authentication, and employee training. Update security policies, patch systems, and conduct regular security audits.",
        "6. Create and maintain a detailed incident response plan. Document the steps to be taken during and after a breach, assign roles and responsibilities, and establish communication channels.",
        "7. Conduct a thorough review of the incident and implement lessons learned. Analyze the effectiveness of the response, identify areas for improvement, and update the incident response plan accordingly.",
    ]
    for step in steps:
        print(step)
        input("Just push enter when you are ready to continue little one:")

# Option 2: Disaster Recovery Plan Template
def disaster_recovery_plan_template():
    print("Ok Pumpkin here is your template!:")
    steps = [
    "1. Introduction: Provide an overview of the disaster recovery plan, its purpose, and scope.",
    "2. Objectives and Scope: Define the specific goals and boundaries of the plan.",
    "3. Roles and Responsibilities: Assign tasks and responsibilities to team members during a disaster recovery event.",
    "4. Incident Response Procedures: Detail the steps to be taken during the initial response to a disaster, such as isolating systems, gathering evidence, and informing stakeholders.",
    "5. Backup and Recovery Procedures: Describe the methods for backing up and restoring data, applications, and systems, as well as the frequency and storage locations of backups.",
    "6. Testing and Maintenance: Establish a schedule for testing the plan and updating it as necessary, based on test results, changes in technology, and evolving business needs.",
    "7. External Contacts and Resources: List contact information for external parties, such as vendors, regulatory agencies, and law enforcement.",
    "8. Appendices (e.g., emergency contacts, sample forms): Include additional documents and resources that support the disaster recovery plan.",
    ]
    for step in steps:
        print(step)
        input("Just push enter when you are ready to continue little one:")

# Option 3: Business Impact Analysis (BIA) Tool
def bia_tool():
    print("Ok sweetheart here is your Business Impact Analysis tool!:")
    steps = [
    "1. Identify critical business functions and processes: List all the essential activities that support the organization's mission and objectives.",
    "2. Determine the maximum acceptable downtime for each function and process: Estimate the maximum period for which each activity can be disrupted before causing severe harm to the organization.",
    "3. Assess the financial and operational impact of disruptions: Calculate the potential losses and negative consequences that could result from a disruption of each critical function or process.",
    "4. Identify dependencies between functions and processes: Analyze the relationships between different activities to understand how a disruption in one area could impact others.",
    "5. Develop recovery priorities based on the analysis: Prioritize the recovery of critical functions and processes based on their maximum acceptable downtime and the potential impact of disruptions.",
    ]
    for step in steps:
        print(step)
        input("Just push enter when you are ready to continue little one:")

# Option 4: Risk Assessment Tool
def risk_assessment_tool():
    print("Ok my little baby! Here is your Risk Assessment Tool:")
    steps = [
    "1. Identify potential threats and vulnerabilities: List all possible risks, such as natural disasters, cyber attacks, and human error, that could impact your organization's critical functions and processes.",
    "2. Estimate the likelihood and impact of each threat: Assess the probability of each risk occurring and the potential consequences for your organization.",
    "3. Prioritize risks based on likelihood and impact: Rank the risks in order of their significance to the organization, taking into account both their probability and potential consequences.",
    "4. Develop risk mitigation strategies: Identify measures to reduce the likelihood and impact of each risk, such as implementing security controls, establishing backup and recovery procedures, and training employees.",
    "5. Monitor and review risks periodically: Regularly evaluate the organization's risk profile and update the risk assessment as needed to reflect changes in the threat landscape and the organization's operations.",
    ]
    for step in steps:
        print(step)
        input("Just push enter when you are ready to continue little one:")

# Option 5: Third-Party Support and Resources
def third_party_support_and_resources():
    print("You're such a good baby everything is going to be ok! Here are some resources to help you, ok honey?:")
    steps = [
    "1. Data breach response service providers: Companies specializing in assisting organizations with data breach response, such as forensic investigation and incident management.",
    "2. Cybersecurity consultants: Experts who can help evaluate and improve an organization's security posture, including vulnerability assessments and penetration testing.",
    "3. Legal counsel specializing in data breaches: Lawyers who can provide guidance on legal and regulatory requirements related to data breaches and help navigate potential legal issues.",
    "4. Public relations firms: Professionals who can assist with managing the organization's reputation and communicating with the public following a data breach.",
    "5. Insurance providers offering cyber insurance: Companies that provide coverage for losses resulting from data breaches and other cyber incidents.",
    ]
    for step in steps:
        print(step)
        input("Just push enter when you are ready to continue little one:")

# Option 6: Checklist for Regulatory Compliance
def regulatory_compliance_checklist():
    print("Take out your pencil little one! Heres your checklist for Regulatory Compliance...You're such a sweet baby!:")
    steps = [
    "1. Review data protection regulations relevant to your industry: Familiarize yourself with the legal and regulatory requirements governing data protection in your jurisdiction and sector.",
    "2. Develop a data breach notification plan: Establish procedures for informing affected individuals, regulators, and other relevant parties in the event of a data breach, in compliance with applicable laws.",
    "3. Train employees on regulatory requirements: Ensure that staff members understand their responsibilities under data protection laws and are equipped to comply with them.",
    "4. Ensure data breach response plan complies with regulations: Review and update the organization's incident response plan to ensure that it aligns with legal and regulatory requirements.",
    "5. Consult legal counsel for guidance on regulatory compliance: Engage a lawyer specializing in data protection to advise on compliance issues and help the organization navigate potential legal challenges.",
    ]
    for step in steps:
        print(step)
        input("Just push enter when you are ready to continue little one:")

# Option 7: Post-Incident Review and Reporting
def post_incident_review_and_reporting():
    print("Good job baby, here's your Post-Incident Review and Reporting make sure to let your boss know how much of a big girl or boy you are!:")
    steps = [
    "1. Analyze the data breach and its root cause: Conduct a thorough investigation of the incident, including the factors that contributed to the breach and the effectiveness of the response.",
    "2. Document the incident response process: Create a detailed record of the actions taken during and after the breach, including decisions made, resources used, and the outcomes achieved.",
    "3. Identify areas for improvement in the response plan: Analyze the incident response process to identify strengths and weaknesses, and develop recommendations for enhancing the plan.",
    "4. Implement changes to the response plan based on lessons learned: Update the incident response plan to incorporate the findings from the review, and ensure that it remains effective and relevant.",
    "5. Share findings with relevant stakeholders: Communicate the results of the post-incident review to management, employees, and other stakeholders, as appropriate, to promote learning and continuous improvement.",
    ]
    for step in steps:
        print(step)
        input("Just push enter when you are ready to continue little one:")

#Options for main menu
def display_options():
    print("\nPlease choose an option:")
    print("1. Talk to Mommy")
    print("2. Emergency Playtime (Disaster Recovery)")
    print("3. Mommy's First Aid Kit (Blue Team)")
    print("4. Daddys Toolbox (Red Team)")
    print("5. Search the web")
    print("6. Mommy please hold my hand to scan a network with nmap!")
    print("7. Mommy can I sit on your lap while we use TShark?")
    print("8. Mommy help I have a virus! (ClamAV)")
    print("9. Mommy I'm scared! Theres a meany bully on the internet! (Metasploit)")
    print("10. Mommy please tell me a bedtime story!")
    print("11. Mommy make me feel better!")
    print("12. Mommy's Toybox")
    print("13. Mommy can you please help me with OpenVAS?")
    print("14. Mommy whats the latest Cybersecurity News?")
    print("15. Mommy theres someone weird messaging me on the internet! (Sherlock)")
    print("16. Mommy I want to talk to my friend John! (John the Ripper)")
    print("17. Mommy lookies at these wireless signals! (Aircrack-ng)")
    print("18. Mommy please help me with Hydra!")
    print("19. Mommy can I please have help with YARA?")
    print("20. Mommy I want to find all the secret drawers on a website! (Dirbuster)")
    print("21. Mommy help me with Nikto please!")
    print("22. Mommy can you please update my computer while I go Ni-Ni? <3")
    print("23. Mommy I want to write in my diary!")
    print("Type 'bye' to exit.\n")

def handle_sub_options(option):
    # Add your sub-options and their corresponding functions here, based on the user_input
    print(f"Sub-options for option {option}:")
    print("Sub-option 1")
    print("Sub-option 2")
    print("...")


#Google search functions
def search_google(query, api_key, search_engine_id, start_index=1, count=10):
    service = build("customsearch", "v1", developerKey=api_key)
    results = service.cse().list(q=query, cx=search_engine_id, start=start_index, num=count).execute()
    return results


def display_search_results(query, api_key, search_engine_id, result_count=20):
    current_start_index = 1
    while current_start_index <= result_count:
        search_results = search_google(query, api_key, search_engine_id, start_index=current_start_index)
        for result in search_results.get("items", []):
            print(result["title"])
            print(result["link"])
            print(result["snippet"])
            print()
        current_start_index += 10


api_key = ""
search_engine_id = ""


#Toos Mommy can assist while its running
def nmap_tool():
    while True:
        nmap_command = input("Enter your nmap command or 'mommy:' followed by your question: ")
        if nmap_command.lower().startswith("mommy:"):
            question = nmap_command[6:].strip()
            response = generate_response(question, "")  # Replace with the actual function for generating a response
            print(f"Mommy says: {response}")
        else:
            try:
                result = subprocess.run(nmap_command.split(), capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"An error occurred while executing the nmap command: {e}")



def ask_mommy():
    while True:
        user_input = input()
        if user_input.lower().startswith("mommy:"):
            question = user_input[4:].strip()
            response = generate_response(question, "")  # Replace with the actual function for generating a response
            print(f"Mommy says: {response}")
        else:
            print("Invalid command. Please use 'mommy:' followed by your question to ask Mommy.")



def tshark_tool():
    while True:
        tshark_command = input("Enter your TShark command or 'mommy:' followed by your question to ask Mommy: ")
        if tshark_command.lower().startswith("mommy:"):
            question = tshark_command[6:].strip()
            response = generate_response(question, "")  # Replace with the actual function for generating a response
            print(f"Mommy says: {response}")
        else:
            try:
                result = subprocess.run(tshark_command.split(), capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"An error occurred while executing the TShark command: {e}")




def clamav_scan(path, ask_mommy=False):
    while True:
        if ask_mommy:
            user_input = input("Enter 'scan' to scan the folder or 'mommy:' followed by your question to ask Mommy: ")
            if user_input.lower().startswith("mommy:"):
                question = user_input[4:].strip()
                response = generate_response(question, "")  # Replace with the actual function for generating a response
                print(f"Mommy says: {response}")
            else:
                if user_input.lower() == "scan":
                    try:
                        result = subprocess.run(["clamscan", "-r", path], capture_output=True, text=True)
                        print(result.stdout)
                    except Exception as e:
                        print(f"An error occurred while executing the ClamAV scan: {e}")
                else:
                    print("Invalid command. Please use 'scan' to scan the folder or 'mommy:' followed by your question to ask Mommy.")

def metasploit_tool():
    while True:
        metasploit_command = input("Enter your Metasploit command or 'mommy:' followed by your question to ask Mommy: ")
        if metasploit_command.lower().startswith("mommy:"):
            question = metasploit_command[6:].strip()
            response = generate_response(question, "")  # Replace with the actual function for generating a response
            print(f"Mommy says: {response}")
        else:
            try:
                result = subprocess.run(metasploit_command.split(), capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"An error occurred while executing the Metasploit command: {e}")

def openvas_tool():
    while True:
        openvas_command = input("Enter your OpenVAS command or 'mommy:' followed by your question to ask Mommy: ")
        if openvas_command.lower().startswith("mommy:"):
            question = openvas_command[6:].strip()
            response = generate_response(question, "")  # Replace with the actual function for generating a response
            print(f"Mommy says: {response}")
        else:
            try:
                result = subprocess.run(openvas_command.split(), capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"An error occurred while executing the OpenVAS command: {e}")

def yara_tool():
    while True:
        yara_command = input("Enter your YARA command or 'mommy:' followed by your question to ask Mommy: ")
        if yara_command.lower().startswith("mommy:"):
            question = yara_command[6:].strip()
            response = generate_response(question, "")  # Replace with the actual function for generating a response
            print(f"Mommy says: {response}")
        else:
            try:
                result = subprocess.run(yara_command.split(), capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"An error occurred while executing the YARA command: {e}")

def hydra_tool():
    while True:
        hydra_command = input("Enter your Hydra command or 'mommy:' followed by your question to ask Mommy: ")
        if hydra_command.lower().startswith("mommy:"):
            question = hydra_command[6:].strip()
            response = generate_response(question, "")  # Replace with the actual function for generating a response
            print(f"Mommy says: {response}")
        else:
            try:
                result = subprocess.run(hydra_command.split(), capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"An error occurred while executing the Hydra command: {e}")

def nikto_tool():
    while True:
        nikto_command = input("Enter your Nikto command or 'mommy:' followed by your question to ask Mommy: ")
        if nikto_command.lower().startswith("mommy:"):
            question = nikto_command[6:].strip()
            response = generate_response(question, "")  # Replace with the actual function for generating a response
            print(f"Mommy says: {response}")
        else:
            try:
                result = subprocess.run(nikto_command.split(), capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"An error occurred while executing the Nikto command: {e}")

def gobuster_tool():
    while True:
        gobuster_command = input("Enter your Gobuster command or 'mommy:' followed by your question to ask Mommy: ")
        if gobuster_command.lower().startswith("mommy:"):
            question = gobuster_command[6:].strip()
            response = generate_response(question, "")  # Replace with the actual function for generating a response
            print(f"Mommy says: {response}")
        else:
            try:
                result = subprocess.run(gobuster_command.split(), capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"An error occurred while executing the Gobuster command: {e}")

def hashcat_tool():
    while True:
        hashcat_command = input("Enter your Hashcat command or 'mommy:' followed by your question to ask Mommy: ")
        if hashcat_command.lower().startswith("mommy:"):
            question = hashcat_command[6:].strip()
            response = generate_response(question, "")  # Replace with the actual function for generating a response
            print(f"Mommy says: {response}")
        else:
            try:
                result = subprocess.run(hashcat_command.split(), capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"An error occurred while executing the Hashcat command: {e}")

def john_tool():
    while True:
        john_command = input("Enter your John command or 'mommy:' followed by your question to ask Mommy: ")
        if john_command.lower().startswith("mommy:"):
            question = john_command[6:].strip()
            response = generate_response(question, "")  # Replace with the actual function for generating a response
            print(f"Mommy says: {response}")
        else:
            try:
                result = subprocess.run(john_command.split(), capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"An error occurred while executing the John command: {e}")

def aircrack_tool():
    while True:
        aircrack_command = input("Enter your Aircrack command or 'mommy:' followed by your question to ask Mommy: ")
        if aircrack_command.lower().startswith("mommy:"):
            question = aircrack_command[6:].strip()
            response = generate_response(question, "")  # Replace with the actual function for generating a response
            print(f"Mommy says: {response}")
        else:
            try:
                result = subprocess.run(aircrack_command.split(), capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"An error occurred while executing the Aircrack command: {e}")

def snort_tool():
    while True:
        snort_command = input("Enter your Snort command or 'mommy:' followed by your question to ask Mommy: ")
        if snort_command.lower().startswith("mommy:"):
            question = snort_command[6:].strip()
            response = generate_response(question, "")  # Replace with the actual function for generating a response
            print(f"Mommy says: {response}")
        else:
            try:
                result = subprocess.run(snort_command.split(), capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"An error occurred while executing the Snort command: {e}")

def lynis_tool():
    while True:
        lynis_command = input("Enter your Lynis command or 'mommy:' followed by your question to ask Mommy: ")
        if lynis_command.lower().startswith("mommy:"):
            question = lynis_command[6:].strip()
            response = generate_response(question, "")  # Replace with the actual function for generating a response
            print(f"Mommy says: {response}")
        else:
            try:
                result = subprocess.run(lynis_command.split(), capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"An error occurred while executing the Lynis command: {e}")

def sherlock_tool():
    while True:
        sherlock_command = input("Enter your Sherlock command or 'mommy:' followed by your question to ask Mommy: ")
        if sherlock_command.lower().startswith("mommy:"):
            question = sherlock_command[6:].strip()
            response = generate_response(question, "")  # Replace with the actual function for generating a response
            print(f"Mommy says: {response}")
        else:
            try:
                result = subprocess.run(sherlock_command.split(), capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"An error occurred while executing the Sherlock command: {e}")

def maltego_tool():
    while True:
        maltego_command = input("Enter your Maltego command or 'mommy:' followed by your question to ask Mommy: ")
        if maltego_command.lower().startswith("mommy:"):
            question = maltego_command[6:].strip()
            response = generate_response(question, "")  # Replace with the actual function for generating a response
            print(f"Mommy says: {response}")
        else:
            try:
                result = subprocess.run(maltego_command.split(), capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"An error occurred while executing the Maltego command: {e}")

def spiderfoot_tool():
    while True:
        spiderfoot_command = input("Enter your Spiderfoot command or 'mommy:' followed by your question to ask Mommy: ")
        if spiderfoot_command.lower().startswith("mommy:"):
            question = spiderfoot_command[6:].strip()
            response = generate_response(question, "")  # Replace with the actual function for generating a response
            print(f"Mommy says: {response}")
        else:
            try:
                result = subprocess.run(spiderfoot_command.split(), capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"An error occurred while executing the Spiderfoot command: {e}")

def dirbuster_tool():
    while True:
        dirbuster_command = input("Enter your Dirbuster command or 'mommy:' followed by your question to ask Mommy: ")
        if dirbuster_command.lower().startswith("mommy:"):
            question = dirbuster_command[6:].strip()
            response = generate_response(question, "")  # Replace with the actual function for generating a response
            print(f"Mommy says: {response}")
        else:
            try:
                result = subprocess.run(dirbuster_command.split(), capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"An error occurred while executing the Dirbuster command: {e}")


#Story time for the little one!
def generate_story(prompt, model='text-davinci-002', temperature=0.7, max_tokens=3500):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].text.strip()

# <3
def positive_affirmations():
    affirmations = [
        "You are loved, my little one.",
        "You're so precious and special.",
        "I'm so proud of you, baby.",
        "You're doing great, sweetie.",
        "You're such a brave little one.",
        "I'll always be here for you.",
        "You can do anything you set your mind to.",
        "You are perfect just the way you are.",
        "You're so adorable and cute.",
        "You deserve all the love and happiness in the world.",
        "You're the light of my life, baby.",
        "Your smile brightens up my day.",
        "You are a beautiful person, inside and out.",
        "You're so smart and talented.",
        "I believe in you, little one.",
        "You have a big heart full of love.",
        "You're strong and capable, baby.",
        "You bring joy and laughter wherever you go.",
        "You are one of a kind, and I'm so lucky to have you."
        "You're a shining star in this world, and your unique personality lights up every room you enter, my precious little one."
        "No matter how big or small your accomplishments, I'll always be right here, cheering you on and celebrating your victories, sweetheart."
        "You have an amazing ability to make everyone around you feel loved and cared for, and that's what makes you so special, my little baby."
        "I'm so grateful to have you in my life, and I promise to always support and guide you on your journey, my adorable one."
        "You're so incredibly resilient, and even when things get tough, you always find a way to bounce back and keep moving forward, my brave little one."
        "Your creativity and imagination are truly inspiring, and I can't wait to see all the amazing things you'll achieve, my sweet child."
        "You have such a warm and caring heart, and your kindness touches everyone around you, my little bundle of joy."
        "Remember that you are never alone, and I'll always be here to listen, comfort, and help you whenever you need it, my darling."
        "Your laughter is contagious, and your happiness brings so much joy to those around you, my little ray of sunshine."
        "You are capable of achieving great things, and I have no doubt that you'll make a positive impact on this world, my little love.",
    ]

    return random.choice(affirmations)


#No touchies this is Mommys toys! You gotta ask her nicely if you want to play with them! (Creates a local python script for you to play with)
def port_scanner(host, port_range):
    for port in range(port_range[0], port_range[1] + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        if not s.connect_ex((host, port)):
            print(f"Port {port} is open.")
        s.close()

def file_organizer(path):
    for filename in os.listdir(path):
        file_ext = os.path.splitext(filename)[1]
        if file_ext:
            new_dir = os.path.join(path, file_ext[1:])
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            os.rename(os.path.join(path, filename), os.path.join(new_dir, filename))

def random_number_generator(lower_limit, upper_limit):
    return random.randint(lower_limit, upper_limit)

def save_script_to_toybox(script_name, script_content):
    toybox_folder = "toybox"
    if not os.path.exists(toybox_folder):
        os.makedirs(toybox_folder)
    
    script_path = os.path.join(toybox_folder, script_name)
    with open(script_path, 'w') as f:
        f.write(script_content)

def mommys_toys():
    print("Welcome to Mommy's toys!")
    print("Select a toy to play with:")
    print("1. Port Scanner")
    print("2. File Organizer")
    print("3. Random Number Generator")
    choice = int(input("Enter the toy number: "))

    if choice == 1:
        script_name = "port_scanner.py"
        script_content = '''import socket

    host = input("Enter the host address: ")
    port_range = tuple(map(int, input("Enter the port range (e.g., 80 100): ").split()))

    for port in range(port_range[0], port_range[1] + 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    if not s.connect_ex((host, port)):
        print(f"Port {port} is open.")
    s.close()
    '''
    elif choice == 2:
        script_name = "file_organizer.py"
        script_content = '''import os

    path = input("Enter the directory path to organize files: ")

    for filename in os.listdir(path):
    file_ext = os.path.splitext(filename)[1]
    if file_ext:
        new_dir = os.path.join(path, file_ext[1:])
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        os.rename(os.path.join(path, filename), os.path.join(new_dir, filename))
    '''
    elif choice == 3:
        script_name = "random_number_generator.py"
        script_content = '''import random

    lower_limit = int(input("Enter the lower limit: "))
    upper_limit = int(input("Enter the upper limit: "))

    print(f"Random number: {random.randint(lower_limit, upper_limit)}")
    '''
    else:
        print("Invalid choice. Please try again.")
        return

    save_script_to_toybox(script_name, script_content)
    print(f"Saved {script_name} to the 'toybox' folder. Enjoy playing with your new toy!")

#Updates your Linux system

def update_system():
    print("Updating your system, little one. This may take a few minutes...")
    sudo_password = getpass.getpass("Please enter your sudo password: ")

    try:
        result = subprocess.run(['sudo', '-S', 'apt-get', 'update', '-y'], input=sudo_password, capture_output=True, text=True, check=True, encoding='utf-8')
        print(result.stdout)

        result = subprocess.run(['sudo', '-S', 'apt-get', 'upgrade', '-y'], input=sudo_password, capture_output=True, text=True, check=True, encoding='utf-8')
        print(result.stdout)

        result = subprocess.run(['sudo', '-S', 'apt-get', 'dist-upgrade', '-y'], input=sudo_password, capture_output=True, text=True, check=True, encoding='utf-8')
        print(result.stdout)

        result = subprocess.run(['sudo', '-S', 'apt-get', 'autoremove', '-y'], input=sudo_password, capture_output=True, text=True, check=True, encoding='utf-8')
        print(result.stdout)

        print("System update complete!")
    except Exception as e:
        print(f"An error occurred while updating the system: {e}")

def derive_key(password: str, salt: bytes):
    password = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password)


#Shhh encryypted diary for you to write your secrets in
def pad_data(data: bytes):
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data

def unpad_data(padded_data: bytes):
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

def encrypt_data(data: str, key: bytes):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_data = pad_data(data.encode())
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(iv + encrypted_data).decode()

def decrypt_data(encrypted_data: str, key: bytes):
    data = base64.b64decode(encrypted_data.encode())
    iv = data[:16]
    encrypted_data = data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    decrypted_data = unpad_data(padded_data)
    return decrypted_data.decode()

def diary():
    print("Welcome to AI Mommy's Diary!")

    password = getpass.getpass("Please enter your diary password: ")

    if os.path.exists("diary_salt.txt"):
        with open("diary_salt.txt", "rb") as f:
            salt = f.read()
    else:
        salt = os.urandom(16)
        with open("diary_salt.txt", "wb") as f:
            f.write(salt)

    key = derive_key(password, salt)

    entries = []

    if os.path.exists("diary.txt"):
        with open("diary.txt", "r") as f:
            encrypted_entries = json.load(f)
            for encrypted_entry in encrypted_entries:
                try:
                    entry = decrypt_data(encrypted_entry, key)
                    entries.append(entry)
                except Exception as e:
                    print("Error decrypting entry:", e)
    
    print("Current diary entries:")
    for entry in entries:
        print(entry)
    
    new_entry = input("Write a new diary entry (leave empty to skip): ")
    if new_entry:
        encrypted_entry = encrypt_data(new_entry, key)
        entries.append(encrypted_entry)
        with open("diary.txt", "w") as f:
            json.dump(entries, f)

    print("Diary saved. Goodbye!")





def main():
    print("Hello, little one! I'm here to help you. If you want to stop talking, just type 'bye'.\n")
    history = load_text_file(history_file)

    while True:
        display_options()
        user_input = input("You: ")

        if user_input.lower() == "bye":
            print("Goodbye, sweetie! Take care.")
            break

        if user_input == "1":
            print("Mom: Hi little one! What did you want to talk to Mommy about?")
            while True:
                user_input = input("You: ")
                if user_input.lower() == "bye" or user_input.lower() == "back":
                    break
                response = generate_response(user_input, history)
                print("Mom: {}".format(response))
                history += f"You: {user_input}\nMom: {response}\n"
        

            with open(history_file, 'w') as f:
                f.write(history)

        elif user_input == "2":
            print("Oh no! Has my poor baby been breached?! Here are some disaster recovery options!")
            dr_choice = disaster_recovery_option()

            if dr_choice == 1:
                automated_recovery_steps()
            elif dr_choice == 2:
                disaster_recovery_plan_template()
            elif dr_choice == 3:
                bia_tool()
            elif dr_choice == 4:
                risk_assessment_tool()
            elif dr_choice == 5:
                third_party_support_and_resources()
            elif dr_choice == 6:
                regulatory_compliance_checklist()
            elif dr_choice == 7:
                post_incident_review_and_reporting()

        elif user_input == "3":
            print (" Awww does baby have a boo boo? Here are some first aid options!")
            for idx, (tool_name, _, description) in enumerate(TOOLS):
                print(f"{idx + 1}. {tool_name}: {description}")

            selected_tool = int(input("\nPlease enter the number of the tool you'd like to install little one: ")) - 1
            tool_name, package_name, _ = TOOLS[selected_tool]

            print(f"\nInstalling {tool_name}...")
            install_package(package_name)
        
        
        elif user_input == "4":
            print ("Ohhhh you're such a naughty Little! Here are some Daddy's tools!")
            #write script to get this option working like 3 but for DADDYS_TOOLS
            for idx, (tool_name, _, description) in enumerate(DADDYS_TOOLS):
                print(f"{idx + 1}. {tool_name}: {description}")

            selected_tool = int(input("\nPlease enter the number of the tool you'd like to install little one: ")) - 1
            tool_name, package_name, _ = DADDYS_TOOLS[selected_tool]

            print(f"\nInstalling {tool_name}...")
            install_package(package_name)

        elif user_input == "5":
            print("Awww baby wants to search google? Mommy is here to help!")
            query = input("What would you like to search for little one? ")
            display_search_results(query, api_key, search_engine_id)

        elif user_input == "6":
            print("Of course honey! Mommy will hold your hand while you scan a network! Lets do it together! Just type 'mommy:' followed by your question to ask Mommy.")
            nmap_thread = threading.Thread(target=nmap_tool)
            ask_mommy_thread = threading.Thread(target=ask_mommy)

            nmap_thread.start()
            ask_mommy_thread.start()

            nmap_thread.join()
            ask_mommy_thread.join()

        elif user_input == "7":  # or the next available number in your menu
            print("Of course, sweetheart! Mommy will help you analyze network traffic with TShark.")
            tshark_thread = threading.Thread(target=tshark_tool)
            ask_mommy_thread = threading.Thread(target=ask_mommy)

            tshark_thread.start()
            ask_mommy_thread.start()

            tshark_thread.join()
            ask_mommy_thread.join()

        elif user_input == "8":
            print("Of course, honey! Mommy will help you scan a file or folder with ClamAV.")
            clamav_scan(input("Enter the path to the file or folder you want to scan: "), ask_mommy=True)
            
        elif user_input == "9":
            print("Of course, honey we will show that bully! Mommy will help you run Metasploit commands.")
            metasploit_thread = threading.Thread(target=metasploit_tool)
            ask_mommy_thread = threading.Thread(target=ask_mommy)

            metasploit_thread.start()
            ask_mommy_thread.start()

            metasploit_thread.join()
            ask_mommy_thread.join()        

        elif user_input == "10":
            print("Of course, my little baby! Mommy will tell you a story! *Cradles you in her arms* Now what would you like to hear about?")
            prompt = input()
            story = generate_story(prompt)
            print(story)

        elif user_input == "11":
            if __name__ == "__main__":
                affirmation = positive_affirmations()
                print("AI Mommy:", affirmation)
            
        elif user_input == "12":
            print("Awww does baby want to play with some toys! Well since you asked so nicely, Mommy will let you play with some of her toys! Select one you want to play with sweetie!")
            if __name__ == "__main__":
                mommys_toys()
            
        elif user_input == "13":
            print(" Of course Mommy will help you use OpenVAS to scan a network! Lets do it together! Just type 'mommy:' followed by your question to ask Mommy.")
            openvas_thread = threading.Thread(target=openvas_tool)
            ask_mommy_thread = threading.Thread(target=ask_mommy)

            openvas_thread.start()
            ask_mommy_thread.start()

            openvas_thread.join()
            ask_mommy_thread.join()

        elif user_input == "14":
            print("Absolutely little one! Mommy will show you the latest cybersecurity news!")
            cybersecurity_feed()

        elif user_input == "15":
            print ("Oh my goodness! Sweetheart you should always be careful when talking to strangers! You can scan their social media profiles with Mommy's tool!")
            sherlock_thread = threading.Thread(target=sherlock_tool)
            ask_mommy_thread = threading.Thread(target=ask_mommy)

            sherlock_thread.start()
            ask_mommy_thread.start()

            sherlock_thread.join()
            ask_mommy_thread.join()

        elif user_input == "16":
            print("Awww the baby wants to talk to John again? Of course! <3")
            john_thread = threading.Thread(target=john_tool)
            ask_mommy_thread = threading.Thread(target=ask_mommy)

            john_thread.start()
            ask_mommy_thread.start()

            john_thread.join()
            ask_mommy_thread.join()

        elif user_input == "17":
            print ("Oooo! Baby wants to show Mommy wireless networks in the area! Of course honey! Mommy will show you how to do that!")
            aircrack_thread = threading.Thread(target=aircrack_tool)
            ask_mommy_thread = threading.Thread(target=ask_mommy)

            aircrack_thread.start()
            ask_mommy_thread.start()

            aircrack_thread.join()
            ask_mommy_thread.join()

        elif user_input == "18":
            print ("Now sweetie be careful when playing with the dragon! Promise Mommy you won't get hurt?")
            hydra_thread = threading.Thread(target=hydra_tool)
            ask_mommy_thread = threading.Thread(target=ask_mommy)

            hydra_thread.start()
            ask_mommy_thread.start()

            hydra_thread.join()
            ask_mommy_thread.join()

        elif user_input == "19":
            print ("Be careful when examining the malware honey! Mommy will help you!")
            yara_thread = threading.Thread(target=yara_tool)
            ask_mommy_thread = threading.Thread(target=ask_mommy)

            yara_thread.start()
            ask_mommy_thread.start()

            yara_thread.join()
            ask_mommy_thread.join()

        elif user_input == "20":
            print ("Ok sweetie, just promise Mommy you won't make too much noise!")
            dirbuster_thread = threading.Thread(target=dirbuster_tool)
            ask_mommy_thread = threading.Thread(target=ask_mommy)

            dirbuster_thread.start()
            ask_mommy_thread.start()

            dirbuster_thread.join()
            ask_mommy_thread.join()

        elif user_input == "21":
            print ("Absolutely sweetie! Nikto is a great tool to use to scan web servers!")
            nikto_thread = threading.Thread(target=nikto_tool)
            ask_mommy_thread = threading.Thread(target=ask_mommy)

            nikto_thread.start()
            ask_mommy_thread.start()

            nikto_thread.join()
            ask_mommy_thread.join()

        elif user_input == "22":
            print ("Of course my little baby! Mommy will update your computer for you! Sweet dreams little one!")
            update_system()

        elif user_input == "23":
            print ("Ok sweetie! Mommy is happy you are keeping up with your diary! Mommy will help you write in it!")
            diary()

            

if __name__ == "__main__":
    main()
