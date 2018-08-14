from lxml import etree
import requests


HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
}
BASE_DOMAIN = 'https://hr.tencent.com/'
def get_detail_urls(url):
    response = requests.get(url,headers=HEADERS)
    text = response.text
    html = etree.HTML(text)
    detail_urls = html.xpath("//tr[@class='odd']//a/@href|//tr[@class='even']//a/@href")
    detail_urls = map(lambda url:BASE_DOMAIN+url,detail_urls)
    return detail_urls

def parse_per_url(url):
    position = {}
    respnse = requests.get(url,headers=HEADERS)
    html = etree.HTML(respnse.text)
    title = html.xpath("//td[@id='sharetitle']/text()")[0]
    position['title'] = title
    info_trs = html.xpath("//tr[@class='c bottomline']")
    for tr in info_trs:
        location = tr.xpath('.//td[1]/text()')[0]
        category = tr.xpath(".//td[2]/text()")[0]
        nums = tr.xpath(".//td[3]/text()")[0]
        position['location'] = location
        position['category'] = category
        position['nums'] = nums

    job_content = html.xpath("//tr[@class='c'][1]//ul[@class='squareli']//text()")
    position['job_content'] = job_content
    job_require = html.xpath("//tr[@class='c'][2]//ul[@class='squareli']//text()")
    position['job_require'] =job_require
    return position
def main():
    positions = []
    base_url = 'https://hr.tencent.com/position.php?lid=&tid=87&keywords=Python&start={}#a'
    for i in range(0,20,10):
        new_url = base_url.format(i)
        all_urls = get_detail_urls(new_url)
        for url in all_urls:
            position = parse_per_url(url)
            positions.append(position)
    print(positions)
    print(len(positions))
if __name__ == '__main__':
    main()