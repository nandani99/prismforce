
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

f = open(r'C:\Users\itskr\Downloads\pf-sde-master\pf-sde-master\2-input.json')

data = json.load(f)
date = set()
mp_expend = {}
mp_revenue = {}


for i in data['expenseData']:
    timestamp = i['startDate']
    month = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    key = month
    date.add(key)
    key = key.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    if key in mp_expend:
        mp_expend[key]+=i["amount"]
    else:
        mp_expend[key] = i["amount"]



for i in data['revenueData']:
    timestamp = i['startDate']
    month = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    key = month
    date.add(key)
    key = key.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    if key in mp_revenue:
        mp_revenue[key]+=i["amount"]
    else:
        mp_revenue[key] = i["amount"]


#to get all the timestamps between the minimum and maximum one 
max_timestamp = max(date)
min_timestamp = min(date)

def generate_months(min_timestamp, max_timestamp):
    result = set()

    current = min_timestamp.replace(day=1)
    while current <= max_timestamp:
        result.add(current.strftime("%Y-%m-%d %H:%M:%S"))
        current += relativedelta(months=1)

    return result

months = generate_months(min_timestamp,max_timestamp)
months = sorted(months)

total_months = []
for i in months:
    dt = datetime.strptime(i, "%Y-%m-%d %H:%M:%S")
    iso = dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    total_months.append(iso)


ans = {}

for i in total_months:
    rev = 0
    exp = 0
    if i in mp_expend:
        exp = mp_expend[i]
    if i in mp_revenue:
        rev = mp_revenue[i]

    ans[i] = (rev-exp)


balance_list = []
for timestamp, amount in ans.items():
    balance = {
        "amount": amount,
        "startDate": timestamp[:-3] + "Z"
    }
    balance_list.append(balance)

result = {
    "balance": balance_list
}

json_data_output = json.dumps(result, indent=2)

print(json_data_output)


f.close()



