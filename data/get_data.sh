echo "Getting the midi data"
gdown https://storage.googleapis.com/magentadata/datasets/e-gmd/v1.0.0/e-gmd-v1.0.0-midi.zip

echo "Unzipping the archive"
unzip e-gmd-v1.0.0-midi.zip

echo "Moving midi files to the data folder"
python extract_data.py --append 2 -y e-gmd-v1.0.0/ midi/ midi

echo "Cleaning up the remaining files"
rm -rvf e-gmd-v1.0.0/
rm -v e-gmd-v1.0.0-midi.zip