import datetime
import json
import requests


def newton(update, context):
    update.message.reply_text(juvenes())


def reaktori(update, context):
    update.message.reply_text(returnreaktori())


def hertsi(update, context):
    update.message.reply_text(returnhertsi())


def juvenes(KitchenId="6", MenuTypeId="60"):
    try:
        date = str(datetime.date.today())
        day = date[8:]
        month = date[5:7]

        teksti = ""
        url = "http://www.juvenes.fi/DesktopModules/Talents.LunchMenu/LunchMenuServices.asmx/GetMenuByDate?KitchenId=" \
              + KitchenId + "&MenuTypeId=" + MenuTypeId + "&Date='" + day + "/" + month + "'&lang='fi'&format=json"
        x = requests.get(url)

        if x.status_code != 200:
            return "Error " + x.status_code + "occured when retrieving data."

        x = x.content

        menu = json.loads(json.loads(x, encoding='utf-8')['d'])

        for item in menu["MealOptions"]:
            first_menu_item = item["MenuItems"][0]
            name = first_menu_item["Name"]
            diets = first_menu_item["Diets"]
            teksti += "• " + name + " " + diets + "\n"

        if not teksti:
            teksti = "Ei mitään syötävää!\n\n"
    except ValueError:
        teksti = "Ei mitään syötävää!\n\n"
    return teksti


def returnreaktori(compact=False):
    date = str(datetime.date.today())

    url = "https://www.fazerfoodco.fi/modules/json/json/Index?costNumber=0812&language=fi"
    x = requests.get(url)

    if x.status_code != 200:
        return "Error " + x.status_code + "occured when retrieving data."

    x = x.content.decode("utf-8")
    x = x.replace("  ", "")

    teksti = ""
    menu = json.loads(x, encoding='utf-8')

    for item in menu["MenusForDays"]:
        if date in item["Date"]:
            for set_menu in item["SetMenus"]:
                if compact is True:
                    if set_menu["Name"] == "lounas":
                        if set_menu["Name"] not in teksti:
                            teksti += set_menu["Name"] + ": " + "\n"
                        for menu_component in set_menu["Components"]:
                            teksti += "    • " + menu_component + "\n"

                else:
                    if set_menu["Name"] not in teksti:
                        teksti += set_menu["Name"] + ": " + "\n"
                    for menu_component in set_menu["Components"]:
                        teksti += "    • " + menu_component + "\n"
            teksti = teksti.replace("xc2xb4", "'")
            aukioloaika = str(item["LunchTime"])

            teksti += "\nReaktori on avoinna " + aukioloaika + "\n"

    if not teksti:
        teksti = "Ei mitään syötävää!\n\n"

    return teksti


def returnhertsi(compact=False):
    date = str(datetime.date.today())
    day = date[8:]
    month = date[5:7]
    year = date[:4]

    url = "http://www.sodexo.fi/ruokalistat/output/daily_json/12812/" + year + "/" + month + "/" + day + "/fi"
    x = requests.get(url)

    if x.status_code != 200:
        return "Error " + x.status_code + "occured when retrieving data."

    x = x.content.decode("utf-8")

    menu = json.loads(x, encoding='utf-8')

    teksti = "\n⚡️" + "️Hertsissä tänään" + "⚡️\n\n"

    try:
        for item in menu["courses"]:

            # tarkasta erikoisruokavaliot

            if "properties" in item.keys():
                properties = item["properties"] + "\n"
            else:
                properties = "\n"

            # tulosta compact modessa vain 2,60 maksavat ruuat
            if compact is True:
                if "2,60" in item["price"]:
                    teksti += item["category"] + ":\n"
                    teksti += "    • " + item["title_fi"] + properties

            # muussa modessa tulosta kaikki ruuat
            else:
                teksti += item["category"] + ":\n"
                teksti += "    • " + item["title_fi"] + properties

    except KeyError:
        teksti += "Ei mitään syötävää!\n\n"

    teksti += "\nHertsi on avoinna Ma-Pe 10.30 - 15.00, kahvila Bitti palvelee klo 08.00 - 17.00 Ma-Pe"

    return teksti


def returnmenu():
    päämuuttuja = "⚖️ Newtonissa tarjolla ⚖️\n\n"

    päämuuttuja += juvenes("6", "60")
    päämuuttuja += "\nRavintola Newton palvelee yleensä ma-to 10.30-16.00 ja pe 10.30-15.00" + "\n\n" + "🍛 Sååsibaarissa 🍛\n\n"
    päämuuttuja += juvenes("60038", "77")
    päämuuttuja += "SÅÅSBAR on avoinna ma-pe 10.30-19.00" + "\n\n" + "🍔 Fusarissa 🍔\n\n"
    päämuuttuja += juvenes("60038", "3")
    päämuuttuja += "Fusion Kitchen on avoinna ma-pe 10.30-18.45, Café Konehuone palvelee ma-pe klo 8-19" + "\n"

    päämuuttuja += "\n☢️ Reaktori tarjoaa ☢️\n\n"
    päämuuttuja += returnreaktori(True)  # reaktorin tiedot

    päämuuttuja += returnhertsi(True)  # hertsin tiedot

    päämuuttuja += "\n\nFor more options, see /fullmenu"

    return päämuuttuja

def returnfullmenu():
    päämuuttuja = "⚖️ Newtonissa tarjolla ⚖️\n\n"

    päämuuttuja += juvenes("6", "60")
    päämuuttuja += "\nRavintola Newton palvelee yleensä ma-to 10.30-16.00 ja pe 10.30-15.00" + "\n\n" + "🍛 Sååsibaarissa 🍛\n\n"
    päämuuttuja += juvenes("60038", "77")
    päämuuttuja += "\nSÅÅSBAR on avoinna ma-pe 10.30-19.00" + "\n\n" + "🍔 Fusarissa 🍔\n\n"
    päämuuttuja += juvenes("60038", "3")
    päämuuttuja += "\nFusion Kitchen on avoinna ma-pe 10.30-18.45, Café Konehuone palvelee ma-pe klo 8-19" + "\n"

    päämuuttuja += "\n☢️ Reaktori tarjoaa ☢️\n\n"
    päämuuttuja += returnreaktori(False)  # reaktorin tiedot

    päämuuttuja += returnhertsi(False)  # hertsin tiedot

    return päämuuttuja

def menu(update, context):
    update.message.reply_text(returnmenu())

def fullmenu(update, context):
    update.message.reply_text(returnfullmenu())
