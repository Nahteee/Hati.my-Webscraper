import requests
import csv
from bs4 import BeautifulSoup


def decodeEmail(e):
    de = ""
    k = int(e[:2], 16)

    for i in range(2, len(e) - 1, 2):
        de += chr(int(e[i:i + 2], 16) ^ k)

    return de


def createFile(number):
    global record_count
    global file
    global writer
    record_count = 0
    file = open(f'Hati NGOs {number}.csv', 'w', encoding='utf8', newline='')
    writer = csv.writer(file)

    # writer header rows
    writer.writerow(['Lead ID', 'Company', 'First Name', 'Last Name',
                 'Title', 'Email', 'Phone', 'Mobile', 'Website', 'Lead Source', 'Lead Status', 'Industry',
                 'No. of Employees', 'Rating', 'Modified By', 'Modified By ID',
                 'Created Time', 'Modified Time', 'Street', 'City', 'State', 'Zip Code', 'Country', 'Description',
                 'Email Opt Out', 'Salutation', 'Secondary Email', 'Last Activity Time', 'Lead Conversion Time',
                 'Unsubscribed Mode', 'Unsubscribed Time', 'Converted Account', 'Converted Account Id',
                 'Converted Contact', 'Converted Contact Id', 'Converted Deal', 'Converted Deal Id', 'Record Id',
                 'Is Converted'])

URL = "https://www.hati.my/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="content-area")
categories = results.find_all("div", class_="col-12 col-md-6 col-lg-3 mt-3")
category_links = []
record_count = 0
file_number = 1
file = open(f'Hati NGOs {file_number}.csv', 'w', encoding='utf8', newline='')
writer = csv.writer(file)

# writer header rows
writer.writerow(['Lead ID', 'Company', 'First Name', 'Last Name',
                 'Title', 'Email', 'Phone', 'Mobile', 'Website', 'Lead Source', 'Lead Status', 'Industry',
                 'No. of Employees', 'Rating', 'Modified By', 'Modified By ID',
                 'Created Time', 'Modified Time', 'Street', 'City', 'State', 'Zip Code', 'Country', 'Description',
                 'Email Opt Out', 'Salutation', 'Secondary Email', 'Last Activity Time', 'Lead Conversion Time',
                 'Unsubscribed Mode', 'Unsubscribed Time', 'Converted Account', 'Converted Account Id',
                 'Converted Contact', 'Converted Contact Id', 'Converted Deal', 'Converted Deal Id', 'Record Id',
                 'Is Converted'])

for category in categories:
    links = category.find_all("a")
    for link in links:
        link_url = link["href"]
        category_links.append(link_url)

for category_link in category_links:
    page_number = 1
    while True:
        url = category_link + "/page/" + str(page_number)
        print(url)
        print("Counting records...")
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="content")
        next_page = results.find("a", class_="next page-numbers")

        NGOs = results.find_all("h2", class_="entry-title2")

        for NGO in NGOs:
            NGO_name = NGO.text.strip()  # Title
            # print(NGO_name)
            link = NGO.find("a")
            link_url = link["href"]
            page = requests.get(link_url)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find(id="context")
            NGO_info = results.find("div", class_="col-12 col-lg-6 order-1 order-lg-1")
            desc = NGO_info.find_all("p")

            full_desc = ''
            for line in desc:
                # print(line.text.strip())  # Description Paragraphs
                full_desc = full_desc + " " + line.text.strip()
            points = NGO_info.find_all("li")
            for point in points:
                # print(point.text.strip())  # Description Bullet Points
                full_desc = full_desc + point.text.strip()
            # print(full_desc) # Full Description

            NGO_details = NGO_info.find_all("td", class_="tooltip1")
            email = ''
            phone = ''
            website = ''
            address = ''
            reg = ''

            for line in NGO_details:
                line = line.text.strip()
                if "Email" in line:
                    try:
                        email_tag = NGO_info.find("span", class_="__cf_email__")
                        email = email_tag["data-cfemail"]
                        email = decodeEmail(email)
                        # print(email)  # Email
                    except:
                        email = ''
                if "Website" in line:
                    website = line[:-7]
                    # print(website)  # Website
                if "Phone Number" in line:
                    phone = line[:-12]
                    # print(phone)  # Phone Number
                if "Registration Number" in line:
                    reg = line[:-19]
                    # print(reg)  # Registration Number
                if "Address" in line:
                    address = line[:-7]
                    # print(address)  # Address
            if record_count < 1000:
                writer.writerow(['', NGO_name, '', '-', '', email, phone,
                                 '', website, 'Web', '', 'NGO', '', '', '',
                                 '', '', '', address, '', '', '', 'Malaysia', "Registration Number - " + reg + " " +
                                 "\n" + full_desc, 'FALSE', '', '', '', '',
                                 '',
                                 '', '', '', '', '', '', '', '', ''])
                record_count += 1
                print(record_count)
            else:
                file.close()
                file_number += 1
                createFile(file_number)
                writer.writerow(['', NGO_name, '', '-', '', email, phone,
                                 '', website, 'Web', '', 'NGO', '', '', '',
                                 '', '', '', address, '', '', '', 'Malaysia', "Registration Number - " + reg + " " +
                                 "\n" + full_desc, 'FALSE', '', '', '', '',
                                 '',
                                 '', '', '', '', '', '', '', '', ''])
                record_count += 1
                print(record_count)
        if str(next_page) != "None":
            page_number += 1
        else:
            break
file.close()

