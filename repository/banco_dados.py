import sqlite3
from typing import List, Optional, Type
from contextlib import contextmanager

from sqlalchemy.orm import Session

from models.centro_distribuicao import CentroDistribuicao
from models.caminhao import Caminhao
from models.cliente import Cliente
from models.entrega import Entrega
from service.sistema_logistico import logger


class ErroBancoDados(Exception):
    pass

class BancoDados:
    def __init__(self, session: Session,nome_bd: str = "entregaAI.db"):
        self.session = session
        try:
            self.conn = sqlite3.connect(nome_bd)
            self.cursor = self.conn.cursor()
            self.criar_tabelas()
        except sqlite3.Error as e:
            logger.error(f"Falha ao inicializar o banco de dados: {str(e)}")
            raise ErroBancoDados(f"Falha ao inicializar o banco de dados: {str(e)}")

    @contextmanager
    def transacao(self):
        try:
            yield self.cursor
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            raise ErroBancoDados(f"Falha na transação: {str(e)}")

    def criar_tabelas(self) -> None:
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
        try:
            with self.transacao() as cursor:
                cursor.execute(
                    "INSERT OR REPLACE INTO centro_distribuicao (nome) VALUES (?)",
                    (centro.nome,)
                )
                centro.id = cursor.lastrowid
                logger.info(f"Centro de distribuição '{centro.nome}' salvo com sucesso.")
        except ErroBancoDados as e:
            logger.error(f"Falha ao salvar centro de distribuição '{centro.nome}': {str(e)}")
            raise ErroBancoDados(f"Falha ao salvar centro de distribuição: {str(e)}")

    def buscar_centro(self, codigo: str) -> Optional[CentroDistribuicao]:
        try:
            centro = self.session.query(CentroDistribuicao).filter_by(codigo=codigo).first()
            return centro
        except Exception as e:
            raise ErroBancoDados(f"Falha ao buscar centro de distribuição: {str(e)}")

    def listar_caminhoes(self) -> list[Type[Caminhao]]:
        try:
            caminhoes = self.session.query(Caminhao).all()
            return caminhoes
        except Exception as e:
            raise ErroBancoDados(f"Falha ao listar caminhões: {str(e)}")

    def listar_centros(self) -> list[Type[CentroDistribuicao]]:
        try:
            centros_distribuicao = self.session.query(CentroDistribuicao).all()
            return centros_distribuicao
        except Exception as e:
            raise ErroBancoDados(f"Falha ao listar caminhões: {str(e)}")

    def listar_entregas(self) -> list[Type[Entrega]]:
        try:
            entregas = self.session.query(Entrega).all()
            return entregas
        except Exception as e:
            raise ErroBancoDados(f"Falha ao listar caminhões: {str(e)}")

    def salvar_caminhao(self, caminhao: Caminhao, session: Session) -> None:
        try:
            self.session.add(caminhao)
        except Exception as e:
            raise ErroBancoDados(f"Falha ao salvar caminhão: {str(e)}")

    def buscar_caminhao_disponivel(self, capacidade_necessaria: int) -> List[Caminhao]:
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
            caminhoes = []
            for row in rows:
                caminhao = Caminhao(
                    id=row[0],
                    capacidade=row[1],
                    horas_operacao=row[2],
                    carga_atual=row[3],
                    status=row[4],
                    updated_at=row[5],
                    centro_distribuicao_id=row[6]
                )
                caminhoes.append(caminhao)
            return caminhoes
        except sqlite3.Error as e:
            raise ErroBancoDados(f"Falha ao buscar caminhões disponíveis: {str(e)}")

    def atualizar_status_caminhao(self, caminhao_id: str, status: str) -> None:
        status_validos = {'disponivel', 'em_rota', 'manutencao'}
        if status not in status_validos:
            raise ValueError(f"Status inválido. Deve ser um dos seguintes: {status_validos}")

        self.cursor.execute("SELECT status FROM caminhao WHERE id = ?", (caminhao_id,))
        row = self.cursor.fetchone()
        if row and row[0] == status:
            logger.info(f"Status do caminhão {caminhao_id} já é '{status}'. Nenhuma atualização necessária.")
            return

        try:
            with self.transacao() as cursor:
                cursor.execute("""
                        UPDATE caminhao 
                        SET status = ?, ultima_atualizacao = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (status, caminhao_id))
            logger.info(f"Status do caminhão {caminhao_id} atualizado para '{status}'.")
        except ErroBancoDados as e:
            raise ErroBancoDados(f"Falha ao atualizar o status do caminhão: {str(e)}")


    def listar_clientes(self) -> List[Cliente]:
        """
        Lista todos os clientes cadastrados no banco de dados.
        """
        try:
            self.cursor.execute("""
                SELECT id, nome, cnpj, endereco, cidade, estado, latitude, longitude 
                FROM cliente
            """)
            rows = self.cursor.fetchall()
            clientes = []
            for row in rows:
                cliente = Cliente(
                    id=row[0],
                    nome=row[1],
                    cnpj=row[2],
                    endereco=row[3],
                    cidade=row[4],
                    estado=row[5],
                    latitude=row[6],
                    longitude=row[7]
                )
                clientes.append(cliente)
            return clientes
        except sqlite3.Error as e:
            logger.error(f"Falha ao listar clientes: {str(e)}")
            raise ErroBancoDados(f"Falha ao listar clientes: {str(e)}")

    def remover_cliente(self, cliente_id: int) -> None:
        """
        Remove um cliente do banco de dados pelo ID.
        """
        try:
            self.cursor.execute("SELECT id FROM cliente WHERE id = ?", (cliente_id,))
            row = self.cursor.fetchone()

            if row is None:
                raise ValueError(f"Cliente com ID {cliente_id} não encontrado.")
            with self.transacao() as cursor:
                cursor.execute("DELETE FROM cliente WHERE id = ?", (cliente_id,))
                logger.info(f"Cliente com ID {cliente_id} removido com sucesso.")
        except ValueError as e:
            logger.error(str(e))
            raise ErroBancoDados(str(e))
        except sqlite3.Error as e:
            logger.error(f"Falha ao remover cliente: {str(e)}")
            raise ErroBancoDados(f"Falha ao remover cliente: {str(e)}")


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fechar_conexao()

    def fechar_conexao(self) -> None:
        try:
            if self.conn:
                self.conn.close()
                logger.info("Conexão com o banco de dados fechada com sucesso.")
        except sqlite3.Error as e:
            logger.error(f"Erro ao fechar a conexão com o banco de dados: {str(e)}")
            raise ErroBancoDados(f"Erro ao fechar a conexão com o banco de dados: {str(e)}")
