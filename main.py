from pathlib import Path
import pandas as pd
import mutagen


music_folder = Path('C:/Users/Lenovo/Music')   # Enter main music folder
folder_list = ['mp3 style', 'mp3 album', 'mp3 vinyl']  # Enter specific folder inside music folder
mp3list = []


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


def delete():
    join_paths(folder_list)
    df = pd.DataFrame([el for el in mp3list], columns=['title', 'bpm', 'folder', 'absolute'])
    dfa = df[df['title'].isin(df[df['title'].duplicated()]['title'].values)].sort_values(by='title', ascending=False)

    for each in dfa['title'].unique():
        print(df[df['title'] == each].reset_index()[['title', 'folder', 'bpm']])
        dfb = df[df['title'] == each]
        delete = input('Delete:')
        Path(dfb['absolute'].iloc[int(delete)]).unlink()


if __name__ == '__main__':
    delete()



