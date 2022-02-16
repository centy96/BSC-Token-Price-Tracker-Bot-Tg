import requests
import time

def get_price(token):
    responce = requests.get(url=f"https://api.pancakeswap.info/api/v2/tokens/{token}")
    data = responce.json()
    price1 = float(data["data"]["price"])
    return price1

def calcolo_incremento(price_f, price_i):
    incremento = ((price_f - price_i)/price_i) * 100
    return incremento

def get_info(token):
    try:
        responce = requests.get(url=f"https://api.pancakeswap.info/api/v2/tokens/{token}")
        data = responce.json()
        stringa = (f"Link grafico PooCoin:\nhttps://poocoin.app/tokens/{token}\n\n")
        info_token = data["data"]
        for (key, value) in info_token.items():
            if key == "price":
                stringa += (f"PREZZO INIZIALE -----------> {value}$\n")
            else:
                stringa += (f"{key} -----------> {value}\n")
        return stringa
    except:
        stringa = "Token non valido"
        return stringa

def main_loop(update, contex,token, percentuale_riferimento,prezzo_riferimento):
    last_price = prezzo_riferimento
    update.message.reply_text("IL BOT E' ATTIVO 👀... \nRiceverai un messaggio appena il prezzo entrerà nel range di interesse! 📡")
    while True:
        time.sleep(120)
        price_f = (get_price(token))
        if price_f != last_price:
            var_prezzo_assoluto = calcolo_incremento(price_f, prezzo_riferimento)
            print(f"\nIl cambio rispetto al valore assoluto:\n{str(var_prezzo_assoluto)}%")
            if var_prezzo_assoluto <= - int(percentuale_riferimento):
                update.message.reply_text(
                    f"\n🔻🔻🔻 IL PREZZO E' SCESO DEL {round((var_prezzo_assoluto),2)} % dall'ultimo avviso\nBuy more on PancakeSwap 💸:\nhttps://pancakeswap.finance/swap?outputCurrency={token}")
                prezzo_riferimento = price_f
                print(f"Il nuovo prezzo di riferimento è {price_f}$")
            var_prezzo = calcolo_incremento(price_f, last_price)
            print(f"\nVariazione ultimi 5 minuti:\n{var_prezzo}%")
            last_price = price_f
        
