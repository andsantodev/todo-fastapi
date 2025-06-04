from fastapi import FastAPI
from database import engine
from auth import verificar_token
import models
import time

print(">> Iniciando aplicação")

app = FastAPI()

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
import schemas
import models

for i in range(3):
    try:
        models.Base.metadata.create_all(bind=engine)
        print(">> Tabelas criadas com sucesso.")
        break
    except Exception as e:
        print(">> Tentativa de criação falhou:", e)
        time.sleep(2)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Criação de uma tarefa
@app.post("/tarefas", response_model=schemas.TarefaResposta, status_code=status.HTTP_201_CREATED)
def criar_tarefa(tarefa: schemas.TarefaCreate, db: Session = Depends(get_db), _: str = Depends(verificar_token)):
    nova_tarefa = models.Tarefa(**tarefa.dict())
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa

# Listagem de tarefas
from typing import List, Optional
from fastapi import Query

# Listar tarefas com filtro opcional de concluída
@app.get("/tarefas", response_model=List[schemas.TarefaResposta])
def listar_tarefas(concluida: Optional[bool] = Query(None), db: Session = Depends(get_db), _: str = Depends(verificar_token)):
    if concluida is None:
        return db.query(models.Tarefa).all()
    return db.query(models.Tarefa).filter(models.Tarefa.concluida == concluida).all()

# Detalhes de uma tarefa
@app.put("/tarefas/{tarefa_id}", response_model=schemas.TarefaResposta)
def atualizar_tarefa(tarefa_id: int, tarefa_dados: schemas.TarefaUpdate, db: Session = Depends(get_db), _: str = Depends(verificar_token)):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tarefa.titulo = tarefa_dados.titulo
    tarefa.descricao = tarefa_dados.descricao
    db.commit()
    db.refresh(tarefa)
    return tarefa

# Marcar tarefa como concluída
@app.patch("/tarefas/{tarefa_id}/concluir", response_model=schemas.TarefaResposta)
def concluir_tarefa(tarefa_id: int, db: Session = Depends(get_db), _: str = Depends(verificar_token)):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tarefa.concluida = True
    db.commit()
    db.refresh(tarefa)
    return tarefa

# Excluir uma tarefa
@app.delete("/tarefas/{tarefa_id}", status_code=204)
def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db), _: str = Depends(verificar_token)):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(tarefa)
    db.commit()

# Middleware para verificar token de autenticação
from auth import verificar_token