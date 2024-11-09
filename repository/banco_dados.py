import sqlite3
from entity.centro_distribuicao import CentroDistribuicao


class BancoDados:
    def __init__(self, nome_bd="entregaAI.db"):
        self.conn = sqlite3.connect(nome_bd)
        self.criar_tabelas()

    def criar_tabelas(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS centro_distribuicao (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT UNIQUE NOT NULL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS caminhao (
                    id TEXT PRIMARY KEY,
                    capacidade_maxima INTEGER,
                    horas_operacao INTEGER,
                    carga_atual INTEGER,
                    centro_id INTEGER,
                    FOREIGN KEY(centro_id) REFERENCES centro_distribuicao(id)
                )
            """)

    def salvar_centro(self, centro):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO centro_distribuicao (nome) VALUES (?)", (centro.nome,))
            centro.id = cursor.lastrowid  # Recupera o ID gerado automaticamente
            self.conn.commit()

    def buscar_centro(self, nome):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM centro_distribuicao WHERE nome = ?", (nome,))
        row = cursor.fetchone()
        if row:
            return CentroDistribuicao(id=row[0], nome=row[1])  # Cria o objeto CentroDistribuicao com os dados do banco
        return None

    def salvar_caminhao(self, caminhao, centro_nome):
        centro = self.buscar_centro(centro_nome)  # Corrigido para usar self.buscar_centro
        if centro:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO caminhao (id, capacidade_maxima, horas_operacao, carga_atual, centro_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                caminhao.id, caminhao.capacidade_maxima, caminhao.horas_operacao, caminhao.carga_atual, centro.id))
                self.conn.commit()
                print(f"Caminhão {caminhao.id} salvo no centro {centro_nome}.")
        else:
            print(f"Centro {centro_nome} não encontrado.")

    def listar_caminhoes(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, capacidade_maxima FROM caminhao")
        caminhoes = cursor.fetchall()
        print("Caminhões disponíveis:")
        for caminhao in caminhoes:
            print(f"ID: {caminhao[0]}, Capacidade Máxima: {caminhao[1]}")
        return caminhoes

    def buscar_caminhao_disponivel(self, capacidade_necessaria):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM caminhao WHERE capacidade_maxima >= ?
        """, (capacidade_necessaria,))
        caminhoes_disponiveis = cursor.fetchall()

        if caminhoes_disponiveis:
            print(f"{len(caminhoes_disponiveis)} caminhões encontrados com capacidade suficiente.")
            for caminhao in caminhoes_disponiveis:
                print(f"ID: {caminhao[0]}, Capacidade Máxima: {caminhao[2]}")
        else:
            print("Nenhum caminhão disponível com capacidade para a entrega.")

    def fechar_conexao(self):
        self.conn.close()
