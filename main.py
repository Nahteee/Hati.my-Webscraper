import requests
import csv
from bs4 import BeautifulSoup


def decodeEmail(e):
    de = ""
    k = int(e[:2], 16)

    for i in range(2, len(e) - 1, 2):
        de += chr(int(e[i:i + 2], 16) ^ k)

    return de


URL = "https://www.hati.my/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="content-area")
categories = results.find_all("div", class_="col-12 col-md-6 col-lg-3 mt-3")
category_links = []

file = open('Hati NGOs.csv', 'w', encoding='utf8', newline='')
writer = csv.writer(file)

# writer header rows
writer.writerow(['Lead ID', 'Leader Owner', 'Leader Owner ID', 'Company', 'First Name', 'Last Name',
                 'Title', 'Email', 'Phone', 'Mobile', 'Website', 'Lead Source', 'Lead Status', 'Industry',
                 'No. of Employees', 'Rating', 'Created By', 'Created by ID', 'Modified By', 'Modified By ID',
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
        # url = 'https://www.hati.my/category/culture/page/11/'
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="content")
        next_page = results.find("a", class_="next page-numbers")
        if str(next_page) != "None":
            page_number += 1
        else:
            break

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
                full_desc = full_desc + line.text.strip()
            points = NGO_info.find_all("li")
            for point in points:
                # print(point.text.strip())  # Description Bullet Points
                full_desc = full_desc + point.text.strip()
            # print(full_desc) # Full Description
            # NGO_check = NGO_info.find_all("td", class_="tooltip1")
            # Detail_list = []
            # for line in NGO_check:
            #     line = line.text.strip()
            #     Detail_list.append(line)
            # print(Detail_list)

            NGO_details = NGO_info.find_all("td", class_="tooltip1")
            email = ''
            phone = ''
            website = ''
            address = ''
            reg = ''

            # writer.writerow([NGO_name, full_desc, email, website, phone, reg, address])

            for line in NGO_details:
                line = line.text.strip()
                if "Email" in line:
                    try:
                        email_tag = NGO_info.find("span", class_="__cf_email__")
                        # print(email_tag)
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
            writer.writerow(['', 'Melvin Lim', 'zcrm_5493297000000388001', NGO_name, '', '-', '', email, phone,
                             '', website, 'Web', '', 'NGO', '', '', 'Melvin Lim', 'zcrm_5493297000000388001', '',
                             '', '', '', address, '', '', '', 'Malaysia', reg + full_desc, 'FALSE', '', '', '', '', '',
                             '', '', '', '', '', '', '', '', ''])
file.close()
