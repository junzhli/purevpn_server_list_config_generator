#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from purevpn_server_list.spiders.base import purevpnserverlistSpider
from purevpn_server_list.util import cleanup


def crawler_from_server():
    settings = get_project_settings()
    settings.set('FEED_FORMAT', 'json', priority='cmdline')
    settings.set('FEED_URI', os.path.join('templates', 'data.json'), priority='cmdline')
    process = CrawlerProcess(settings)

    process.crawl(purevpnserverlistSpider)
    process.start()


def read_server_list():
    with open(os.path.join('templates', 'data.json')) as data_file:
        data = json.load(data_file)
    return data


def generate_config_file(server, protocol):
    supported_protocol = {
        'TCP': [server['address_openvpn_tcp'], '80'],
        'UDP': [server['address_openvpn_udp'], '53']
    }
    if protocol in supported_protocol:
        # TCP/UDP solution
        with open(os.path.join('templates', protocol + '.ovpn'),
                  'r') as tempFile:
            data = tempFile.readlines()
        data[3] = ' '.join(
            map(str, [
                'remote', supported_protocol[protocol][0], supported_protocol[
                    protocol][1], '\n'
            ]))

        create_folder_if_nesscessary(os.path.join('generated_config_file'))
        with open(
                os.path.join('generated_config_file', '-'.join([
                    server['region'], server['country'], server['city'],
                    protocol
                ]) + '.ovpn'), 'w') as file:
            file.writelines(data)


def create_folder_if_nesscessary(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


if __name__ == '__main__':

    crawler_from_server()

    server_list = read_server_list()
    cleanup(os.path.join('generated_config_file'))
    for server in server_list:
        generate_config_file(server, 'TCP')
        generate_config_file(server, 'UDP')
