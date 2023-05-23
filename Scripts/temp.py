from fastapi import FastAPI
import requests
import json
from time import sleep
from Logs import logInfo

# Maintaining User Based on Strategis
with open("../Jsons/raw_details.json") as f:
    raw_details = json.load(f)

# Inserting all Strategies in the dictionary
userBasedOnStrategy = {}
strategywiseStock = {}
userWiseStockPurchased = {}

stockCount = {}

for strat in raw_details["STRATEGIES"]:
    userBasedOnStrategy[strat] = []
    stockCount[strat] = {}

# Loading Generated Profiles
with open("../Jsons/user_profile.json") as f:
    user_profiles = json.load(f)

for user in user_profiles:
    for strat in user_profiles[user]:
        userBasedOnStrategy[strat].append(user)
        if strat not in strategywiseStock.keys():
            strategywiseStock[strat] = user_profiles[user][strat]
for strat in strategywiseStock:
    for stock in strategywiseStock[strat]:
        stockCount[strat][stock] = 0
# for strat in userBasedOnStrategy:
#     for users in userBasedOnStrategy[strat]:
#         userWiseStockPurchased[users] = {}
#         for stock in strategywiseStock[strat]:
#             userWiseStockPurchased[users][stock] = False

for i in strategywiseStock:
    print(i," :: ",strategywiseStock[i])
for i in userBasedOnStrategy:
    print(i," :: ",userBasedOnStrategy[i])
for i in stockCount:
    print(i," :: ",stockCount[i])

def canOrder(order : dict):
    # Fetching details from dictionary
    strat = order["STRATEGY"]
    stock = order["INSTRUMENT"]
    position = order["POSITION"]

    # Check if the order is valid
    if len(userBasedOnStrategy[strat]) == 0:
        return {
            "Order Status" : "Failed",
            "Reason" : f"No user in {strat}"
        }
    
    if stock not in strategywiseStock[strat]:
        return {
            "Order Status" : "Failed",
            "Reason" : f"{stock} not found in {strat}"
        }
    if position == "BUY":
        if stockCount[strat][stock] == len(userBasedOnStrategy[strat]):
            return {
                "Order Status" : "Failed",
                "message":"No user available"
            }
        else:
            stockCount[strat][stock] = stockCount[strat][stock] + 1
            return {
                "Order Status" : "Accepted",
                "message":"Purchased"
            }
    else: 
        if stockCount[strat][stock] == 0:
            return {
                "Order Status" : "Failed",
                "message":"No buy, direct sell"
            }
        else:
            stockCount[strat][stock] = stockCount[strat][stock] - 1
            return {
                "Order Status" : "Accepted",
                "message":"Selled"
            }
        
    return {
        "Order Status" : "Failed",
        "Reason" : "Invalid Order"
    }

rees = canOrder({'STRATEGY': 'STRATEGY_G', 'INSTRUMENT': 'NTPC', 'POSITION': 'BUY'})
res = {"RESPONSE":rees}
print("Order response: {}".format(res['RESPONSE']))