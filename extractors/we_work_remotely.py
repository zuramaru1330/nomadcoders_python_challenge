from requests import get
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?term="
    search_term = keyword

    response = get(f"{base_url}{search_term}")
    if response.status_code != 200:
        print("Can't request website")
    else:
        results = []
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all('section', class_="jobs")
        for job_section in jobs:
            job_posts = job_section.find_all('li')
            job_posts.pop(-1)
            for post in job_posts:
                anchors = post.find_all('a')
                anchor = anchors[1]
                link = anchor['href']
                company, position, region = anchor.find_all('span', class_="company")
                title = anchor.find('span', class_='title')
                job_data = {
                    'company' : company.string,
                    'position' : position.string,
                    'region' : region.string,
                    'title' : title.string,
                    'link' : f"https://weworkremotely.com{link}"
                }
                results.append(job_data)
        return results