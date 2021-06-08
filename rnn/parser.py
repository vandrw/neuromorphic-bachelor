import muspy
import os
from pathlib import Path
from typing import Tuple, Union, Dict
from muspy import music

from muspy.inputs import read_midi
from muspy.music import Music
from tensorflow.data import Dataset as TFDataset


class MidiFolderDataset(muspy.FolderDataset):
    _extension = "midi"

    def read(self, filename: Union[str, Path]) -> Music:
        """Read a file into a Music object."""
        return read_midi(self.root / filename)


class MidiParser:
    def __init__(self) -> None:
        pass

    def loadDataset(self, data_dir) -> Tuple[Dict[str, "TFDataset"], Dict[str, "TFDataset"]]:
        music_dataset = MidiFolderDataset(data_dir, convert=True)
        # We convert the MusPy Music object dataset to a tensorflow.data.Dataset split in train and test.
        # The splits can be accessed by music_dataset['train] (and ['test']).
        music_dataset = music_dataset.to_tensorflow_dataset(
            representation="pianoroll", splits=[0.8, 0.2]
        )

        return music_dataset['train'], music_dataset['test']


def main():
    parser = MidiParser()
    train_d, test_d = parser.loadDataset("../data/midi")

    for element in train_d:
        print(element.shape)


if __name__ == "__main__":
    main()
