from typing import Type

from models import RepoBaseModel
from tables import Base

from .create import CreateRepo
from .read import ReadRepo
from .update import UpdateRepo
from .delete import DeleteRepo


class CRUDRepo[
    TableType: Base,
    ReadModel: RepoBaseModel,
    CreateModel: RepoBaseModel,
    UpdateModel: RepoBaseModel,
](
    CreateRepo[TableType, ReadModel, CreateModel],
    ReadRepo[TableType, ReadModel],
    UpdateRepo[TableType, ReadModel, UpdateModel],
    DeleteRepo[TableType, ReadModel],
):
    def __init__(
        self,
        table_class: Type[TableType],
        read_model_class: Type[ReadModel],
        create_model_class: Type[CreateModel],
        update_model_class: Type[UpdateModel],
    ):
        ReadRepo.__init__(self, table_class, read_model_class)
        CreateRepo.__init__(self, table_class, read_model_class, create_model_class)
        UpdateRepo.__init__(self, table_class, read_model_class, update_model_class)
        DeleteRepo.__init__(self, table_class, read_model_class)
