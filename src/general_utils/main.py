import json
import logging
import math
import os
import random
import tarfile
import unicodedata
from abc import ABC
from collections import Counter
from dataclasses import astuple
from pathlib import Path
from typing import (Any, Dict, Generic, List, Optional, Set, Tuple, Type,
                    TypeVar, Union)

import numpy as np
import pandas as pd
import torch
import wget
from matplotlib.figure import Figure
from PIL import Image
from tqdm import tqdm

_T = TypeVar('_T')

def have_common_entries(l: Union[Tuple[_T], List[_T]], s: Union[Tuple[_T], List[_T]]) -> bool:
  res = len(set(l).union(set(s))) > 0
  return res


def contains_only_allowed_symbols(l: Union[Tuple[_T], List[_T]], allowed: Union[Tuple[_T], List[_T]]) -> bool:
  res = len(set(l).difference(set(allowed))) == 0
  return res

def cast_as(obj, _: _T) -> _T:
  return obj


def pass_lines(method: Any, text: str):
  lines = text.split("\n")
  for l in lines:
    method(l)


def figure_to_numpy_rgb(figure: Figure) -> np.ndarray:
  figure.canvas.draw()
  data = np.fromstring(figure.canvas.tostring_rgb(), dtype=np.uint8, sep='')
  data = data.reshape(figure.canvas.get_width_height()[::-1] + (3,))
  return data


def get_filenames(parent_dir: str) -> List[str]:
  assert os.path.isdir(parent_dir)
  _, _, filenames = next(os.walk(parent_dir))
  filenames.sort()
  return filenames


def get_filepaths(parent_dir: str) -> List[str]:
  names = get_filenames(parent_dir)
  res = [os.path.join(parent_dir, x) for x in names]
  return res


def get_subfolder_names(parent_dir: str) -> List[str]:
  assert os.path.isdir(parent_dir)
  _, subfolder_names, _ = next(os.walk(parent_dir))
  subfolder_names.sort()
  return subfolder_names


def get_subfolders(parent_dir: str) -> List[str]:
  """return full paths"""
  names = get_subfolder_names(parent_dir)
  res = [os.path.join(parent_dir, x) for x in names]
  return res


def console_out_len(text: str):
  res = len([c for c in text if unicodedata.combining(c) == 0])
  return res


def make_batches_v_h(arr: List[_T], v: int, h: int) -> List[List[_T]]:
  vertical_merge_count = math.ceil(len(arr) / v)
  # print("v", vertical_merge_count)
  horizontal_merge_count = math.ceil(vertical_merge_count / h)
  # print("h", horizontal_merge_count)

  current = 0
  vertical_batches = []

  for _ in range(vertical_merge_count):
    vertical_batch = arr[current:current + v]
    current += v
    vertical_batches.append(vertical_batch)
  # print(vertical_batches)

  current = 0
  horizontal_batches = []
  for _ in range(horizontal_merge_count):
    horizontal_batch = vertical_batches[current:current + h]
    current += h
    horizontal_batches.append(horizontal_batch)

  return horizontal_batches

# TODO: tests


def make_batches_h_v(arr: List[_T], v: int, h: int) -> List[List[_T]]:
  horizontal_merge_count = math.ceil(len(arr) / h)
  # print("v", vertical_merge_count)
  vertical_merge_count = math.ceil(horizontal_merge_count / v)
  # print("h", horizontal_merge_count)

  current = 0
  horizontal_batches = []
  for _ in range(horizontal_merge_count):
    horizontal_batch = arr[current:current + h]
    current += h
    horizontal_batches.append(horizontal_batch)

  current = 0
  vertical_batches = []

  for _ in range(vertical_merge_count):
    vertical_batch = horizontal_batches[current:current + v]
    current += v
    vertical_batches.append(vertical_batch)
  # print(vertical_batches)

  return vertical_batches


class GenericList(list, Generic[_T]):
  def save(self, file_path: str, header: bool = False):
    data = [astuple(xi) for xi in self.items()]
    dataframe = pd.DataFrame(data)
    header_cols = None
    if header and len(self) > 0:
      first_entry = self.items()[0]
      header_cols = list(first_entry.__dataclass_fields__.keys())
    save_df(dataframe, file_path, header_columns=header_cols)

  @classmethod
  def load(cls, member_class: Type[_T], file_path: str):
    data = try_load_df(file_path)
    data_is_not_empty = data is not None
    if data_is_not_empty:
      data_loaded: List[_T] = [member_class(*xi) for xi in data.values]
      res = cls(data_loaded)
      res.load_init()
    else:
      res = cls()
    return res

  def load_init(self):
    return self

  def items(self, with_tqdm: bool = False) -> List[_T]:
    if with_tqdm:
      return tqdm(self)
    return self

  def get_random_entry(self) -> _T:
    idx = random.choice(range(len(self)))
    return self[idx]


def try_load_df(path: str) -> Optional[pd.DataFrame]:
  try:
    return load_df(path)
  except pd.errors.EmptyDataError:
    return None


def load_df(path: str) -> pd.DataFrame:
  data = pd.read_csv(path, header=None, sep=CSV_SEPERATOR)
  return data


def save_df(dataframe: pd.DataFrame, path: str, header_columns: Optional[List[str]]):
  dataframe.to_csv(path, header=header_columns, index=None, sep=CSV_SEPERATOR)



def get_sorted_list_from_set(unsorted_set: Set[_T]) -> List[_T]:
  res: List[_T] = list(sorted(list(unsorted_set)))
  return res


def remove_duplicates_list_orderpreserving(l: List[str]) -> List[str]:
  result = []
  for x in l:
    if x not in result:
      result.append(x)
  assert len(result) == len(set(result))
  return result


def get_counter(l: List[List[_T]]) -> Counter:
  items = []
  for sublist in l:
    items.extend(sublist)
  symbol_counter = Counter(items)
  return symbol_counter


def get_unique_items(of_list: List[Union[List[_T], Set[_T]]]) -> Set[_T]:
  items: Set[_T] = set()
  for sub_entries in of_list:
    items = items.union(set(sub_entries))
  return items

def make_same_dim(a: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
  dim_a = a.shape[1]
  dim_b = b.shape[1]
  diff = abs(dim_a - dim_b)
  if diff > 0:
    adding_array = np.zeros(shape=(a.shape[0], diff))
    if dim_a < dim_b:
      a = np.concatenate((a, adding_array), axis=1)
    else:
      b = np.concatenate((b, adding_array), axis=1)
  assert a.shape == b.shape
  return a, b


def get_basename(filepath: str) -> str:
  '''test.wav -> test'''
  basename, _ = os.path.splitext(os.path.basename(filepath))
  return basename


def get_parent_dirname(filepath: str) -> str:
  last_dir_name = Path(filepath).parts[-1]
  return last_dir_name


def get_chunk_name(i, chunksize, maximum) -> str:
  assert i >= 0
  assert chunksize > 0
  assert maximum >= 0
  start = i // chunksize
  start *= chunksize
  end = start + chunksize - 1
  if end > maximum:
    end = maximum
  res = f"{start}-{end}"
  return res

def download_tar(download_url, dir_path, tarmode: str = "r:gz") -> None:
  print("Starting download of {}...".format(download_url))
  os.makedirs(dir_path, exist_ok=True)
  dest = wget.download(download_url, dir_path)
  downloaded_file = os.path.join(dir_path, dest)
  print("\nFinished download to {}".format(downloaded_file))
  print("Unpacking...")
  tar = tarfile.open(downloaded_file, tarmode)
  tar.extractall(dir_path)
  tar.close()
  os.remove(downloaded_file)
  print("Done.")


def args_to_str(args) -> str:
  res = ""
  for arg, value in sorted(vars(args).items()):
    res += "{}: {}\n".format(arg, value)
  return res


def parse_json(path: str) -> dict:
  assert os.path.isfile(path)
  with open(path, 'r', encoding='utf-8') as f:
    tmp = json.load(f)
  return tmp


def save_json(path: str, mapping_dict: Dict) -> None:
  with open(path, 'w', encoding='utf-8') as f:
    json.dump(mapping_dict, f, ensure_ascii=False, indent=2)


def save_txt(path: str, text: str) -> None:
  with open(path, 'w', encoding='utf-8') as f:
    f.write(text)



def read_lines(path: str) -> List[str]:
  assert os.path.isfile(path)
  with open(path, "r", encoding='utf-8') as f:
    lines = f.readlines()
  res = [x.strip("\n") for x in lines]
  return res


def read_text(path: str) -> str:
  res = '\n'.join(read_lines(path))
  return res
