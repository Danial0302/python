import pygame.mixer
import pygame
import time

class MusicPlayer:
    def __init__(self, playlist):
        pygame.mixer.init()
        self.playlist = playlist
        self.current_index = 0
        self.is_playing = False
        self.is_paused = False
        self.current_sound = None
        self.length = 0
        self.start_time = 0
        self.pause_time = 0

    def play(self):
        if not self.is_playing:
            try:
                pygame.mixer.music.load(self.playlist[self.current_index])
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play()
                self.start_time = time.time()
                self.is_playing = True
                self.is_paused = False
                print(f"Playing: {self.playlist[self.current_index]}")
            except Exception as e:
                print(f"Error playing {self.playlist[self.current_index]}: {e}")
                self.is_playing = False

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.start_time = 0
        self.pause_time = 0
        print("Stopped")

    def pause_resume(self):
        if self.is_playing:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.start_time += time.time() - self.pause_time
                self.is_paused = False
                print("Resumed")
            else:
                pygame.mixer.music.pause()
                self.pause_time = time.time()
                self.is_paused = True
                print("Paused")

    def next_track(self):
        self.stop()
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.length = 0  # Reset to load new length
        self.play()

    def previous_track(self):
        self.stop()
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.length = 0  # Reset to load new length
        self.play()

    def get_current_track(self):
        return self.playlist[self.current_index]

    def get_length(self):
        if self.length == 0:
            try:
                temp_sound = pygame.mixer.Sound(self.playlist[self.current_index])
                self.length = temp_sound.get_length()
            except Exception as e:
                print(f"Error getting length: {e}")
                self.length = 0
        return self.length

    def get_position(self):
        if self.is_playing:
            if self.is_paused:
                return self.pause_time - self.start_time
            else:
                return pygame.mixer.music.get_pos() / 1000.0
        return 0