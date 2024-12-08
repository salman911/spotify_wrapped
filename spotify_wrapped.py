import json
import pandas as pd
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os


# Set theme and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SpotifyAnalyzer:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Spotify Data Analyzer")
        self.root.geometry("900x700")

        self.data = None
        self.setup_gui()

    def setup_gui(self):
        # Create main container
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # File selection section
        file_frame = ctk.CTkFrame(main_container)
        file_frame.pack(fill="x", padx=10, pady=5)

        self.load_button = ctk.CTkButton(
            file_frame,
            text="Select JSON Files",
            command=self.load_files,
            width=150
        )
        self.load_button.pack(side="left", padx=5, pady=5)

        self.files_label = ctk.CTkLabel(
            file_frame,
            text="No files loaded",
            wraplength=600
        )
        self.files_label.pack(side="left", padx=5, pady=5)

        # Controls section
        controls_frame = ctk.CTkFrame(main_container)
        controls_frame.pack(fill="x", padx=10, pady=5)

        # Year selection
        year_label = ctk.CTkLabel(controls_frame, text="Select Year:")
        year_label.pack(side="left", padx=5, pady=5)

        self.year_var = ctk.StringVar()
        self.year_combo = ctk.CTkOptionMenu(
            controls_frame,
            variable=self.year_var,
            values=[""],
            command=self.update_total_time,
            width=100
        )
        self.year_combo.pack(side="left", padx=5, pady=5)

        # Total time display
        self.total_time_var = ctk.StringVar(value="Total Listening Time: N/A")
        total_time_label = ctk.CTkLabel(
            controls_frame,
            textvariable=self.total_time_var,
            font=("Helvetica", 12, "bold")
        )
        total_time_label.pack(side="left", padx=20, pady=5)
        # Minimum playtime section
        playtime_frame = ctk.CTkFrame(main_container)
        playtime_frame.pack(fill="x", padx=10, pady=5)

        playtime_label = ctk.CTkLabel(playtime_frame, text="Minimum Playtime (seconds):")
        playtime_label.pack(side="left", padx=5, pady=5)

        self.min_playtime = ctk.CTkEntry(
            playtime_frame,
            width=100,
            placeholder_text="30"
        )
        self.min_playtime.insert(0, "30")
        self.min_playtime.pack(side="left", padx=5, pady=5)
        # Minimum plays section
        min_plays_frame = ctk.CTkFrame(main_container)
        min_plays_frame.pack(fill="x", padx=10, pady=5)

        min_plays_label = ctk.CTkLabel(min_plays_frame, text="Minimum Plays:")
        min_plays_label.pack(side="left", padx=5, pady=5)

        self.min_plays = ctk.CTkEntry(
            min_plays_frame,
            width=100,
            placeholder_text="10"
        )
        self.min_plays.insert(0, "10")
        self.min_plays.pack(side="left", padx=5, pady=5)

        # Analysis buttons - Create buttons_frame FIRST
        buttons_frame = ctk.CTkFrame(main_container)
        buttons_frame.pack(fill="x", padx=10, pady=5)

        self.songs_button = ctk.CTkButton(
            buttons_frame,
            text="Show Top Songs",
            command=self.show_top_songs,
            width=150
        )
        self.songs_button.pack(side="left", padx=5, pady=5)

        self.artists_button = ctk.CTkButton(
            buttons_frame,
            text="Show Top Artists",
            command=self.show_top_artists,
            width=150
        )
        self.artists_button.pack(side="left", padx=5, pady=5)

        self.albums_button = ctk.CTkButton(
            buttons_frame,
            text="Show Top Albums",
            command=self.show_top_albums,
            width=150
        )
        self.albums_button.pack(side="left", padx=5, pady=5)



        # Add Skip Analysis button
        self.skip_button = ctk.CTkButton(
            buttons_frame,
            text="Analyze Skips",
            command=self.analyze_skip_behavior,
            width=150
        )
        self.skip_button.pack(side="left", padx=5, pady=5)

        # Results area
        self.result_text = ctk.CTkTextbox(
            main_container,
            width=800,
            height=400,
            font=("Helvetica", 12)
        )
        self.result_text.pack(fill="both", expand=True, padx=10, pady=5)



    def format_time(self, minutes):
        days = minutes // (24 * 60)
        remaining_minutes = minutes % (24 * 60)
        hours = remaining_minutes // 60
        minutes = remaining_minutes % 60
        return f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes"

    def update_total_time(self, *args):
        if self.data is None:
            return

        try:
            year = int(self.year_var.get())
            year_data = self.data[self.data['year'] == year]
            total_minutes = year_data['ms_played'].sum() / (1000 * 60)
            formatted_time = self.format_time(total_minutes)
            self.total_time_var.set(f"{year} Total: {formatted_time}")
        except:
            self.total_time_var.set("Total Listening Time: N/A")

    def load_files(self):
        files = filedialog.askopenfilenames(filetypes=[("JSON files", "*.json")])
        if not files:
            return

        all_data = []
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    all_data.extend(data)
            except Exception as e:
                messagebox.showerror("Error", f"Error loading file {os.path.basename(file)}: {str(e)}")
                return

        self.data = pd.DataFrame(all_data)
        self.data['ts'] = pd.to_datetime(self.data['ts'])
        self.data['year'] = self.data['ts'].dt.year

        # Update year dropdown
        available_years = sorted(self.data['year'].unique())
        self.year_combo.configure(values=[str(year) for year in available_years])
        if available_years:
            self.year_combo.set(str(available_years[-1]))
            self.update_total_time()

        # Update files label
        file_names = [os.path.basename(f) for f in files]
        self.files_label.configure(text=f"Loaded {len(files)} files: {', '.join(file_names)}")

        messagebox.showinfo("Success",
                          f"Loaded {len(self.data)} entries from {len(files)} files\n"  
                          f"Years available: {', '.join(map(str, available_years))}")

    def filter_data(self):
        if self.data is None:
            messagebox.showerror("Error", "Please load data files first")
            return None

        try:
            year = int(self.year_var.get())
            min_playtime = int(self.min_plays.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid year or minimum playtime")
            return None

        filtered_data = self.data[
            (self.data['year'] == year) &
            (self.data['ms_played'] >= min_playtime * 1000)
        ].copy()

        return filtered_data

    def analyze_skip_behavior(self):
        filtered_data = self.filter_data()
        if filtered_data is None:
            return

        try:
            min_plays = int(self.min_plays.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for minimum plays")
            return

            # Add skipped column based on ms_played
        filtered_data['skipped'] = filtered_data[
                                       'ms_played'] < 30000  # Consider tracks played less than 30 seconds as skipped

        # Group by track and calculate stats
        skip_stats = filtered_data.groupby('master_metadata_track_name').agg({
            'skipped': 'sum',
            'ms_played': 'count',
            'master_metadata_album_artist_name': 'first'  # Get artist name
        }).reset_index()

        # Calculate skip rate and filter by minimum plays
        skip_stats['skip_rate'] = (skip_stats['skipped'] / skip_stats['ms_played'] * 100).round(2)
        skip_stats = skip_stats[skip_stats['ms_played'] >= min_plays]  # Filter by minimum plays
        skip_stats = skip_stats.sort_values('skip_rate', ascending=False).head(20)

        # Display results
        self.result_text.delete("0.0", "end")
        self.result_text.insert("0.0",
                                f"Top 20 Most Skipped Songs ({self.year_var.get()})\n"
                                f"Minimum {min_plays} total plays required\n\n"
                                )

        for _, row in skip_stats.iterrows():
            self.result_text.insert("end",
                                    f"Track: {row['master_metadata_track_name']}\n"
                                    f"Artist: {row['master_metadata_album_artist_name']}\n"
                                    f"Skip Rate: {row['skip_rate']}%\n"
                                    f"Total Plays: {row['ms_played']}\n"
                                    f"Times Skipped: {int(row['skipped'])}\n\n"
                                    )

    def show_top_albums(self):
        filtered_data = self.filter_data()
        if filtered_data is None:
            return

            # Group by album name and calculate stats
        album_stats = filtered_data.groupby(
            ['master_metadata_album_album_name', 'master_metadata_album_artist_name']
        ).agg({
            'ms_played': ['count', 'sum']
        }).reset_index()

        # Rename columns for clarity
        album_stats.columns = ['Album', 'Artist', 'Play Count', 'Total Time (ms)']
        album_stats['Total Time (hours)'] = album_stats['Total Time (ms)'] / (1000 * 60 * 60)

        # Sort by total playtime and get the top 20 albums
        album_stats = album_stats.sort_values('Total Time (ms)', ascending=False).head(20)

        # Display results in the result_text widget
        self.result_text.delete("0.0", "end")
        self.result_text.insert("0.0", f"Top 20 Albums for {self.year_var.get()}:\n\n")

        for _, row in album_stats.iterrows():
            self.result_text.insert("end",
                                    f"Album: {row['Album']}\n"
                                    f"Artist: {row['Artist']}\n"
                                    f"Play Count: {row['Play Count']}\n"
                                    f"Total Time: {row['Total Time (hours)']:.2f} hours\n\n"
                                    )

    def show_top_songs(self):
        filtered_data = self.filter_data()
        if filtered_data is None:
            return

        song_stats = filtered_data.groupby(
            ['master_metadata_track_name', 'master_metadata_album_artist_name']
        ).agg({
            'ms_played': ['count', 'sum']
        }).reset_index()

        song_stats.columns = ['Track', 'Artist', 'Play Count', 'Total Time (ms)']
        song_stats['Total Time (hours)'] = song_stats['Total Time (ms)'] / (1000 * 60 * 60)
        song_stats = song_stats.sort_values('Total Time (ms)', ascending=False).head(20)

        self.result_text.delete("0.0", "end")
        self.result_text.insert("0.0", f"Top 20 Songs for {self.year_var.get()}:\n\n")

        for _, row in song_stats.iterrows():
            self.result_text.insert("end",
                f"Track: {row['Track']}\n"  
                f"Artist: {row['Artist']}\n"  
                f"Play Count: {row['Play Count']}\n"  
                f"Total Time: {row['Total Time (hours)']:.2f} hours\n\n"
            )

    def show_top_artists(self):
        filtered_data = self.filter_data()
        if filtered_data is None:
            return

        artist_stats = filtered_data.groupby('master_metadata_album_artist_name').agg({
            'ms_played': ['count', 'sum']
        }).reset_index()

        artist_stats.columns = ['Artist', 'Play Count', 'Total Time (ms)']
        artist_stats['Total Time (hours)'] = artist_stats['Total Time (ms)'] / (1000 * 60 * 60)
        artist_stats = artist_stats.sort_values('Total Time (ms)', ascending=False).head(20)

        self.result_text.delete("0.0", "end")
        self.result_text.insert("0.0", f"Top 20 Artists for {self.year_var.get()}:\n\n")

        for _, row in artist_stats.iterrows():
            self.result_text.insert("end",
                f"Artist: {row['Artist']}\n"  
                f"Play Count: {row['Play Count']}\n"  
                f"Total Time: {row['Total Time (hours)']:.2f} hours\n\n"
            )

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SpotifyAnalyzer()
    app.run()



