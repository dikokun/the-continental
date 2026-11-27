# Slate for THE DAYWATCH — Thursday 26 November 2026.
# Every fact verified Thu 2026-11-26 in the wire sweeps (Reuters/AP/ONS/
# KCNA/dpa/FOX Weather/NPR). Day-anchor audit: stories that happened
# earlier are run only as their Thursday development, with the earlier
# day named in the deck, or excluded in DATE_CHECK.

HEROES = [
    dict(n=1, region="EUROPE", field="WAR", chip="CONFIRMED", part="NIGHT", hour=1.0,
         head="113 drones hit Kyiv",
         deck="Missiles and drones struck Desnianskyi; a shopping centre burns, 7 wounded; Zelensky warns of worse.",
         banner="KYIV HIT · 7 WOUNDED", scene="kyiv", fig="113 DRONES"),
    dict(n=2, region="AMERICAS", field="WEATHER", chip="CONFIRMED", part="AFTERNOON", hour=14.7,
         head="Parade grounded",
         deck="Macy's parade postponed — a first in 100 years. 81.5M travel; gusts 65 mph; nearly 1M homes dark.",
         banner="A FIRST IN 100 YEARS", scene="storm", fig="81.5M"),
    dict(n=3, region="EUROPE", field="POLITICS", chip="REPORTED", part="MORNING", hour=10.0,
         head="€45bn loan fight",
         deck="Summit ends without a deal: 24 of 27 back Kyiv's €45bn loan, but the €1.58tn budget fight rolls to December.",
         banner="MERZ: “27, NOT 23 OR 24”", scene="summit", fig="€45BN"),
]

MIDS = [
    dict(n=4, region="MIDDLE EAST", field="GAZA", chip="CONFIRMED", part="NIGHT", hour=0.5, fig="9 DEAD",
         head="Nine killed in Gaza",
         deck="A deputy minister is among them — the third straight night of strikes despite the year-old ceasefire."),
    dict(n=5, region="ASIA", field="NORTH KOREA", chip="OFFICIAL", part="NIGHT", hour=2.0, fig="TACTICAL NUKES",
         head="Kim tours nuke plants",
         deck="Orders a wider tactical deployment. KCNA calls the status “absolutely inviolable”."),
    dict(n=6, region="ASIA", field="MINE", chip="CONFIRMED", part="MORNING", hour=5.0, fig="13 + 13",
         head="Bogor mine: 13 dead",
         deck="Thirteen dead are confirmed, 13 still trapped; rain halts the search and police open a criminal probe."),
    dict(n=7, region="EUROPE", field="MIGRATION", chip="OFFICIAL", part="AFTERNOON", hour=13.0, fig="77,000",
         head="Net migration: 77,000",
         deck="The lowest since 1997: down from 204,000 a year ago and 92% below the 2023 peak, says the ONS."),
    dict(n=8, region="EUROPE", field="SECURITY", chip="OFFICIAL", part="MORNING", hour=7.0, fig="17 RAIDS",
         head="Cologne plot: two held",
         deck="Two Iraqi suspects are held after 250 officers raided 17 addresses over the synagogue bomb plot."),
    dict(n=9, region="AFRICA", field="EGYPT", chip="OFFICIAL", part="MORNING", hour=10.5, fig="31 DEAD",
         head="Admits 110 km/h",
         deck="The driver is arrested and admits 110 km/h; the tanker fire itself was Wednesday's news."),
    dict(n=11, region="AMERICAS", field="DIPLOMACY", chip="REPORTED", part="AFTERNOON", hour=15.0, fig="NO CEASEFIRE",
         head="Kushner: no ceasefire",
         deck="Kushner says Putin is “not interested” in a ceasefire; the territorial gap cannot be bridged."),
    dict(n=12, region="ASIA", field="MARKETS", chip="CONFIRMED", part="MORNING", hour=6.2, fig="+1.4%",
         head="Asia shrugs off tariffs",
         deck="Asia rallies, shrugging off the tariff plan: Nikkei +1.4% and Kioxia +12.6% on its Nvidia pact."),
    dict(n=14, region="MIDDLE EAST", field="HORMUZ", chip="CLAIM", part="MORNING", hour=8.0, fig="2M BARRELS",
         head="Hormuz tanker mined",
         deck="The IRGC claims a supertanker was mined at Hormuz; the UK logs a blast near a tanker off Dubai."),
]

ALSO = [
    (10, "EUROPE", "UA", "Ukraine — Drones hit Nevinnomyssk plant in Russia"),
    (13, "ASIA", "KR", "S. Korea — Central bank hikes policy rate to 3.25%"),
    (15, "EUROPE", "UA", "Ukraine — Kyiv claims 2,319 Russian losses in a day"),
    (16, "EUROPE", "UA", "Ukraine — Kherson: 33 settlements struck by fire"),
    (17, "EUROPE", "UA", "Ukraine — Zaporizhzhia: four investigators killed"),
    (18, "EUROPE", "UA", "Ukraine — Kryvyi Rih hit by drone waves overnight"),
    (19, "EUROPE", "RU", "Russia — Duma passes a record wartime arms budget"),
    (20, "EUROPE", "LT", "Lithuania — Call to list the GRU as a terrorist body"),
    (21, "EUROPE", "IT", "Italy — Meloni: war must not spread past Ukraine"),
    (22, "EUROPE", "RU", "Russia — Lavrov: Washington grasps the root causes"),
    (23, "AMERICAS", "US", "US — Nvidia halts SE-Asia shipments of its AI chips"),
    (24, "GLOBAL", "GL", "Global — RAM prices triple as AI demand surges"),
    (25, "AMERICAS", "US", "US — New York bans AI bots that pose as humans"),
    (26, "AMERICAS", "US", "US — 40+ attorneys general fight chat-data auction"),
    (27, "EUROPE", "EU", "EU — Academy breach: data stolen in cyber attack"),
    (28, "GLOBAL", "GL", "Global — Salt Typhoon turns to AI hacking tools"),
    (29, "GLOBAL", "GL", "Global — Gold slumps ~3% as rate-hike bets build"),
    (30, "AMERICAS", "US", "US — FCC clears orbital data centres in ruling"),
    (31, "ASIA", "MM", "Myanmar — Junta rejects parts of the ICJ ruling"),
    (32, "MIDDLE EAST", "PS", "Gaza — Storm threat: 1.7M people in tents at risk"),
    (33, "AMERICAS", "US", "US — NFL Thanksgiving: Bears, Eagles, Bills win late"),
    (34, "AMERICAS", "US", "US — Rams beat Packers 26-13 (played Wed. Eve)"),
    (35, "OCEANIA", "AU", "Australia — ASX 200 index closes +0.8% at 8,764"),
    (36, "AMERICAS", "US", "US — Wall Street shut for the Thanksgiving holiday"),
]

REGION_COUNTS = "EUROPE 14 · AMERICAS 9 · ASIA 5 · MIDDLE EAST 3 · GLOBAL 3 · AFRICA 1 · OCEANIA 1 = 36 STORIES"

RAIL = [("113", "DRONES OVER KYIV (Nº1)"), ("81.5M", "US TRAVELLERS (Nº2)"),
        ("€45BN", "UKRAINE LOAN FOUGHT OVER (Nº3)"), ("77,000", "UK NET MIGRATION (Nº7)"),
        ("31", "DEAD IN GIZA FIRE (Nº9)"), ("2,319", "LOSSES KYIV CLAIMS (Nº15)")]

DATE_CHECK = [
    ("WED 25", "Giza crash itself, 18:08 — the fire was Wednesday's news; the driver's arrest and his confession are Thursday's"),
    ("WED 25", "Shenzhou-24 docks at Tiangong — Wednesday's story, told there, not repeated as Thursday's"),
    ("TUE 24", "Huawei Brooklyn verdict — Tuesday's verdict, left out of Thursday's edition in full"),
    ("SUN 22", "COP31 collapse — Sunday's collapse, left out; only its fallout would run"),
    ("MON 23", "Bogor mine floods — the flood was Monday's; Thursday's news is the toll, the search and the police probe"),
    ("SAT 28", "Macy's parade flies — the balloons fly Saturday; Thursday's news is the postponement itself"),
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
