from typing import Annotated

from sqlalchemy.orm import mapped_column

pk_id = Annotated[int, mapped_column(primary_key=True)]
