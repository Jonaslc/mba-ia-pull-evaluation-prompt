"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()

# Mapeia: arquivo YAML local -> (chave dentro do YAML, nome do prompt no Hub)
PROMPTS_TO_PUSH = [
    {
        "file": "prompts/bug_to_user_story_v2.yml",
        "key": "bug_to_user_story_v2",
        "hub_name": "bug_to_user_story_v2",
    },
]


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Reaproveita validate_prompt_structure (utils) que checa: campos obrigatórios,
    system_prompt não vazio, ausência de TODOs e mínimo de 2 técnicas.

    Args:
        prompt_data: Dados do prompt (bloco interno do YAML)

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    return validate_prompt_structure(prompt_data)


def build_chat_prompt(prompt_data: dict) -> ChatPromptTemplate:
    """
    Constrói um ChatPromptTemplate a partir do bloco do YAML.

    O system_prompt não deve conter variáveis de template; a única variável
    ({bug_report}) fica no user_prompt — compatível com o dataset de avaliação.
    """
    system_prompt = prompt_data.get("system_prompt", "").strip()
    user_prompt = prompt_data.get("user_prompt", "{bug_report}").strip()

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("user", user_prompt),
        ]
    )


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt no Hub (sem o username; o LangSmith prefixa)
        prompt_data: Dados do prompt (bloco interno do YAML)

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        chat_prompt = build_chat_prompt(prompt_data)

        # Tags incluindo as técnicas aplicadas, para rastreabilidade no Hub
        tags = list(prompt_data.get("tags", []))
        for technique in prompt_data.get("techniques_applied", []):
            slug = "tecnica:" + technique.lower().replace(" ", "-")
            if slug not in tags:
                tags.append(slug)

        description = prompt_data.get("description", "").strip() or (
            "Prompt otimizado de Bug to User Story"
        )

        client = Client()
        url = client.push_prompt(
            prompt_name,
            object=chat_prompt,
            is_public=True,
            tags=tags,
            description=description,
        )

        print(f"  ✓ Push concluído (PÚBLICO): {prompt_name}")
        print(f"    URL: {url}")
        return True

    except Exception as e:
        print(f"  ❌ Erro ao fazer push de '{prompt_name}': {e}")
        return False


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS OTIMIZADOS AO LANGSMITH HUB")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1

    all_ok = True

    for item in PROMPTS_TO_PUSH:
        print(f"\n→ Processando: {item['file']}")

        data = load_yaml(item["file"])
        if data is None:
            print(f"  ❌ Não foi possível carregar {item['file']}")
            all_ok = False
            continue

        # Extrai o bloco interno (ex.: data['bug_to_user_story_v2'])
        prompt_data = data.get(item["key"], data)

        is_valid, errors = validate_prompt(prompt_data)
        if not is_valid:
            print("  ❌ Prompt inválido:")
            for err in errors:
                print(f"     - {err}")
            all_ok = False
            continue

        print("  ✓ Validação OK")

        if not push_prompt_to_langsmith(item["hub_name"], prompt_data):
            all_ok = False

    print()
    if all_ok:
        print("✅ Push concluído com sucesso!")
        print("   Verifique em: https://smith.langchain.com/prompts")
        print("   Próximo passo: python src/evaluate.py")
        return 0
    else:
        print("⚠️  Push concluído com erros. Revise as mensagens acima.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
