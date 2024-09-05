# GitHub Topics Web Scraping Project

## Introduction
- Web scraping is a technique used to extract data from websites. It involves fetching the content of web pages and then parsing the relevant data out of the HTML.
- GitHub is a popular platform for hosting and sharing code repositories. The website contains a wealth of information about various topics related to programming and software development.
- In this project, our goal is to scrape GitHub's topics page to extract the top repositories for each topic. We'll be using Python, along with the `requests` library to download web pages, `BeautifulSoup` to parse HTML, and `pandas` to structure and save the data.

## Steps to Follow

### Step 1: Scrape the List of Topics from GitHub
To scrape the list of topics, we'll follow these steps:
1. Use the `requests` library to download the HTML content of the GitHub topics page.
2. Use `BeautifulSoup` to parse the HTML and extract the necessary information, such as topic titles, topic URLs, and descriptions.
3. Organize the extracted data into a `pandas` DataFrame, which allows us to easily manipulate and save the data.

### Step 2: Scrape the Top 25 Repositories for Each Topic
For each topic, we'll:
1. Use the topic URL to navigate to the specific topic page.
2. Extract information about the top 25 repositories listed on the topic page. 
3. For each repository, we'll gather the following details:
   - Repository name: The name of the repository.
   - Username: The GitHub username of the repository owner.
   - Stars: The number of stars the repository has received. This is an indicator of the repository's popularity.
   - Repository URL: The direct URL to the repository on GitHub.

To achieve this:
1. We'll first download the HTML content of the topic page using `requests`.
2. We'll parse the HTML to find the relevant tags that contain the repository information using `BeautifulSoup`.
3. We'll process the stars count to convert it into a numerical value (handling cases where stars are represented in thousands, e.g., "3.5k").
4. Finally, we'll store the extracted information in a `pandas` DataFrame for further processing.

### Step 3: Save the Extracted Data to CSV Files
After collecting the repository data for each topic:
1. We'll save the data to a CSV file named after the topic. This will allow us to easily access and analyze the information later.
2. Each CSV file will be saved in a "data" directory, and will contain the following columns:
   - Repo Name
   - Username
   - Stars
   - Repo URL

This step involves:
1. Creating a new directory named "data" (if it doesn't already exist).
2. Checking if a CSV file for the topic already exists to avoid redundant scraping.
3. Writing the DataFrame containing the repository information to a CSV file using `pandas`.

### Step 4: Putting It All Together
Finally, we'll combine all the above steps into a single function that orchestrates the entire scraping process:
1. We'll start by scraping the list of topics from GitHub.
2. For each topic, we'll scrape the top repositories and save the results to a CSV file.
3. We'll add logging and print statements to track the progress of our scraping.

By the end of this process, we'll have a comprehensive dataset of top GitHub repositories for various programming topics, organized into CSV files that can be used for analysis or reporting.
