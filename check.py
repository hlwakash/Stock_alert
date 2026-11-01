import os, json, requests
T=os.environ["BOT_TOKEN"]; C=os.environ["CHAT_ID"]; U=os.environ["PRODUCT_URL"]
def send(m):
    requests.post(f"https://api.telegram.org/bot{T}/sendMessage",data={"chat_id":C,"text":m},timeout=15)
h={"User-Agent":"Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36","Accept-Language":"en-IN,en;q=0.9"}
r=requests.get(U,headers=h,timeout=20)
print("status",r.status_code)
if r.status_code!=200: raise SystemExit("Flipkart ne block kiya")
t=r.text.lower()
out=any(w in t for w in ["sold out","currently unavailable","notify me"])
ins=(not out) and ("add to cart" in t or "buy now" in t)
print("out:",out,"in_stock:",ins,"len:",len(t))
try: last=json.load(open("state.json"))
except Exception: last=None
if last is None:
    send("Bot chal gaya. Abhi stock: "+("HAI" if ins else "NAHI HAI"))
elif ins and not last.get("in_stock"):
    send(f"IN STOCK on Flipkart!\n{U}")
json.dump({"in_stock":ins},open("state.json","w"))
