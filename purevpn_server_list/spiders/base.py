#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from purevpn_server_list.items import PurevpnServerListItem

class purevpnserverlistSpider(Spider):
    name = "purevpnserverlistSpider"
    allowed_domains = ["support.purevpn.com"]
    start_urls = [
        "https://support.purevpn.com/vpn-servers"
    ]

    def parse(self, response):
        # Backup
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)

        # Data
        purevpn_data_list = []
        body = response.xpath('//tbody[@id="servers_data"]/tr')
        for index, tbody in enumerate(body):
            # yield {
            #     'region': tbody.xpath('td[1]/text()').extract(),
            #     'country': tbody.xpath('td[2]/text()').extract(),
            #     'city': tbody.xpath('td[3]/text()').extract(),
            #     'server_address_1': tbody.xpath('td[4]/text()').extract(),
            #     'server_address_2': tbody.xpath('td[5]/text()').extract(),
            #     'server_address_3': tbody.xpath('td[6]/text()').extract()
            # }
            purevpn_data = PurevpnServerListItem()
            purevpn_data['region'] = tbody.xpath('td[1]/text()').extract()
            purevpn_data['country'] = tbody.xpath('td[2]/text()').extract()
            purevpn_data['city'] = tbody.xpath('td[3]/text()').extract()
            purevpn_data['address_pp2p'] = purevpn_data['address_l2tp'] = purevpn_data['address_sstp'] = purevpn_data['address_ikev2'] = tbody.xpath('td[4]/text()').extract()
            purevpn_data['address_openvpn_udp'] = tbody.xpath('td[5]/text()').extract()
            purevpn_data['address_openvpn_tcp'] = tbody.xpath('td[6]/text()').extract()
            purevpn_data_list.append(purevpn_data)


            # args = (index, tbody.xpath('td[1]/text()').extract(), tbody.xpath('td[2]/text()').extract())
            # print (args)
        return purevpn_data_list
