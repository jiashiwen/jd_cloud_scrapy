import re

f = open("/Users/jiashiwen/aiprojects/jd_cloud_scrapy/pages/account-assets/coupon-questions.md")

text=f.read()
print(text)

# u=re.search(r"\\u[a-z|0-9]{4}",text,re.M).group(1)
# print(u)

print("\u003C".encode())