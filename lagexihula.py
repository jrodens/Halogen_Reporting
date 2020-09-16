import pygame
import traceback
import sys
import copy
import math
from collections import defaultdict

class States(object):
   def __init__(self):
       self.fnt = pygame.font.SysFont("comicsans", 40)
       self.fnt2 = pygame.font.SysFont("comicsans", 15)
       self.done = False
       self.next = None
       self.quit = False
       self.previous = None

class Menu(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'game'
        self.menu_size = self.menu_width, self.menu_height = (540,600)

    def cleanup(self) -> None:
        print('cleaning up Menu state stuff')

    def startup(self) -> None:
        print('starting Menu state stuff')

    def get_event(self, event: pygame.event) -> None:
        if event.type == pygame.KEYDOWN:
            print('Menu State keydown')
            self.done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.done = True

    def update(self, screen: pygame.Surface, delta_time) -> None:
        self.draw(screen)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((255,255,255))

        menu_text = ['Menu','Press any key to start game']
        num_of_lines = len(menu_text)
        for text in menu_text:
            line = self.fnt.render(text, 1, (0,0,0))
            y = 200 - ((line.get_height()+50)*num_of_lines)/2
            x = 270 - line.get_width()/2
            screen.blit(line,(x,y))
            num_of_lines -= 1

        menu_text = ['Game Play:','Press M to open the Menu', 'Press S to play solution']
        num_of_lines = len(menu_text)
        for text in menu_text:
            line = self.fnt.render(text, 1, (0,0,0))
            y = 400 - ((line.get_height()+50)*num_of_lines)/2
            x = 270 - line.get_width()/2
            screen.blit(line,(x,y))
            num_of_lines -= 1


class Game(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'menu'
        self.board_size = self.board_width, self.board_height = (540,540)
        self.cell_size = self.board_width / 9
        self.selected_cell_left, self.selected_cell_top = (0, 0)
        self.selected_cell_left_prev, self.selected_cell_top_prev = (0, 0)
        self.cell_center_x, self.cell_center_y = (0, 0)
        self.cell_selected = False
        self.slove_board = False
        self.key = 0
        self.board = [[7,8,0,4,0,0,1,2,0],
                      [6,0,0,0,7,5,0,0,9],
                      [0,0,0,6,0,1,0,7,8],
                      [0,0,7,0,4,0,2,6,0],
                      [0,0,1,0,5,0,9,3,0],
                      [9,0,4,0,6,0,0,0,5],
                      [0,7,0,3,0,0,0,1,2],
                      [1,2,0,0,0,7,4,0,0],
                      [0,4,9,2,0,6,0,0,7]]

        self.player_guesses = [[0,0,0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0,0,0]]

        self.possible_solutions = self.find_possible_solutions()

    def cleanup(self) -> None:
        print('cleaning up Game state stuff')

    def startup(self) -> None:
        print('starting Game state stuff')

    def get_event(self, event: pygame.event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                self.done = True
            elif event.key == pygame.K_s:
                self.done = True
                self.next = 'solve'
            elif event.key in (pygame.K_1, pygame.K_KP1):
                self.key = 1
            elif event.key in (pygame.K_2, pygame.K_KP2):
                self.key = 2
            elif event.key in (pygame.K_3, pygame.K_KP3):
                self.key = 3
            elif event.key in (pygame.K_4, pygame.K_KP4):
                self.key = 4
            elif event.key in (pygame.K_5, pygame.K_KP5):
                self.key = 5
            elif event.key in (pygame.K_6, pygame.K_KP6):
                self.key = 6
            elif event.key in (pygame.K_7, pygame.K_KP7):
                self.key = 7
            elif event.key in (pygame.K_8, pygame.K_KP8):
                self.key = 8
            elif event.key in (pygame.K_9, pygame.K_KP9):
                self.key = 9
            elif event.key == pygame.K_UP:
                self.write_to_board()
                self.possible_solutions = self.find_possible_solutions()
                if self.selected_cell_top != 0:
                    self.selected_cell_top -= 60
            elif event.key == pygame.K_DOWN:
                self.write_to_board()
                self.possible_solutions = self.find_possible_solutions()
                if self.selected_cell_top != 480:
                    self.selected_cell_top += 60
            elif event.key == pygame.K_LEFT:
                self.write_to_board()
                self.possible_solutions = self.find_possible_solutions()
                if self.selected_cell_left != 0:
                    self.selected_cell_left -= 60
            elif event.key == pygame.K_RIGHT:
                self.write_to_board()
                self.possible_solutions = self.find_possible_solutions()
                if self.selected_cell_left != 480:
                    self.selected_cell_left += 60
            elif event.key == pygame.K_RETURN:
                if self.board[int(self.selected_cell_left//60)][int(self.selected_cell_top//60)] == 0:
                    self.write_to_board()
                    self.possible_solutions = self.find_possible_solutions()
            elif event.key == pygame.K_DELETE:
                self.player_guesses[int(self.selected_cell_left//60)][int(self.selected_cell_top//60)] = 0
                self.possible_solutions = self.find_possible_solutions()
                self.clear_cell()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.selected_cell_left, self.selected_cell_top = self.select_cell(pygame.mouse.get_pos())
            if self.board[int(self.selected_cell_left//60)][int(self.selected_cell_top//60)] == 0:
                self.cell_selected = True
                if (self.selected_cell_left, self.selected_cell_top) != (self.selected_cell_left_prev, self.selected_cell_top_prev):
                    self.clear_cell()
                print(self.selected_cell_left, self.selected_cell_top)
            else:
                self.cell_selected = False

        if self.key in range(1,10) and self.cell_selected:
            pass
            # print(self.key)

    def update(self, screen: pygame.Surface, delta_time: float) -> None:
        self.draw(screen, delta_time)

    def draw(self, screen: pygame.Surface, delta_time: float) -> None:
        screen.fill((255,255,255))
        self.draw_grid(screen)
        self.draw_time(screen)

    def draw_time(self, screen: pygame.Surface) -> None:
        Clock = pygame.time.get_ticks()
        running_clock = self.fnt.render(f'Time: {self.format_time(Clock)}', 1, (0,0,0))
        screen.blit(running_clock, (540 - 200, 560))

    def format_time(self, ms: int) -> None:
        sec, minute, hour = ms%60000//1000, ms%3600000//60000, ms%86400000//(60000*60)
        return f'{hour:02}:{minute:02}:{sec:02}'

    def draw_grid(self, screen: pygame.Surface) -> None:
        for i in range(10):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1

            pygame.draw.line(screen, (0,0,0), (0, i*self.cell_size), (self.board_width, i*self.cell_size), thick)
            pygame.draw.line(screen, (0,0,0), (i*self.cell_size, 0), (i*self.cell_size, self.board_height), thick)

        self.print_board(screen)

        if self.cell_selected:
            self.selected_cell_left_prev, self.selected_cell_top_prev = self.selected_cell_left, self.selected_cell_top
            pygame.draw.rect(screen, (255,0,0), (self.selected_cell_left, self.selected_cell_top, self.cell_size, self.cell_size), 3)
            if self.key and self.board[int(self.selected_cell_left//60)][int(self.selected_cell_top//60)] == 0:
                guessed_number = self.fnt.render(str(self.key), 1, (128,128,128))
                screen.blit(guessed_number, (self.selected_cell_left+5, self.selected_cell_top+5))

    def print_board(self, screen: pygame.Surface) -> None:
        for x in range(9):
            for y in range(9):
                position = (x*self.cell_size, y*self.cell_size)
                number = self.fnt.render(str(self.board[x][y]), 1, (0,0,0))
                player_guess = self.fnt.render(str(self.player_guesses[x][y]), 1, (128,128,128))
                possible_solutions = self.fnt2.render(str(self.possible_solutions[(x,y)]), 1, (128,128,128))
                center = position[0]+30-number.get_width()/2, position[1]+30-number.get_height()/2
                center_x, center_y = position[0]+30-possible_solutions.get_width()/2, position[1]+60-possible_solutions.get_height()-1
                if self.board[x][y] != 0:
                    screen.blit(number, center)
                else:
                    if self.possible_solutions[(x,y)]:
                        screen.blit(possible_solutions, (center_x,center_y))
                if self.player_guesses[x][y] != 0:
                    screen.blit(player_guess, center)

    def clear_cell(self) -> None:
        self.key = 0

    def write_to_board(self) -> None:
        x, y = int(self.selected_cell_left//60), int(self.selected_cell_top//60)
        if self.is_possible_solutions(x, y, self.key):
            # self.board[x][y] = self.key
            self.player_guesses[x][y] = self.key
        self.clear_cell()

    def select_cell(self, postion: tuple) -> None:
        x , y = postion
        if x > self.board_width or y > self.board_height:
            self.cell_selected = False

        return x//self.cell_size * self.cell_size, y//self.cell_size * self.cell_size

    def find_possible_solutions(self):
        possible_solutions = defaultdict(list)
        for y in range(9):
            for x in range(9):
                if self.board[y][x] == 0:
                    for n in range(1,10):
                        if self.is_possible_solutions(y,x,n):
                            possible_solutions[(y,x)].append(n)
        return possible_solutions

    def is_possible_solutions(self, y: int, x: int, n: int) -> bool:
        already_found = set()

        for i in range(9):
            already_found.add(self.board[y][i])
            already_found.add(self.board[i][x])
            already_found.add(self.player_guesses[y][i])
            already_found.add(self.player_guesses[i][x])

        sqr_y = (y//3)*3
        sqr_x = (x//3)*3
        for i in range(3):
            for j in range(3):
                already_found.add(self.board[sqr_y+i][sqr_x+j])
                already_found.add(self.player_guesses[sqr_y+i][sqr_x+j])

        return n not in already_found


class Solve(Game):
    def __init__(self):
        Game.__init__(self)
        self.solved_board = []
        self.board_solved = False

    def cleanup(self) -> None:
        print('cleaning up Solve state stuff')

    def startup(self) -> None:
        print('starting Solve state stuff')
        self.__init__()

    def get_event(self, event: pygame.event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_m, pygame.K_q):
                self.done = True
                self.next = 'menu'
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass

    def update(self, screen: pygame.Surface, delta_time: float) -> None:
        self.draw(screen, delta_time)

    def draw(self, screen: pygame.Surface, delta_time: float) -> None:
        screen.fill((255,255,255))
        if not self.board_solved:
            self.solve(screen)
        self.draw_grid(screen)
        self.draw_time(screen)

    def solve(self, screen: pygame.Surface) -> bool:
        find = self.find_empty()
        if find:
            y, x = find
            for n in range(1,10):
                if self.done:
                    return True
                if self.is_possible_solutions(y,x,n):
                    self.player_guesses[y][x] = n
                    self.solve_animation(screen,y,x)
                    if self.solve(screen):
                        return True
                    self.player_guesses[y][x] = 0
                    self.solve_animation(screen,y,x)

            return False
        self.solved_board = copy.deepcopy(self.player_guesses)
        self.board_solved = True
        self.cell_selected = False
        return True

    def find_empty(self) -> tuple or None:
        for y in range(9):
            for x in range(9):
                if self.board[y][x] == 0 and self.player_guesses[y][x] == 0:
                    return (y,x)

    def solve_animation(self, screen: pygame.Surface, y: int, x: int) -> None:
        for event in pygame.event.get():
            self.get_event(event)

        self.cell_selected = True
        screen.fill((255,255,255))

        self.selected_cell_left, self.selected_cell_top = self.select_cell((y*60,x*60))
        pygame.draw.rect(screen, (255,0,0), (self.selected_cell_left, self.selected_cell_top, self.cell_size, self.cell_size), 3)

        self.possible_solutions = self.find_possible_solutions()

        self.draw_grid(screen)
        self.draw_time(screen)

        pygame.display.update()
        pygame.time.delay(150)


class Control:
    def __init__(self, **settings: dict):
        self.__dict__.update(settings)
        self.done = False
        self.cell_selected = False

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Sudoku')

        self.clock = pygame.time.Clock()

    def setup_states(self, state_dict: dict, start_state: object) -> None:
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def flip_state(self) -> None:
        self.state.done = False
        self.state.previous, self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()

    def update(self, delta_time: float) -> None:
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()

        self.state.update(self.screen, delta_time)

    def event_loop(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            self.state.get_event(event)

    def main_game_loop(self) -> None:
        while not self.done:
            delta_time = self.clock.tick(self.fps)/1000.0
            self.event_loop()
            self.update(delta_time)
            pygame.display.update()


if __name__ == '__main__':
    settings = {
        'size':(540,600),
        'fps' :60
    }

    app = Control(**settings)
    state_dict = {
        'menu': Menu(),
        'game': Game(),
        'solve': Solve()
    }
    try:
        app.setup_states(state_dict, 'menu')
        app.main_game_loop()
    except Exception:
        print(Exception)
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()
