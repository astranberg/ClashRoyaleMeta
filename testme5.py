import csv


def makeunique_multi(l):
    check = set()
    res = []
    for i in l:
        x = ''
        for j in i:
            x = x + (j)
        if not x in check:
            res.append(i)
            check.add(x)
        else:
            pass
    return res


lUnknownDecks = [{'name': 'Golem', 'id': 26000009, 'level': 7, 'maxLevel': 8, 'iconUrls': {'medium': 'https://api-assets.clashroyale.com/cards/300/npdmCnET7jmVjJvjJQkFnNSNnDxYHDBigbvIAloFMds.png'}}, {'name': 'Night Witch', 'id': 26000048, 'level': 3, 'maxLevel': 5, 'iconUrls': {'medium': 'https://api-assets.clashroyale.com/cards/300/NpCrXDEDBBJgNv9QrBAcJmmMFbS7pe3KCY8xJ5VB18A.png'}}, {'name': 'Lumberjack', 'id': 26000035, 'level': 3, 'maxLevel': 5, 'iconUrls': {'medium': 'https://api-assets.clashroyale.com/cards/300/E6RWrnCuk13xMX5OE1EQtLEKTZQV6B78d00y8PlXt6Q.png'}}, {'name': 'Magic Archer', 'id': 26000062, 'level': 3, 'maxLevel': 5, 'iconUrls': {'medium': 'https://api-assets.clashroyale.com/cards/300/Avli3W7BxU9HQ2SoLiXnBgGx25FoNXUSFm7OcAk68ek.png'}}, {'name': 'Baby Dragon', 'id': 26000015, 'level': 6, 'maxLevel': 8, 'iconUrls': {'medium': 'https://api-assets.clashroyale.com/cards/300/cjC9n4AvEZJ3urkVh-rwBkJ-aRSsydIMqSAV48hAih0.png'}}, {'name': 'Dark Prince', 'id': 26000027, 'level': 5, 'maxLevel': 8, 'iconUrls': {'medium': 'https://api-assets.clashroyale.com/cards/300/M7fXlrKXHu2IvpSGpk36kXVstslbR08Bbxcy0jQcln8.png'}}, {'name': 'Mega Minion', 'id': 26000039, 'level': 8, 'maxLevel': 11, 'iconUrls': {'medium': 'https://api-assets.clashroyale.com/cards/300/-T_e4YLbuhPBKbYnBwQfXgynNpp5eOIN_0RracYwL9c.png'}}, {'name': 'Tornado', 'id': 28000012, 'level': 5, 'maxLevel': 8, 'iconUrls': {'medium': 'https://api-assets.clashroyale.com/cards/300/QJB-QK1QJHdw4hjpAwVSyZBozc2ZWAR9pQ-SMUyKaT0.png'}}]
# lUnknownDecks = [['a','b','c','d','e','f','g','h','i'],['a','b','c','d','e','f','g','h','i'],['x','b','c'],['x','b','c'],['z','b','c']]
a = ','.join([str(x['name']) for x in lUnknownDecks])
print(a)
