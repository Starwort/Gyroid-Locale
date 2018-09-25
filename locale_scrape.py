from bs4 import BeautifulSoup as BS
import aiohttp
import asyncio

bugs_en = {}
bugs_fr = {}
bugs_de = {}
bugs_es = {}
bugs_it = {}

fish_en = {}
fish_fr = {}
fish_de = {}
fish_es = {}
fish_it = {}

deepsea_en = {}
deepsea_fr = {}
deepsea_de = {}
deepsea_es = {}
deepsea_it = {}

villagers_en = {}
villagers_fr = {}
villagers_de = {}
villagers_es = {}
villagers_it = {}

async def getkey(name):
    return name.lower().strip("\n").strip(" ").strip("*").replace(' ','_').replace('(','').replace(')','')

async def strip(x):
    return x.split("</a>")[-1].split("<small>")[0].strip("<td>").strip("</td>").strip()

async def getlocale(name):
    exceptions = {"Apple":"Apple (villager)","Frog":"Frog (fish)","Pearl oyster":"Pearl_oyster_(deep-sea_creature)",
     "Lobster":"Lobster (deep-sea creature)","Octopus":"Octopus (deep-sea creature)","Aurora":"Aurora (villager)",
     "Carmen":"Carmen (rabbit)","Cherry":"Cherry (villager)","Hazel":"Hazel (New Leaf)"}
    if name in exceptions:
         name = exceptions[name]   
    async with aiohttp.ClientSession() as session:
        async with session.get("https://animalcrossing.wikia.com/wiki/{}".format(name.replace(" ","_"))) as resp:
            data = await resp.read()
    parser = BS(data.decode("utf-8"),"html.parser")
    try:
        localetable = [x for x in parser.find_all("table") if "Regional names" in x.text][0]
        row = [x for x in localetable.find_all("tr") if "Regional names" in x.text][0]
    except:
        print(name)
        return name,name,name,name,name
    column = row.find_all("td")[1]
    fr = de = it = es = name
    for x in str(column).split("<br/>"):
        if "France" in x:
            fr = await strip(x)
        if "Germany" in x:
            de = await strip(x)
        if "Italy" in x:
            it = await strip(x)
        if "Spain" in x:
            es = await strip(x)
    return name, fr, de, es, it


async def bugs():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://animalcrossing.wikia.com/wiki/Bugs_(New_Leaf)") as resp:
            data = await resp.read()

    parser  = BS(data, "html.parser")
    bugtable = parser.find_all("table")[1].find_all("table")[0]
    rows = bugtable.find_all("tr")
    columns = [row.find_all("td") for row in rows if row.find_all("td")!=[]]
    listofbugs = []
    for x in range(0,len(columns)):
        name = columns[x][0].text.strip("\n").strip(" ").strip("*")
        listofbugs.append(name)
    return listofbugs

async def fish():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://animalcrossing.wikia.com/wiki/Fish_(New_Leaf)") as resp:
            data = await resp.read()

    parser  = BS(data, "html.parser")
    fishtable = parser.find_all("table")[1].find_all("table")[0]
    rows = fishtable.find_all("tr")
    columns = [row.find_all("td") for row in rows if row.find_all("td")!=[]]
    listoffish = []
    for x in range(0,len(columns)):
        name = columns[x][0].text.strip("\n").strip(" ").strip("*")
        listoffish.append(name)
    return listoffish

async def deepsea():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://animalcrossing.wikia.com/wiki/Deep-Sea_Creatures") as resp:
            data = await resp.read()

    parser  = BS(data, "html.parser")
    dstable = parser.find_all("table")[1].find_all("table")[0]
    rows = dstable.find_all("tr")
    columns = [row.find_all("td") for row in rows if row.find_all("td")!=[]]
    listofds = []
    for x in range(0,len(columns)):
        name = columns[x][0].text.strip("\n").strip(" ").strip("*")
        listofds.append(name)
    return listofds

async def villagers():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://animalcrossing.wikia.com/wiki/Villager_list_(New_Leaf)") as resp:
            data = await resp.read()

    parser  = BS(data, "html.parser")
    vtable = parser.find_all("table")[1].find_all("table")[0]
    rows = vtable.find_all("tr")
    columns = [row.find_all("td") for row in rows if row.find_all("td")!=[]]
    listofvillagers = []
    for x in range(0,len(columns)):
        name = columns[x][0].text.strip("\n").strip(" ").strip("*")
        listofvillagers.append(name)
    return listofvillagers

async def bugsearch(listofbugs):
    for bug in listofbugs:
        en, fr, de, es, it = await getlocale(bug)
        key = await getkey(bug)
        bugs_en[key] = en
        bugs_fr[key] = fr
        bugs_de[key] = de
        bugs_es[key] = es
        bugs_it[key] = it

async def fishsearch(listoffish):
    for fish in listoffish:
        en, fr, de, es, it = await getlocale(fish)
        key = await getkey(fish)
        fish_en[key] = en
        fish_fr[key] = fr
        fish_de[key] = de
        fish_es[key] = es
        fish_it[key] = it

async def seasearch(listofds):
    for ds in listofds:
        en, fr, de, es, it = await getlocale(ds)
        key = await getkey(ds)
        deepsea_en[key] = en
        deepsea_fr[key] = fr
        deepsea_de[key] = de
        deepsea_es[key] = es
        deepsea_it[key] = it

async def villagersearch(listofvillagers):
    for villager in listofvillagers:
        en, fr, de, es, it = await getlocale(villager)
        key = await getkey(villager)
        villagers_en[key] = en
        villagers_fr[key] = fr
        villagers_de[key] = de
        villagers_es[key] = es
        villagers_it[key] = it


async def yaml(dictie,yml):
    locale = yml.split(".")[1]
    message = f"{locale}:\n"
    listie = [f"    {x}: {dictie[x]}" for x in dictie]
    with open(yml,"w",encoding="utf-8") as file:
        file.write(message + "\n".join(listie))
    print(yml)
    
async def function():
    await bugsearch(await bugs())
    print("Bugs")
    await fishsearch(await fish())
    print("Fish")
    await seasearch(await deepsea())
    print("Deepsea")
    await villagersearch(await villagers())
    print("Villagers")
    await yaml(villagers_en,"villagers.en.yml")
    await yaml(villagers_de,"villagers.de.yml")
    await yaml(villagers_es,"villagers.es.yml")
    await yaml(villagers_fr,"villagers.fr.yml")
    await yaml(villagers_it,"villagers.it.yml")
    await yaml(bugs_en,"bugs.en.yml")
    await yaml(bugs_fr,"bugs.fr.yml")
    await yaml(bugs_es,"bugs.es.yml")
    await yaml(bugs_de,"bugs.de.yml")
    await yaml(bugs_it,"bugs.it.yml")
    await yaml(fish_en,"fish.en.yml")
    await yaml(fish_es,"fish.es.yml")
    await yaml(fish_de,"fish.de.yml")
    await yaml(fish_fr,"fish.fr.yml")
    await yaml(fish_it,"fish.it.yml")
    await yaml(deepsea_en,"deepsea.en.yml")
    await yaml(deepsea_es, "deepsea.es.yml")
    await yaml(deepsea_de,"deepsea.de.yml")
    await yaml(deepsea_it,"deepsea.it.yml")
    await yaml(deepsea_fr,"deepsea.fr.yml")
    print("ALL DONE!")


asyncio.get_event_loop().run_until_complete(function())
