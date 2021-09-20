import os
from pathlib import Path
from typing import List


def get_basename(filepath: Path) -> str:
  '''test.wav -> test'''
  basename, _ = os.path.splitext(os.path.basename(filepath))
  return basename


def get_filepaths(parent_dir: Path) -> List[Path]:
  names = get_filenames(parent_dir)
  res = [parent_dir / x for x in names]
  return res


def get_filenames(parent_dir: Path) -> List[str]:
  assert parent_dir.is_dir()
  _, _, filenames = next(os.walk(parent_dir))
  filenames.sort()
  return filenames


def get_subfolders(parent_dir: Path) -> List[Path]:
  """return full paths"""
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


def read_text(path: Path, encoding: str = 'utf-8') -> str:
  res = '\n'.join(read_lines(path, encoding))
  return res
