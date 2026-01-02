import json
import logging
from pathlib import Path

from .constants import (NOVA_SE, SECAOMAPREVERSO, ORDEMSECOES, SE_REGEX,
                       SECAO_REGEX, SECAO_MAP)


logger = logging.getLogger(__name__)


def nova_se():
    return {
        "configuracao_se": [],
        "configuracao_servicos": [],
        "configuracao_comunicacao": [],
        "atencao": [],
        "nao_conformidades_termicas": [],
        "observacoes": [],
        "intervencoes_em_andamento": [],
        "intervencoes_suspensa": [],
        "intervencoes_entregue": [],
        "intervencoes_devolvida": [],
        "nm_emitidas": [],
        "ocorrencias": [],
        "outras_acoes_operacionais": [],
        "outras_informacoes": []
    }


class PassagemTurnoParser:
    """
    Camada de dominio responsável por ler, interpretar, montar e persistir
    arquivos de passagem de turno em formatos texto e JSON.

    Centraliza regras de parsing, serialização e reconstrução do conteúdo.
    """

    @staticmethod
    def _ler_linhas(txt_file):
        """
        Lê um arquivo de texto e retorna suas linhas como uma lista de strings.
        Remove quebras de linha e espaços à direita de cada linha.
        Args:
            txt_file (str | Path): Caminho do arquivo de texto.

        Returns:
            list[str] | None: Lista de linhas do arquivo ou None em caso de erro
            (arquivo inexistente, erro de encoding ou falha de leitura).
        """

        try:
            caminho_txt = Path(txt_file)
            if not caminho_txt.exists():
                logger.error(f"Arquivo não encontrado: {txt_file}")
                return None

            linhas = caminho_txt.read_text(encoding="utf-8").splitlines()
            linhas = [l.rstrip() for l in linhas]
            return linhas

        except UnicodeDecodeError:
            logger.error(f"Erro de encoding ao ler {txt_file}")
            return None
        except Exception as e:
            logger.error(f"Erro ao ler arquivo {txt_file}: {e}")
            return None

    @staticmethod
    def _processar_linha(linha: str, dados: dict, estado: dict, se_regex,
                          secao_regex, secao_map):

        """
        Processa uma única linha do arquivo de passagem de turno, atualizando
        incrementalmente o estado do parser e o dicionário final de dados.

        A função identifica:
           - separadores visuais
           - início de uma nova subestação (SE)
           - início de uma nova seção
           - conteúdo textual pertencente à seção atual

       Args:
           linha (str): Linha atual do arquivo.
           dados (dict): Estrutura principal onde os dados parseados são acumulados.
           estado (dict): Estado mutável do parser contendo:
               - se_atual: subestação corrente
               - secao_atual: seção corrente
               - buffer: linhas acumuladas da seção
           se_regex (Pattern): Regex para identificar cabeçalhos de SE.
           secao_regex (Pattern): Regex para identificar cabeçalhos de seção.
           secao_map (dict): Mapeamento entre nomes de seções no texto e chaves JSON.

       Returns:
           None
       """

        if linha.startswith("----"):
            return

        se_match = se_regex.match(linha)
        if se_match:
            estado['se_atual'] = se_match.group(1)
            dados[estado['se_atual']] = nova_se()
            estado['secao_atual'] = None
            estado['buffer'] = []
            return

        secao_match = secao_regex.match(linha)
        if secao_match:
            if estado['secao_atual'] and estado['buffer']:
                # Adiciona buffer à seção anterior
                chave_json = secao_map[estado['secao_atual']]
                dados[estado['se_atual']][chave_json].extend(estado['buffer'])
            estado['secao_atual'] = secao_match.group(1)
            estado['buffer'] = []
            return

        if linha.strip():
            estado['buffer'].append(linha.strip())

    @staticmethod
    def load_text(configuracao: list[str] | None, default: str = "") -> str:
        """
        Converte uma lista de strings em um único texto com quebras de linha.

        Útil para transformar listas armazenadas no JSON em blocos de texto
        exibíveis ou exportáveis.

        Args:
            configuracao (list[str] | None): Lista de linhas.
            default (str): Valor padrão retornado caso a entrada seja inválida.

        Returns:
            str: Texto unificado ou valor padrão.
        """
        if not configuracao:
            return default
        try:
            return "\n".join(configuracao)
        except TypeError as e:
            logger.error(f"Erro ao converter configuração em texto: {e}")
            return default

    @staticmethod
    def montar_texto(conteudo: dict[str, dict]) -> str:
        """
        Reconstrói o texto completo da passagem de turno no formato original,
        a partir da estrutura de dados em dicionário.

        Percorre subestações e seções respeitando a ordem definida em constantes,
        aplicando títulos e separadores visuais.

        Args:
            conteudo (dict[str, dict]): Estrutura completa das subestações e seções.

        Returns:
            str: Texto final formatado da passagem de turno.
        """
        secao_map_reverso = SECAOMAPREVERSO
        ordem_secoes = ORDEMSECOES
        texto_total = []

        for nome_se, estado in conteudo.items():
            texto_total.append(f"SE-{nome_se}:")
            texto_total.append("-" * 80)

            for secao_chave in ordem_secoes:
                titulo = secao_map_reverso.get(secao_chave, secao_chave.upper())
                conteudo_secao = estado.get(secao_chave, [])

                texto_total.append(f"{titulo}:")
                if isinstance(conteudo_secao, list):
                    texto_total.extend(
                        conteudo_secao if conteudo_secao else [""])
                elif isinstance(conteudo_secao, str):
                    texto_total.append(conteudo_secao)
                else:
                    texto_total.append("")
                texto_total.append("-" * 80)

            texto_total.append("")  # quebra entre SEs

        return "\n".join(texto_total).strip()

    @staticmethod
    def salvar_texto(nome_arquivo: str, conteudo: str) -> bool:
        """
        Salva um conteúdo textual em um arquivo.

        Args:
            nome_arquivo (str): Caminho do arquivo de saída.
            conteudo (str): Texto a ser salvo.

        Returns:
            bool: True se o arquivo foi salvo com sucesso, False caso contrário.
        """
        try:
            Path(nome_arquivo).write_text(conteudo, encoding="utf-8")
            return True
        except Exception as e:
            logger.error(f"[ERRO] Falha ao salvar {nome_arquivo}")
            return False

    @staticmethod
    def get_passagem_turno(json_file):
        """
        Carrega e desserializa um arquivo JSON de passagem de turno.

        Args:
            json_file (str | Path): Caminho do arquivo JSON.

        Returns:
            dict | None: Dados carregados do JSON ou None em caso de erro
            (arquivo inexistente, JSON inválido ou falha de leitura).
        """
        try:
            file_path = Path(json_file)
            if not file_path.exists():
                logger.warning(f"Arquivo não encontrado: {json_file}")
                return None
            with open(json_file, 'r', encoding="utf-8") as arquivo_json:
                dados = json.load(arquivo_json)
            return dados
        except json.JSONDecodeError as e:
            logger.error(f"JSON inválido em {json_file}: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro ao carregar {json_file}: {e}")
            return None

    @staticmethod
    def parse_passagem_turno(txt_file, json_file='passagem_turno.json'):
        """
        Processa um arquivo de passagem de turno em formato texto e gera
        sua representação estruturada em JSON.

        O método:
        - lê o arquivo texto
        - executa o parsing linha a linha
        - organiza os dados por subestação e seção
        - persiste o resultado em um arquivo JSON

        Args:
            txt_file (str | Path): Caminho do arquivo .txt de entrada.
            json_file (str | Path): Caminho do arquivo .json de saída.

        Returns:
            bool: True se o processamento e salvamento ocorreram com sucesso,
            False em caso de falha.
        """
        linhas = PassagemTurnoParser._ler_linhas(txt_file)

        dados = {}
        estado = {
            'se_atual': None,
            'secao_atual': None,
            'buffer': [],
        }

        se_regex = SE_REGEX
        secao_regex = SECAO_REGEX
        secao_map = SECAO_MAP

        if not linhas:
            return False

        for linha in linhas:
            PassagemTurnoParser._processar_linha(
                linha, dados, estado, se_regex, secao_regex, secao_map)

        # Salva último buffer
        if estado['se_atual'] and estado['secao_atual'] and estado['buffer']:
            chave = secao_map[estado['secao_atual']]
            dados[estado['se_atual']][chave].extend(estado['buffer'])

        # Salva JSON
        if PassagemTurnoParser.salvar_json(dados, json_file):
            logger.info(f"Parse concluído: {len(dados)} subestações encontradas")
            return True
        return False

    @staticmethod
    def salvar_json(estado: dict, arquivo="passagemturno.json") -> bool:
        try:
            caminho = Path(arquivo)
            with caminho.open("w", encoding="utf-8") as outfile:
                json.dump(estado, outfile, ensure_ascii=False, indent=4)  # NOQA

            return True
        except Exception as e:
            logger.error(f"[Erro] ao salvar JSON: {e}")
            return False
