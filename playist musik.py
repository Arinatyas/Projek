class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

    def __str__(self):
        return f"{self.title} - {self.artist}"

class Playlist:
    def __init__(self):
        self.songs = []
        self.history = []

    def push(self, song):
        self.songs.append(song)
        self.history.append(("add", song))

    def remove_song(self, title, artist):
        song = self.search_by_title_and_artist(title, artist)
        if song:
            self.songs.remove(song)
            self.history.append(("remove", song))
            return True
        return False

    def bubble_sort_by_title(self):
        n = len(self.songs)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.songs[j].title.lower() > self.songs[j+1].title.lower():
                    self.songs[j], self.songs[j+1] = self.songs[j+1], self.songs[j]

    def bubble_sort_by_artist(self):
        n = len(self.songs)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.songs[j].artist.lower() > self.songs[j+1].artist.lower():
                    self.songs[j], self.songs[j+1] = self.songs[j+1], self.songs[j]

    def sorting(self):
        print("1. Urutkan berdasarkan judul")
        print("2. Urutkan berdasarkan penyanyi")
        sub_choice = input("Masukkan pilihan Anda (1/2): ")
        if sub_choice == '1':
            self.bubble_sort_by_title()
            print("Playlist diurutkan berdasarkan Judul Lagu:")
            for song in self.songs:
                print(song)
        elif sub_choice == '2':
            self.bubble_sort_by_artist()
            print("Playlist diurutkan berdasarkan Penyanyi:")
            for song in self.songs:
                print(song)
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

    def pop(self):
        if not self.history:
            print("Playlist kosong.")
            return
        action, song = self.history.pop()
        if action == "add":
            self.songs.remove(song)
            print(f"Lagu '{song.title}' dibatalkan untuk ditambahkan dari Playlist")
        elif not self.history:
            print("Playlist kosong.")
            return
        else:
            print("Tidak ada tindakan yang dapat dibatalkan")

    def search_by_title(self, title):
        return [song for song in self.songs if song.title.lower() == title.lower()]

    def search_by_artist(self, artist):
        return [song for song in self.songs if song.artist.lower() == artist.lower()]
    
    def search_by_title_and_artist(self, title, artist):
        for song in self.songs:
            if song.title.lower() == title.lower() and song.artist.lower() == artist.lower():
                return song
        return None    

    def search(self):
        print("1. Cari berdasarkan judul")
        print("2. Cari berdasarkan penyanyi")
        sub_choice = input("Masukkan pilihan Anda (1/2): ")
        
        if sub_choice == '1':
            title = input("Masukkan judul lagu yang ingin dicari: ")
            songs = self.search_by_title(title)
            if songs:
                print(f"Lagu dengan judul '{title}' ditemukan:")
                for song in songs:
                    print(song)
            else:
                print("Lagu tidak ditemukan dalam playlist.")
        elif sub_choice == '2':
            artist = input("Masukkan nama penyanyi: ")
            songs = self.search_by_artist(artist)
            if songs:
                print(f"Penyanyi {artist} ditemukan:")
                for song in songs:
                    print(song)
            else:
                print("Penyanyi tidak ditemukan dalam playlist.")
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

    def display_playlist(self, sorted_by=None):
        if not self.songs:
            print("Playlist kosong.")
            return
        if sorted_by == 'title':
            self.bubble_sort_by_title()
        elif sorted_by == 'artist':
            self.bubble_sort_by_artist()
        for i, song in enumerate(self.songs, start=1):
            print(f"{i}. {song}")

def display_menu():
    print("\n======== Menu Playlist Musik ========")
    print("1. Tambah Lagu ke Playlist")
    print("2. Hapus Lagu dari Playlist")
    print("3. Hapus Lagu Terakhir di Playlist")
    print("4. Urutkan Lagu")
    print("5. Cari Lagu")
    print("6. Tampilkan Playlist")
    print("7. Keluar")
    print("=====================================")

def main():
    playlist = Playlist()

    while True:
        display_menu()
        choice = input("Pilih opsi (1-7): ")

        if choice == '1':
            title = input("Masukkan judul lagu: ")
            artist = input("Masukkan nama artis: ")
            song = Song(title, artist)
            playlist.push(song)
            print("Lagu berhasil ditambahkan ke playlist.")
        elif choice == '2':
            title = input("Masukkan judul lagu yang ingin dihapus: ")
            artist = input("Masukkan nama artis: ")
            if playlist.remove_song(title, artist):
                print("Lagu berhasil dihapus dari playlist.")
            else:
                print("Lagu tidak ditemukan dalam playlist.")
        elif choice == '3':
            playlist.pop()
        elif choice == '4':
            playlist.sorting()
        elif choice == '5':
            playlist.search()
        elif choice == '6':
            print("Playlist:")
            playlist.display_playlist()
        elif choice == '7':
            print("Terima kasih telah menggunakan aplikasi.")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih antara 1-7.")

if __name__ == "__main__":
    main()
