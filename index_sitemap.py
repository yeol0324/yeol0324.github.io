import os
import json
import requests
import xml.etree.ElementTree as ET
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# GitHub Secrets 계정 키 load
service_account_info = json.loads(os.environ.get('GCP_SERVICE_ACCOUNT_KEY'))
credentials = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=['https://www.googleapis.com/auth/indexing']
)

# 자격 증명 새로고침 
if not credentials.valid:
    credentials.refresh(Request())

# sitemap.xml 파일 경로 
SITEMAP_PATH = 'sitemap.xml' 

def get_urls_from_sitemap(sitemap_path):
    """sitemap.xml에서 URL 목록 추출"""
    urls = []
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        # sitemap.xml 네임스페이스 처리
        namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        for url_element in root.findall('sitemap:url', namespace):
            loc_element = url_element.find('sitemap:loc', namespace)
            if loc_element is not None:
                urls.append(loc_element.text)
    except FileNotFoundError:
        print(f"Error: sitemap.xml not found at {sitemap_path}")
    except ET.ParseError:
        print(f"Error: Could not parse sitemap.xml at {sitemap_path}")
    return urls

def send_indexing_request(url, credentials):
    """Google Indexing API 색인 요청"""
    api_url = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {credentials.token}'
    }
    payload = {
        'url': url,
        'type': 'URL_UPDATED'
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # HTTP 오류 발생 시 예외
        print(f"Successfully requested indexing for: {url}")
    except requests.exceptions.RequestException as e:
        print(f"Error requesting indexing for {url}: {e}")
        if response.status_code == 429: # Too Many Requests
            print("Quota exceeded. Stopping further requests.")
            return False # 할당량 초과 시 False 반환하여 중단
    return True

if __name__ == '__main__':
    urls_to_index = get_urls_from_sitemap(SITEMAP_PATH)
    if not urls_to_index:
        print("No URLs found in sitemap. Exiting.")
    else:
        print(f"Found {len(urls_to_index)} URLs in sitemap.xml. Starting indexing requests...")
        for url in urls_to_index:
            if not send_indexing_request(url, credentials):
                break # 할당량 초과 등으로 요청 실패 시 중단