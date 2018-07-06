import time

name = "sunjiajia"

if "sun" in name:
    print("ok")

print("*" * 30)

old_time = "Mon Jan 16 12:55:58 +0800 2017"
new_time = ""

time1 = time.strptime(old_time.replace("+0800", ""))
time2 = time.strftime("%Y-%m-%d %H:%M:%S", time1)
print(time1)
print(time2)

print("*" * 30)

user_api_url = "https://m.weibo.cn/api/container/getIndex?type=uid&value={uid}"

test_uids = [
    # suprsvn
    '3781960940',
    # AndroidTips
    '5082883214',
    # gitopen
    '6211974038'
]

start_urls = [user_api_url.format(uid=uid) for uid in test_uids]
print(start_urls[0])

print("*" * 30)

bbb = "2013-06-08"
result = bbb.split("-")
print(result)
year = int(result[0])
month = int(result[1])
day = int(result[2])

if month > 5:
    print(month)

print("*" * 30)

ccc = "2013-06-08 00:00:01"
temp = time.strptime(ccc,"%Y-%m-%d %H:%M:%S")

print(temp)
print(int(time.mktime(temp)))

print("*" * 30)

now_time = time.strftime('%Y-%m-%d %H:%M:%S')
print(now_time)

print("*" * 30)

cards = [
    {"name":"sun1"},
    {"name":"sun2"},
    {"name":"sun3"}
         ]
for card in cards:
    if cards.index(card) != 0:
        print(card['name'])
