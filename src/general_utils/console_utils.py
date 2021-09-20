from typing import Dict, List, Optional, Set, Tuple


def parse_tuple_list(tuple_list: Optional[str] = None) -> Optional[List[Tuple]]:
  """ tuple_list: "a,b;c,d;... """
  if tuple_list is None:
    return None

  step1: List[str] = tuple_list.split(';')
  result: List[Tuple] = [tuple(x.split(',')) for x in step1]
  result = list(sorted(set(result)))
  return result


def split_hparams_string(hparams: Optional[str]) -> Optional[Dict[str, str]]:
  if hparams is None:
    return None

  assignments = hparams.split(",")
  result = dict([x.split("=") for x in assignments])
  return result


def split_int_set_str(ints: Optional[str]) -> Optional[Set[int]]:
  """ tuple_list: "1,2,4" """
  if ints is None:
    return None
  if len(ints) == 0:
    return set()
  ints_list = ints.split(",")
  ints_set = set(map(int, ints_list))
  return ints_set


def split_str_set_symbols(string_input: Optional[str]) -> Optional[Set[str]]:
  """ tuple_list: "a b c" """
  if string_input is None:
    return None
  if len(string_input) == 0:
    return set()
  symbols_list = string_input.split(" ")
  symbols_set = set(symbols_list)
  return symbols_set


def parse_set(set_str: str, split_symbol: str) -> Set[str]:
  """ tuple_list: "a b c d" """
  step1: List[str] = set_str.split(split_symbol)
  result = set(step1)
  return result


def split_string(s: Optional[str], sep: str = "|") -> Optional[List[str]]:
  if s is None:
    return None

  res = s.split(sep)
  return res
