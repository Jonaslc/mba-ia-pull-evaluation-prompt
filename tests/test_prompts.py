"""
Testes automatizados para validação do prompt otimizado (v2).

Executar com:
    pytest tests/test_prompts.py -v
"""
import re
import sys
import yaml
import pytest
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure  # noqa: E402

PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
PROMPT_KEY = "bug_to_user_story_v2"


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def prompt():
    """Retorna o bloco interno do prompt v2 (ex.: data['bug_to_user_story_v2'])."""
    data = load_prompts(PROMPT_FILE)
    assert data is not None, "Arquivo YAML do prompt v2 está vazio ou inválido"
    return data.get(PROMPT_KEY, data)


class TestPrompts:
    def test_prompt_has_system_prompt(self, prompt):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in prompt, "Campo 'system_prompt' ausente"
        assert prompt["system_prompt"].strip(), "'system_prompt' está vazio"

    def test_prompt_has_role_definition(self, prompt):
        """Verifica se o prompt define uma persona (ex.: 'Você é um Product Manager')."""
        system_prompt = prompt.get("system_prompt", "").lower()
        # Procura por marcadores de definição de persona/role
        role_markers = [
            "você é um",
            "você é uma",
            "voce e um",
            "product manager",
            "analista de negócios",
            "atue como",
            "como um product",
        ]
        assert any(marker in system_prompt for marker in role_markers), (
            "O prompt não define uma persona/role claramente "
            "(ex.: 'Você é um Product Manager sênior...')"
        )

    def test_prompt_mentions_format(self, prompt):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = prompt.get("system_prompt", "").lower()
        format_markers = [
            "markdown",
            "critérios de aceitação",
            "criterios de aceitacao",
            "como um",  # template de user story
            "para que",
            "dado que",  # gherkin
        ]
        assert any(marker in system_prompt for marker in format_markers), (
            "O prompt não especifica o formato esperado da resposta "
            "(User Story padrão / Critérios de Aceitação / Markdown)"
        )

    def test_prompt_has_few_shot_examples(self, prompt):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = prompt.get("system_prompt", "").lower()
        # Heurística: presença da palavra "exemplo" + pares relato->user story
        has_example_keyword = "exemplo" in system_prompt or "few-shot" in system_prompt
        # Pelo menos 2 blocos de exemplo (entrada/saída)
        relato_count = system_prompt.count("relato de bug")
        user_story_count = system_prompt.count("user story")
        assert has_example_keyword, "Não há marcação de 'Exemplo' no prompt (Few-shot)"
        assert relato_count >= 2 and user_story_count >= 2, (
            "O prompt deve conter ao menos 2 exemplos de entrada/saída (Few-shot)"
        )

    def test_prompt_no_todos(self, prompt):
        """Garante que você não esqueceu nenhum [TODO] no texto."""
        # Concatena todos os campos textuais relevantes (preserva o case original:
        # o placeholder é o token MAIÚSCULO 'TODO', não a palavra portuguesa 'todo/todos').
        blob = " ".join(
            str(prompt.get(field, ""))
            for field in ("description", "system_prompt", "user_prompt")
        )
        # Marca placeholders comuns deixados por engano
        leftover_markers = [r"\[TODO\]", r"\bTODO\b", r"\[PREENCHER\]", r"\bFIXME\b", r"XXX+"]
        for pattern in leftover_markers:
            assert not re.search(pattern, blob), (
                f"O prompt ainda contém placeholder não preenchido (padrão: {pattern})"
            )

    def test_minimum_techniques(self, prompt):
        """Verifica (via metadados do YAML) se pelo menos 2 técnicas foram listadas."""
        techniques = prompt.get("techniques_applied", [])
        assert isinstance(techniques, list), "'techniques_applied' deve ser uma lista"
        assert len(techniques) >= 2, (
            f"Mínimo de 2 técnicas requeridas; encontradas: {len(techniques)}"
        )

    def test_validate_prompt_structure_passes(self, prompt):
        """Teste extra: a validação completa de estrutura (utils) deve passar."""
        is_valid, errors = validate_prompt_structure(prompt)
        assert is_valid, f"Estrutura inválida: {errors}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
