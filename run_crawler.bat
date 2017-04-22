@echo off
cd crawler/comment_crawler
echo scrapy crawl %1 -a m_id=%2
scrapy crawl %1 -a m_id=%2
popd
