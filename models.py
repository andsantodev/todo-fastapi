from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String)
    concluida = Column(Boolean, default=False, nullable=False)