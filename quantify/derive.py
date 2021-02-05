import copy
import time
import pickle
import math
import matplotlib.pyplot as plt

"""
Self Notes:
    For every ngram, we calculate I given every chord
    P(e_i| e_i-(n-1) ... ) = P(e_i-(n-1) ... and e_i) / P(e_i)

    P(e) = freq of chord / nr of chords
    P(e_i-(n-1) ... and e) = freq of ngram / nr of ngrams (of the same order)

    H will be calculated by reducing the size of the ngram,
    starting from 1 before the chord to the first one
    e.g. Eb:maj F:min9 Bb:sus4(b7) Eb:maj Ab:min9 Db:9
    First  : Ab:min9 Db:9
    Second : Eb:maj Ab:min9 Db:9
    Third  : Bb:sus4(b7) Eb:maj Ab:min9 Db:9
    ...

    Each will be summed.

    entropy is uncertainity
    infor_content is surprise

TODO:
    - check against figure 1A
    - look into IDyOM Python
    - update ngram code
"""


class PPM:
    """
    Prediction by Partial Matchin algorithm.
    """
    def __init__(self):
        self.chord_freq = {}
        self.ngram_freq = {}
        self.content = {}
        self.entropy = {}

    def countChord(self, chord):
        if chord not in self.chord_freq:
            self.chord_freq[chord] = 1
        else:
            self.chord_freq[chord] += 1

    def countNgram(self, chord, ngram):
        if chord not in self.ngram_freq:
            self.ngram_freq[chord] = {}
            self.ngram_freq[chord][ngram] = 1
        else:
            if ngram not in self.ngram_freq[chord]:
                self.ngram_freq[chord][ngram] = 1
            else:
                self.ngram_freq[chord][ngram] += 1

    def probChords(self):
        # Calculating the probability of each chord.
        nr_chords = len(self.chord_freq.keys())
        for chord in self.chord_freq.keys():
            self.chord_freq[chord] /= nr_chords

    def countNgramLen(self):
        lengths = {}
        for chord in self.ngram_freq.keys():
            for seq in self.ngram_freq[chord]:
                if len(seq) in lengths:
                    lengths[len(seq)] += 1
                else:
                    lengths[len(seq)] = 1
        
        return lengths

    def calcInfoContent(self, lengths):
        self.content = copy.deepcopy(self.ngram_freq)
        for chord in self.ngram_freq.keys():
            for seq in self.ngram_freq[chord]:
                self.ngram_freq[chord][seq] = (
                    self.ngram_freq[chord][seq] / lengths[len(seq)]) / \
                    self.chord_freq[chord]

                self.content[chord][seq] = (-1) * \
                    math.log2(self.ngram_freq[chord][seq])

    def calcEntropy(self):
        self.entropy = copy.deepcopy(self.ngram_freq)
        for chord in self.entropy.keys():
            for seq in self.entropy[chord]:
                self.entropy[chord][seq] = 0

        for chord in self.ngram_freq.keys():
            for seq in self.ngram_freq[chord]:
                self.entropy[chord][seq] += self.ngram_freq[chord][seq] * \
                    self.content[chord][seq]

    def saveData(self):
        with open("quantify/objects/ngram_data.pkl", "wb") as ngram_output:
            pickle.dump(self.ngram_freq, ngram_output, pickle.HIGHEST_PROTOCOL)
        with open("quantify/objects/chord_data.pkl", "wb") as chord_output:
            pickle.dump(self.chord_freq, chord_output, pickle.HIGHEST_PROTOCOL)

    def loadData(self):
        with open("quantify/ngram_data.pkl", "rb") as ngram_output:
            self.ngram_freq = pickle.load(ngram_output)
        with open("quantify/chord_data.pkl", "rb") as chord_output:
            self.chord_freq = pickle.load(chord_output)

    def plotMetrics(self, uncertainity, surprise):
        plt.scatter(uncertainity, surprise)
        plt.xlabel("Uncertainty (bits)")
        plt.ylabel("Surprise (bits)")
        plt.show()

    def train(self, file_path):
        """
        Train on a Corpus of song sequences, given by the file_path.
        """
        with open(file_path, 'r') as chords:
            for line in chords:
                line_chords = line.split(' ')
                song_length = len(line_chords)

                # Calculating the occurence of a chord in
                # the entire dataset
                for i in range(0, song_length):
                    curr_chord = line_chords[i]
                    self.countChord(curr_chord)

                    # Not sure here... Calculating the occurence
                    # of engrams that contain the previous chord?
                    if i > 0:
                        for j in range(i, 0, -1):
                            ngram = ' '.join(line_chords[j-1:i])
                            self.countNgram(curr_chord, ngram)
                    else:
                        self.countNgram(curr_chord,
                                        "start " + curr_chord)

        # Count of each sequence size (to calculate information 
        # content based on order)
        lengths = self.countNgramLen()

        # Calculate information content
        self.calcInfoContent(lengths)

        # Entropy of each progression(sequence) + prob of each 
        # sequence, given a chord.
        self.calcEntropy()

    def predict(self, file_path):
        uncer = []
        surpr = []
        with open(file_path, 'r') as chords:
            for line in chords:
                line_chords = line.split(' ')
                song_length = len(line_chords)

                # Calculating the occurence of a chord in
                # the entire dataset
                for i in range(0, song_length):
                    curr_chord = line_chords[i]

                    if i > 0:
                        ngram = ' '.join(line_chords[0:i])
                        # Impossible to happen, since I check on the same set.
                        # TODO: Change what's commented below later. Introduce
                        # a very small proability in this case.
                        # if ngram not in self.ngram_freq[curr_chord]:

                        surpr.append(self.content[curr_chord][ngram])
                        uncer.append(self.entropy[curr_chord][ngram])
                    else:
                        surpr.append(
                            self.content[curr_chord]["start " + curr_chord])
                        uncer.append(self.entropy[curr_chord]
                                     ["start " + curr_chord])
        
        return uncer, surpr


def main():
    start = time.time()

    ppm = PPM()
    ppm.train("quantify/chords.txt")
    uncer, surpr = ppm.predict("quantify/chords.txt")
    ppm.plotMetrics(uncer, surpr)

    print("Finished in {}".format(time.time() - start))


if __name__ == "__main__":
    main()
