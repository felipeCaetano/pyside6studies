import json
import logging
from pathlib import Path

from .constants import (SECAOMAPREVERSO, ORDEMSECOES, SE_REGEX,
                        SECAO_REGEX, SECAO_MAP, SECOES_GLOBAIS, SECOES_POR_SE)

logger = logging.getLogger(__name__)

def _flush_buffer(dados, estado):
    """
    Descarrega o conteúdo acumulado no buffer da seção atual para a
    estrutura final de dados.

    O destino do buffer depende do tipo da seção:
    - Seções globais são armazenadas em dados["_global"]
    - Seções vinculadas a uma subestação são armazenadas sob a SE atual

    Após a gravação, o buffer é limpo.

    Args:
        dados (dict): Estrutura principal onde os dados parseados são
        acumulados.
        estado (dict): Estado atual do parser, contendo seção, subestação
        e buffer.
    """
    if not estado["secao_atual"] or not estado['buffer']:
        return

    titulo = estado["secao_atual"]

    if titulo in SECOES_GLOBAIS:
        chave = SECOES_GLOBAIS[titulo]
        dados["_global"][chave].extend(estado['buffer'])
    elif titulo in SECOES_POR_SE:
        chave = SECOES_POR_SE[titulo]
        subestacao = estado['se_atual']

        if subestacao:
            dados[subestacao][chave].extend(estado['buffer'])

    estado['buffer'] = []

def nova_se():
     """
    Cria e retorna a estrutura base de dados para uma nova subestação (SE).

    Cada chave representa uma seção possível da passagem de turno,
    inicializada com listas vazias para armazenamento do conteúdo textual.

    Returns:
        dict: Estrutura padrão de uma subestação.
    """
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
    }


class PassagemTurnoParser:
    """
    Responsável por interpretar, estruturar, serializar e reconstruir
    passagens de turno em formato texto e JSON.

    Esta classe centraliza as regras de parsing e garante que o conteúdo
    seja organizado por subestação e por seção, mantendo consistência
    entre leitura, persistência e reconstrução do texto original.
    """

    @staticmethod
    def _ler_linhas(txt_file):
        """
        Lê um arquivo de texto e retorna seu conteúdo como uma lista de
        linhas.

        Remove quebras de linha e espaços à direita de cada linha.
        Em caso de erro (arquivo inexistente, encoding inválido ou falha de
        IO),
        retorna None e registra o erro em log.

        Args:
            txt_file (str | Path): Caminho do arquivo de texto.

        Returns:
            list[str] | None: Lista de linhas ou None em caso de erro.
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
    def _processar_linha(linha: str, dados: dict, estado: dict):
        """
        Processa uma única linha da passagem de turno e atualiza o estado
        interno do parser e a estrutura final de dados.

        A linha pode representar:
        - Um cabeçalho de subestação (SE)
        - Um cabeçalho de seção
        - Conteúdo pertencente à seção atual
        - Separadores visuais ou linhas vazias (ignorados)

        O método utiliza expressões regulares definidas em constantes
        para identificar SEs e seções.

        Args:
            linha (str): Linha atual do arquivo.
            dados (dict): Estrutura principal onde os dados são acumulados.
            estado (dict): Estado mutável do parser contendo:
                - se_atual: subestação corrente
                - secao_atual: seção corrente
                - buffer: linhas acumuladas da seção atual
        """

        linha = linha.strip()
        if not linha or linha.startswith("----"):
            return

        se_match = SE_REGEX.match(linha)
        if se_match:
            _flush_buffer(dados, estado)

            codigo_se = f'SE-{se_match.group(1)}'
            estado['se_atual'] = codigo_se
            estado['secao_atual'] = None
            estado['buffer'] = []
            if codigo_se not in dados:
                dados[codigo_se] = nova_se()
            return

        secao_match = SECAO_REGEX.match(linha)
        if secao_match:
            _flush_buffer(dados, estado)

            titulo_secao = secao_match.group(1)
            estado['secao_atual'] = titulo_secao
            estado['buffer'] = []
            return

        if estado['secao_atual']:
            estado['buffer'].append(linha.strip())

    @staticmethod
    def load_text(configuracao: list[str] | None, default: str = "") -> str:
       """
        Converte uma lista de strings em um único texto com quebras de linha.

        Utilizado principalmente para transformar dados armazenados no JSON
        em blocos de texto exibíveis em interface gráfica ou exportação.

        Args:
            configuracao (list[str] | None): Lista de linhas de texto.
            default (str): Valor retornado caso a entrada seja inválida ou vazia.

        Returns:
            str: Texto concatenado ou valor padrão.
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
    def parse_from_text(texto):
        if not texto or not texto.strip():
            logging.warning("O texto não pode estar vazio!")
            return None
        
        linhas = [l.rstrip() for l in texto.splitlines()]
        dados = {
            '_global': {
                "outras_acoes_operacionais": [],
                "outras_informacoes": []
            }
        }
        estado = {
            'se_atual': None,
            'secao_atual': None,
            'buffer': [],
        }

        for linha in linhas:
            PassagemTurnoParser._processar_linha(linha, dados, estado)
        _flush_buffer(dados, estado)

        return dados


    @staticmethod
    def parse_passagem_turno(txt_file, json_file='passagem_turno.json'):
        """
        Processa um arquivo de passagem de turno em formato texto e gera
        sua representação estruturada em JSON.

        O método:
        - lê o arquivo texto
        - executa o parsing linha a linha
        - persiste o resultado em um arquivo JSON

        Args:
            txt_file (str | Path): Caminho do arquivo .txt de entrada.
            json_file (str | Path): Caminho do arquivo .json de saída.

        Returns:
            bool: True se o processamento e salvamento ocorreram com sucesso,
            False em caso de falha.
        """
        linhas = PassagemTurnoParser._ler_linhas(txt_file)
        if not linhas:
            return False

        texto = "\n".join(linhas)
        dados = PassagemTurnoParser.parse_from_text(texto)
        if not dados:
            return False

        # Salva JSON
        if PassagemTurnoParser.salvar_json(dados, json_file):
            logger.info(
                f"Parse concluído: {len(dados) - 1} subestações encontradas")
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

    @staticmethod
    def get_sessao_map(filter):
        if filter == 'CONFIGURAÇÃO ATENÇÃO':
            filter = 'ATENÇÃO'
            return SECAO_MAP.get(filter, 'configuracao_se')
        return SECAO_MAP.get(filter, 'configuracao_se')
