from pygame import mixer
from pathlib import Path
import pandas as pd
import mutagen


music_folder = Path('C:/Users/Lenovo/Music')   # Enter main music folder
folder_list = ['mp3 style', 'mp3 album', 'mp3 vinyl']  # Enter specific folder inside music folder
mp3list = []


class Mp3file:
    def __init__(self, df, title):
        self.dfb = df[df['title'] == title]
        self.absolute_path = self.dfb['absolute'].iloc[0]
        self.print_duplicates()
        self.options()

    def options( self ):
        print('(0 | 1) delete file, (P)lay, (S)top, (N)ext')
        call = input('Input:')
        if call in ('0', '1'):
            self.delete(call)
        elif call == 'p':
            self.play(self.absolute_path)
            self.options()
        elif call == 's':
            self.stop()
            self.options()
        elif call == '>':
            self.skip()
            self.options()
        elif call == 'n':
            print('>>> next')
            pass

    def print_duplicates(self):
        print(self.dfb.reset_index()[['title', 'folder', 'bpm']])

    def delete(self, call):
        Path(self.dfb['absolute'].iloc[int(call)]).unlink()

    def play(self, absolute_path ):
        mixer.init()
        mixer.music.load(absolute_path)
        mixer.music.play()

    def stop(self):
        mixer.music.stop()

    def skip(self):
        mixer.music.set_pos(100)


def get_attr(name, path):
    try:
        tags = mutagen.File(path, easy=True)
        return tags[name][0]
    except (KeyError, mutagen.MutagenError) as err:
        return None


def crawl(path):
    for entry in path:
        if len(entry.suffixes) == 0 and entry.is_dir():
            crawl(entry.iterdir())
        elif '.mp3' in entry.suffixes and '.asd' not in entry.suffixes:
            bpm = get_attr('bpm', entry.as_posix())
            mp3el = entry.stem, bpm, entry.parent.stem, entry.absolute()
            mp3list.append(mp3el)
        else:
            pass


def join_paths(folders):
    for folder in folders:
        crawl(music_folder.joinpath(folder).iterdir())


join_paths(folder_list)

df = pd.DataFrame([el for el in mp3list], columns=['title', 'bpm', 'folder', 'absolute'])

# show only duplicates
dfa = df[df['title'].isin(df[df['title'].duplicated()]['title'].values)].sort_values(by='title', ascending=False)


if __name__ == '__main__':
    for each in dfa['title'].unique():
        Mp3file(df, each)

