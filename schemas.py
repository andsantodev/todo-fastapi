from pydantic import BaseModel

class TarefaBase(BaseModel):
    titulo: str
    descricao: str | None = None

# Modelo base para tarefa
class TarefaCreate(TarefaBase):
    pass

# Resposta de tarefa
class TarefaResposta(TarefaBase):
    id: int
    concluida: bool

    class Config:
        orm_mode = True

# Update de tarefa
class TarefaUpdate(BaseModel):
    titulo: str
    descricao: str | None = None