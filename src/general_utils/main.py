import dataclasses
import json
import math
import os
import pickle
import unicodedata
from pathlib import Path
from typing import (Any, Callable, Dict, List, Optional, Set, Tuple, Type,
                    TypeVar)


def get_basename(filepath: Path) -> str:
  '''test.wav -> test'''
  return filepath.stem
  # basename, _ = os.path.splitext(os.path.basename(filepath))
  # return basename


def get_all_files_in_all_subfolders(dir: Path) -> Set[Path]:
  all_files = set()
  for root, _, files in os.walk(dir):
    for name in files:
      file_path = Path(root) / name
      all_files.add(file_path)
  return all_files


def get_filepaths(parent_dir: Path) -> List[Path]:
  names = get_filenames(parent_dir)
  res = [parent_dir / x for x in names]
  return res


def get_filenames(parent_dir: Path) -> List[Path]:
  assert parent_dir.is_dir()
  _, _, filenames = next(os.walk(parent_dir))
  filenames.sort()
  filenames = [Path(filename) for filename in filenames]
  return filenames


def get_subfolders(parent_dir: Path) -> List[Path]:
  names = get_subfolder_names(parent_dir)
  res = [parent_dir / x for x in names]
  return res


def get_subfolder_names(parent_dir: Path) -> List[str]:
  assert parent_dir.is_dir()
  _, subfolder_names, _ = next(os.walk(parent_dir))
  subfolder_names.sort()
  return subfolder_names


def read_lines(path: Path, encoding: str = 'utf-8') -> List[str]:
  assert path.is_file()
  with path.open(mode="r", encoding=encoding) as f:
    lines = f.readlines()
  res = [x.strip("\n") for x in lines]
  return res


def save_obj(obj: Any, path: Path) -> None:
  assert path.parent.exists() and path.parent.is_dir()
  with open(path, mode="wb") as file:
    pickle.dump(obj, file)


def load_obj(path: Path) -> Any:
  assert path.exists() and path.is_file()
  with open(path, mode="rb") as file:
    return pickle.load(file)


def args_to_str(args) -> str:
  res = ""
  for arg, value in sorted(vars(args).items()):
    res += f"{arg}: {value}\n"
  return res


def str_to_int(val: str) -> int:
  '''maps a string to int'''
  mapped = [(i + 1) * ord(x) for i, x in enumerate(val)]
  res = sum(mapped)
  return res


_T = TypeVar('_T')


def parse_json(path: Path, encoding: str = 'utf-8') -> Dict:
  assert path.is_file()
  with path.open(mode='r', encoding=encoding) as f:
    tmp = json.load(f)
  return tmp


def save_json(path: Path, obj: Dict, encoding: str = 'utf-8') -> None:
  with path.open(mode='w', encoding=encoding) as f:
    json.dump(obj, f, ensure_ascii=False, indent=2)


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


def pass_lines(method: Callable[[str], Any], text: str) -> None:
  lines = text.split("\n")
  pass_lines_list(method, lines)


def pass_lines_list(method: Callable[[str], Any], lines: List[str]) -> None:
  for l in lines:
    method(l)


def cast_as(obj, _: _T) -> _T:
  return obj


def get_chunk_name(i: int, chunksize: int, maximum: int) -> str:
  assert i >= 0
  assert chunksize > 0
  assert maximum >= 0
  start = i // chunksize
  start *= chunksize
  end = start + chunksize - 1
  end = min(end, maximum)
  res = f"{start}-{end}"
  return res


def get_value_in_type(old_value: _T, new_value: str) -> _T:
  old_type = type(old_value)
  if new_value == "":
    new_value_with_original_type = None
  else:
    new_value_with_original_type = old_type(new_value)
  return new_value_with_original_type


def check_has_unknown_params(params: Dict[str, str], hparams: _T) -> bool:
  available_params = dataclasses.asdict(hparams)
  for custom_hparam in params.keys():
    if custom_hparam not in available_params.keys():
      return True
  return False


def set_types_according_to_dataclass(params: Dict[str, str], hparams: _T) -> None:
  available_params = dataclasses.asdict(hparams)
  for custom_hparam, new_value in params.items():
    assert custom_hparam in available_params.keys()
    hparam_value = available_params[custom_hparam]
    params[custom_hparam] = get_value_in_type(hparam_value, new_value)


def get_only_known_params(params: Dict[str, str], hparams: _T) -> Dict[str, str]:
  available_params = dataclasses.asdict(hparams)
  res = {k: v for k, v in params.items() if k in available_params.keys()}
  return res


def overwrite_custom_hparams(hparams_dc: _T, custom_hparams: Optional[Dict[str, str]]) -> _T:
  if custom_hparams is None:
    return hparams_dc

  # custom_hparams = get_only_known_params(custom_hparams, hparams_dc)
  if check_has_unknown_params(custom_hparams, hparams_dc):
    raise Exception()

  set_types_according_to_dataclass(custom_hparams, hparams_dc)

  result = dataclasses.replace(hparams_dc, **custom_hparams)
  return result


def get_dataclass_from_dict(params: Dict[str, str], dc: Type[_T]) -> Tuple[_T, Set[str]]:
  field_names = {x.name for x in dataclasses.fields(dc)}
  res = {k: v for k, v in params.items() if k in field_names}
  ignored = {k for k in params.keys() if k not in field_names}
  return dc(**res), ignored
