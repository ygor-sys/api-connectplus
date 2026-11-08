# Central de Comunicados Corporativos — ConnectPlus (Atividade 06)

API em **Python + FastAPI**, banco **SQLite** (SQLAlchemy), autenticação **JWT (Bearer)** e senhas com **bcrypt**.

## Como rodar
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Swagger: http://127.0.0.1:8000/docs  (botão **Authorize** → e-mail no campo *username*)

## Contas de demonstração (criadas automaticamente)
| Perfil | E-mail | Senha |
|---|---|---|
| Administrador | admin@connectplus.com | admin123 |
| Colaborador | colaborador@connectplus.com | colab123 |

## Endpoints
| Método | Rota | Quem | Requisito |
|---|---|---|---|
| POST | /auth/login | todos | RF01 |
| GET | /auth/me | autenticado | RF02 |
| POST | /comunicados | admin | RF03 |
| GET | /comunicados, /comunicados/{id} | autenticado | RF04 |
| PUT | /comunicados/{id} | admin (autor) | RF05 |
| DELETE | /comunicados/{id} | admin (autor) | RF06 |

## Códigos HTTP
200/201/204 sucesso · **401** sem identificação ou credencial errada · **403** colaborador tentando operação de admin · **404** comunicado inexistente · **422** dados inválidos (ex.: sem título).

## Regras de negócio → onde estão
- RN01: `usuario_atual` em `app/deps.py` (todas as rotas de comunicados)
- RN02/03: `somente_admin` em `app/deps.py`
- RN04: validators em `app/schemas.py`
- Restrição ao próprio recurso: `_exigir_autor()` em `app/routers/comunicados.py` (403 se outro admin tentar editar/excluir)
- RN05: `_buscar()` em `app/routers/comunicados.py`
- RN06: autor vem do token; o schema rejeita `autor_id` (`extra="forbid"`)
- RN07: `UsuarioOut` não tem senha/hash
- RN08: nenhum schema de comunicado aceita `perfil`

## Testes (10 cenários da atividade)
```bash
python -m pytest -q
```

## Evidências para a entrega (via Swagger)
1. Login como admin → Authorize → POST /comunicados (201).
2. Login como colaborador → POST ou DELETE /comunicados (403).
3. Sem Authorize → GET /comunicados (401).
4. Criar comunicado → parar o uvicorn → subir de novo → GET /comunicados (continua lá).
