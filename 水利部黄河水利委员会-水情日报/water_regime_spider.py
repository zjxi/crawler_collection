import time
import requests
import urllib
import selenium
from selenium import webdriver
import datetime
import pandas as pd

"""
    水利部黄河水利委员会-水情日报数据
"""

_cookie = 'ASP.NET_SessionId=jzrtwny4yfiwozghgkbi4ylk; .ASPXAUTH=B59F62DF370739DF252FAB2A9E514E83B9D2294E05B98C25C2CE11FE3BDA66D8B0AE5C1E509C3571B86667271B4A2B99CD87B9C31F824771AFA6AC7E40E3B053D06E5512072A2A09778396ECAB40BA9C0F41B46775C05FE65468DBA359364B77E31FA6287FE9D50276D92737F59C8891C9EE442F3934EA1DF3316ACD032BA2CD3F85F88E423831E19EE2D4658C1F69B76CCC1F9F1E7786BA6BF09B05DDE885E2E5F0332592A8E88D997ADF10D59C4788'


def request_url(url):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '14186',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': _cookie,
        'Host': 'www.hwswj.gov.cn:8006',
        'Origin': 'http://www.hwswj.gov.cn:8006',
        'Referer': 'http://www.hwswj.gov.cn:8006/hwsq.aspx?sr=0nkRxv6s9CTRMlwRgmfFF6jTpJPtAv87',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
        'X-MicrosoftAjax': 'Delta=true',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = {
        # 'ctl00$ScriptManager1': 'ctl00$ScriptManager1|ctl00$ContentLeft$Button1',
        # '__EVENTTARGET': '',
        # '__EVENTARGUMENT': '',
        'ctl00$ContentLeft$menuDate1$TextBox11': '2021-04-14',
        # '__VIEWSTATE': '/wEPDwULLTEwMDI5NzA1NzkPZBYCZg9kFgICAw9kFgICBQ9kFgJmD2QWAgIBD2QWAgIBDxYCHglpbm5lcmh0bWwFzEw8dGFibGUgd2lkdGg9Ijk4JSIgYm9yZGVyPSIwIiBjZWxscGFkZGluZz0iMCIgY2VsbHNwYWNpbmc9IjEiIGJnY29sb3I9IiNEMUREQUEiIGFsaWduPSJjZW50ZXIiPjx0cj48dGQgaGVpZ2h0PSI0MCIgYmFja2dyb3VuZD0ic2tpbi9pbWFnZXMvbmV3bGluZWJnMy5naWYiPjx0YWJsZSB3aWR0aD0iOTglIiBib3JkZXI9IjAiIGNlbGxzcGFjaW5nPSIwIiBjZWxscGFkZGluZz0iMCI+PHRyPjx0ZCBhbGlnbj0iY2VudGVyIj48ZGl2IGNsYXNzPSdmaXJzdFRpdGxlJz7msLTmg4Xml6XmiqU8L2Rpdj48ZGl2IGNsYXNzPSdzZWNUaXRsZSc+MjAyMS0wNC0yOTwvZGl2PjwvdGQ+PC90cj48L3RhYmxlPjwvdGQ+PC90cj48L3RhYmxlPjx0YWJsZSB3aWR0aD0iOTglIiBib3JkZXI9IjAiIGNlbGxwYWRkaW5nPSIyIiBjZWxsc3BhY2luZz0iMSIgYmdjb2xvcj0iI0QxRERBQSIgYWxpZ249ImNlbnRlciIgc3R5bGU9Im1hcmdpbi10b3A6OHB4IiBjbGFzcz0ibWFpblR4dCI+PHRyPjx0ZCB3aWR0aD0iNTAlIj48dGFibGUgd2lkdGg9IjEwMCUiIGJvcmRlcj0iMCIgY2VsbHBhZGRpbmc9IjIiIGNlbGxzcGFjaW5nPSIxIiBiZ2NvbG9yPSIjRDFEREFBIiBhbGlnbj0iY2VudGVyIiBzdHlsZT0ibWFyZ2luLXRvcDo4cHgiIGNsYXNzPSJtYWluVHh0Ij48VFIgYWxpZ249J2NlbnRlcicgYmdjb2xvcj0nI0U3RTdFNycgaGVpZ2h0PScyMicgY2xhc3M9J3RhYmxlVGl0bGUnID48VEQgd2lkdGg9IjE1JSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+5rKz5ZCNPC9URD48VEQgd2lkdGg9IjI1JSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+56uZ5ZCNPC9URD48VEQgd2lkdGg9IjIwJSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+5rC05L2NPC9URD48VEQgd2lkdGg9IjIwJSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+5rWB6YePPC9URD48VEQgd2lkdGg9IjIwJSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+5ZCr5rKZ6YePPC9URD48L1RSPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7llJDkuYPkuqUgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4yNjcxLjE0PC90ZD48dGQ+NDEyPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+6b6Z576K5bOh5YWl5bqTPC90ZD48dGQ+LTwvdGQ+PHRkPjQ1MzwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPum+mee+iuWzoeiThOawtOmHjzwvdGQ+PHRkPjI1OTAuNTwvdGQ+PHRkPigyMDUp5Lq/PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+6b6Z576K5bOh5Ye65bqTPC90ZD48dGQ+LTwvdGQ+PHRkPjk5MDwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWImOWutuWzoeWFpeW6kzwvdGQ+PHRkPi08L3RkPjx0ZD4xMTIwPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5YiY5a625bOh6JOE5rC06YePPC90ZD48dGQ+MTczMS43OTwvdGQ+PHRkPigzNS44KeS6vzwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWImOWutuWzoeWHuuW6kzwvdGQ+PHRkPi08L3RkPjx0ZD4xNDYwPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5YWw5beeICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4xNTEyLjA5PC90ZD48dGQ+MTcxMDwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuS4i+ays+ayvyAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjEyMzAuODU8L3RkPjx0ZD4xNjEwPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+55+z5Zi05bGxICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTA4Ni45MjwvdGQ+PHRkPjE3NTA8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7lt7Tlvabpq5jli5IgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTA1MC4wMjwvdGQ+PHRkPjEzOTA8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7kuInmuZbmsrPlj6MgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTAxNy4wMzwvdGQ+PHRkPjEwOTA8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7ljIXlpLQgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjEwMDIuMzwvdGQ+PHRkPjEwODA8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7lpLTpgZPmi5AgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD45ODcuMjc8L3RkPjx0ZD4xMjIwPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5LiH5a625a+o6JOE5rC06YePPC90ZD48dGQ+OTc5LjYzPC90ZD48dGQ+KDUuNzcp5Lq/PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5LiH5a625a+o5LiK5Ye65bqTPC90ZD48dGQ+LTwvdGQ+PHRkPjY3MjwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuS4h+WutuWvqOS4iyAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD44OTkuNTg8L3RkPjx0ZD42NzI8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7lupzosLcgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjgwOC4xMTwvdGQ+PHRkPjg3NjwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWQtOWgoSAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+NjM2Ljg4PC90ZD48dGQ+MTExMDwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPum+memXqCAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+Mzc3Ljg4PC90ZD48dGQ+ODI3PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuaxvuaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5rKz5rSlICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4zNzAuMzY8L3RkPjx0ZD4xNS4xPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuWMl+a0m+aysyAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPueKtuWktCAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MzYwLjg3PC90ZD48dGQ+MjMuNzwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7ms77msrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuW8oOWutuWxsSAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjQyMC4zNzwvdGQ+PHRkPjYzLjk8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5rit5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7lkrjpmLMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjM3Ni45NzwvdGQ+PHRkPjIwNjwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7muK3msrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWNjuWOvyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MzM1LjYxPC90ZD48dGQ+NTE0PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5r285YWzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4zMjYuNDc8L3RkPjx0ZD4xNjAwPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5Y+y5a625rup6JOE5rC06YePPC90ZD48dGQ+MzE4LjM1PC90ZD48dGQ+KDYuMjgp5Lq/PC90ZD48dGQ+LTwvdGQ+PC90cj48L3RhYmxlPjwvdGQ+PHRkIHdpZHRoPSI1MCUiPjx0YWJsZSB3aWR0aD0iMTAwJSIgYm9yZGVyPSIwIiBjZWxscGFkZGluZz0iMiIgY2VsbHNwYWNpbmc9IjEiIGJnY29sb3I9IiNEMUREQUEiIGFsaWduPSJjZW50ZXIiIHN0eWxlPSJtYXJnaW4tdG9wOjhweCIgY2xhc3M9Im1haW5UeHQiPjxUUiBhbGlnbj0nY2VudGVyJyBiZ2NvbG9yPScjRTdFN0U3JyBoZWlnaHQ9JzIyJyBjbGFzcz0ndGFibGVUaXRsZScgPjxURCB3aWR0aD0iMTUlIiBzdHlsZT0iZm9udC1zaXplOjExcHQ7Ij7msrPlkI08L1REPjxURCB3aWR0aD0iMjUlIiBzdHlsZT0iZm9udC1zaXplOjExcHQ7Ij7nq5nlkI08L1REPjxURCB3aWR0aD0iMjAlIiBzdHlsZT0iZm9udC1zaXplOjExcHQ7Ij7msLTkvY08L1REPjxURCB3aWR0aD0iMjAlIiBzdHlsZT0iZm9udC1zaXplOjExcHQ7Ij7mtYHph488L1REPjxURCB3aWR0aD0iMjAlIiBzdHlsZT0iZm9udC1zaXplOjExcHQ7Ij7lkKvmspnph488L1REPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7kuInpl6jls6EgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4yNzQuOTwvdGQ+PHRkPjE0NjA8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7lsI/mtarlupXkuIrok4TmsLTph488L3RkPjx0ZD4yNjYuMzM8L3RkPjx0ZD4oNzMuMinkur88L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7lsI/mtarlupUgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4xMzQuNDg8L3RkPjx0ZD4xNTkwPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuS8iuaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5Lic5rm+ICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4zNjMuNDY8L3RkPjx0ZD4yNS4yPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuS8iuaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+6ZmG5rWR5Z2d5LiK6JOE5rC06YePPC90ZD48dGQ+MzE1LjI0PC90ZD48dGQ+KDUuMDQp5Lq/PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuS8iuaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+6ZmG5rWR5Z2d5LiK5Ye65bqTPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5LyK5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7pvpnpl6jplYcgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4xNDcuMzc8L3RkPjx0ZD44Ljk1PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPua0m+aysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5Y2i5rCPICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD41NTAuOTI8L3RkPjx0ZD42MjwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7mtJvmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuaVheWOv+awtOW6k+iThOawtOmHjzwvdGQ+PHRkPjUzMS4zMjwvdGQ+PHRkPig1LjU3KeS6vzwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7mtJvmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuaVheWOv+awtOW6k+WHuuW6kzwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPua0m+aysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+6ZW/5rC077yI5LqM77yJICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4zNzcuOTQ8L3RkPjx0ZD4zLjI0PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPua0m+aysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+55m96ams5a+6ICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTEzLjA2PC90ZD48dGQ+MTM1PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuS8iua0m+aysyAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPum7keefs+WFsyAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjEwNi4wMjwvdGQ+PHRkPjE2MDwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7kuLnmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWxsei3r+WdqiAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuaygeaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5LqU6b6Z5Y+jICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5rKB5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7mrabpmZ8gICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjk4LjI1PC90ZD48dGQ+Mi43NjwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuiKseWbreWPoyAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjg5LjU2PC90ZD48dGQ+MTczMDwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWkueays+a7qSAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjcyLjE4PC90ZD48dGQ+MTY5MDwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPumrmOadkSAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+NTguMjU8L3RkPjx0ZD4xNjcwPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5a2Z5Y+jICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD40My40NjwvdGQ+PHRkPjE0ODA8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5aSn5rG25rKzICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5oi05p2R5Z2dPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5Lic5bmz5rmWICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5Lic5bmz5rmW6ICB5rmW6JOE5rC06YePPC90ZD48dGQ+NDEuNjI8L3RkPjx0ZD4oNS41NCnkur88L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5aSn5rG25rKzICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5Ye65rmW6Ze4PC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7oib7lsbEgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjM2LjczPC90ZD48dGQ+MTQ3MDwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuazuuWPoyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MjUuNDY8L3RkPjx0ZD4xMjkwPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5Yip5rSlICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD45LjE5PC90ZD48dGQ+MTE3MDwvdGQ+PHRkPi08L3RkPjwvdHI+PC90YWJsZT48L3RkPjwvdHI+PC90YWJsZT5kZGwtWJpP2+zaWVRyGzFArspoj8csq/fVQ2tRHfq0qVSP',
        # '__VIEWSTATEGENERATOR': 'E4DC7756',
        # '__EVENTVALIDATION': '/wEdAANz/1sxWTsKzeYHGebIQAo19DkLBAR+UXBBGQ1m5cY+HY5Ggl8DGIT46Qo2GBY6Yh4xTByeHxEQgdz39HP98byQVEbbl4zzhpb+1U/AVCMj9w==',
        # '__ASYNCPOST': 'true',
        'ctl00$ContentLeft$Button1': '查询'
    }
    # resp = requests.get(url=url, headers=headers)
    data = urllib.parse.urlencode(data)
    resp = requests.post(url=url, headers=headers, data=data)
    resp.encoding = 'utf-8'

    return resp.text


def web_driver(url, date):
    try:
        browser = webdriver.Chrome("C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe")
        browser.get(url)

        # 找到日期输入框
        textbox = browser.find_element_by_id("ContentLeft_menuDate1_TextBox11")
        # 消除readonly属性，更改输入日期
        browser.execute_script("arguments[0].removeAttribute('readonly')", textbox)
        textbox.clear()
        textbox.send_keys(f'{date}')

        # 找到按钮元素，并点击
        button = browser.find_element_by_id("ContentLeft_Button1")
        button.click()
        # browser.execute_script("arguments[0].click", button)

        # 解析“水情信息”数据
        time.sleep(2)  # 延迟2s，便于获取更新后的数据
        data = browser.find_element_by_xpath(".//div[@id='UpdatePanel1']")
        print(data.text)
        with open("data_supplement.csv", 'a', encoding='utf-8') as fw:
            fw.write(data.text)
            fw.write("\n")

        browser.close()

    except Exception as e:
        print(date, e)


def generate_date_list():
    """
    生成日历列表，从2002/01/01-至今
    :return:
    """
    dates = []
    # 现在的时间
    now = datetime.datetime.now()
    # 递减的时间
    delta = datetime.timedelta(days=-1)
    # 10年后的时间
    endnow = now - datetime.timedelta(days=3529 * 2)
    # 20年后的时间转换成字符串
    endnow = str(endnow.strftime('%Y-%m-%d'))
    offset = now
    while str(offset.strftime('%Y-%m-%d')) != endnow:
        offset += delta
        dates.append(str(offset.strftime('%Y-%m-%d')))

    return dates


def main():
    url = 'http://www.hwswj.gov.cn:8006/hwsq.aspx?sr=0nkRxv6s9CTRMlwRgmfFF6jTpJPtAv87'
    # 生成日期列表
    # dates = generate_date_list()
    dates = ['2020-12-01', '2007-04-05']
    for date in dates:
        print(f'------------当前日期为：{date}----------')
        web_driver(url, date)


def process_data():
    spider_dates = []
    with open('data.csv', 'r', encoding='utf-8') as fr:
        lines = fr.readlines()
        for i, line in enumerate(lines):
            if line.startswith("20"):
                # print(i)
                spider_dates.append(line.replace("\n", ""))

    with open('data2.csv', 'r', encoding='utf-8') as fr:
        lines = fr.readlines()
        for i, line in enumerate(lines):
            if line.startswith("20"):
                # print(i)
                spider_dates.append(line.replace("\n", ""))

    return spider_dates


def compare_dates():
    s_dates = process_data()
    dates = generate_date_list()
    sup_dates = []
    with open('data_supplement.csv', 'r', encoding='utf-8') as fr:
        lines = fr.readlines()
        for i, line in enumerate(lines):
            if line.startswith("20"):
                # print(i)
                sup_dates.append(line.replace("\n", ""))
    no_dates = []
    for d in dates:
        if d not in s_dates:
            no_dates.append(d)
            # print(d)
    for d in no_dates:
        if d not in sup_dates:
            print(d)
    # print(dates)
    # print(len(no_dates))
    return no_dates


def reform_data():
    data_list = []
    idx_list = []
    with open('data_supplement.csv', 'r', encoding='utf-8') as fr:
        lines = fr.readlines()
        for i, line in enumerate(lines):
            if line.startswith("20"):
                idx_list.append(i)
    # print(idx_list)

    with open('data_supplement.csv', 'r', encoding='utf-8') as fr:
        lines = fr.readlines()
        for i in idx_list:
            idx = 2
            # print(i)
            while idx < 56:
                arr = lines[i + idx].split(' ')
                river_name = arr[0]
                station_name = arr[1]
                water_loc = arr[2]
                flow = arr[3]
                try:
                    sediment_concentration = arr[4].replace("\n", "")
                except:
                    sediment_concentration = '-'
                dist = {
                    '日期': lines[i].replace("\n", ""),
                    '河名': river_name,
                    '站名': station_name,
                    '水位': water_loc,
                    '流量': flow,
                    '含沙量': sediment_concentration
                }
                print(dist)
                data_list.append(dist)
                idx += 1

    return data_list


def to_excel(data_list):
    df = pd.DataFrame(data_list, index=None)
    df.to_excel("水情数据3.xlsx", index=None, index_label=None, encoding='utf-8')


if __name__ == '__main__':
    to_excel(reform_data())
