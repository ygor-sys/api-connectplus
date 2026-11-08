# Matriz de permissões — ConnectPlus

> ⚠️ Confira com a matriz que você definiu na Primeira Unidade; ajuste se houver diferença.

| Endpoint | Anônimo | Colaborador | Administrador | Proteção (código) |
|---|---|---|---|---|
| POST /auth/login | ✅ | ✅ | ✅ | pública |
| GET /auth/me | ❌ 401 | ✅ (só os próprios dados) | ✅ (só os próprios dados) | `usuario_atual` |
| GET /comunicados | ❌ 401 | ✅ | ✅ | `usuario_atual` |
| GET /comunicados/{id} | ❌ 401 | ✅ | ✅ | `usuario_atual` |
| POST /comunicados | ❌ 401 | ❌ 403 | ✅ | `somente_admin` |
| PUT /comunicados/{id} | ❌ 401 | ❌ 403 | ✅ só o autor (outro admin: 403) | `somente_admin` + `_exigir_autor` |
| DELETE /comunicados/{id} | ❌ 401 | ❌ 403 | ✅ só o autor (outro admin: 403) | `somente_admin` + `_exigir_autor` |

**401** = não identificado (sem token, token inválido/expirado, senha errada).
**403** = identificado, mas o perfil não permite a operação.

Endpoints protegidos: 6 (3 só para admin, 3 para qualquer autenticado).

## Restrição aos próprios recursos
- `/auth/me` devolve apenas os dados do usuário do token.
- PUT e DELETE de comunicado: o administrador só altera/exclui comunicados dos quais é o autor (`_exigir_autor` em `app/routers/comunicados.py`). Qualquer autenticado continua podendo ler.
