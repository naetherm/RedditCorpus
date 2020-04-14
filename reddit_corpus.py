# Copyright 2019-2020, University of Freiburg.
# Chair of Algorithms and Data Structures.
# Markus Näther <naetherm@informatik.uni-freiburg.de>

import os
import sys
import argparse
import ujson as json
import bz2
import zstandard
import lzma
import shutil
from pathlib import Path
from html.parser import HTMLParser

class MLStripper(HTMLParser):
  def __init__(self):
    super(MLStripper, self).__init__()
    self.reset()
    self.strict = False
    self.convert_charrefs= True
    self.fed = []
  def handle_data(self, d):
    self.fed.append(d)
  def get_data(self):
    return ''.join(self.fed)

def strip_tags(html):
  s = MLStripper()
  s.feed(html)
  return s.get_data()

def decompress_bz2_to_folder(input_file, dest_dir):
  unpackedfile = bz2.BZ2File(input_file)
  #data = unpackedfile.read()
  with open(dest_dir, 'wb') as fout:
    shutil.copyfileobj(unpackedfile, fout)
    #fout.write(unpackedfile.read())

def decompress_lzma_to_folder(input_file, dest_dir):
  input_file = pathlib.Path(input_file)
  with lzma.open(input_file) as compressed:
    output_path = pathlib.Path(dest_dir) / input_file.stem
    with open(output_path, 'wb') as destination:
      shutil.copyfileobj(compressed, destination)

def decompress_zstandard_to_folder(input_file, dest_dir):
  input_file = pathlib.Path(input_file)
  with open(input_file, 'rb') as compressed:
    decomp = zstandard.ZstdDecompressor()
    output_path = pathlib.Path(dest_dir) / input_file.stem
    with open(output_path, 'wb') as destination:
      decomp.copy_stream(compressed, destination)


def main(argv=None):

  #root_dir = Path(__file__).resolve().parents[0]
  #data_dir = root_dir / 'data'
  #dump_dir = root_dir / 'dump'
  #mkdirs(data_dir, dump_dir)

  if argv is None:
    argv = sys.argv

  parser = argparse.ArgumentParser()
  parser.add_argument("--input-dir", required=True, type=str, help="The input directory, where all packed archive are located.")
  parser.add_argument("--output-dir", required=True, type=str, help="The output directory, where the combinated comments file is saved.")
  parser.add_argument("--threshold", type=int, default=3, help="Threshold for the minimum word length of a comment. (default: 3)")
  args = parser.parse_args()


  # Fetch
  input_path = args.input_dir
  output_path = args.output_dir

  files = os.listdir(input_path)

  reddit_body_text = open(os.path.join(output_path, 'reddit_body_text.dat'), 'w')

  for file_path in files:
    ext_ = os.path.splitext(file_path)[1]
    print("Ext: {}".format(ext_))
    if ext_ == ".bz2":
      decompress_bz2_to_folder(os.path.join(input_path,file_path), os.path.join(output_path, os.path.splitext(file_path)[0]))
    if ext_ == ".xz":
      decompress_lzma_to_folder(os.path.join(input_path,file_path), os.path.join(output_path, os.path.splitext(file_path)[0]))
    if ext_ == ".zst":
      decompress_zstandard_to_folder(os.path.join(input_path,file_path), os.path.join(output_path, os.path.splitext(file_path)[0]))

    raw_content = None

    with open(os.path.join(output_path, os.path.splitext(file_path)[0]), 'r', encoding='utf-8') as fin:
      for line in fin:
        json_input = json.loads(line)

        if ((json_input["body"] != None) and (json_input["body"] != "[deleted]") and (len(json_input["body"].split()) > args.threshold)):
          reddit_body_text.write(strip_tags(json_input["body"]) + '\n')
    os.remove(os.path.join(output_path, os.path.splitext(file_path)[0]))

  reddit_body_text.close()

if __name__ == '__main__':
  main()
