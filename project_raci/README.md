1)
do a cd project_raci
2)
do a pip install -r /workspaces/WebDev/project_raci/requirements.txt
3)
open de database
sqlite3 database.db
4)
Ctrl K Ctrl 0 for colapse functions
5) run main
/home/codespace/.python/current/bin/python /workspaces/WebDev/project_raci/main.py

6)
get context:
find . -type f \( -name "*.py" -o -name "*.sql" \) -exec sh -c '
echo "\n=== $1 ===\n"
cat "$1"
' _ {} \; > contexto_projeto.txt

--------------
# Project RACI

Sistema web para gestão de projetos baseado na matriz RACI, desenvolvido em Python utilizando NiceGUI e SQLite.

## Objetivo

O Project RACI foi criado para centralizar o gerenciamento de:

* Projetos
* Atividades
* Etapas
* Responsáveis
* Áreas
* Clientes
* Status
* Durações
* Dependências entre atividades
* Matriz RACI

O sistema permite modelar projetos completos, definir responsabilidades, dependências e cronogramas de forma visual e simples.

---

# Tecnologias Utilizadas

## Backend

* Python 3.12
* SQLite

## Frontend

* NiceGUI

## Banco de Dados

* SQLite (`database.db`)

---

# Estrutura Geral

```text
project_raci/

├── components/
│   ├── crud_template.py
│   ├── layout.py
│   └── menu.py
│
├── repositories/
│   ├── atividade_repository.py
│   ├── alocacao_repository.py
│   ├── dependencia_repository.py
│   ├── duracao_repository.py
│   ├── projeto_repository.py
│   ├── responsavel_repository.py
│   ├── status_repository.py
│   └── lookups.py
│
├── telas/
│   ├── atividades.py
│   ├── alocacoes.py
│   ├── dependencias.py
│   ├── duracoes.py
│   ├── projetos.py
│   ├── responsaveis.py
│   └── ...
│
├── db.py
├── crud.py
├── main.py
├── database.db
└── requirements.txt
```

---

# Principais Conceitos

## Projeto

Representa uma iniciativa ou demanda de negócio.

Exemplos:

* Implantação SAP
* Dashboard Financeiro
* CRM Global

---

## Etapa

Agrupa atividades semelhantes.

Exemplos:

* Planejamento
* Desenvolvimento
* Testes
* Homologação
* Go Live

---

## Atividade

Representa uma tarefa específica.

Exemplos:

* Levantamento de Requisitos
* Construção do Dashboard
* Testes Integrados

Cada atividade pertence a uma etapa.

---

## Matriz RACI

Define responsabilidade das áreas.

### R

Responsible

Quem executa.

### A

Accountable

Responsável final pela entrega.

### C

Consulted

Consultado durante a execução.

### I

Informed

Mantido informado.

---

## Dependências

Controla precedência entre atividades.

Exemplo:

```text
Levantamento de Requisitos
            ↓
Desenvolvimento
            ↓
Testes
            ↓
Homologação
```

Uma atividade pode possuir:

* múltiplas predecessoras
* múltiplas sucessoras

Tabela utilizada:

```sql
tb_dependencias
```

Campos:

```sql
id_atividade_pai
id_atividade_filho
```

---

## Duração

Permite registrar duração planejada de atividades.

Tabela:

```sql
tb_duracao
```

---

# Instalação

## 1. Entrar na pasta do projeto

```bash
cd project_raci
```

---

## 2. Instalar dependências

```bash
pip install -r /workspaces/WebDev/project_raci/requirements.txt
```

---

## 3. Abrir banco SQLite

```bash
sqlite3 database.db
```

---

## 4. Executar aplicação

```bash
/home/codespace/.python/current/bin/python /workspaces/WebDev/project_raci/main.py
```

---

# Desenvolvimento

## Colapsar funções rapidamente no VS Code

Atalho:

```text
Ctrl + K
Ctrl + 0
```

Útil para navegar arquivos grandes.

---

# Gerar Contexto Completo do Projeto

Comando utilizado para extrair todo o código Python e SQL:

```bash
find . -type f \( -name "*.py" -o -name "*.sql" \) -exec sh -c '
echo "\n=== $1 ===\n"
cat "$1"
' _ {} \; > contexto_projeto.txt
```

Isso gera:

```text
contexto_projeto.txt
```

contendo todo o código-fonte do projeto.

Ideal para:

* análise por IA
* documentação
* auditoria
* revisão técnica

---

# Padrão Arquitetural

O projeto segue uma arquitetura simples baseada em Repository Pattern.

Fluxo:

```text
Tela NiceGUI
      ↓
crud.py
      ↓
Repository
      ↓
SQLite
```

Exemplo:

```text
telas/alocacoes.py
        ↓
crud.py
        ↓
repositories/alocacao_repository.py
        ↓
database.db
```

---

# CRUD Template

Grande parte das telas utiliza:

```python
components/crud_template.py
```

Responsável por:

* Cadastro
* Edição
* Exclusão
* Busca global
* Paginação
* Seleção de registros

Benefícios:

* Menos código repetido
* Padronização visual
* Maior velocidade de desenvolvimento

---

# Funcionalidades Implementadas

## Projetos

* Criar
* Editar
* Excluir
* Listar

## Atividades

* Criar
* Editar
* Excluir
* Associar à etapa

## Áreas

* Cadastro
* Consulta

## Clientes

* Cadastro
* Consulta

## Responsáveis

* Cadastro
* Consulta

## Status

* Cadastro
* Consulta

## RACI

* Cadastro
* Edição
* Exclusão

## Dependências

* Cadastro visual
* Predecessoras
* Sucessoras
* Consulta

## Duração

* Planejamento de atividades

---

# Banco de Dados

Entidades principais:

```text
tb_projeto
tb_atividade
tb_etapa
tb_area
tb_business_unit
tb_responsavel
tb_status
tb_legenda_raci
tb_alocacao
tb_dependencias
tb_duracao
```

---

# Próximas Evoluções

Possíveis melhorias:

* Gráfico de Gantt
* Critical Path Method (CPM)
* Exportação Excel
* Exportação PDF
* Dashboard Executivo
* Controle de capacidade
* Controle de recursos
* Timeline visual
* Dependências por drag-and-drop
* Alertas de atraso
* Integração Power BI

---

# Autor

Projeto desenvolvido para gestão de projetos baseada em RACI utilizando Python, NiceGUI e SQLite.

Esse README já está estruturado para ser colocado diretamente no `README.md` do repositório.
