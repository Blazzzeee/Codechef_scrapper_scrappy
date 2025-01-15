import scrapy
import json


class CodechefSpider(scrapy.Spider):
    name = "static1"
    max_page = 0
    init_parse = False

    def start_requests(self):
        # Start with the first page (page=0)
        yield scrapy.Request(
            url="https://www.codechef.com/recent/user?page=0&user_handle=vashuvats1",
            callback=self.parse
        )

    def parse(self, response):
        json_data = json.loads(response.text)
        self.max_page = json_data.get("max_page", 0)
        html_content = json_data.get("content", "")
        selector = scrapy.Selector(text=html_content)
        data = []

        for row in selector.css("table.dataTable > tbody > tr"):
            problem = row.css("td:nth-child(2) a::text").get()
            result = row.css("td:nth-child(3) span::attr(title)").get()
            if result == "accepted":
                data.append({
                    "problem": problem,
                    "result": result,
                })

        yield {"data": data}


        for page in range(1,self.max_page):
            next_page_url = f"https://www.codechef.com/recent/user?page={page}&user_handle=vashuvats1"
            yield scrapy.Request(url=next_page_url, callback=self.parse_page)

    def parse_page(self, response):
        json_data = json.loads(response.text)
        html_content = json_data.get("content", "")
        selector = scrapy.Selector(text=html_content)
        data = []

        for row in selector.css("table.dataTable > tbody > tr"):
            problem = row.css("td:nth-child(2) a::text").get()
            result = row.css("td:nth-child(3) span::attr(title)").get()
            if result == "accepted":
                data.append({
                    "problem": problem,
                    "result": result,
                })

        yield {"data": data}

