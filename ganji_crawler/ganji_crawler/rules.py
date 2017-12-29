# -*- coding: utf-8 -*-


rules_xpath = {
    'house_list' : '//a[@class="list-info-title"]/@href',
    'house_list_nextpage' : '//a[@class="next"]/@href',


    'guwen' : '//*[@class="person-name"][1]/text()',
    'guwen_phone' : '//*[@class="contact-mobile"]/text()',
    'company' : '//*[@class="company-name"]/text()',
    'company_url' : '//*[@class="my-shop"]/a/@href',
    'building_name' : u'//*[contains(text(), "写字楼名称")]/following-sibling::*/text()',
    'district_name' : '//li[@class="with-area clearfix"]/a[2]/text()',
    'street_name' : '//li[@class="with-area clearfix"]/a[3]/text()',
    'area' : u'//*[contains(text(), "写字楼面积")]/parent::*/text()',
    'rent_price' : '//*[@class="basic-info-price"]/text()',
    'rent_price_unit' : '//*[@class="basic-info-price"]/parent::li/text()[2]',
    'pub_date' : u'//li[contains(text(), "发布")]/i/text()',
    'title' : '//h1/text()',


}


rules_qiuzu = {
    'house_list' : '//div[@class="img-wrap"]/a/@href',
    'house_list_nextpage' : '//a[@class="next"]/@href',

    'path_list' : '//ul[@class="basic-info-ul"]/li',
    'guwen' : '//i[@class="fc-4b"]/text()',
    'guwen_phone' : '//*[@class="contact-mobile"]/text()',
    'company' : '//h1[@class="title-name"]/text()',
    'company_url' : '//*[@class="my-shop"]/a/@href',
    'building_name' : u'//*[contains(text(), "写字楼名称")]/following-sibling::*/text()',
    'district_name' : '//ul[@class="basic-info-ul"]/li[5]/a[2]/text()',
    'street_name' : '//ul[@class="basic-info-ul"]/li[5]/a[3]/text()',
    'address' : '//ul[@class="basic-info-ul"]/li[6]/span[2]/text()',
    'area' : u'//ul[@class="basic-info-ul"]/li[2]/text()',
    'rent_price' : '//ul[@class="basic-info-ul"]/li[1]/b/text()',
    'rent_price_unit' : '//*[@class="basic-info-price"]/parent::li/text()[2]',
    'pub_date' : u'//li[contains(text(), "发布")]/i/text()',
    'click_num' : u'//li[contains(text(), "浏览")]/i/text()',
    'title' : '//h1/text()',
    'isperson' : '//div[@class="col-right"]/div/fieldset/legend/text()'

}
