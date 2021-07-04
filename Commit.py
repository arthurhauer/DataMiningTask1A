from datetime import datetime
from typing import List


class Commit:
    dia_semana: str
    usuario: str
    projeto: str
    tamanho_descricao: int
    # descricao: str
    bug: bool
    merge: bool

    # def _is_empty(self, row: List[str], index: int):
    #     row[index *]

    def __init__(self, row: List[str], index: int, data: datetime):
        self._get_data(data)
        self._get_usuario(row, index)
        self._get_projeto(row, index)
        self._process_descricao(row, index)

    def _get_data(self, data: datetime):
        self.dia_semana = data.strftime('%A')

    def _get_usuario(self, row: List[str], index: int):
        usuario_column_base_index = 1
        self.usuario = \
            row[usuario_column_base_index].replace('https://gitlab.cits.br/', '').replace('mailto:', '').split('@', 1)[
                0]

    def _get_projeto(self, row: List[str], index: int):
        projeto_column_base_index = 3
        projeto = row[projeto_column_base_index].split('/-/', 1)[0].split('/')
        self.projeto = projeto[len(projeto) - 1]

    def _process_descricao(self, row: List[str], index: int):
        bug_keywords = ['fix', 'fixes', 'correção', 'correções', 'correction', 'corrections', 'bug', 'bugs', 'ajuste',
                        'ajustes']
        merge_keywords = ['merge']
        message_column_base_index = 2
        descricao_column_base_index = 4
        descricao = row[descricao_column_base_index].lower()
        message = row[message_column_base_index].lower()
        self.bug = any(key in message for key in bug_keywords)
        self.merge = any(key in message for key in merge_keywords)
        self.tamanho_descricao = 0 if self.merge else len(descricao)

    @staticmethod
    def get_csv_headers() -> List[str]:
        return ['Usuario', 'Projeto', 'Bug', 'Merge', 'DiaDaSemana', 'TamanhoDescricao']

    def to_csv(self) -> List[str]:
        return [str(self.usuario), str(self.projeto), str(self.bug), str(self.merge), str(self.dia_semana),
                str(self.tamanho_descricao)]
