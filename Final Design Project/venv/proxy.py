# Proxy creation to deter Amazon issues, code created by:
# https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/
###################################################################################

def get_proxies():
    proxy_url = 'https://free-proxy-list.net/'
    proxy_response = requests.get(proxy_url)
    parser = fromstring(proxy_response.text)
    set_proxies = set()
    for i in parser.xpath('//tbody/tr')[:3]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            find_proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            set_proxies.add(find_proxy)
    return set_proxies


proxies = get_proxies()
proxy_pool = cycle(proxies)

url = 'https://httpbin.org/ip'
for i in range(1,4):
    # Get a proxy from the pool
    proxy = next(proxy_pool)
    print("Request #%d"%i)
    try:
        response = requests.get(url,proxies={"http": proxy, "https": proxy})
        print(response.json())
    except:
        # Skip retries as its beyond the scope of this tutorial and we are only downloading a single url
        print("Skipping. Connnection error")



#################################################################################