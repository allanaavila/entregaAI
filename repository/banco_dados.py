import sqlite3
from typing import List, Optional
from contextlib import contextmanager
from models.centro_distribuicao import CentroDistribuicao
from models.caminhao import Caminhao


class ErroBancoDados(Exception):
    """Exceção personalizada para operações no banco de dados."""
    pass


class BancoDados:
    def __init__(self, nome_bd: str = "entregaAI.db"):
        """Inicializa a conexão com o banco de dados com melhor tratamento de erros."""
        try:
            self.conn = sqlite3.connect(nome_bd)
            self.cursor = self.conn.cursor()
            self.criar_tabelas()
        except sqlite3.Error as e:
            raise ErroBancoDados(f"Falha ao inicializar o banco de dados: {str(e)}")

    @contextmanager
    def transacao(self):
        """Gerenciador de contexto para lidar com transações no banco de dados."""
        try:
            yield self.cursor
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            raise ErroBancoDados(f"Falha na transação: {str(e)}")

    def criar_tabelas(self) -> None:
        """Cria as tabelas do banco de dados com um esquema melhorado."""
        try:
            with self.transacao() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS centro_distribuicao (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS caminhao (
                        id TEXT PRIMARY KEY,
                        capacidade_maxima INTEGER NOT NULL CHECK(capacidade_maxima > 0),
                        horas_operacao INTEGER NOT NULL CHECK(horas_operacao >= 0),
                        carga_atual INTEGER NOT NULL DEFAULT 0 CHECK(carga_atual >= 0),
                        centro_id INTEGER,
                        status TEXT CHECK(status IN ('disponivel', 'em_rota', 'manutencao')),
                        ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(centro_id) REFERENCES centro_distribuicao(id) ON DELETE SET NULL,
                        CHECK(carga_atual <= capacidade_maxima)
                    )
                """)
        except ErroBancoDados as e:
            raise ErroBancoDados(f"Falha ao criar tabelas: {str(e)}")

    def salvar_centro(self, centro: CentroDistribuicao) -> None:
        """Salvar ou atualizar o centro de distribuição com tratamento de erro."""
        try:
            with self.transacao() as cursor:
                cursor.execute(
                    "INSERT OR REPLACE INTO centro_distribuicao (nome) VALUES (?)",
                    (centro.nome,)
                )
                centro.id = cursor.lastrowid
        except ErroBancoDados as e:
            raise ErroBancoDados(f"Falha ao salvar centro de distribuição: {str(e)}")

    def buscar_centro(self, nome: str) -> Optional[CentroDistribuicao]:
        """Buscar centro de distribuição pelo nome."""
        try:
            self.cursor.execute(
                "SELECT id, nome FROM centro_distribuicao WHERE nome = ?",
                (nome,)
            )
            row = self.cursor.fetchone()
            return CentroDistribuicao(id=row[0], nome=row[1]) if row else None
        except sqlite3.Error as e:
            raise ErroBancoDados(f"Falha ao buscar centro de distribuição: {str(e)}")

    def listar_caminhoes(self) -> List[Caminhao]:
        """Listar todos os caminhões com informações de seu centro de distribuição."""
        try:
            self.cursor.execute("""
                SELECT 
                    c.id,
                    c.capacidade_maxima,
                    c.horas_operacao,
                    c.carga_atual,
                    c.status,
                    c.ultima_atualizacao,
                    cd.id as centro_id,
                    cd.nome as centro_nome
                FROM caminhao c
                LEFT JOIN centro_distribuicao cd ON c.centro_id = cd.id
                ORDER BY c.id
            """)

            rows = self.cursor.fetchall()
            return [
                Caminhao(
                    id=row[0],
                    capacidade_maxima=row[1],
                    horas_operacao=row[2],
                    carga_atual=row[3],
                    centro=CentroDistribuicao(id=row[6], nome=row[7]) if row[6] else None
                )
                for row in rows
            ] if rows else []

        except sqlite3.Error as e:
            raise ErroBancoDados(f"Falha ao listar caminhões: {str(e)}")

    def salvar_caminhao(self, caminhao: Caminhao, centro_nome: str) -> None:
        """Salvar ou atualizar caminhão com validação e tratamento de erro."""
        try:
            centro = self.buscar_centro(centro_nome)
            if not centro:
                raise ErroBancoDados(f"Centro de distribuição '{centro_nome}' não encontrado")

            with self.transacao() as cursor:
                cursor.execute("""
                    INSERT OR REPLACE INTO caminhao (
                        id, capacidade_maxima, horas_operacao, carga_atual, 
                        centro_id, status, ultima_atualizacao
                    ) VALUES (?, ?, ?, ?, ?, 'disponivel', CURRENT_TIMESTAMP)
                """, (
                    caminhao.id,
                    caminhao.capacidade_maxima,
                    caminhao.horas_operacao,
                    caminhao.carga_atual,
                    centro.id
                ))
        except ErroBancoDados as e:
            raise ErroBancoDados(f"Falha ao salvar caminhão: {str(e)}")

    def buscar_caminhao_disponivel(self, capacidade_necessaria: int) -> List[Caminhao]:
        """Buscar caminhões disponíveis com a capacidade necessária."""
        try:
            self.cursor.execute("""
                SELECT c.*, cd.nome as centro_nome 
                FROM caminhao c
                LEFT JOIN centro_distribuicao cd ON c.centro_id = cd.id
                WHERE c.capacidade_maxima >= ?
                AND c.status = 'disponivel'
                AND c.carga_atual + ? <= c.capacidade_maxima
                ORDER BY c.capacidade_maxima ASC
            """, (capacidade_necessaria, capacidade_necessaria))

            rows = self.cursor.fetchall()
            return [
                Caminhao(
                    id=row[0],
                    capacidade_maxima=row[1],
                    horas_operacao=row[2],
                    carga_atual=row[3],
                    centro=CentroDistribuicao(id=row[4], nome=row[8])
                )
                for row in rows
            ]
        except sqlite3.Error as e:
            raise ErroBancoDados(f"Falha ao buscar caminhões disponíveis: {str(e)}")

    def atualizar_status_caminhao(self, caminhao_id: str, status: str) -> None:
        """Atualizar o status do caminhão com validação."""
        status_validos = {'disponivel', 'em_rota', 'manutencao'}
        if status not in status_validos:
            raise ValueError(f"Status inválido. Deve ser um dos seguintes: {status_validos}")

        try:
            with self.transacao() as cursor:
                cursor.execute("""
                    UPDATE caminhao 
                    SET status = ?, ultima_atualizacao = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (status, caminhao_id))
        except ErroBancoDados as e:
            raise ErroBancoDados(f"Falha ao atualizar o status do caminhão: {str(e)}")

    def __enter__(self):
        """Suporte ao protocolo de gerenciador de contexto."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Garantir o fechamento correto dos recursos do banco de dados."""
        self.fechar_conexao()

    def fechar_conexao(self) -> None:
        """Fechar a conexão com o banco de dados de maneira segura."""
        try:
            if self.conn:
                self.conn.close()
        except sqlite3.Error as e:
            raise ErroBancoDados(f"Erro ao fechar a conexão com o banco de dados: {str(e)}")
