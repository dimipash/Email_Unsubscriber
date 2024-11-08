import os
import imaplib
import email
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests

load_dotenv()

username = os.getenv("EMAIL")
password = os.getenv("PASSWORD")


def connect_to_mail():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")
    return mail


def extract_links_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    links = [
        link["href"]
        for link in soup.find_all("a", href=True)
        if "unsubscribe" in link["href"].lower()
    ]
    return links


def click_link(link):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            print("Successfully vidsited", link)
        else:
            print("Failed to visit", link, "error code", response.status_code)
    except Exception as e:
        print("Error with", link, str(e))


def search_for_email():
    mail = connect_to_mail()

    _, search_data = mail.search(None, '(BODY "unsubscribe")')
    data = search_data[0].split()[-100:]  # Fetching the last 100 emails

    print(f"Found {len(data)} emails matching the search criteria.")

    links = []

    for num in data:
        print(f"Processing email number: {num}")
        _, data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    html_content = part.get_payload(decode=True)
                    try:
                        html_content = html_content.decode(
                            "utf-8"
                        )  # Attempt UTF-8 decoding
                    except UnicodeDecodeError:
                        html_content = html_content.decode(
                            "latin-1", errors="ignore"
                        )  # Fallback to Latin-1
                    try:
                        links.extend(extract_links_from_html(html_content))
                    except UnicodeDecodeError:
                        print("Failed to decode HTML content.")
        else:
            content_type = msg.get_content_type()
            content = msg.get_payload(decode=True)

            try:
                content = content.decode("utf-8")  # Attempt UTF-8 decoding
            except UnicodeDecodeError:
                content = content.decode(
                    "latin-1", errors="ignore"
                )  # Fallback to Latin-1

            if content_type == "text/html":
                links.extend(extract_links_from_html(content))

    mail.logout()
    print(f"Total links found: {len(links)}")
    return links


def save_links(links):
    with open("links.txt", "w") as f:
        f.write("\n".join(links))


links = search_for_email()

for link in links:
    click_link(link)

save_links(links)
