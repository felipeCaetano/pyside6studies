import re

# +++++++ SEÇÕES POR SUBESTAÇÃO +++++++
SECOES_POR_SE = {
    "CONFIGURAÇÃO DA SE": "configuracao_se",
    "CONFIGURAÇÃO SERVIÇOS AUXILIARES": "configuracao_servicos",
    "CONFIGURAÇÃO COMUNICAÇÃO": "configuracao_comunicacao",
    "ATENÇÃO": "atencao",
    "NÃO CONFORMIDADES TÉRMICAS": "nao_conformidades_termicas",
    "NÃO CONFORMIDADES TÉRMICAS COM NOVO VCO": "nao_conformidades_termicas",
    "OBSERVAÇÕES": "observacoes",
    "INTERVENÇÕES": "intervencoes",
    "EM ANDAMENTO": "intervencoes_em_andamento",
    "SUSPENSA(s)/VENCIDA(s)": "intervencoes_suspensa",
    "ENTREGUE(s)": "intervencoes_entregue",
    "DEVOLVIDA(s)": "intervencoes_devolvida",
    "NM EMITIDAS": "nm_emitidas",
    "OCORRÊNCIAS": "ocorrencias",
}

ORDEMSECOES = [
    "configuracao_se", "configuracao_servicos", "configuracao_comunicacao",
    "atencao", "nao_conformidades_termicas", "observacoes",
    "intervencoes_em_andamento", "intervencoes_suspensa",
    "intervencoes_entregue", "intervencoes_devolvida", "nm_emitidas",
    "ocorrencias"
]

# ============== SEÇÕES GLOBAIS ===================

SECOES_GLOBAIS = {
    "OUTRAS AÇÕES OPERACIONAIS": "outras_acoes_operacionais",
    "OUTRAS INFORMAÇÕES": "outras_informacoes"
}

ORDEMSECOES_GLOBAIS = ["outras_acoes_operacionais", "outras_informacoes"]

# ===================== MAPEAMENTOS ============================================

SECAO_MAP = {
    **SECOES_POR_SE,
    **SECOES_GLOBAIS
}

SECAOMAPREVERSO = {"configuracao_se": "CONFIGURAÇÃO DA SE",
                   "configuracao_servicos": "CONFIGURAÇÃO SERVIÇOS AUXILIARES",
                   "configuracao_comunicacao": "CONFIGURAÇÃO COMUNICAÇÃO",
                   "atencao": "ATENÇÃO",
                   "nao_conformidades_termicas": "NÃO CONFORMIDADES TÉRMICAS",
                   "observacoes": "OBSERVAÇÕES",
                   "intervencoes_em_andamento": "EM ANDAMENTO",
                   "intervencoes_suspensa": "SUSPENSA(s)/VENCIDA(s)",
                   "intervencoes_entregue": "ENTREGUE(s)",
                   "intervencoes_devolvida": "DEVOLVIDA(s)",
                   "nm_emitidas": "NM EMITIDAS", "ocorrencias": "OCORRÊNCIAS",
                   "outras_acoes_operacionais": "OUTRAS AÇÕES OPERACIONAIS",
                   "outras_informacoes": "OUTRAS INFORMAÇÕES", }

# ============================= REGEX ==========================================

SE_REGEX = re.compile(r"^SE-(\w+):")

SECAO_REGEX = re.compile(
    r"^(CONFIGURAÇÃO DA SE|CONFIGURAÇÃO SERVIÇOS AUXILIARES"
    r"|CONFIGURAÇÃO COMUNICAÇÃO|ATENÇÃO|NÃO CONFORMIDADES"
    r" TÉRMICAS COM NOVO VCO|NÃO CONFORMIDADES TÉRMICAS|OBSERVAÇÕES"
    r"|INTERVENÇÕES|EM ANDAMENTO|SUSPENSA\(s\)/VENCIDA\(s\)"
    r"|ENTREGUE\(s\)|DEVOLVIDA\(s\)|NM EMITIDAS|OCORRÊNCIAS"
    r"|OUTRAS AÇÕES OPERACIONAIS|OUTRAS INFORMAÇÕES):")
