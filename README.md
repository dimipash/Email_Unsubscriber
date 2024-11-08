# Email Unsubscribe Link Extractor

## Overview

This project is a Python script that connects to a Gmail account, searches for emails containing "unsubscribe" links, and extracts those links for further processing. The extracted links are then visited, and the results are logged. Finally, the links are saved to a text file.

## Features

-   Connects to Gmail using IMAP.
-   Searches for emails containing "unsubscribe" links.
-   Extracts and visits the links.
-   Saves the extracted links to a text file.

## Prerequisites

1. Python 3.x installed on your system.
2. The following Python libraries installed:
    - `imaplib`
    - `email`
    - `bs4` (BeautifulSoup)
    - `dotenv`
    - `requests`
3. A Gmail account with the necessary permissions to access the inbox.

## Setup

1. Clone the repository or download the script file.
2. Create a `.env` file in the same directory as the script and add the following environment variables:
    ```
    EMAIL=your_gmail_username@gmail.com
    PASSWORD=your_gmail_app_password
    ```
3. Install the required Python libraries by running the following command in your terminal:
    ```
    pip install imaplib email bs4 dotenv requests
    ```

## Usage

The script will:

-   Connect to your Gmail inbox.
-   Search for the last 100 emails containing the word "unsubscribe".
-   Extract the unsubscribe links from those emails.
-   Visit each link and log the results.
-   Save all extracted links to `links.txt`.
