from time import sleep
from fltk import rectangle
from fltk import polygone
from fltk import mise_a_jour
from fltk import efface_tout
from fltk import type_ev
from fltk import donne_ev
from fltk import touche
from fltk import ferme_fenetre
from fltk import cree_fenetre
from os import system
import os
import ast
import random
# dimensions du jeu
largeur_fenetre = 600
hauteur_fenetre = 400


def clear():
    sleep(1/30)
    _ = system('cls')


def direction_distance_check(map, dir, direction):
    """
    calculer la distance entre la position du joueur et le mur
    vérifier la direction dans laquelle le joueur face maintenant
    :param list map: la carte
    :param int dir: l'index de la direction de la liste
    :param list direction: list direction
    """
    global distance, x_player, y_player, direction_x, direction_y, facing
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == '@':
                x_player, y_player = x, y
                direction_x, direction_y = direction[dir]
                while map[y][x] != '*' and map[y][x] != 'o':
                    y += direction_y
                    x += direction_x
                if map[y][x] == 'o':
                    facing = True
                else:
                    facing = False
                if direction_y != 0:
                    distance = y_player - y
                else:
                    distance = x_player - x


def player_controller(touche, direction_x, direction_y, x_player, y_player):
    """
    contrôler le mouvement du joueur
    :param str touche: la saisie au clavier
    :param int direction_x: la coordonnée x de la direction
    :param int direction_y: la coordonnée y de la direction
    :param int x_player: la coordonnée x du joueur
    :param int y_player: la coordonnée y du joueur
    """
    global dir, map
    if touche == 'w' and \
       map[y_player+direction_y][x_player+direction_x] != '*':
        map[y_player][x_player], map[y_player+direction_y][x_player + direction_x] = map[y_player+direction_y][x_player+direction_x], map[y_player][x_player]
    if touche == 's' and \
       map[y_player-direction_y][x_player-direction_x] != '*':
        map[y_player][x_player], map[y_player-direction_y][x_player - direction_x] = map[y_player-direction_y][x_player-direction_x], map[y_player][x_player]
    if touche == 'd' and \
       map[y_player - direction_x*(-1)][x_player + direction_y*(-1)] != '*':
        map[y_player][x_player], map[y_player - direction_x*(-1)][x_player + direction_y * (-1)] = map[y_player - direction_x*(-1)][x_player + direction_y*(-1)], map[y_player][x_player]
    if touche == 'a' and \
       map[y_player + direction_x*(-1)][x_player - direction_y*(-1)] != '*':
        map[y_player][x_player], map[y_player + direction_x*(-1)][x_player - direction_y * (-1)] = map[y_player + direction_x*(-1)][x_player - direction_y*(-1)], map[y_player][x_player]
    if touche == 'q':
        dir = dir - 1 if dir > 0 else 3
    if touche == 'e':
        dir = dir + 1 if dir < 3 else 0


def affiche_mur():
    """
    affiche des mur
    """
    if direction_x == 0:
        x1, y1 = 0, 0
        x2, y2 = 0, hauteur_fenetre
        wall = 0
        for y in range(y_player, y_player + direction_y*abs(distance),
                       -1 if distance > 0 else 1):
            length = first_wall_length
            for i in range(0, wall):
                length += wall_length/(2**i)
            x3 = (length**2/(1+(hauteur_fenetre/largeur_fenetre)**2))**0.5
            y3 = (hauteur_fenetre/largeur_fenetre) * x3
            x4, y4 = x3, hauteur_fenetre - y3
            if map[y][x_player + direction_y] != '.':
                polygone([(x1, y1), (x2, y2), (x4, y4), (x3, y3)],
                         remplissage='blue' if map[y][x_player + direction_y] == 'o' else '')
            elif map[y][x_player + direction_y] != '*' and \
                    map[y][x_player + direction_y] != 'o':
                rectangle(x3, y3, x2, y4)
            if map[y][x_player - direction_y] != '.':
                polygone([(largeur_fenetre-x1, y1), (largeur_fenetre-x2, y2),
                         (largeur_fenetre-x4, y4), (largeur_fenetre-x3, y3)],
                         remplissage='blue' if map[y][x_player - direction_y] == 'o' else '')
            elif map[y][x_player - direction_y] != '*' and \
                    map[y][x_player - direction_y] != 'o':
                rectangle(largeur_fenetre-x3, y3, largeur_fenetre-x2, y4)
            x1, y1 = x3, y3
            x2, y2 = x4, y4
            wall += 1
        rectangle(x1, y1, largeur_fenetre - x1, hauteur_fenetre-y1,
                  remplissage='blue' if facing else '')


def affiche_mur2():
    """
    affiche des mur
    """
    if direction_y == 0:
        x1, y1 = 0, 0
        x2, y2 = 0, hauteur_fenetre
        wall = 0
        for x in range(x_player, x_player + direction_x*abs(distance),
                       -1 if distance > 0 else 1):
            length = first_wall_length
            for i in range(0, wall):
                length += wall_length/(2**i)
            x3 = (length**2/(1+(hauteur_fenetre/largeur_fenetre)**2))**0.5
            y3 = (hauteur_fenetre/largeur_fenetre) * x3
            x4, y4 = x3, hauteur_fenetre - y3
            if map[y_player - direction_x][x] != '.':
                polygone([(x1, y1), (x2, y2), (x4, y4), (x3, y3)],
                         remplissage='blue' if map[y_player - direction_x][x] == 'o' else '')
            elif map[y_player - direction_x][x] != '*' and \
                    map[y_player - direction_x][x] != 'o':
                rectangle(x3, y3, x2, y4)
            if map[y_player + direction_x][x] != '.':
                polygone([(largeur_fenetre-x1, y1), (largeur_fenetre-x2, y2),
                         (largeur_fenetre-x4, y4), (largeur_fenetre-x3, y3)],
                         remplissage='blue' if map[y_player + direction_x][x] == 'o' else '')
            elif map[y_player + direction_x][x] != '*' and \
                    map[y_player + direction_x][x] != 'o':
                rectangle(largeur_fenetre-x3, y3, largeur_fenetre-x2, y4)
            x1, y1 = x3, y3
            x2, y2 = x4, y4
            wall += 1
        rectangle(x1, y1, largeur_fenetre-x1, hauteur_fenetre-y1,
                  remplissage='blue' if facing else '')


def map_random(map, map_hauteur, map_largeur):
    """
    randomiser la carte
    :param list map: list de la carte
    :param int map_hauteur: le hauteur de la carte
    :parma int map_largeur: le largeur de la carte
    """
    global x_end, y_end
    for y in range(0, map_largeur):
        map.append([])
    for y in range(len(map)):
        for x in range(0, map_hauteur):
            map[y].append('*')
    map[0][0] = '.'
    point_x = 0
    point_y = 0
    visited = [(0, 0), (1, 0)]
    stack = [(0, 0)]
    while len(visited) < map_hauteur * map_largeur:
        lst_random = []

        while len(lst_random) == 0:
            if point_y - 2 >= 0 and (point_x, point_y - 2) not in visited:
                lst_random.append((point_x, point_y - 2))
            if point_y + 2 < map_hauteur and \
               (point_x, point_y + 2) not in visited:
                lst_random.append((point_x, point_y + 2))
            if point_x - 2 >= 0 and (point_x - 2, point_y) not in visited:
                lst_random.append((point_x - 2, point_y))
            if point_x + 2 < map_largeur and \
               (point_x + 2, point_y) not in visited:
                lst_random.append((point_x + 2, point_y))
            if len(lst_random) == 0:
                stack.remove(stack[len(stack) - 1])
                point_x, point_y = stack[len(stack) - 1]
        x, y = point_x, point_y
        point_x, point_y = random.choice(lst_random)
        map[point_y][point_x] = '.' if len(visited) != map_hauteur * map_largeur - 1 else 'o'

        if point_y == y:
            if point_x > x:
                map[point_y][point_x - 1] = '.'
            elif point_x < x:
                map[point_y][point_x + 1] = '.'
        if point_x == x:
            if point_y > y:
                map[point_y - 1][point_x] = '.'
            elif point_y < y:
                map[point_y + 1][point_x] = '.'

        stack.append((point_x, point_y))
        visited.append((point_x, point_y))

        if point_x+1 < map_largeur and (point_x+1, point_y) not in visited:
            visited.append((point_x+1, point_y))
            if point_y - 1 >= 0 and (point_x+1, point_y - 1) not in visited:
                visited.append((point_x+1, point_y - 1))
            if point_y + 1 < map_hauteur and \
               (point_x+1, point_y + 1) not in visited:
                visited.append((point_x+1, point_y + 1))

        if point_x-1 >= 0 and (point_x-1, point_y) not in visited:
            visited.append((point_x-1, point_y))
            if point_y - 1 >= 0 and (point_x-1, point_y - 1) not in visited:
                visited.append((point_x-1, point_y - 1))
            if point_y + 1 < map_hauteur and \
               (point_x-1, point_y + 1) not in visited:
                visited.append((point_x-1, point_y + 1))

        if point_y+1 < map_hauteur and (point_x, point_y+1) not in visited:
            visited.append((point_x, point_y+1))

        if point_y-1 >= 0 and (point_x, point_y-1) not in visited:
            visited.append((point_x, point_y-1))
    for y in range(len(map)):
        map[y] = ['*'] + map[y] + ['*']
    map.insert(0, ['*'] * (map_largeur + 2))
    map.append(['*'] * (map_largeur + 2))
    return map


def mini_map():
    """
    affiche une petite carte
    """
    x_s, y_s = 0, 0
    rectangle(x_s, y_s, 70, 70, couleur='black', remplissage='black')
    for y in range(y_player - 3, y_player + 4):
        for x in range(x_player - 3, x_player + 4):
            if y < len(map) and x < len(map[y]) and y >= 0 and x >= 0:
                if map[y][x] == '*':
                    rectangle(x_s, y_s, x_s + 10, y_s + 10, couleur='black',
                              remplissage='white')
                if map[y][x] == '@':
                    rectangle(x_s, y_s, x_s + 10, y_s + 10, couleur='red',
                              remplissage='red')
                if map[y][x] == 'o':
                    rectangle(x_s, y_s, x_s + 10, y_s + 10, couleur='black',
                              remplissage='blue')
            x_s += 10
        x_s = 0
        y_s += 10


def load():
    global map
    script_dir = os.path.dirname(__file__)
    rel_path = "save.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    try:
        f = open(abs_file_path, 'r')
        map = ast.literal_eval(f.read())
    except IOError:
        pass


def save():
    global map
    script_dir = os.path.dirname(__file__)
    rel_path = "save.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    try:
        f = open(abs_file_path, 'w')
        f.write(str(map))
    except IOError:
        f = open(abs_file_path, 'w', 'x')
        f.write(map)


# programme principal
if __name__ == "__main__":

    # initialisation du jeu
    framerate = 30   # taux de rafraîchissement du jeu en images/s
    direction = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # list of direction
    dir = 1  # starting direction
    direction_x, direction_y = 0, 0
    distance = 0
    x_player, y_player = 0, 0  # coordinate of player
    x_end, y_end = 0, 0
    facing = False
    loading = True
    start = True

    # wall length set up
    first_wall_length = (hauteur_fenetre**2+largeur_fenetre**2)**0.5/16
    wall_length = (hauteur_fenetre**2+largeur_fenetre**2)**0.5/4.5

    # change later the map
    level = 0
    map_largeur = 15
    map_hauteur = 15
    map = []
    cree_fenetre(largeur_fenetre, hauteur_fenetre)

    # boucle principale
    jouer = True
    while jouer:
        if loading:
            if start:
                load()
                start = False
            if map == []:
                map = map_random(map, map_hauteur, map_largeur)
                map[1][1] = '@'
            for y in range(len(map)):
                for x in range(len(map[y])):
                    if map[y][x] == 'o':
                        x_end = x
                        y_end = y
            loading = False
        # affichage des objets
        efface_tout()
        affiche_mur()
        affiche_mur2()
        mini_map()
        mise_a_jour()
        # gestion des événements
        direction_distance_check(map, dir, direction)
        ev = donne_ev()
        ty = type_ev(ev)
        if y_player == y_end and x_player == x_end:
            map = []
            loading = True
        if ty == 'Quitte':
            jouer = False
        elif ty == 'Touche':
            player_controller(touche(ev), direction_x, direction_y, x_player,
                              y_player)
        if not jouer:
            save()
        # attente avant rafraîchissement
        sleep(1/framerate)
    # fermeture et sortie
    ferme_fenetre()
