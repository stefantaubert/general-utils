import dataclasses
import random
from typing import Generic, List, Optional, TypeVar

from tqdm import tqdm

_T = TypeVar('_T')


class GenericList(list, Generic[_T]):
  # def save(self, file_path: str, header: bool = False):
  #   data = [dataclasses.astuple(xi) for xi in self.items()]
  #   dataframe = pd.DataFrame(data)
  #   header_cols = None
  #   if header and len(self) > 0:
  #     first_entry = self.items()[0]
  #     header_cols = list(first_entry.__dataclass_fields__.keys())
  #   save_df(dataframe, file_path, header_columns=header_cols)

  # @classmethod
  # def load(cls, member_class: Type[_T], file_path: str):
  #   data = try_load_df(file_path)
  #   data_is_not_empty = data is not None
  #   if data_is_not_empty:
  #     data_loaded: List[_T] = [member_class(*xi) for xi in data.values]
  #     res = cls(data_loaded)
  #     res.load_init()
  #   else:
  #     res = cls()
  #   return res

  # def load_init(self):
  #   return self

  def items(self, with_tqdm: bool = False) -> List[_T]:
    if with_tqdm:
      return tqdm(self)
    return self

  def items_tqdm(self) -> List[_T]:
    return tqdm(self)

  def get_random_entry(self) -> Optional[_T]:
    if len(self) == 0:
      return None
    idx = random.choice(range(len(self)))
    return self[idx]
