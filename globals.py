def init():
    global l_arch
    global l_deck
    global l_include
    global l_exclude
    global officialAPIToken
    global unofficialAPIToken
    global databasename
    databasename = 'A:\ClashRoyaleMetaDBFile\SeasonX.db'
    deck_printer_path = "F:\Dropbox\Games\crmeta\\"
    # Define Tokens
    officialAPIToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjYyNTgwNTVkLTAyMDMtNDFhOS05NTRjLWUwNjNmYzk1ZDQ0ZCIsImlhdCI6MTY1NTE1NDEwMSwic3ViIjoiZGV2ZWxvcGVyLzZlYmYzNzdmLWVkNjQtMmFlZC02MjRhLWE3Nzg5YmM4OGZiNCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI3My43Ny41OC42MyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.4wG7WwYjTQQIkd5_czrhLtmh2str4V1OmPLdTSG2RIrMufqJfk_BYmmf_Xz98kASYUfCJxtygn3UuMFHR7y4SA"
    unofficialAPIToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTQ0MywiaWRlbiI6IjIyNzk4NjE5NzM3MTE1ODUyOCIsIm1k" \
                         "Ijp7InVzZXJuYW1lIjoiS2luZ0tvbmciLCJkaXNjcmltaW5hdG9yIjoiOTcxOSIsImtleVZlcnNpb24iOjN9LCJ0cyI6MTU" \
                         "3NjgwMjAxMTk1Mn0.tUBrvk38lBSrg9ilpshqBD9PbzFoOqImLVrM8hUucLg "
    # print these lists from the print_archetypes() function in the CRCU.xlsm file
    l_arch = [['Dual Lane', '3M'], ['Balloon', 'Cycle'], ['Balloon', 'Freeze'], ['Bridge Spam'],
              ['Beatdown', 'Dual Lane', '3M'], ['Bait'], ['Beatdown'], ['Beatdown', 'Elixir Golem'],
              ['Beatdown', 'Giant', 'Dual Lane'], ['Giant', 'Cycle'], ['Beatdown', 'Giant'],
              ['Beatdown', 'Graveyard', 'Giant'], ['Giant', 'Balloon'], ['Beatdown', 'Giant', 'Miner', 'Cycle'],
              ['Giant', 'Control'], ['Clone'], ['Beatdown', 'Giant'], ['Beatdown', 'Goblin Giant'],
              ['Beatdown', 'Goblin Giant'], ['Beatdown', 'Golem'], ['Beatdown', 'Balloon', 'Golem'],
              ['Beatdown', 'Golem'], ['Graveyard', 'Control'], ['Hog', 'Cycle'], ['Hog', 'Bait', 'Cycle'],
              ['Hog', 'Cycle'], ['Hog', 'Cycle'], ['Hog', 'Siege'], ['Hog', 'Siege', 'Bait', 'Cycle'],
              ['Hog', 'Control'], ['Siege'], ['Beatdown', 'Lavahound'], ['Beatdown', 'Balloon'], ['Beatdown', 'Miner'],
              ['Balloon', 'Cycle'], ['Miner', 'Bait'], ['Miner', 'Cycle', 'Balloon'], ['Miner', 'Control'],
              ['Miner', 'Cycle'], ['Hog', 'Miner'], ['Miner', 'Control', 'Cycle'], ['Miner', 'Cycle'],
              ['Miner', 'Cycle'], ['Bait', 'Control'], ['Miner', 'Control'], ['Hog', 'Miner'],
              ['Siege', 'Miner', 'Bait'], ['Siege', 'Cycle'], ['Rage'], ['Miner', 'Control'], ['Bridge Spam'],
              ['Royale giant', 'Beatdown'], ['Dual Lane'], ['Siege'], ['Siege'], ['Spawner'], ['Beatdown'],
              ['Beatdown'], ['None']]
    l_deck = ['3M No Pump', 'Balloon Cycle', 'Balloon Freeze', 'Bridge Spam', 'Classic 3M Pump', 'Classic Bait',
              'EG Healer', 'EG Sparky', 'Giant 3M', 'Giant Cycle', 'Giant Dbl Prince', 'Giant GY', 'Giant Loon',
              'Giant Miner', 'Giant Prince', 'Giant Skely Clone', 'Giant Sparky', 'Goblin Giant Sparky',
              'Goblin Giant Dbl Prince', 'Golem', 'Golem Balloon', 'Golem Lightning', 'GY Control', 'Hog 2.6',
              'Hog Bait', 'Hog Cycle', 'Hog EQ', 'Hog Mortar', 'Hog Mortar Bait', 'HogXNado', 'Icebow', 'LavaClone',
              'Lavaloon', 'Lavaminer', 'LJ Balloon', 'Miner Bait', 'Miner Balloon', 'Miner Cycle', 'Miner Cycle',
              'Miner Hog', 'Miner Poison', 'Miner Rocket', 'Miner WB', 'MK Bait', 'MK Control', 'MK Hog',
              'Mortar Miner Bait', 'Mortar Cycle', 'Noob Rage', 'Pekka Miner', 'Ram Rider Spam', 'RG', 'Royal Hogs',
              'Xbow 3.0', 'Xbow Misc', 'Ebarb Spawner', 'EGiant MW', 'EGiant No MW', 'No WC']
    l_include = [['three musketeers'], ['balloon'], ['balloon', 'freeze'], ['battle ram', 'p.e.k.k.a'],
                 ['three musketeers', 'elixir collector'], ['goblin barrel'], ['elixir golem', 'battle healer'],
                 ['elixir golem', 'sparky'], ['giant', 'three musketeers'], ['giant'],
                 ['giant', 'dark prince', 'prince'], ['giant', 'graveyard'], ['giant', 'balloon'], ['giant', 'miner'],
                 ['giant', 'prince'], ['giant skeleton', 'clone'], ['giant', 'sparky'], ['goblin giant', 'sparky'],
                 ['goblin giant', 'prince', 'dark prince'], ['golem'], ['golem', 'balloon'], ['golem', 'lightning'],
                 ['graveyard'], ['hog rider', 'musketeer', 'ice spirit', 'skeletons', 'fireball'],
                 ['hog rider', 'goblin barrel'], ['hog rider'], ['hog rider', 'earthquake'], ['hog rider', 'mortar'],
                 ['hog rider', 'mortar', 'goblin barrel'], ['hog rider', 'executioner', 'tornado'],
                 ['x-bow', 'ice wizard'], ['lava hound', 'clone'], ['lava hound', 'balloon'], ['lava hound', 'miner'],
                 ['balloon', 'lumberjack'], ['miner', 'goblin barrel'], ['miner', 'balloon'], ['miner', 'valkyrie'],
                 ['miner', 'skeletons'], ['miner', 'hog rider'], ['miner', 'poison'], ['miner', 'rocket'],
                 ['miner', 'wall breakers'], ['mega knight', 'goblin barrel'], ['mega knight'],
                 ['mega knight', 'hog rider'], ['mortar', 'miner', 'goblin gang'], ['mortar'],
                 ['rage', 'elite barbarians'], ['p.e.k.k.a', 'miner'], ['ram rider'], ['royal giant'], ['royal hogs'],
                 ['x-bow', 'archers'], ['x-bow'], ['elite barbarians', 'goblin hut'], ['electro giant', 'mother witch'],
                 ['electro giant'], ['']]
    l_exclude = [['elixir collector'], ['lavahound', 'miner'], [''], [''], [''],
                 ['giant', 'hog rider', 'lavahound', 'mortar'], ['sparky'], [''], [''], ['miner', 'balloon', 'prince'],
                 [''], [''], [''], [''], ['dark prince'], [''], [''], [''], ['sparky'], ['lightning', 'balloon'], [''],
                 [''], ['giant', 'golem'], [''], [''], ['goblin barrel', 'mortar', 'executioner'], [''],
                 ['goblin barrel'], [''], [''], [''], [''], ['miner'], [''], [''], ['mortar', 'hog rider'],
                 ['lava hound'], ['wall breakers'], ['giant', 'hog rider', 'lavahound', 'balloon'], ['mega knight'],
                 ['wall breakers'], [''], ['mega knight'], ['hog rider'], ['hog rider', 'goblin barrel'], [''], [''],
                 ['miner', 'hog rider'], ['balloon'], [''], [''], [''], [''], [''], ['ice wizard', 'archers'], [''],
                 [''], ['mother witch'],
                 ['balloon', 'miner', 'giant', 'golem', 'goblin giant', 'royal giant', 'lava hound', 'mortar', 'x-bow',
                  'goblin barrel', 'ram rider', 'battle ram', 'hog rider', 'graveyard', 'three musleteers',
                  'elixir golem', 'electro giant']]
    l_cards = []
