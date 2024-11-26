# 🚚 **Otimização Logística com Múltiplos Centros de Distribuição**

Este projeto é uma solução algorítmica para otimizar o roteamento de entregas de uma empresa de logística com múltiplos centros de distribuição, minimizando custos e maximizando a eficiência operacional.

---

## 📋 **Objetivo**

- **Minimizar custos de transporte** (tempo e distância percorrida).  
- **Alocar caminhões de forma eficiente** com base na capacidade e disponibilidade.  
- **Garantir a entrega dentro do prazo estipulado**.  
- Determinar o **centro de distribuição mais próximo** para cada entrega.  

---

## 🛠️ **Funcionalidades**

1. **Cálculo de rotas mais curtas** utilizando algoritmos baseados em grafos.  
2. **Integração com APIs externas** para localização geográfica (OpenCage Geocoder).  
3. **Gestão de frota e entregas** com controle de capacidade e priorização.  
4. **Interface de visualização** com menus dedicados para caminhões, clientes, entregas, centros e sistema principal.  

---

## 🗂️ **Estrutura do Projeto**

```plaintext
📦 projeto-logistica
├── database/               # Configurações e inicialização do banco de dados
│   ├── config.py           # Configurações de conexão com o banco
│   └── init_db.py          # Inicialização e criação de tabelas
│
├── models/                 # Modelos do banco de dados
│   ├── caminhao.py         # Modelo de caminhão
│   ├── centro.py           # Modelo de centro de distribuição
│   ├── cliente.py          # Modelo de cliente
│   ├── entrega.py          # Modelo de entrega
│   ├── models.py           # Base e enumerações
│   └── rota.py             # Modelo de rota
│
├── repository/             # Repositório e acesso ao banco de dados
│   └── banco_dados.py      # Repositório para consultas gerais
│
├── service/                # Regras de negócio e serviços
│   ├── cadastro.py         # Cadastro e gerenciamento de dados
│   └── sistema_logistico.py# Lógica principal do sistema logístico
│
├── util/                   # Funções auxiliares
│   ├── calcular_distancia.py # Cálculo de distâncias
│   └── encontrar_localizacao.py # API de localização
│
├── visual/                 # Interface de menus
│   ├── menu_caminhoes.py   # Menu para gestão de caminhões
│   ├── menu_clientes.py    # Menu para gestão de clientes
│   ├── menu_entregas.py    # Menu para gestão de entregas
│   ├── menu_centros.py     # Menu para centros de distribuição
│   └── menu_principal.py   # Menu principal do sistema
│
└── README.md               # Documentação do projeto


