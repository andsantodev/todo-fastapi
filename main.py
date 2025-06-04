from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from typing import List, Optional
import time

from auth import verificar_token
from database import engine, SessionLocal
import schemas
import models

print(">> Iniciando aplicação")

app = FastAPI()


# Tentativa de criar tabelas (com retry)
for i in range(3):
    try:
        models.Base.metadata.create_all(bind=engine)
        print(">> Tabelas criadas com sucesso.")
        break
    except Exception as e:
        print(">> Tentativa de criação falhou:", e)
        time.sleep(2)


# Gerenciador de sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Configuração para exibir o botão "Authorize" no Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="FastAPI",
        version="1.0.0",
        description="API para gerenciamento de tarefas com autenticação via token",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# ------------------ ROTAS ------------------

@app.post("/tarefas", response_model=schemas.TarefaResposta, status_code=status.HTTP_201_CREATED)
def criar_tarefa(tarefa: schemas.TarefaCreate, db: Session = Depends(get_db), _: str = Depends(verificar_token)):
    nova_tarefa = models.Tarefa(**tarefa.dict())
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa

@app.get("/tarefas", response_model=List[schemas.TarefaResposta])
def listar_tarefas(concluida: Optional[bool] = Query(None), db: Session = Depends(get_db), _: str = Depends(verificar_token)):
    if concluida is None:
        return db.query(models.Tarefa).all()
    return db.query(models.Tarefa).filter(models.Tarefa.concluida == concluida).all()

@app.put("/tarefas/{tarefa_id}", response_model=schemas.TarefaResposta)
def atualizar_tarefa(tarefa_id: int, tarefa_dados: schemas.TarefaUpdate, db: Session = Depends(get_db), _: str = Depends(verificar_token)):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tarefa.titulo = tarefa_dados.titulo
    tarefa.descricao = tarefa_dados.descricao
    tarefa.concluida = tarefa_dados.concluida
    db.commit()
    db.refresh(tarefa)
    return tarefa

@app.delete("/tarefas/{tarefa_id}", status_code=204)
def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db), _: str = Depends(verificar_token)):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(tarefa)
    db.commit()