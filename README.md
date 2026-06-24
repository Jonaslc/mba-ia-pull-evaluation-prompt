# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Você deve entregar um software capaz de:

1. **Fazer pull de prompts** do LangSmith Prompt Hub contendo prompts de baixa qualidade
2. **Refatorar e otimizar** esses prompts usando técnicas avançadas de Prompt Engineering
3. **Fazer push dos prompts otimizados** de volta ao LangSmith
4. **Avaliar a qualidade** através de métricas customizadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
5. **Atingir pontuação mínima** de 0.8 (80%) em todas as métricas de avaliação

---

## Exemplo no CLI

**Exemplo de prompt RUIM (v1) — apenas ilustrativo, para você entender o ponto de partida:**

```
==================================================
Prompt: {seu_username}/bug_to_user_story_v1
==================================================

Métricas Derivadas:
  - Helpfulness: 0.45 ✗
  - Correctness: 0.52 ✗

Métricas Base:
  - F1-Score: 0.48 ✗
  - Clarity: 0.50 ✗
  - Precision: 0.46 ✗

❌ STATUS: REPROVADO
⚠️  Métricas abaixo de 0.8: helpfulness, correctness, f1_score, clarity, precision
```

**Exemplo de prompt OTIMIZADO (v2) — seu objetivo é chegar aqui:**

```bash
# Após refatorar os prompts e fazer push
python src/push_prompts.py

# Executar avaliação
python src/evaluate.py

Executando avaliação dos prompts...
==================================================
Prompt: {seu_username}/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.94 ✓
  - Correctness: 0.96 ✓

Métricas Base:
  - F1-Score: 0.93 ✓
  - Clarity: 0.95 ✓
  - Precision: 0.92 ✓

✅ STATUS: APROVADO - Todas as métricas >= 0.8
```

---

## Tecnologias obrigatórias

- **Linguagem:** Python 3.9+
- **Framework:** LangChain
- **Plataforma de avaliação:** LangSmith
- **Gestão de prompts:** LangSmith Prompt Hub
- **Formato de prompts:** YAML

---

## Pacotes recomendados

```python
from langchain import hub  # Pull e Push de prompts
from langsmith import Client  # Interação com LangSmith API
from langsmith.evaluation import evaluate  # Avaliação de prompts
from langchain_openai import ChatOpenAI  # LLM OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # LLM Gemini
```

---

## OpenAI

- Crie uma **API Key** da OpenAI: https://platform.openai.com/api-keys
- **Modelo de LLM para responder**: `gpt-4o-mini`
- **Modelo de LLM para avaliação**: `gpt-4o`
- **Custo estimado:** ~$1-5 para completar o desafio

## Gemini (modelo free)

- Crie uma **API Key** da Google: https://aistudio.google.com/app/apikey
- **Modelo de LLM para responder**: `gemini-2.5-flash`
- **Modelo de LLM para avaliação**: `gemini-2.5-flash`
- **Limite:** 15 req/min, 1500 req/dia

---

## Requisitos

### 1. Pull do Prompt inicial do LangSmith

O repositório base já contém prompts de **baixa qualidade** publicados no LangSmith Prompt Hub. Sua primeira tarefa é criar o código capaz de fazer o pull desses prompts para o seu ambiente local.

**Tarefas:**

1. Configurar suas credenciais do LangSmith no arquivo `.env` (conforme o arquivo `.env.example`)
2. Implementar o script `src/pull_prompts.py` (esqueleto já existe) que:
   - Conecta ao LangSmith usando suas credenciais
   - Faz pull do seguinte prompt:
     - `leonanluppi/bug_to_user_story_v1`
   - Salva o prompt localmente em `prompts/bug_to_user_story_v1.yml`

---

### 2. Otimização do Prompt

Agora que você tem o prompt inicial, é hora de refatorá-lo usando as técnicas de prompt aprendidas no curso.

**Tarefas:**

1. Analisar o prompt em `prompts/bug_to_user_story_v1.yml`
2. Criar um novo arquivo `prompts/bug_to_user_story_v2.yml` com suas versões otimizadas
3. Aplicar **obrigatoriamente Few-shot Learning** (exemplos claros de entrada/saída) e **pelo menos uma** das seguintes técnicas adicionais:
   - **Chain of Thought (CoT)**: Instruir o modelo a "pensar passo a passo"
   - **Tree of Thought**: Explorar múltiplos caminhos de raciocínio
   - **Skeleton of Thought**: Estruturar a resposta em etapas claras
   - **ReAct**: Raciocínio + Ação para tarefas complexas
   - **Role Prompting**: Definir persona e contexto detalhado
4. Documentar no `README.md` quais técnicas você escolheu e por quê

**Requisitos do prompt otimizado:**

- Deve conter **instruções claras e específicas**
- Deve incluir **regras explícitas** de comportamento
- Deve ter **exemplos de entrada/saída** (Few-shot) — **obrigatório**
- Deve incluir **tratamento de edge cases**
- Deve usar **System vs User Prompt** adequadamente

---

### 3. Push e Avaliação

Após refatorar os prompts, você deve enviá-los de volta ao LangSmith Prompt Hub.

**Tarefas:**

1. Implementar o script `src/push_prompts.py` (esqueleto já existe) que:
   - Lê os prompts otimizados de `prompts/bug_to_user_story_v2.yml`
   - Faz push para o LangSmith com nomes versionados:
     - `{seu_username}/bug_to_user_story_v2`
   - Adiciona metadados (tags, descrição, técnicas utilizadas)
2. Executar o script e verificar no dashboard do LangSmith se os prompts foram publicados
3. Deixá-lo público

---

### 4. Iteração

- Espera-se 3-5 iterações.
- Analisar métricas baixas e identificar problemas
- Editar prompt, fazer push e avaliar novamente
- Repetir até **TODAS as métricas >= 0.8**

### Critério de Aprovação:

```
- Helpfulness >= 0.8
- Correctness >= 0.8
- F1-Score >= 0.8
- Clarity >= 0.8
- Precision >= 0.8

MÉDIA das 5 métricas >= 0.8
```

**IMPORTANTE:** TODAS as 5 métricas devem estar >= 0.8, não apenas a média!

### 5. Testes de Validação

**O que você deve fazer:** Edite o arquivo `tests/test_prompts.py` e implemente, no mínimo, os 6 testes abaixo usando `pytest`:

- `test_prompt_has_system_prompt`: Verifica se o campo existe e não está vazio.
- `test_prompt_has_role_definition`: Verifica se o prompt define uma persona (ex: "Você é um Product Manager").
- `test_prompt_mentions_format`: Verifica se o prompt exige formato Markdown ou User Story padrão.
- `test_prompt_has_few_shot_examples`: Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
- `test_prompt_no_todos`: Garante que você não esqueceu nenhum `[TODO]` no texto.
- `test_minimum_techniques`: Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas.

**Como validar:**

```bash
pytest tests/test_prompts.py
```

---

## Estrutura obrigatória do projeto

Faça um fork do repositório base: **[Clique aqui para o template](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt)**

```
mba-ia-pull-evaluation-prompt/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Sua documentação do processo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml  # Prompt inicial (já incluso)
│   └── bug_to_user_story_v2.yml  # Seu prompt otimizado (criar)
│
├── datasets/
│   └── bug_to_user_story.jsonl   # 15 exemplos de bugs (já incluso)
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith (implementar)
│   ├── push_prompts.py       # Push ao LangSmith (implementar)
│   ├── evaluate.py           # Avaliação automática (pronto)
│   ├── metrics.py            # 5 métricas implementadas (pronto)
│   └── utils.py              # Funções auxiliares (pronto)
│
├── tests/
│   └── test_prompts.py       # Testes de validação (implementar)
```

**O que você deve implementar:**

- `prompts/bug_to_user_story_v2.yml` — Criar do zero com seu prompt otimizado
- `src/pull_prompts.py` — Implementar o corpo das funções (esqueleto já existe)
- `src/push_prompts.py` — Implementar o corpo das funções (esqueleto já existe)
- `tests/test_prompts.py` — Implementar os 6 testes de validação (esqueleto já existe)
- `README.md` — Documentar seu processo de otimização

**O que já vem pronto (não alterar):**

- `src/evaluate.py` — Script de avaliação completo
- `src/metrics.py` — 5 métricas implementadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
- `src/utils.py` — Funções auxiliares
- `datasets/bug_to_user_story.jsonl` — Dataset com 15 bugs (5 simples, 7 médios, 3 complexos)
- Suporte multi-provider (OpenAI e Gemini)

## Repositórios úteis

- [Repositório boilerplate do desafio](https://github.com/devfullcycle/mba-ia-prompt-engineering)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## VirtualEnv para Python

Crie e ative um ambiente virtual antes de instalar dependências:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Ordem de execução

### 1. Executar pull dos prompts ruins

```bash
python src/pull_prompts.py
```

### 2. Refatorar prompts

Edite manualmente o arquivo `prompts/bug_to_user_story_v2.yml` aplicando as técnicas aprendidas no curso.

### 3. Fazer push dos prompts otimizados

```bash
python src/push_prompts.py
```

### 4. Executar avaliação

```bash
python src/evaluate.py
```

---

## Entregável

**1. Repositório público no GitHub** (fork do repositório base) contendo:

- Todo o código-fonte implementado
- Arquivo `prompts/bug_to_user_story_v2.yml` 100% preenchido e funcional
- Arquivo `README.md` atualizado

**2. README.md deve conter:**

**A) Seção "Técnicas Aplicadas (Fase 2)":**

- Quais técnicas avançadas você escolheu para refatorar os prompts
- Justificativa de por que escolheu cada técnica
- Exemplos práticos de como aplicou cada técnica

**B) Seção "Resultados Finais":**

- Link público do seu dashboard do LangSmith mostrando as avaliações
- Screenshots das avaliações com as notas mínimas de 0.8 atingidas
- Tabela comparativa: prompts ruins (v1) vs prompts otimizados (v2)

**C) Seção "Como Executar":**

- Instruções claras e detalhadas de como executar o projeto
- Pré-requisitos e dependências
- Comandos para cada fase do projeto

**3. Evidências no LangSmith:**

- Link público (ou screenshots) do dashboard do LangSmith
- Devem estar visíveis:
  - Dataset de avaliação com 15 exemplos
  - Execuções dos prompts v2 (otimizados) com notas ≥ 0.8
  - Tracing detalhado de pelo menos 3 exemplos

---

## Dicas Finais

- **Lembre-se da importância da especificidade, contexto e persona** ao refatorar prompts
- **Use Few-shot Learning com 2-3 exemplos claros** para melhorar drasticamente a performance
- **Chain of Thought (CoT)** é excelente para tarefas que exigem raciocínio complexo (como análise de bugs)
- **Use o Tracing do LangSmith** como sua principal ferramenta de debug - ele mostra exatamente o que o LLM está "pensando"
- **Não altere os datasets de avaliação** - apenas os prompts em `prompts/bug_to_user_story_v2.yml`
- **Itere, itere, itere** - é normal precisar de 3-5 iterações para atingir 0.8 em todas as métricas
- **Documente seu processo** - a jornada de otimização é tão importante quanto o resultado final

---
---

# 📦 Documentação da Entrega (Solução)

> Esta seção documenta a resolução do desafio: técnicas aplicadas, resultados e como executar.

## A) Técnicas Aplicadas (Fase 2)

O prompt otimizado está em [`prompts/bug_to_user_story_v2.yml`](prompts/bug_to_user_story_v2.yml).
Foram aplicadas **4 técnicas** de Prompt Engineering (Few-shot obrigatório + 3 adicionais):

| Técnica | Por que escolhi | Como apliquei |
|---|---|---|
| **Few-shot Learning** (obrigatória) | É a alavanca mais forte para padronizar o **formato** e o **escopo** da saída, que é exatamente o que as métricas F1/Correctness comparam contra o *ground truth*. Ampliar a cobertura dos exemplos foi o que levou o F1 de 0.81 → 0.88. | Incluí exemplos entrada→saída no `system_prompt` cobrindo os três níveis: **SIMPLES** (carrinho, validação de email, UI mobile, dado incorreto, compatibilidade de navegador), **MÉDIO** (webhook HTTP 500, permissões/OWASP, cálculo de desconto, performance/índice SQL, estoque com critérios de prevenção) e **COMPLEXO** (checkout com XSS + race condition + timeout). Cada um demonstra o formato e o nível de detalhe esperados. |
| **Role Prompting** | Dar uma persona especialista calibra tom, vocabulário e profundidade — melhora **Clarity** e **Helpfulness**. | Persona definida na 1ª linha: *"Você é um Product Manager sênior e Analista de Negócios especialista em metodologias ágeis…"*. |
| **Chain of Thought (CoT)** | Bugs complexos exigem raciocínio (quem é o usuário? qual o valor? quais edge cases?). Mas CoT **visível** polui a resposta e derruba **Precision/Clarity** (penalizam verbosidade e divagação). | Apliquei **CoT silencioso**: instruo o modelo a pensar passo a passo (persona → ação → benefício → complexidade → critérios) **internamente** e a responder **apenas** a User Story final, sem expor o raciocínio. |
| **Skeleton of Thought (SoT)** | A saída precisa de estrutura previsível e testável para maximizar Format/Completeness. | Defini "esqueletos" de saída que **escalam com a complexidade**: bugs simples/médios usam `Como um… / Critérios de Aceitação (Gherkin)`; bugs complexos usam seções `=== USER STORY PRINCIPAL / CRITÉRIOS DE ACEITAÇÃO / CRITÉRIOS TÉCNICOS / CONTEXTO DO BUG / TASKS TÉCNICAS ===`. |

**Outros cuidados de engenharia aplicados ao prompt:**

- **System vs User Prompt:** todas as regras, persona, formato e exemplos ficam no **system prompt**; o **user prompt** contém apenas o relato (`{bug_report}`) — separação limpa de responsabilidades.
- **Regras explícitas de comportamento:** template de User Story obrigatório, Critérios de Aceitação em **Gherkin** (Dado/Quando/Então/E), preservação de detalhes técnicos e **proibição de alucinação**.
- **Tratamento de edge cases:** relato vago, relato vazio/sem sentido (resposta de recusa controlada), múltiplos problemas (vira COMPLEXO) e bug sem usuário final óbvio (persona técnica).

## B) Resultados Finais

Avaliação executada com `python src/evaluate.py` (provider **OpenAI**: `gpt-4o-mini` para responder, `gpt-4o` como juiz), sobre o dataset de **15 bugs** (5 simples, 7 médios, 3 complexos).

- **Prompt público no Hub:** https://smith.langchain.com/hub/jonaslc/bug_to_user_story_v2
- **Projeto/Tracing no LangSmith:** `prompt-optimization-challenge-resolved`
- **Traces públicos (evidência de execução do prompt — 3 exemplos):**
  1. https://smith.langchain.com/public/1c14b9e4-3bfb-4322-a1ac-78a3d02db965/r
  2. https://smith.langchain.com/public/45a621d3-c0d3-43bb-ba8c-19243e5a68cc/r
  3. https://smith.langchain.com/public/d93535c8-b96f-4bf0-932f-c796cda9c085/r
- **Screenshots:** salve em `screenshots/` e referencie aqui (avaliação final no terminal + os traces acima).

**Tabela comparativa (v1 ruim → v2 otimizado):**

| Métrica | v1 (baixa qualidade)¹ | v2 (otimizado) | Meta |
|---|---|---|---|
| Helpfulness | ~0.45 | **0.93** ✓ | ≥ 0.80 |
| Correctness | ~0.52 | **0.90** ✓ | ≥ 0.80 |
| F1-Score | ~0.48 | **0.88** ✓ | ≥ 0.80 |
| Clarity | ~0.50 | **0.94** ✓ | ≥ 0.80 |
| Precision | ~0.46 | **0.92** ✓ | ≥ 0.80 |
| **Média Geral** | ~0.48 | **0.9132** | ≥ 0.80 |
| **Status** | ❌ REPROVADO | ✅ **APROVADO** | Todas ≥ 0.80 |

¹ Baseline do prompt original (`leonanluppi/bug_to_user_story_v1`): instruções vagas, sem persona, sem exemplos e com `{bug_report}` duplicado no system/user. Valores ilustrativos do enunciado.

### Iterações até a aprovação

| Iteração | Mudança principal | F1 | Média | Status |
|---|---|---|---|---|
| 1 | v2 inicial (Role + Few-shot + CoT silencioso + SoT) | 0.76 | — | ❌ só F1 < 0.80 |
| 2 | Bugs **médios** deixaram de usar o formato de "complexo"; passei a **preservar dados concretos** (fórmulas, códigos HTTP, severidade, OWASP, log de auditoria) e adicionei exemplos few-shot de bug médio (cálculo e segurança) | 0.82 | 0.8468 | ✅ APROVADO (folga pequena) |
| 3 | **Ampliei a cobertura do Few-shot** para os 5 níveis de bug simples e mais casos médios (performance, estoque com critérios de prevenção), reforçando o padrão de formato/escopo esperado | **0.88** | **0.9132** | ✅ APROVADO (folga confortável) |

> A saída completa da avaliação final está versionada em [`screenshots/evaluation_output.txt`](screenshots/evaluation_output.txt).

## C) Como Executar

### Pré-requisitos
- **Python 3.9+** (testado com 3.13)
- Conta no **LangSmith** (API key) e chave da **OpenAI**
- Seu **username** do LangSmith Hub

### 1. Ambiente e dependências
```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Credenciais
Copie `.env.example` para `.env` e preencha (este projeto já vem com `.env` configurado para **OpenAI** — basta colar suas chaves):
```bash
cp .env.example .env
# edite .env e preencha:
#   LANGSMITH_API_KEY, USERNAME_LANGSMITH_HUB, OPENAI_API_KEY
# provider já configurado: LLM_PROVIDER=openai / LLM_MODEL=gpt-4o-mini / EVAL_MODEL=gpt-4o
```

### 3. Pipeline do desafio
```bash
# (a) Pull do prompt ruim (v1) do LangSmith Hub
python src/pull_prompts.py

# (b) [já feito] Prompt otimizado em prompts/bug_to_user_story_v2.yml

# (c) Push do prompt v2 (PÚBLICO) para o seu Hub
python src/push_prompts.py

# (d) Avaliação automática (cria dataset + roda as 5 métricas)
python src/evaluate.py
```

### 4. Testes de validação do prompt
```bash
pytest tests/test_prompts.py -v
```

### Estrutura do que foi implementado
- `prompts/bug_to_user_story_v2.yml` — prompt otimizado (Role + Few-shot + CoT + SoT)
- `src/pull_prompts.py` — pull do Hub e serialização em YAML
- `src/push_prompts.py` — validação, build do `ChatPromptTemplate` e push **público**
- `tests/test_prompts.py` — 7 testes (os 6 exigidos + validação de estrutura)
