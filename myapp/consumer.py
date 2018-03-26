import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.class_name = self.scope['url_route']['kwargs']['class_name'].replace(" ", "_")
        self.class_group_name = 'chat_%s' % self.class_name.replace(',', '_')

        # Join room group
        await self.channel_layer.group_add(
            self.class_group_name,
            self.channel_name
        )

        await self.channel_layer.group_add(
            'status-updates',
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.class_group_name,
            self.channel_name
        )

        await self.channel_layer.group_discard(
            'status-updates',
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.send(
            "thumbnails-generate",
            {
                'type': 'do_stuff',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))



class ThumbnailConsumer(AsyncConsumer):
    async def do_stuff(self, event):
        from selenium import webdriver
        import os
        import json
        import requests
        import sys
        import time
        os.environ["PATH"] += os.pathsep + os.getcwd()
        download_path = "dataset/"
        num_requested = 15
        number_of_scrolls = round(num_requested / 400 + 1)
        searchtext = event['message']
        if not os.path.exists(download_path + searchtext.replace(" ", "_")):
            os.makedirs(download_path + searchtext.replace(" ", "_"))
        url = "https://www.google.co.in/search?q=" + searchtext + "&source=lnms&tbm=isch"
        path_driver = os.getcwd()
        print(path_driver + "/chromedriver")
        driver = webdriver.Chrome(path_driver + "/chromedriver")
        driver.get(url)
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        extensions = {"jpg", "jpeg", "png"}
        img_count = 0
        downloaded_img_count = 0
        for _ in range(number_of_scrolls + 1):
            for __ in range(10):
                # multiple scrolls needed to show all 400 images
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)
            # to load next 400 images
            time.sleep(2)
            try:
                driver.find_element_by_xpath("//input[@value='Інші результати']").click()
            except Exception as e:
                print("Less images found:", e)
                break

        # imges = driver.find_elements_by_xpath('//div[@class="rg_meta"]') # not working anymore
        imges = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
        print("Total images:", len(imges), "\n")
        for img in imges:
            img_count += 1
            img_url = json.loads(img.get_attribute('innerHTML'))["ou"]
            img_type = json.loads(img.get_attribute('innerHTML'))["ity"]
            print("Downloading image", img_count, ": ", img_url)
            try:
                if img_type not in extensions:
                    img_type = "jpg"
                req_data = requests.get(img_url, headers=headers).content
                # raw_img = urllib.request.urlopen(req).read()
                f = open(
                    download_path + searchtext.replace(" ", "_") + "/" + str(downloaded_img_count) + "." + img_type,
                    "wb")
                f.write(req_data)
                f.close()
                downloaded_img_count += 1
                await self.channel_layer.group_send(
                    'status-updates',
                    {
                        'type': 'chat_message',
                        'message': f'{downloaded_img_count} of {num_requested} is successful downloads!'
                    }
                )
            except Exception as e:
                print("Download failed:", e)
            finally:
                print()
            if downloaded_img_count >= num_requested:
                break
        print("Total downloaded: ", downloaded_img_count, "/", img_count)
        driver.quit()