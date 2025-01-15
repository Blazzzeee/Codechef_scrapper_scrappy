import scrapy
from scrapy_playwright.page import PageMethod

class CodechefSpider(scrapy.Spider):
    name = "codechef"
    allowed_domains = ["codechef.com"]
    start_urls = ["https://www.codechef.com/users/vashuvats1"]
    pages = 0

    def start_requests(self):
        """
        Instead of scraping the page source as-is, we want to load the page using
        a headless browser and wait for the page to render the content using
        JavaScript. We then wait for a specific element to appear on the page
        (in this case, a table with the class "dataTable"). Once the element
        appears, we yield the response to the `parse` method, which will then
        extract the desired information from the page.

        This approach is useful when the page uses a lot of JavaScript to load
        its content, and the page source does not contain the information we
        need.
        """
        yield scrapy.Request(
            url="https://www.codechef.com/users/vashuvats1",
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "table.dataTable")
                ],
            },
        )

    def parse(self, response):
        """
        Extract information from a page about a Codechef user's submissions.

        The page is expected to contain a table with the class "dataTable" which
        contains the user's submissions. The table should have the following columns:

        - Problem name
        - Result

        The function yields a dictionary containing the user's submissions, with
        the problem name as the key and the result as the value.

        :param response: The response object containing the page source
        :yield: A dictionary containing the user's submissions
        """
        data = []
        for row in response.css("table.dataTable > tbody > tr"):
            problem = row.css("td:nth-child(2) a::text").get()
            result = row.css("td:nth-child(3) span::attr(title)").get()

            if result == "accepted":
                data.append({
                    "problem": problem,
                    "result": result,
                })

        yield {"data": data}
