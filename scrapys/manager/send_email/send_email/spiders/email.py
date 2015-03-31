#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.contrib.auth.models import User
from scrapy.spider import Spider
from scrapy.mail import MailSender
from app.scrapy_manager.models import SendEmailItem
from send_email.util import *

class Email(Spider):

    name = "email"
    allowed_domains = []
    start_urls = []

    result = True
    log_file = None
    scrapy_type = None

    email_receiver = []
    email_cc = []

    def __init__(self, result=None, log_file=None, scrapy_type=None):
        super(Email, self)
	if result == None or result == "" or result == "success":
	    self.result = True
	else:
	    self.result = False
	self.log_file = log_file
	self.scrapy_type = scrapy_type

	if self.scrapy_type != None:
	    email_item_list = SendEmailItem.objects.filter(type=self.scrapy_type)
	    for email_item in email_item_list:
	        self.email_receiver.append(email_item.receiver_email)
		self.email_cc.append(email_item.cc_email)

    def parse(self, response):
        pass

    def closed(self, reason):
        if self.log_file == None:
	    self.send_email(self.email_receiver, self.email_cc, "爬虫运行异常", "Email类中: 参数log_file不能为空, 请检查")
	    return

	if self.result == True:
	    subject = self.scrapy_type + "爬虫运行成功"
	else:
	    subject = self.scrapy_type + "爬虫运行异常"
        (attachs, merges) = attachs_and_merge_target_files(get_scrapy_root_path() + self.scrapy_type, self.log_file)
	self.send_email(self.email_receiver, self.email_cc, subject, merges, attachs)

    # send email
    def send_email(self, to=[], cc=[], subject="爬虫运行异常", body="", attachs=[]):
	# 如果收件人邮箱为空, 则发送到root账户的邮箱
        if len(to) == 0:
	    root_user = User.objects.filter(is_superuser=1)
	    if len(root_user) == 0:
	        raise Exception("root账户不存在, 请添加root账户和root账户的邮箱")
	    root_user_email = root_user[0].email
	    if root_user_email == None or root_user_email == "":
	        raise Exception("root账户没有配置邮箱, 请添加root账户的邮箱")
	    self.email_receiver.append(root_user_email)

	mailer = MailSender()
	mailer.send(to=to, cc=cc, subject=subject.encode("utf-8"), body=body.encode("utf-8"), attachs=attachs)
