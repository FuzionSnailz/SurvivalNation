import os
import json
import time
import requests
import pygame
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
import random

CONFIG_FILE = "config.json"
SONG_DATA_URL = "https://fuzionsnailz.github.io/QDEX/music-repo/songs.json"
TEMP_DIR = "temp_songs"
current_tmp_path = None
current_song = None
paused = False
last_played_song = None
playlist_queue = []

# Initialize pygame mixer
pygame.mixer.init()

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"playlists": {"Library": [], "Favorites": []}}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def clean_old_temp_files():
    global current_tmp_path
    temp_files = [os.path.join(TEMP_DIR, f) for f in os.listdir(TEMP_DIR) if f.endswith(".wav")]
    temp_files.sort(key=lambda x: os.path.getmtime(x))
    if len(temp_files) > 5:
        for song in temp_files[:-4]:
            if song != current_tmp_path:
                try:
                    os.remove(song)
                except Exception as e:
                    print(f"Error removing file {song}: {e}")

def load_songs():
    try:
        response = requests.get(SONG_DATA_URL)
        response.raise_for_status()
        return response.json().get("songs", [])
    except Exception as e:
        print(f"Error loading songs: {e}")
        return []

def load_and_play_song(url, song_title):
    global current_tmp_path, current_song, last_played_song, paused
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        temp_id = int(time.time())
        current_tmp_path = os.path.join(TEMP_DIR, f"temp_song_{temp_id}.wav")
        with open(current_tmp_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        pygame.mixer.music.load(current_tmp_path)
        pygame.mixer.music.play()
        paused = False
        last_played_song = current_song
        current_song = song_title
        update_status()
    except Exception as e:
        print(f"Error playing song: {e}")

def update_status():
    now_playing_var.set(f"Now Playing: {current_song if current_song else 'None'}")

def play():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False

def pause():
    global paused
    pygame.mixer.music.pause()
    paused = True

def play_previous():
    if last_played_song:
        song = next((s for s in songs if s["title"] == last_played_song), None)
        if song:
            load_and_play_song(song["url"], song["title"])

def repeat():
    if current_tmp_path:
        pygame.mixer.music.load(current_tmp_path)
        pygame.mixer.music.play()

def skip():
    if playlist_queue:
        next_song = playlist_queue.pop(0)
        load_and_play_song(next_song["url"], next_song["title"])

def shuffle():
    if playlist_queue:
        random_song = random.choice(playlist_queue)
        load_and_play_song(random_song["url"], random_song["title"])

def search_song():
    query = search_entry.get().lower()
    song_listbox.delete(0, tk.END)
    for song in songs:
        if query in song["title"].lower() or query in song["artist"].lower():
            song_listbox.insert(tk.END, f"{song['title']} by {song['artist']}")

def play_all_songs():
    global playlist_queue
    playlist_queue = []
    for i in range(song_listbox.size()):
        song_info = song_listbox.get(i)
        song = next((s for s in songs if f"{s['title']} by {s['artist']}" == song_info), None)
        if song:
            playlist_queue.append(song)
    if playlist_queue:
        first_song = playlist_queue.pop(0)
        load_and_play_song(first_song['url'], first_song['title'])

def song_selected(event):
    selection = song_listbox.curselection()
    if selection:
        index = selection[0]
        song_info = song_listbox.get(index)
        song = next((s for s in songs if f"{s['title']} by {s['artist']}" == song_info), None)
        if song:
            clean_old_temp_files()
            load_and_play_song(song["url"], song["title"])

def playlist_song_selected(event):
    selection = playlist_song_listbox.curselection()
    if selection:
        index = selection[0]
        song_info = playlist_song_listbox.get(index)
        song = next((s for s in songs if f"{s['title']} by {s['artist']}" == song_info), None)
        if song:
            clean_old_temp_files()
            load_and_play_song(song["url"], song["title"])

def update_playlist_dropdown():
    playlist_menu['menu'].delete(0, 'end')
    for name in config['playlists']:
        playlist_menu['menu'].add_command(label=name, command=lambda n=name: select_playlist(n))

def select_playlist(playlist_name):
    playlist_var.set(playlist_name)
    global playlist_queue
    playlist_queue = [s for s in songs if s['title'] in config['playlists'][playlist_name]]
    if playlist_queue:
        first_song = playlist_queue.pop(0)
        load_and_play_song(first_song['url'], first_song['title'])

def check_music_end():
    if not pygame.mixer.music.get_busy() and not paused and playlist_queue:
        next_song = playlist_queue.pop(0)
        load_and_play_song(next_song['url'], next_song['title'])
    root.after(1000, check_music_end)

def add_to_playlist():
    if not current_song:
        messagebox.showinfo("No Song", "No song is currently playing.")
        return

    playlists = list(config['playlists'].keys())
    if not playlists:
        messagebox.showerror("No Playlists", "You have no playlists. Please create one first.")
        return

    selection_win = tk.Toplevel(root)
    selection_win.title("Select Playlist")
    tk.Label(selection_win, text="Select a Playlist to Add the Song To:").pack(pady=10)

    def on_select(playlist_name):
        if current_song not in config['playlists'][playlist_name]:
            config['playlists'][playlist_name].append(current_song)
            if current_song not in config['playlists']['Library']:
                config['playlists']['Library'].append(current_song)
            save_config(config)
            messagebox.showinfo("Added", f"'{current_song}' added to '{playlist_name}' playlist.")
        else:
            messagebox.showinfo("Exists", f"'{current_song}' already in '{playlist_name}' playlist.")
        selection_win.destroy()

    for pl in playlists:
        tk.Button(selection_win, text=pl, command=lambda p=pl: on_select(p)).pack(pady=2)

def remove_from_playlist():
    if not current_song:
        messagebox.showinfo("No Song", "No song is currently playing.")
        return

    playlists = [name for name, songs in config['playlists'].items() if current_song in songs]
    if not playlists:
        messagebox.showinfo("Not in Playlist", "This song is not in any playlists.")
        return

    selection_win = tk.Toplevel(root)
    selection_win.title("Remove from Playlist")
    tk.Label(selection_win, text="Select a Playlist to Remove the Song From:").pack(pady=10)

    def on_select(playlist_name):
        config['playlists'][playlist_name].remove(current_song)
        save_config(config)
        messagebox.showinfo("Removed", f"'{current_song}' removed from '{playlist_name}' playlist.")
        selection_win.destroy()

    for pl in playlists:
        tk.Button(selection_win, text=pl, command=lambda p=pl: on_select(p)).pack(pady=2)


def create_new_playlist():
    name = simpledialog.askstring("New Playlist", "Enter Playlist Name:")
    if name and name not in config['playlists']:
        config['playlists'][name] = []
        save_config(config)
        update_playlist_buttons()
        update_playlist_dropdown()

def update_playlist_buttons():
    for widget in playlist_frame.winfo_children():
        if isinstance(widget, tk.Button):
            widget.destroy()

    playlists = list(config['playlists'].keys())
    row = 0
    col = 0

    for i, name in enumerate(playlists):
        if i >= 25:
            break
        button = tk.Button(playlist_frame, text=name, command=lambda n=name: show_playlist(n))
        button.grid(row=row, column=col, padx=5, pady=5)
        col += 1
        if col == 5:
            col = 0
            row += 1

def show_playlist(name):
    playlist_song_listbox.delete(0, tk.END)
    for title in config['playlists'][name]:
        full_title = next((f"{s['title']} by {s['artist']}" for s in songs if s['title'] == title), title)
        playlist_song_listbox.insert(tk.END, full_title)


root = tk.Tk()
root.title("QP3")
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

main_tab = ttk.Frame(notebook)
notebook.add(main_tab, text="Main")
tk.Label(main_tab, text="QP3", font=("Arial", 20)).pack(pady=10)
now_playing_var = tk.StringVar(value="Now Playing: None")
tk.Label(main_tab, textvariable=now_playing_var).pack()

tk.Button(main_tab, text="Play", command=play).pack(side=tk.LEFT, padx=10)
tk.Button(main_tab, text="Pause", command=pause).pack(side=tk.LEFT, padx=10)
tk.Button(main_tab, text="Previous", command=play_previous).pack(side=tk.LEFT, padx=10)
tk.Button(main_tab, text="Next", command=skip).pack(side=tk.LEFT, padx=10)
tk.Button(main_tab, text="Repeat", command=repeat).pack(side=tk.LEFT, padx=10)
tk.Button(main_tab, text="Shuffle", command=shuffle).pack(side=tk.LEFT, padx=10)
tk.Button(main_tab, text="Add to Playlist", command=add_to_playlist).pack(side=tk.LEFT, padx=10)

playlist_var = tk.StringVar()
playlist_menu = ttk.OptionMenu(main_tab, playlist_var, "Select Playlist")
playlist_menu.pack(pady=10)

# Find Music Tab
find_tab = ttk.Frame(notebook)
notebook.add(find_tab, text="Find Music")
tk.Label(find_tab, text="Search").pack(pady=5)
search_entry = ttk.Entry(find_tab)
search_entry.pack(pady=5)
tk.Button(find_tab, text="Search", command=search_song).pack()
tk.Button(find_tab, text="Play All", command=play_all_songs).pack(pady=5)
song_listbox = tk.Listbox(find_tab, width=50)
song_listbox.pack(pady=10, padx=10)
song_listbox.bind('<<ListboxSelect>>', song_selected)

# Playlists Tab
playlist_tab = ttk.Frame(notebook)
notebook.add(playlist_tab, text="Playlists")
tk.Label(playlist_tab, text="Playlists").pack(pady=5)
playlist_frame = tk.Frame(playlist_tab)
playlist_frame.pack()
tk.Button(playlist_tab, text="Create New Playlist", command=create_new_playlist).pack(pady=10)
tk.Button(playlist_tab, text="Remove from Playlist", command=remove_from_playlist).pack(side=tk.LEFT, padx=10)

playlist_song_listbox = tk.Listbox(playlist_tab, width=50)
playlist_song_listbox.pack(pady=10)
playlist_song_listbox.bind('<<ListboxSelect>>', playlist_song_selected)

# Load data
config = load_config()
songs = load_songs()

for song in songs:
    song_listbox.insert(tk.END, f"{song['title']} by {song['artist']}")

update_playlist_buttons()
update_playlist_dropdown()
check_music_end()

root.mainloop()



