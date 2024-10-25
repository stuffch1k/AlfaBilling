from pydantic import BaseModel, ConfigDict, EmailStr


class OperatorLoginSchema(BaseModel):
    """
    Pydantic модель оператора для входа

    Attributes
    ----------
    email: EmailStr
        почта
    password: str
        пароль
    """
    email: EmailStr
    password: str


class OperatorBaseSchema(BaseModel):
    name: str
    surname: str
    email: EmailStr


class OperatorCreateSchema(OperatorBaseSchema):
    """
    Pydantic модель оператора для регистрации

    Attributes
    ----------
    name: str
        имя
    surname: str
        фамилия
    email: EmailStr
        почта
    password: str
        пароль
    """
    password: str


class OperatorSchema(OperatorBaseSchema):
    """
    Pydantic модель оператора

    Attributes
    ----------
    id: int
        id оператора из бд
    name: str
        имя
    surname: str
        фамилия
    email: EmailStr
        почта
    role: str
        роль "operator"
    """
    id: int
    role: str = "operator"

    model_config = ConfigDict(from_attributes=True)
