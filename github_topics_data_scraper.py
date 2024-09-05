# Scraping Top Repositories for Topics on GitHub

#----------------------------------------------------------------------------------------------
#Let's write a function to download the page.

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def get_topics_page():
    # TODO - add comments
    topics_url = 'https://github.com/topics'
    response = requests.get(topics_url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topic_url))
    doc = BeautifulSoup(response.text, 'html.parser')
    return doc

doc = get_topics_page()
# print(doc)


#Let's create some helper functions to parse information from the page.

# To get topic titles, we can pick p tags with the class ...


def get_topic_titles(doc):
    selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
    topic_title_tags = doc.find_all('p', {'class': selection_class})
    topic_titles = []
    for tag in topic_title_tags:
        topic_titles.append(tag.text)
    return topic_titles
titles = get_topic_titles(doc)
print(f"Topic Titles from the webpage:\n{titles}")

#No.of Titles
print(f"\nNumber of Topic titles: {len(titles)}")

#Top 5 Titles
print(f"\nTop 5 Topic titles:\n{titles[:5]}\n")

#Similarly we have defined functions for descriptions and URLs.

def get_topic_description(doc):
    description_selector = 'f5 color-fg-muted mb-0 mt-1'
    topic_description_tags = doc.find_all('p', {'class': description_selector})
    topic_description = []
    for tag in topic_description_tags:
        topic_description.append(tag.text.strip())
    return topic_description
description = get_topic_description(doc)
# print(f"\nDescription from the webpage:\n{description}")

def get_topic_urls(doc):
    topic_link_tags = doc.find_all('a', {'class': 'no-underline flex-1 d-flex flex-column'})
    topic_urls = []
    base_url = 'https://github.com'
    for tag in topic_link_tags:
        topic_urls.append(base_url + tag['href'])
    return topic_urls
topic_url = get_topic_urls(doc)
# print(topic_url)

#Let's put this all together into a single function

def scrape_topics():
    # topics_url = 'https://github.com/topics'
    # response = requests.get(topics_url)
    # if response.status_code != 200:
    #     raise Exception('Failed to load page {}'.format(topic_url))
    # doc = BeautifulSoup(response.text, 'html.parser')
    topics_dict = {
        'Topic title': get_topic_titles(doc),
        'Topic description': get_topic_description(doc),
        'Topic url': get_topic_urls(doc)
    }
    df = pd.DataFrame(topics_dict)
    df.index +=1 #index starts from 1 
    return df
topics_df = scrape_topics()
print(topics_df)

#Get the top 25 repositories from a topic page

def get_topic_page(topic_url):
    # Download the page
    response = requests.get(topic_url)
    # Check successful response
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topic_url))
    # Parse using Beautiful soup
    topic_doc = BeautifulSoup(response.text, 'html.parser')
    return topic_doc

# doc = get_topic_page('https://github.com/topics/3d')

def parse_star_count(stars):
    stars=stars.strip()
    if stars[-1]=='k':
        return int(float(stars[:-1])*1000)
    return(int(stars))

def get_repo_info(h1_tag, star_tag):
    # returns all the required info about a repository
    a_tags = h1_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    base_url = 'https://github.com'
    repo_url =  base_url + a_tags[1]['href']
    stars = parse_star_count(star_tag.text.strip())
    return username, repo_name, stars, repo_url

def get_topic_repos(topic_doc):
    # Get the h1 tags containing repo title, repo URL and username
    repo_tags = topic_doc.find_all('article',{'class':'border rounded color-shadow-small color-bg-subtle my-4'})

    # Get star tags
    star_tags=topic_doc.find_all('span',{'id':'repo-stars-counter-star'})

    topic_repos_dict = { 'username': [], 'repo_name': [], 'stars': [],'repo_url': []}

    # Get repo info
    for i in range(len(repo_tags)):
        repo_info = get_repo_info(repo_tags[i], star_tags[i])
        topic_repos_dict['username'].append(repo_info[0])
        topic_repos_dict['repo_name'].append(repo_info[1])
        topic_repos_dict['stars'].append(repo_info[2])
        topic_repos_dict['repo_url'].append(repo_info[3])

    return pd.DataFrame(topic_repos_dict)

def scrape_topic(topic_url, path):
    if os.path.exists(path):
        print("The file {} already exists. Skipping...".format(path))
        return
    topic_df = get_topic_repos(get_topic_page(topic_url))
    topic_df.to_csv(path, index=None)

''' Putting it all together

- We have a funciton to get the list of topics
- We have a function to create a CSV file for scraped repos from a topics page
- Let's create a function to put them together'''

def scrape_topics_repos():
    print('Scraping list of topics')
    topics_df = scrape_topics()

    os.makedirs('Output_Data_csv_files', exist_ok=True)
    for index, row in topics_df.iterrows():
        print('Scraping top repositories for "{}"'.format(row['Topic title']))
        scrape_topic(row['Topic url'], 'Output_Data_csv_files/{}.csv'.format(row['Topic title']))

print(scrape_topics_repos())