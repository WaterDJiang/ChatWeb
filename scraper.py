
import requests
from bs4 import BeautifulSoup, Comment
from markdownify import markdownify as md

def scrape_website(url):
    """
    爬取网页内容，并将其转换为Markdown格式。
    :param url: 要爬取的网页URL。
    :return: 网页的标题和Markdown格式的内容。
    """
    try:
        with requests.Session() as session:
            user_agent = (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36'
            )
            session.headers = {'User-Agent': user_agent}
            response = session.get(url)
            response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        remove_unwanted_elements(soup)
        title = extract_title(soup)
        content_md = convert_to_markdown(soup)

        return title, content_md.strip()
    except (requests.RequestException, requests.ConnectionError, requests.Timeout) as e:
        return None, f"Error occurred: {e}"

def remove_unwanted_elements(soup):
    tags_to_remove = ["script", "style", "header", "footer", "nav", "aside", "iframe", "embed", "br", "hr", "button", "input", "a"]
    for tag in tags_to_remove:
        for element in soup.find_all(tag):
            element.extract()

    for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
        comment.extract()

def extract_title(soup):
    title_tag = soup.find('title')
    return title_tag.get_text(strip=True) if title_tag else "No Title"

def convert_to_markdown(soup):
    for tag in soup.find_all(True):
        tag.attrs = {}
    process_tables(soup)
    markdown_text = md(str(soup))
    return remove_empty_lines(markdown_text)

def remove_empty_lines(text):
    return '\n'.join(line for line in text.split('\n') if line.strip())

def process_tables(soup):
    """
    处理网页中的所有表格，转换为Markdown格式。
    :param soup: BeautifulSoup对象。
    """
    for table in soup.find_all('table'):
        markdown_table = []
        # 处理表头
        headers = table.find_all('th')
        if headers:
            header_row = [header.get_text(strip=True) for header in headers]
            markdown_table.append('| ' + ' | '.join(header_row) + ' |')
            markdown_table.append('|' + '|'.join(['---'] * len(header_row)) + '|')

        # 处理表格体
        for row in table.find_all('tr'):
            cols = row.find_all(['td', 'th'])
            if cols:
                markdown_row = [col.get_text(strip=True) for col in cols]
                markdown_table.append('| ' + ' | '.join(markdown_row) + ' |')

        # 将生成的Markdown表格替换原HTML表格
        table.replace_with('\n'.join(markdown_table))
        pass
