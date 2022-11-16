from map import Map
import time
import os
import json
from helicopter import Helicompter as Helico
from pynput import keyboard
from clouds import Clouds

TICK_SLEEP = 0.05
TREE_UPDATE = 5
CLOUDS_UPDATE = 50
FIRE_UPDATE = 10
MAP_W, MAP_H = 20, 10
MOVES = {'ц': (-1, 0), 'в': (0, 1), 'ы': (1, 0), 'ф':(0, -1)}
# f - сохранение, g - восстановление
field = Map(MAP_W, MAP_H)
helico = Helico(MAP_W, MAP_H)
clouds = Clouds(MAP_W, MAP_H)

def game_over():
    print('XXXXXXXXXXXXXXXXXXX')
    print('                   ')
    print('GAME OVER, YOUR SCORE IS', helico.score)
    print('                   ')
    print('XXXXXXXXXXXXXXXXXXX')


def process_key(key):
    global helico, tick, clouds, field
    c = key.char.lower()
    if c in MOVES.keys():
        dx, dy = MOVES[c][0], MOVES[c][1]
        helico.move(dx, dy)
    if c == 'а':
        data = {'helicopter': helico.export_data(), 'clouds': clouds.export_data(), 'field': field.export_data(), 'tick': tick}
        with open('level.json', 'w') as lvl:
            json.dump(data, lvl)
    if c == 'п':
        with open('level.json', 'r') as lvl:
            data = json.load(lvl)
            helico.import_data(data['helicopter'])
            tick = data['tick'] or 1
            field.import_data(data['field'])
            clouds.import_data(data['clouds'])


listener = keyboard.Listener(
    on_press=None,
    on_release=process_key)
listener.start()

tick = 1

while True:
    os.system('clear')
    field.process_helicopter(helico, clouds)
    helico.print_menu()
    field.print_map(helico, clouds)
    print('Tick', tick)
    tick += 1
    time.sleep(TICK_SLEEP)
    if (tick % TREE_UPDATE == 0):
        field.generate_tree()
    if (tick % FIRE_UPDATE == 0):
        field.update_fires()
    if (tick % CLOUDS_UPDATE == 0):
        clouds.update()


