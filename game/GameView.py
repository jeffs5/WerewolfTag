#
# python imports
#
import os
import time
import pygame
from base import Globals

#
# Game View Class Module
#
class GameView():
    #
    # default constructor
    #
    def __init__(self, model):
        # initialize pygame
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        self.screen = pygame.display.set_mode([Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT], pygame.FULLSCREEN if Globals.WINDOW_FULLSCREEN else pygame.RESIZABLE)
        pygame.mouse.set_visible(False)
        
        # set caption and font
        pygame.display.set_caption("Play Tag!")
        self.myfont = pygame.font.Font(None, 16)
        
        # set class properties
        self.m = model
        self.play_music()
        
    #
    # display game view
    #
    def display(self):
        # clear screen surface
        self.screen.fill((0, 0, 0))

        if self.m.game_running:
            self.print_game_in_progress()

        # start screen
        elif self.m.mode == 0:
            self.print_title()

        # countdown screen       
        elif self.m.mode == 1:
            time_up = self.m.now + 5
            if time.time() < time_up:
                self.print_countdown(time_up)

        # actual game
        elif self.m.mode == 2:
            self.play_music()

            # # change for time
            time_up = self.m.now + self.m.GAME_LENGTH
            if time.time() < time_up:
                # take out?
                # clock.tick(self.m.FRAMERATE)

                # check to see if any player is still transforming & checks player powerups
                for player in self.m.players.values():

                    if time.time() >= player.speed_timer:
                        player.end_speed()

                    if time.time() >= player.in_hole_timer:
                        player.end_hole()

                    if player.transforming:
                        if time.time() >= player.transform_complete:
                            player.finish_transform()

                        # randomly tested modulo numbers were used for the animation
                        elif player.transform_counter % 18 == 1:
                            player.color = (255, 255, 255)
                        elif player.transform_counter % 6 == 1:
                            player.color = (255, 0, 0)

                        # counter used to determine which transformation animation should be shown
                        player.transform_counter += 1

                    player.draw_player(self.screen)
                    
                display_number = self.m.player_number + 1
                self.print_game_stats(time_up)

                for powerup in self.m.powerups:
                    powerup.draw_powerup(self.screen)

                for placeable in self.m.placeables:
                    placeable.draw_placeable(self.screen)

        # once the time is up!
        elif self.m.mode == 3:
            self.print_end_game()

        # draw screen to display
        pygame.display.flip()

    #
    # print game in progress screen
    #
    def print_game_in_progress(self):
        title = self.myfont.render("Werewolf Tag", 1, (255, 255, 255))
        intro_message = self.myfont.render("A game is currently in progress.", 1, (255, 255, 255))
        instructions = self.myfont.render("Please wait for the current game to end", 1, (255, 255, 255))
        self.screen.blit(title, (240, 10))
        self.screen.blit(intro_message, (180, 190))
        self.screen.blit(instructions, (140, 210))

    #
    # print game title screen
    #
    def print_title(self):
        title = self.myfont.render("Werewolf Tag", 1, (255, 255, 255))
        intro_message = self.myfont.render("You are player {0}".format(self.m.player_number + 1), 1, (255, 255, 255))
        instructions1 = self.myfont.render("When Everyone is Ready...", 1, (255, 255, 255))
        instructions2 = self.myfont.render("Press SPACE to Start Countdown", 1, (255, 255, 255))
        self.screen.blit(title, (250, 10))
        self.screen.blit(intro_message, (230, 190))
        self.screen.blit(instructions1, (210, 230))
        self.screen.blit(instructions2, (180, 245))

    #
    # print countdown screen
    #
    def print_countdown(self, time_up):
        instructions = self.myfont.render("Get Ready to start!", 1, (255, 255, 255))
        countdown = self.myfont.render("{0}".format(int(time_up - time.time()) + 1) , 1, (255, 255, 255))
        self.screen.blit(instructions, (210, 210))
        self.screen.blit(countdown, (300, 230))

    #
    # print game statistics screen
    #
    def print_game_stats(self, time_up):
        display_number = self.m.player_number + 1
        player = self.m.players[str(self.m.player_number)]
        x = player.currentSprite.rect.x
        y = player.currentSprite.rect.y

        player_score = self.myfont.render(
            "Your score: {0}".format(self.m.players[str(self.m.player_number)].get_score()), 1, (255, 255, 255))
        time_left = self.myfont.render("Time left: {0}".format(int(time_up - time.time())), 1, (255, 255, 255))
        pointer = self.myfont.render(" {0}".format(self.m.player_number + 1), 1, (255, 255, 255))
        self.screen.blit(player_score, (16, 400))
        self.screen.blit(time_left, (250, 10))
        self.screen.blit(pointer, (x - 6, y - 23))

    #
    # print end game screen
    #
    def print_end_game(self):
        time_up = self.myfont.render("Time's Up!", 1, (255, 255, 255))

        if self.m.player_number != self.m.winner_number:
            winner_text = self.myfont.render(
                "The winner is: Player {0} with a score of {1}".format((self.m.winner_number + 1), self.m.winner_score), 1, (255, 255, 255))
            self.screen.blit(winner_text, (110, 210))
        else:
            winner_text = self.myfont.render("You won!", 1, (255, 255, 255))
            self.screen.blit(winner_text, (250, 210))

        your_text = self.myfont.render(
            "Your score was: {0} ".format(self.m.players[str(self.m.player_number)].get_score()), 1, (255, 255, 255))
        restart_text = self.myfont.render("Press Space to continue", 1, (255, 255, 255))

        self.screen.blit(time_up, (250, 10))
        self.screen.blit(your_text, (200, 225))
        self.screen.blit(restart_text, (180, 270))

    #
    # select winner helper method
    #
    def select_winner(self, players):
        winner = self.m.players.values()[0]
        for player in self.m.players.values():
            if player.get_score() > winner.get_score():
                winner = player

        return winner

    #
    # play music helper method
    #
    def play_music(self):
            if self.m.music_mode == 0:
                pygame.mixer.music.load("Music/01 A Night Of Dizzy Spells.mp3")
                pygame.mixer.music.play(-1)
                self.m.music_mode = 1

            if self.m.music_mode == 1 and self.m.mode == 2:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Music/03 Chibi Ninja.mp3")
                pygame.mixer.music.play()
                self.m.music_mode = 2
