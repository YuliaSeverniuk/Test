import scrapy
from datetime import datetime
from dateutil.parser import parse
import re


class LandCourtSpider(scrapy.Spider):
    name = "LandCourt"

    allowed_domains = ['tauntondeeds.com']
    start_urls = ['http://www.tauntondeeds.com/Searches/ImageSearch.aspx']

    def parse(self, response):
        today = datetime.today().strftime('%Y-%m-%d') + "-00-00-00"
        return scrapy.FormRequest.from_response(
            response,
            formdata={"ctl00$cphMainContent$txtLCSTartDate$dateInput": "2020-01-01-00-00-00",
                      "ctl00$cphMainContent$txtLCEndDate$dateInput": today,
                      "ctl00$cphMainContent$ddlLCDocumentType$vddlDropDown": "101627",
                      },
            clickdata={'value': 'Search Land Court'},
            callback=self.crawled_deeds)

    def crawled_deeds(self, response):
        cases = response.xpath('//table[@id="ctl00_cphMainContent_gvSearchResults"]//tr')
        for case in cases[1:]:
            data = case.xpath("td//text()").extract()
            if len(data) > 10:
                date = data[1]
                type = data[2]
                book = data[3]
                page_num = data[4]
                doc_num = data[5]
                city = data[6]
                description = data[8]
                if '$' in data[8]:
                    pre_cost = re.findall(', (.*)', data[8])[0]
                    cost = float(pre_cost.replace("$", ""))
                    if "SP" in data[8]:
                        pre_street_address = re.findall('SP (.*),', data[8])[0]
                        street_address_lst = (pre_street_address.split())[1:]
                        street_address = " ".join(street_address_lst)
                    else:
                        pre_street_address = re.findall(' (.*),', data[8])[0]
                        street_address_lst = (pre_street_address.split())[1:]
                        street_address = " ".join(street_address_lst)
                else:
                    cost = float()
                    if "SP" in data[8]:
                        pre_street_address = re.findall('SP (.*)', data[8])[0]
                        street_address_lst = (pre_street_address.split())[1:]
                        street_address = " ".join(street_address_lst)
                    else:
                        street_address = data[8]
                if 'STATE' in data[8]:
                    pre_state = re.findall('STATE (.*)', data[8])[0]
                    state = str((pre_state.split())[0])
                else:
                    state = ""
                zip = ""

                result = {'date': date, 'type': type, 'book': book, 'page_num': page_num,
                          'doc_num': doc_num, 'city': city, 'description': description, "cost": cost,
                          "street_address": street_address, "state": state, "zip": zip}

                yield result

        # crawl paginated pages
        pages = response.xpath('//tr[@class="gridPager"]//td//text()').extract()
        pages_list = sorted([p for p in set(pages) if p.isdigit()])

        current_page = list(set(response.xpath('//tr[@class="gridPager"]//span//text()').extract()))
        str_current_page = ' '.join([str(elem) for elem in current_page])

        for page in pages_list[1:]:
            if page != str_current_page:
                argument = "Page$" + page
                print("next page = ", argument)
                print("curent page = ", str_current_page)
                formdata = {
                    "__EVENTTARGET": "ctl00$cphMainContent$gvSearchResults",
                    "__EVENTARGUMENT": argument,}
                yield scrapy.FormRequest.from_response(response, formdata=formdata, dont_click=True,
                                                       dont_filter=True, callback=self.crawled_deeds)
