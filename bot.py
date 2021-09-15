import asyncio
import webbrowser
import re
from time import sleep
from pyppeteer import launch


# Init
from win10toast import ToastNotifier
_TOAST = ToastNotifier()

_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
_URL = "https://shop.nvidia.com/fr-fr/geforce/store/gpu/?page=1&limit=9&locale=fr-fr&category=GPU&gpu=RTX%203080,RTX%203080%20Ti&manufacturer=NVIDIA&gpu_filter=RTX%203090~1,RTX%203080%20Ti~1,RTX%203080~1,RTX%203070%20Ti~1,RTX%203070~1,RTX%203060%20Ti~1,RTX%203060~0,RTX%203050%20Ti~0,RTX%203050~0,RTX%202080%20Ti~0,RTX%202080%20SUPER~0,RTX%202080~0,RTX%202070%20SUPER~0,RTX%202070~0,RTX%202060~0,GTX%201660%20Ti~0,GTX%201660%20SUPER~0,GTX%201660~0,GTX%201650%20Ti~0,GTX%201650%20SUPER~0,GTX%201650~0"
_NB_GPU_TO_WATCH = 2
_DELAY_BETWEEN_REQUESTS = 0
_DELAY_BETWEEN_NOTIFS = 30

def alert(content):
    print("IN STOCK")
    print(_URL)

    os_notification("LIBEREZ LES CHIENS", _URL)

    try:
        search_and_open_ldlc(content)
    except Exception as e:
        print(e)

    webbrowser.open(_URL, new=2)

    sleep(2)
    os_notification("LIBEREZ LES CHIENS", _URL)
    sleep(2)
    os_notification("LIBEREZ LES CHIENS", _URL)
    sleep(2)
    os_notification("LIBEREZ LES CHIENS", _URL)

    sleep(_DELAY_BETWEEN_NOTIFS)

def search_and_open_ldlc(content):
    json_property_match = re.search('"purchaseLink": "https:\/\/www.ldlc.com\/.*"', content)
    if (json_property_match != None):
        json_property = content[json_property_match.start() : json_property_match.end()]
        link_match = re.search('https:\/\/www.ldlc.com\/.*"', json_property)
        link = json_property[link_match.start() : link_match.end() - 1]
        webbrowser.open(link, new=1)
    else:
        json_property_match = re.search('"purchaseLink": "https:\/\/gethatch.com\/.*"', content)
        json_property = content[json_property_match.start() : json_property_match.end()]
        link_match = re.search('https:\/\/gethatch.com\/.*"', json_property)
        link = json_property[link_match.start() : link_match.end() - 1]
        webbrowser.open(link, new=1)

def os_notification(title, text):
    _TOAST.show_toast(title, text, duration=3, icon_path="icon.ico")

async def fetch(url, string_to_find="RUPTURE DE STOCK"):
    browser = await launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe')
    page = await browser.newPage()
    await page.setUserAgent(_UA)
    await page.goto(url, timeout=10000)
    sleep(1)
    content = await page.evaluate('document.body.textContent', force_expr=True)
    await browser.close()

    if (not '"productId":' in content):
        return -1

    return content.count(string_to_find) + content.count("out_of_stock"), content

async def main():
    nb_try = 0

    print("watching {} gpus on url {}".format(_NB_GPU_TO_WATCH, _URL))
    print("=================================\n")

    while True:
        nb_try += 1
        print(f"try number {nb_try}")

        try:
            current_oos_count, content = await fetch(_URL)
        except Exception as e:
            print(e)
            continue

        if (current_oos_count == -1):
            print("fetch failed.")
            continue

        print(current_oos_count)
        if current_oos_count < _NB_GPU_TO_WATCH:
            f = open("log.txt", "a")
            f.write(content)
            f.close()
            alert(content)

        sleep(_DELAY_BETWEEN_REQUESTS)

asyncio.run(main())