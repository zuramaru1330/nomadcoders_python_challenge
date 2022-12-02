from bs4 import BeautifulSoup
import requests

result = []

def extract_jobs(term):
  url = f"https://remoteok.com/remote-{term}-jobs"
  request = requests.get(url, headers={"User-Agent": "Kimchi"})
  if request.status_code == 200:
    soup = BeautifulSoup(request.text, "html.parser")
    # write your ✨magical✨ code here


    jobs = soup.find_all('td', class_="company position company_and_position") 

    for jobs_find_query in jobs:
      position = jobs_find_query.select_one('h2')
      position_str = position.string
      position_str = position_str.replace('\n',"")
      company_name = jobs_find_query.select_one('h3')
      company_name_str = company_name.string
      company_name_str = company_name_str.replace('\n',"")
      region_and_salary = jobs_find_query.select('div.location')
      ahref_query = jobs_find_query.select('a[href^="/remote-jobs/"]')

      link = []   ## 잘못된 link 리스트 선언위치.... 에러의 원인
      for link_rep in ahref_query:
        link.append(link_rep.attrs['href'])

      cnt = 0
      link_cnt = 0
      for processing_data in region_and_salary:
        cnt = cnt + 1 
        if cnt % 2 != 0:
          region = processing_data.string
        else:
          salary = processing_data.string
         
          job_data = { "link" : 
                      f"https://remoteok.com{link[link_cnt]}", 
                      "company" : company_name_str,
                     "position" : position_str,
                     "region" : region,
                     "salary" : salary}
          
          link_cnt = link_cnt + 1
          result.append(job_data)
          
      
    for print_result in result:
      print(print_result)
      print("##################")
      
  else:
    print("Can't get jobs.")

extract_jobs("rust")
extract_jobs("golang")
extract_jobs("python")
extract_jobs("react")