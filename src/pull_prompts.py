"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

# Prompt(s) de baixa qualidade publicados no Hub que devem ser baixados.
# Mapeia: identificador no Hub -> arquivo local de destino.
PROMPTS_TO_PULL = {
    "leonanluppi/bug_to_user_story_v1": "prompts/bug_to_user_story_v1.yml",
}


def _extract_messages(prompt_template) -> dict:
    """
    Extrai system_prompt e user_prompt de um ChatPromptTemplate retornado pelo Hub.

    Faz o melhor esforço para lidar com diferentes formatos de mensagem do LangChain
    (SystemMessagePromptTemplate, HumanMessagePromptTemplate, etc.).
    """
    system_parts = []
    user_parts = []

    messages = getattr(prompt_template, "messages", None) or []

    for message in messages:
        # Cada item normalmente é um *MessagePromptTemplate com .prompt.template
        template_text = ""
        prompt_attr = getattr(message, "prompt", None)
        if prompt_attr is not None and hasattr(prompt_attr, "template"):
            template_text = prompt_attr.template
        elif hasattr(message, "content"):
            template_text = message.content
        elif hasattr(message, "template"):
            template_text = message.template

        # Descobrir o "papel" da mensagem
        role = ""
        if hasattr(message, "role"):
            role = str(message.role).lower()
        else:
            role = type(message).__name__.lower()

        if "system" in role:
            system_parts.append(template_text)
        elif "human" in role or "user" in role:
            user_parts.append(template_text)
        else:
            # Fallback: trata como user
            user_parts.append(template_text)

    return {
        "system_prompt": "\n".join(p for p in system_parts if p).strip(),
        "user_prompt": "\n".join(p for p in user_parts if p).strip(),
    }


def pull_prompts_from_langsmith() -> bool:
    """
    Faz pull de todos os prompts configurados em PROMPTS_TO_PULL e os salva
    localmente em formato YAML.

    Returns:
        True se todos os prompts foram baixados com sucesso, False caso contrário.
    """
    all_ok = True

    for hub_name, local_path in PROMPTS_TO_PULL.items():
        print(f"\n→ Fazendo pull de '{hub_name}'...")

        try:
            prompt_template = hub.pull(hub_name)
            print("  ✓ Prompt carregado do Hub")
        except Exception as e:
            print(f"  ❌ Erro ao fazer pull de '{hub_name}': {e}")
            print("     Verifique LANGSMITH_API_KEY no .env e o nome do prompt.")
            all_ok = False
            continue

        extracted = _extract_messages(prompt_template)

        # Nome lógico do prompt = parte após a "/" (sem o owner)
        logical_name = hub_name.split("/")[-1]

        prompt_data = {
            logical_name: {
                "description": "Prompt inicial (baixa qualidade) baixado do LangSmith Hub",
                "system_prompt": extracted["system_prompt"],
                "user_prompt": extracted["user_prompt"],
                "version": "v1",
                "source": hub_name,
                "tags": ["bug-analysis", "user-story", "product-management"],
            }
        }

        if save_yaml(prompt_data, local_path):
            print(f"  ✓ Salvo em: {local_path}")
        else:
            print(f"  ❌ Falha ao salvar em: {local_path}")
            all_ok = False

    return all_ok


def main():
    """Função principal"""
    print_section_header("PULL DE PROMPTS DO LANGSMITH HUB")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1

    success = pull_prompts_from_langsmith()

    print()
    if success:
        print("✅ Pull concluído com sucesso.")
        print("   Próximo passo: analise o prompt v1 e otimize em prompts/bug_to_user_story_v2.yml")
        return 0
    else:
        print("⚠️  Pull concluído com erros. Revise as mensagens acima.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
