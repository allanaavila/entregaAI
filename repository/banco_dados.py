import sqlite3
from entity.centro_distribuicao import CentroDistribuicao
from entity.caminhao import Caminhao  # Supondo que a classe Caminhao seja do módulo entity

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
            centro.id = cursor.lastrowid
            self.conn.commit()

    def buscar_centro(self, nome):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM centro_distribuicao WHERE nome = ?", (nome,))
        row = cursor.fetchone()
        if row:
            return CentroDistribuicao(id=row[0], nome=row[1])
        return None

    def salvar_caminhao(self, caminhao, centro_nome):
        centro = self.buscar_centro(centro_nome)
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
        cursor.execute("SELECT id, capacidade_maxima, horas_operacao, carga_atual, centro_id FROM caminhao")
        caminhoes = cursor.fetchall()
        caminhoneiros = []
        for caminhao in caminhoes:
            centro = self.buscar_centro_por_id(caminhao[4])
            caminhoneiros.append(Caminhao(
                id=caminhao[0],
                capacidade_maxima=caminhao[1],
                horas_operacao=caminhao[2],
                carga_atual=caminhao[3],
                centro=centro
            ))
        return caminhoneiros

    def buscar_caminhao_disponivel(self, capacidade_necessaria):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM caminhao WHERE capacidade_maxima >= ?
        """, (capacidade_necessaria,))
        caminhoes_disponiveis = cursor.fetchall()
        caminhoneiros = []
        if caminhoes_disponiveis:
            for caminhao in caminhoes_disponiveis:
                centro = self.buscar_centro_por_id(caminhao[4])
                caminhoneiros.append(Caminhao(
                    id=caminhao[0],
                    capacidade_maxima=caminhao[1],
                    horas_operacao=caminhao[2],
                    carga_atual=caminhao[3],
                    centro=centro
                ))
            return caminhoneiros
        else:
            print("Nenhum caminhão disponível com capacidade para a entrega.")
            return []

    def buscar_centro_por_id(self, centro_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM centro_distribuicao WHERE id = ?", (centro_id,))
        row = cursor.fetchone()
        if row:
            return CentroDistribuicao(id=row[0], nome=row[1])
        return None

    def fechar_conexao(self):
        self.conn.close()
