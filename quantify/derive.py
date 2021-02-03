import copy
import time
import pickle
import math
import matplotlib.pyplot as plt


class PPM:
    def __init__(self):
        # chord freq/probs
        # ngram freq/entropy
        pass

    def countChords(self, song_sequence):
        pass

    def countNgram(self, ngram):
        pass

    def saveData(self):
        pass

    def loadData(self):
        pass


def PPM(file_path: str):
    """

    """
    # chord_dict = {}
    # ngrams = {}
    # with open(file_path, 'r') as chords:
    #     for line in chords:
    #         line_chords = line.split(' ')
    #         song_length = len(line_chords)

    #         # Calculating the occurence of a chord in
    #         # the entire dataset
    #         for i in range(0, song_length):
    #             curr_chord = line_chords[i]
    #             if curr_chord not in chord_dict:
    #                 chord_dict[curr_chord] = 1
    #             else:
    #                 chord_dict[curr_chord] += 1

    #             # Not sure here... Calculating the occurence
    #             # of engrams that contain the previous chord?
    #             if i > 0:
    #                 for j in range(i, 0, -1):
    #                     ngram = ' '.join(line_chords[j-1:i])
    #                     # print(ngram)
    #                     if curr_chord not in ngrams:
    #                         ngrams[curr_chord] = {}
    #                         ngrams[curr_chord][ngram] = 1
    #                     else:
    #                         if ngram not in ngrams[curr_chord]:
    #                             ngrams[curr_chord][ngram] = 1
    #                         else:
    #                             ngrams[curr_chord][ngram] += 1
    #             else:
    #                 if curr_chord not in ngrams:
    #                     ngrams[curr_chord] = {}
    #                     ngrams[curr_chord]["start " + curr_chord] = 1
    #                 else:
    #                     if "start " + curr_chord not in ngrams[curr_chord]:
    #                         ngrams[curr_chord]["start " + curr_chord] = 1
    #                     else:
    #                         ngrams[curr_chord]["start " + curr_chord] += 1

    # print("Finished parsing songs!")
    # with open("quantify/ngram_data.pkl", "wb") as ngram_output:
    #     pickle.dump(ngrams, ngram_output, pickle.HIGHEST_PROTOCOL)
    # with open("quantify/chord_data.pkl", "wb") as chord_output:
    #     pickle.dump(chord_dict, chord_output, pickle.HIGHEST_PROTOCOL)

    with open("quantify/ngram_data.pkl", "rb") as ngram_output:
        ngrams = pickle.load(ngram_output)
    with open("quantify/chord_data.pkl", "rb") as chord_output:
        chord_dict = pickle.load(chord_output)

    # For every ngram, we calculate I given every chord
    # P(e_i| e_i-(n-1) ... ) = P(e_i-(n-1) ... and e_i) / P(e_i)
    nr_ngrams = sum(len(ngrams[n]) for n in ngrams.keys())
    nr_chords = len(chord_dict.keys())

    # Probability of each chord.
    for chord in chord_dict.keys():
        chord_dict[chord] /= nr_chords

    # Entropy of each progression(sequence) + prob of each sequence, given a chord.
    infor_content = copy.deepcopy(ngrams)
    for chord in ngrams.keys():
        for seq in ngrams[chord]:
            ## TODO: change nr of ngrams to nr of ngrams with similar size
            ngrams[chord][seq] = (ngrams[chord][seq] / nr_ngrams) / chord_dict[chord]
            infor_content[chord][seq] = -math.log2(ngrams[chord][seq])

    print("Finished calculating entropy.")
    # P(e) = freq of chord / nr of chords
    # P(e_i-(n-1) ... and e) = freq of engram / nr of engrams

    entropy = copy.deepcopy(ngrams)
    for chord in entropy.keys():
        for seq in entropy[chord]:
            entropy[chord][seq] = 0

    for chord in ngrams.keys():
        for seq in ngrams[chord]:
            entropy[chord][seq] += ngrams[chord][seq] * infor_content[chord][seq]

    # entropy is uncertainity
    # infor_content is surprise
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
                if curr_chord not in chord_dict:
                    surpr.append(15)
                    uncer.append(8)
                    continue
                

                if i > 0:
                    ngram = ' '.join(line_chords[0:i])
                    # print(ngram)

                    # Impossible to happen, since I check on the same set. 
                    # TODO: Change this later (as well as the one before).
                    if ngram not in ngrams[curr_chord]:
                        surpr.append(15)
                        uncer.append(8)
                        break
                    surpr.append(infor_content[curr_chord][ngram])
                    uncer.append(entropy[curr_chord][ngram])
                else:
                    surpr.append(infor_content[curr_chord]["start " + curr_chord])
                    uncer.append(entropy[curr_chord]["start " + curr_chord])
                
                break
        
    plt.scatter(uncer, surpr)
    plt.xlabel("Uncertainty (bits)")
    plt.ylabel("Surprise (bits)")
                    
    # H will be calculated by reducing the size of the engram,
    # starting from 1 before the chord to the first one
    # e.g. Eb:maj F:min9 Bb:sus4(b7) Eb:maj Ab:min9 Db:9
    # First  : Ab:min9 Db:9
    # Second : Eb:maj Ab:min9 Db:9
    # Third  : Bb:sus4(b7) Eb:maj Ab:min9 Db:9
    # ...

    # Each will be summed.


def main():
    start = time.time()
    PPM("quantify/chords.txt")
    print("Finished in {}".format(time.time() - start))


if __name__ == "__main__":
    main()
