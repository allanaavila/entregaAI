from database.config import get_engine, get_session
from models.centro_distribuicao import CentroDistribuicao
from models.models import Base

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_database():
    engine = get_engine()
    Base.metadata.create_all(engine)
    session = get_session()
    try:
        inserir_dados_iniciais(session)
    finally:
        session.close()


def inserir_dados_iniciais(session):

    cds_iniciais = [
        CentroDistribuicao(
            codigo="CD-PA",
            nome="CD Belém",
            endereco="Endereço CD Belém",
            cidade="Belém",
            estado="PA",
            latitude=-1.4557,
            longitude=-48.4902,
            capacidade_maxima=100000
        ),
        CentroDistribuicao(
            codigo="CD-PE",
            nome="CD Recife",
            endereco="Endereço CD Recife",
            cidade="Recife",
            estado="PE",
            latitude=-8.0476,
            longitude=-34.8770,
            capacidade_maxima=150000
        ),
        CentroDistribuicao(
            codigo="CD-SP",
            nome="CD São Paulo",
            endereco="Endereço CD São Paulo",
            cidade="São Paulo",
            estado="SP",
            latitude=-23.5505,
            longitude=-46.6333,
            capacidade_maxima=200000
        ),
        CentroDistribuicao(
            codigo="CD-PR",
            nome="CD Curitiba",
            endereco="Endereço CD Curitiba",
            cidade="Curitiba",
            estado="PR",
            latitude=-25.4284,
            longitude=-49.2733,
            capacidade_maxima=120000
        )
    ]

    try:
        for cd in cds_iniciais:
            existe = session.query(CentroDistribuicao).filter_by(codigo=cd.codigo).first()
            if not existe:
                session.add(cd)

        session.commit()
        logger.info("Dados iniciais inseridos com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao inserir dados iniciais: {str(e)}")
        session.rollback()
