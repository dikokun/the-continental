# Slate for THE DAYWATCH — Thursday 26 November 2026.
# Every fact verified Thu 2026-11-26 in the wire sweeps (Reuters/AP/ONS/
# KCNA/dpa/FOX Weather/NPR). Day-anchor audit: stories that happened
# earlier are run only as their Thursday development, with the earlier
# day named in the deck, or excluded in DATE_CHECK.

HEROES = [
    dict(n=1, region="EUROPE", field="WAR", chip="CONFIRMED", part="NIGHT", hour=1.0,
         head="KYIV HIT BY 113 DRONES",
         deck="Missiles and drones struck Desnianskyi; a shopping centre burns, 7 wounded; Zelensky warns of worse.",
         banner="KYIV HIT OVERNIGHT · 7 WOUNDED", scene="kyiv", fig="113 DRONES"),
    dict(n=2, region="AMERICAS", field="WEATHER", chip="CONFIRMED", part="AFTERNOON", hour=14.7,
         head="PARADE GROUNDED",
         deck="Macy's parade postponed — a first in 100 years. 81.5M travel; gusts 65 mph; 400,000+ homes dark.",
         banner="A FIRST IN 100 YEARS", scene="storm", fig="81.5M"),
    dict(n=3, region="EUROPE", field="POLITICS", chip="REPORTED", part="MORNING", hour=10.0,
         head="€45BN LOAN FIGHT",
         deck="Brussels wrestles the €1.58tn 2028–34 budget and Kyiv's loan, racing to lock both before Le Pen.",
         banner="MERZ: “27, NOT 23 OR 24”", scene="summit", fig="€45BN"),
]

MIDS = [
    dict(n=4, region="MIDDLE EAST", field="GAZA", chip="CONFIRMED", part="NIGHT", hour=0.5, fig="9 DEAD",
         head="NINE KILLED IN GAZA",
         deck="A deputy minister is among them — the third straight night of strikes despite the year-old ceasefire."),
    dict(n=5, region="ASIA", field="NORTH KOREA", chip="OFFICIAL", part="NIGHT", hour=2.0, fig="TACTICAL NUKES",
         head="KIM TOURS NUCLEAR PLANTS",
         deck="Orders a wider tactical deployment. KCNA calls the status “absolutely inviolable”."),
    dict(n=6, region="ASIA", field="MINE", chip="CONFIRMED", part="MORNING", hour=5.0, fig="13 + 13",
         head="BOGOR MINE: 13 DEAD",
         deck="Thirteen dead are confirmed and 13 still trapped; rain halts the search and six of the dead are named."),
    dict(n=7, region="EUROPE", field="MIGRATION", chip="OFFICIAL", part="AFTERNOON", hour=13.0, fig="77,000",
         head="NET MIGRATION: 77,000",
         deck="The lowest since 1997: down from 204,000 a year ago and 92% below the 2023 peak, says the ONS."),
    dict(n=8, region="EUROPE", field="SECURITY", chip="OFFICIAL", part="MORNING", hour=7.0, fig="17 RAIDS",
         head="COLOGNE PLOT: TWO HELD",
         deck="Two Iraqi suspects are held after 250 officers raided 17 addresses over the synagogue bomb plot."),
    dict(n=9, region="AFRICA", field="EGYPT", chip="OFFICIAL", part="MORNING", hour=10.5, fig="31 DEAD",
         head="DRIVER ADMITS 110 KM/H",
         deck="The driver is arrested and admits 110 km/h; the tanker fire itself was Wednesday's news."),
    dict(n=10, region="EUROPE", field="WAR", chip="REPORTED", part="NIGHT", hour=1.5, fig="NEVINNOMYSSK",
         head="DRONES HIT RUSSIAN PLANT",
         deck="Ukrainian drones hit a power plant at Nevinnomyssk in Stavropol; a fire is reported at the site."),
    dict(n=11, region="AMERICAS", field="DIPLOMACY", chip="REPORTED", part="AFTERNOON", hour=15.0, fig="NO CEASEFIRE",
         head="KUSHNER: NO CEASEFIRE",
         deck="Kushner says Putin is “not interested” in a ceasefire; the territorial gap cannot be bridged."),
    dict(n=12, region="ASIA", field="MARKETS", chip="CONFIRMED", part="MORNING", hour=6.2, fig="+1.4%",
         head="ASIA SHRUGS OFF TARIFFS",
         deck="Asia rallies, shrugging off the tariff plan: Nikkei +1.4% and Kioxia +12.6% on its Nvidia pact."),
    dict(n=13, region="ASIA", field="KOREA", chip="OFFICIAL", part="NIGHT", hour=2.5, fig="3.25%",
         head="KOREA HIKES RATE",
         deck="The Bank of Korea hikes to 3.25%, a two-year high — the third rise of 2026, at the year's last meeting."),
    dict(n=14, region="MIDDLE EAST", field="HORMUZ", chip="CLAIM", part="MORNING", hour=8.0, fig="2M BARRELS",
         head="TANKER ‘MINED’ AT HORMUZ",
         deck="The IRGC claims a supertanker was mined at Hormuz; the UK logs a blast near a tanker off Dubai."),
    dict(n=15, region="EUROPE", field="WAR", chip="CLAIM", part="MORNING", hour=7.4, fig="2,319",
         head="KYIV CLAIMS 2,319 LOSSES",
         deck="Kyiv claims 2,319 Russian losses in one day; November passes October's record inside 25 days."),
]

ALSO = [
    (16, "EUROPE", "UA", "Kherson: 33 settlements struck"),
    (17, "EUROPE", "UA", "Zaporizhzhia: 4 investigators dead"),
    (18, "EUROPE", "UA", "Kryvyi Rih: drone waves overnight"),
    (19, "EUROPE", "RU", "Duma: record arms budget passed"),
    (20, "EUROPE", "LT", "Lithuania: list GRU as terrorists"),
    (21, "EUROPE", "IT", "Meloni: war must not spread"),
    (22, "EUROPE", "RU", "Lavrov: US grasps root causes"),
    (23, "AMERICAS", "US", "Nvidia halts SE-Asia shipments"),
    (24, "GLOBAL", "GL", "RAM prices triple on AI demand"),
    (25, "AMERICAS", "US", "NY bans AI bots posing as human"),
    (26, "AMERICAS", "US", "40+ AGs fight chat-data auction"),
    (27, "EUROPE", "EU", "EU Academy breach: data stolen"),
    (28, "GLOBAL", "GL", "Salt Typhoon turns to AI hacking"),
    (29, "GLOBAL", "GL", "Gold slumps ~3% on hike bets"),
    (30, "AMERICAS", "US", "FCC clears orbital data centres"),
    (31, "ASIA", "MM", "Myanmar rejects ICJ ruling parts"),
    (32, "MIDDLE EAST", "PS", "Storm threat: 1.7M in Gaza tents"),
    (33, "AMERICAS", "US", "NFL: Bears-Lions, Eagles-Cowboys"),
    (34, "AMERICAS", "US", "Rams beat Packers 26-13 (Eve)"),
    (35, "OCEANIA", "AU", "ASX 200 closes +0.8% at 8,764"),
    (36, "AMERICAS", "US", "Wall Street shut for Thanksgiving"),
]

REGION_COUNTS = "EUROPE 14 · AMERICAS 9 · ASIA 5 · MIDDLE EAST 3 · GLOBAL 3 · AFRICA 1 · OCEANIA 1 = 36 STORIES"

RAIL = [("113", "DRONES OVER KYIV (Nº1)"), ("81.5M", "US TRAVELLERS (Nº2)"),
        ("€45BN", "UKRAINE LOAN FOUGHT OVER (Nº3)"), ("77,000", "UK NET MIGRATION (Nº7)"),
        ("31", "DEAD IN GIZA FIRE (Nº9)"), ("2,319", "LOSSES KYIV CLAIMS (Nº15)")]

DATE_CHECK = [
    ("Giza tanker crash itself", "WED 25, 18:08 — Thursday's news is the driver's arrest"),
    ("Shenzhou-24 docks at Tiangong", "WED 25"),
    ("Huawei Brooklyn verdict", "TUE 24"),
    ("COP31 collapse", "SUN 22"),
    ("Bogor mine floods", "MON 23 — Thursday's news is the toll and the search"),
    ("Macy's parade flies", "SAT 28 — not yet"),
]

PINS = {1: (0.565, 0.14), 2: (0.13, 0.32), 3: (0.475, 0.16), 4: (0.545, 0.42),
        5: (0.83, 0.28), 6: (0.755, 0.68), 7: (0.44, 0.10), 8: (0.475, 0.13),
        9: (0.52, 0.52), 10: (0.60, 0.10), 11: (0.15, 0.28), 12: (0.815, 0.30),
        13: (0.835, 0.27), 14: (0.63, 0.38), 15: (0.575, 0.13),
        16: (0.555, 0.17), 17: (0.56, 0.16), 18: (0.55, 0.155), 19: (0.62, 0.08),
        20: (0.52, 0.09), 21: (0.485, 0.20), 22: (0.615, 0.09), 23: (0.14, 0.30),
        24: (0.50, 0.50), 25: (0.155, 0.27), 26: (0.15, 0.31), 27: (0.48, 0.15),
        28: (0.78, 0.32), 29: (0.50, 0.145), 30: (0.145, 0.29), 31: (0.735, 0.42),
        32: (0.55, 0.44), 33: (0.135, 0.26), 34: (0.075, 0.33), 35: (0.875, 0.82),
        36: (0.16, 0.29)}
