#importiing the libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


# Parsing the page
def get_topics_page():
  topics_url = 'https://github.com/topics'
  response = requests.get(topics_url)
  if response.status_code != 200:
    raise Exception('Failed to load page {}'.format(topics_url))
  doc = BeautifulSoup(response.text, 'html.parser')
  return doc


# Scraping Topic Titles Tags
def get_topic_title_tags(doc):
  #<p class="f3 lh-condensed mb-0 mt-1 Link--primary">3D</p>  >> This is the elemnt we need to scrape the topic names
  topic_title_tags = doc.find_all(
      'p', {'class': 'f3 lh-condensed mb-0 mt-1 Link--primary'})
  return topic_title_tags


''''
def get_topic_title_text(topic_tittle_tags):
  topic_title_text = topic_title_tags.text.strip()
  return topic_title_text
#code block ends here

#won’t work as intended for a couple of reasons:
1. .text attribute is used to get the combined text of all tags inside a particular tag. If topic_title_tags is a list of tags (as returned by find_all), then topic_title_tags.text will not work because lists don't have a .text attribute.
2. List of Tags: topic_title_tags is a list of p elements, and you need to extract text from each individual p tag within that list. The .text attribute on the list object won't give you the text from each tag, and .text on a single tag gives you all the text inside that tag, not the tag itself.

#Correct Approach with for Loop:
1. Iterating Over Each Tag: To process multiple tags and extract text from each, you need to loop over each tag in the list and access the .text attribute of each tag individually.
2. Appending to a List: After extracting text from each tag, you append it to a list, which can then be used for further processing or output.
'''


#Scraping Topic Titles Texts
def get_topic_title_text(topic_title_tags):
  topic_title_texts = []
  for tag in topic_title_tags:
    titles = topic_title_texts.append(tag.text.strip())
  return topic_title_texts


#Creating a Folder
folder_name = "OUTPUT GITHUB TOPICS DATA FOLDER"
title_tags_list = os.path.join(folder_name, 'csv_title_tags_list.csv')

#Ensuring the folder exists
if not os.path.exists(folder_name):
  os.makedirs(folder_name)
  print(f"Folder '{folder_name}' created.\n")
else:
  print(f"Folder '{folder_name}' already exits.\n")


#Saving the list of topic titles tags as a CSV file
def save_title_tags_to_csv(topic_title_tags, folder_name):
  # Prepare the CSV file path
  title_tags_file = os.path.join(folder_name, 'csv_title_tags_list.csv')

  # Extract raw HTML from tags
  title_tags = []
  for tag in topic_title_tags:
    title_tags.append(str(tag))

  df = pd.DataFrame(title_tags, columns=['Title Tag'])

  # Save DataFrame to CSV
  df.to_csv(title_tags_file, index=False)
  print(f"Title Tags CSV file saved at: {title_tags_file}\n")


#Saving the list of topic titles texts as a CSV file
def save_title_texts_to_csv(topic_title_texts, folder_name):
  title_texts_file = os.path.join(folder_name, 'csv_title_texts_list.csv')
  df = pd.DataFrame(topic_title_texts, columns=['Title Texts'])
  df.to_csv(title_texts_file, index=False)
  print(f"Title Texts CSV file saved at: {title_texts_file}\n")

#Calling the Functions
doc = get_topics_page()
topic_title_tags = get_topic_title_tags(doc)
topic_title_texts = get_topic_title_text(topic_title_tags)

#Orchestrating the Functions or Calling the Functions to save the files
save_title_tags_to_csv(topic_title_tags, folder_name)
save_title_texts_to_csv(topic_title_texts, folder_name)

#Printing Topic Titles Tags in a List inbuilt
print(f"Topic Titles Tags:\n")
print(topic_title_tags)
print('-' * 100)

#Printing Topic Titles Tags in Rows using For Loop
print("\nTopic Title Tags in Rows:\n")
for tag in topic_title_tags:
  print(tag)
print('-' * 100)

#Printing Topic Titles Texts in a List inbuilt
print(f"\nTopic Title Texts:\n\n{topic_title_texts}\n{'-'*100}")

#Printing Topic Titles Texts in Rows using For Loop
print(f"\nTopic Title Texts in Rows:\n")
for text in topic_title_texts:
  print(text)
print('-' * 100)


#Parsing the complete webpage by specific page number
def get_more_topics_page(page_number):
  ajax_url = f'https://github.com/topics?page={page_number}'
  response = requests.get(ajax_url)
  if response.status_code != 200:
    raise Exception('Failed to load page {}'.format(ajax_url))
  soup = BeautifulSoup(response.text, 'html.parser')
  return soup


#Scraping Topic Title Tags by specific page by number
def get_more_topics_title_tags(soup):
  more_topic_title_tags = soup.find_all(
      'p', {'class': 'f3 lh-condensed mb-0 mt-1 Link--primary'})
  return more_topic_title_tags


#Scraping Topic Title Texts by specific page by number
def get_more_topics_title_texts(more_topic_title_tags):
  more_topics_title_texts = []
  for tag in more_topic_title_tags:
    more_topics_title_texts.append(tag.text.strip())
  return more_topics_title_texts


#Scraping the specific page source code
page_number = 2
soup = get_more_topics_page(page_number)
# print(soup.prettify())

#Scraping the 2nd page Topic Title Tags
more_topic_title_tags = get_more_topics_title_tags(soup)
print("2nd Page Topic Title Tags:\n")
print(more_topic_title_tags)
print(f"\n{'-'*100}")

#Scraping the 2nd page Topic Title Tags using For Loop
print(f"2nd Page Title Tags in Rows:\n")
for tag in more_topic_title_tags:
  print(tag)
print(f"\n{'-'*100}")

#Scraping the 2nd page Topic Title Texts
print(f"2nd Page Title Texts:\n")
more_topics_title_texts = get_more_topics_title_texts(more_topic_title_tags)
print(more_topics_title_texts)
print(f"\n{'-'*100}")

#Scraping the 2nd page Topic Title Texts in rows using For Loop
print(f"2nd Page Title Texts in Rows:\n")
for text in get_more_topics_title_texts(more_topic_title_tags):
  print(text)
print(f"\n{'-'*100}")

#Finding the no.of titles in 2nd page
print(f"No.of Titles in 2nd Page: {len(more_topic_title_tags)}\n{'-'*100}")


#Finding Total No.of Pages (Load more ...)
def total_pages():
  page_number = 1
  while True:
    soup = get_more_topics_page(page_number)
    topic_title_tags = get_more_topics_title_tags(soup)

    if not topic_title_tags:
      break  # Stop if no more topics are found

    page_number += 1

  return page_number - 1  # The last successful page number


total_pages = total_pages()
print(f'Total number of pages: {total_pages}')

#Finding no.of titles in each page
for page_number in range(1, total_pages + 1):
  soup = get_more_topics_page(page_number)
  more_topic_title_tags = get_more_topics_title_tags(soup)
  print(f"No.of Titles in Page {page_number}: {len(more_topic_title_tags)}")
print(f"{'-'*100}")

#Scraping titles tags in each page
print("All Pages Title Tags:\n")
for page_number in range(1, total_pages + 1):
  soup = get_more_topics_page(page_number)
  more_topic_title_tags = get_more_topics_title_tags(soup)
  print(f"Page:{page_number}\n{more_topic_title_tags}\n")
print('-' * 100)

#Scraping titles texts in each page
print("All Pages Title Texts:\n")
for page_number in range(1, total_pages + 1):
  soup = get_more_topics_page(page_number)
  more_topic_title_tags = get_more_topics_title_tags(soup)
  more_topics_title_texts = get_more_topics_title_texts(more_topic_title_tags)
  print(f"Page:{page_number}\n{more_topics_title_texts}\n")
print('-' * 100)

#Scraping titles texts in each page using For Loop
print("All Pages Title Texts in Rows:\n")
for page_number in range(1, total_pages + 1):
  soup = get_more_topics_page(page_number)
  more_topic_title_tags = get_more_topics_title_tags(soup)
  more_topics_title_texts = get_more_topics_title_texts(more_topic_title_tags)
  print(f"Page:{page_number}")
  for text in more_topics_title_texts:
    print(text)
  print()
print('-' * 100)


#Saving the list of page2 topic titles tags as a CSV file
def save_page2_title_tags_to_csv(more_topic_title_tags, folder_name):
  # Prepare the CSV file path
  more_title_tags_file = os.path.join(folder_name,
                                      'csv_page2_title_tags_list.csv')

  # Extract raw HTML from tags
  more_title_tags = []
  for tag in more_topic_title_tags:
    more_title_tags.append(str(tag))

  df = pd.DataFrame(more_title_tags, columns=['page2_Title Tag'])

  # Save DataFrame to CSV
  df.to_csv(more_title_tags_file, index=False)
  print(f"Page2 Title Tags CSV file saved at: {more_title_tags_file}\n")


#Saving the list of page2 topic titles texts as a CSV file
def save_page2_title_texts_to_csv(more_topic_title_texts, folder_name):
  # Prepare the CSV file path
  more_title_texts_file = os.path.join(folder_name,'csv_page2_title_texts_list.csv')

  df = pd.DataFrame(more_topic_title_texts, columns=['page2_Title Texts'])

  # Save DataFrame to CSV
  df.to_csv(more_title_texts_file, index=False)
  print(f"Page2 Title Texts CSV file saved at: {more_title_texts_file}\n")


#Scrape page2 or the specific page
page_number = 2
soup = get_more_topics_page(page_number)
more_topic_title_tags = get_more_topics_title_tags(soup)
more_topic_title_texts = get_more_topics_title_texts(more_topic_title_tags)

# Saving the scraped topic titles tags of page 2 into a CSV file
save_page2_title_tags_to_csv(more_topic_title_tags, folder_name)
save_page2_title_texts_to_csv(more_topic_title_texts, folder_name)




