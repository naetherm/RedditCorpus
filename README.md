# RedditCorpus

Small script for parsing all reddit comment data archives, which one can obtain from [0]

## Requirements

We only require `ujson` and `zstandard`, which can be installed by `pip install --user -r requirements.txt` when using Ubuntu or similar or `pacman -S python-zstandard python-ujson` when using an arch based system.

## Usage

Just call the provided file reddit_corpus.py, the arguments should be self-explanatory.
```bash
usage: reddit_corpus.py [-h] --input-dir INPUT_DIR --output-dir OUTPUT_DIR [--threshold THRESHOLD]

optional arguments:
  -h, --help            show this help message and exit
  --input-dir INPUT_DIR
                        The input directory, where all packed archive are located.
  --output-dir OUTPUT_DIR
                        The output directory, where the combinated comments file is saved.
  --threshold THRESHOLD
                        Threshold for the minimum word length of a comment. (default: 3)
```

[0] https://files.pushshift.io/reddit/comments/
