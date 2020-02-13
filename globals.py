def init():
    global l_arch
    global l_deck
    global l_include
    global l_exclude
    global officialAPIToken
    global unofficialAPIToken
    global databasename
    databasename = 'Season8.db'
    # databasename = 'clans.db'
    # Define Tokens
    officialAPIToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9" \
                       ".eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImYyZjUzYmI2LWIyMDQtNGRkYi1" \
                       "iMGZjLTk0ZTE4ZWU3YzQ2ZSIsImlhdCI6MTU3NDYxNDgzMywic3ViIjoiZGV2ZWxvcGVyLzZlYmYzNzdmLWVkNjQtMmFlZC0" \
                       "2MjRhLWE3Nzg5YmM4OGZiNCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZl" \
                       "ciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI5OC4xOTUuMTU5LjgyIl0sInR5cGUiOiJjbGllbnQifV19.H13g" \
                       "VRs6fkSDyKEAAqPJKscx2AtN9sDbHaWNm2GSpgVZTTAe_sJM_yKkibMTCyOLu8kvOw7xcCOxycIydqqeUw "
    unofficialAPIToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTQ0MywiaWRlbiI6IjIyNzk4NjE5NzM3MTE1ODUyOCIsIm1k" \
                         "Ijp7InVzZXJuYW1lIjoiS2luZ0tvbmciLCJkaXNjcmltaW5hdG9yIjoiOTcxOSIsImtleVZlcnNpb24iOjN9LCJ0cyI6MTU" \
                         "3NjgwMjAxMTk1Mn0.tUBrvk38lBSrg9ilpshqBD9PbzFoOqImLVrM8hUucLg "
    l_arch = [['Dual Lane', '3M'], ['Balloon', 'Cycle'], ['Balloon', 'Freeze'], ['Bridge Spam'],
              ['Beatdown', 'Dual Lane', '3M'], ['Bait'], ['Control'], ['Beatdown', 'Elixir Golem'],
              ['Beatdown', 'Elixir Golem'], ['Beatdown', 'Giant', 'Dual Lane'], ['Giant', 'Cycle'],
              ['Beatdown', 'Giant'], ['Beatdown', 'Graveyard', 'Giant'], ['Beatdown', 'Giant', 'Miner', 'Cycle'],
              ['Clone'], ['Beatdown', 'Goblin Giant'], ['Beatdown', 'Golem'], ['Beatdown', 'Golem'],
              ['Graveyard', 'Control'], ['Hog', 'Cycle'], ['Hog', 'Bait', 'Cycle'], ['Hog', 'Cycle'], ['Hog', 'Cycle'],
              ['Hog', 'Siege'], ['Hog', 'Control'], ['Siege'], ['Beatdown', 'Lavahound'], ['Beatdown', 'Balloon'],
              ['Beatdown', 'Miner'], ['Balloon', 'Cycle'], ['Miner', 'Cycle', 'Balloon'], ['Miner', 'Control'],
              ['Miner', 'Cycle'], ['Hog', 'Miner'], ['Miner', 'Control', 'Cycle'], ['Miner', 'Cycle'],
              ['Miner', 'Cycle'], ['Miner', 'Control'], ['Siege', 'Miner', 'Bait'], ['Miner', 'Control'],
              ['Bridge Spam'], ['Royale giant'], ['Dual Lane'], ['Siege'], ['Siege'], ['Siege'], ['Spawner'],
              ['Spawner'], ['Spawner'], ['No Win Condition']]
    l_deck = ['3M No Pump', 'Balloon Cycle', 'Balloon Freeze', 'Bridge Spam', 'Classic 3M Pump', 'Classic bait',
              'Doulbe Prince', 'EG Sparky', 'EGNW', 'Giant 3M', 'Giant Cycle', 'Giant Dbl Prince', 'Giant GY',
              'Giant Miner', 'Giant Skele Clone', 'Goblin Giant Sparky', 'Golem', 'Golem Lightning', 'GY Control',
              'Hog 2.6', 'Hog Bait', 'Hog Cycle', 'Hog EQ', 'Hog Mortar', 'HogXNado', 'Icebow', 'LavaClone', 'Lavaloon',
              'Lavaminer', 'LJ Balloon', 'Miner Balloon', 'Miner Cycle', 'Miner Cycle', 'Miner Hog', 'Miner Poison',
              'Miner Rocket', 'Miner WB', 'MK Miner Control', 'Mortar Miner Bait', 'Pekka Miner', 'Ram Rider Spam',
              'RG', 'Royal hogs', 'Xbow 2.9', 'Xbow Misc', 'Classic Mortar', 'Spawner', 'Spawner', 'Spawner', 'No WC']
    l_include = [['three musketeers'], ['balloon'], ['balloon', 'freeze'], ['battle ram', 'p.e.k.k.a'],
                 ['three musketeers', 'elixir collector'], ['goblin barrel'], ['prince', 'dark prince'],
                 ['elixir golem', 'sparky'], ['elixir golem', 'night witch'], ['giant', 'three musketeers'], ['giant'],
                 ['giant', 'dark prince', 'prince'], ['giant', 'graveyard'], ['giant', 'miner'],
                 ['giant skeleton', 'clone'], ['goblin giant', 'sparky'], ['golem'], ['golem', 'lightning'],
                 ['graveyard'], ['hog rider', 'musketeer', 'ice spirit', 'skeletons', 'fireball'],
                 ['hog rider', 'goblin barrel'], ['hog rider'], ['hog rider', 'earthquake'], ['hog rider', 'mortar'],
                 ['hog rider', 'executioner'], ['x-bow', 'ice wizard'], ['lava hound', 'clone'],
                 ['lava hound', 'balloon'], ['lava hound', 'miner'], ['balloon', 'lumberjack'], ['miner', 'balloon'],
                 ['miner', 'valkyrie'], ['miner', 'skeletons'], ['miner', 'hog rider'], ['miner', 'poison'],
                 ['miner', 'rocket'], ['miner', 'wall breakers'], ['miner', 'mega knight'],
                 ['mortar', 'miner', 'goblin gang'], ['p.e.k.k.a', 'miner'], ['ram rider'], ['royal giant'],
                 ['royal hogs'], ['x-bow', 'archers'], ['x-bow'], ['mortar'], ['furnace', 'barbarian hut'],
                 ['furnace', 'goblin hut'], ['goblin hut', 'barbarian hut'], ['']]
    l_exclude = [['elixir collector', 'giant'], ['lavahound', 'miner'], ['lavahound'], [''], [''],
                 ['giant', 'hog rider', 'lavahound', 'mortar'], ['giant', 'hog rider', 'lavahound', 'balloon'], [''],
                 ['sparky'], [''], ['miner', 'balloon', 'prince', 'gaveyard', 'three musketeers'], [''], [''], [''],
                 [''], [''], ['lightning'], [''], ['giant', 'golem'], [''], [''],
                 ['goblin barrel', 'mortar', 'executioner'], [''], [''], [''], [''], [''], ['clone'], ['balloon'], [''],
                 ['lava hound'], ['wall breakers'], ['giant', 'hog rider', 'lavahound', 'balloon'], ['mega knight'],
                 ['wall breakers'], [''], [''], [''], [''], [''], [''], [''], [''], [''], ['ice wizard', 'archers'],
                 ['miner', 'hog rider'], [''], [''], [''],
                 ['balloon', 'miner', 'giant', 'golem', 'goblin giant', 'royal giant', 'lava hound', 'mortar', 'x-bow',
                  'goblin barrel', 'ram rider', 'battle ram', 'hog rider', 'graveyard', 'three musleteers',
                  'elixir golem']]
