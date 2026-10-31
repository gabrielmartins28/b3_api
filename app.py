
import streamlit as st
import requests
import os
import json
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

# ==========================================
# CONFIGURAÇÕES
# ==========================================

load_dotenv()

TOKEN = os.getenv("token_api")
URL_BASE = "https://brapi.dev/api/quote/"

st.set_page_config(
    page_title="Análise de Ações",
    page_icon="📈",
    layout="wide"
)

# ==========================================
# ESTILO
# ==========================================

st.markdown("""
<style>
    .main {
        background-color: #f8f9fc;
    }

    div.stButton > button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 8px;
        border: none;
        width: 100%;
    }

    div.stButton > button:hover {
        background-color: #e63e3e;
        color: white;
    }

    [data-testid="stMetric"] {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #eeeeee;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def formatar_moeda(valor):
    if valor is None:
        return "Não disponível"

    try:
        return f"R$ {float(valor):,.2f}".replace(
            ",", "X"
        ).replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return "Não disponível"


def formatar_numero(valor):
    if valor is None:
        return "Não disponível"

    try:
        return f"{float(valor):,.0f}".replace(
            ",", "."
        )
    except (ValueError, TypeError):
        return "Não disponível"


def consultar_acao(ticker, periodo):

    parametros = {
        "range": periodo,
        "interval": "1d"
    }

    cabecalhos = {}

    if TOKEN:
        cabecalhos["Authorization"] = TOKEN

    try:
        resposta = requests.get(
            URL_BASE + ticker,
            params=parametros,
            headers=cabecalhos,
            timeout=30
        )

        dados = resposta.json()

        if resposta.status_code != 200:
            mensagem = dados.get(
                "message",
                dados.get("error", resposta.text)
            )

            return None, f"Erro HTTP {resposta.status_code}: {mensagem}"

        if dados.get("error"):
            return None, str(dados["error"])

        resultados = dados.get("results", [])

        if not resultados:
            return None, "Nenhum resultado encontrado para esse ticker."

        return resultados[0], None

    except requests.exceptions.Timeout:
        return None, "A consulta demorou demais. Tente novamente."

    except requests.exceptions.ConnectionError:
        return None, "Não foi possível conectar à API."

    except ValueError:
        return None, "A API retornou uma resposta inválida."

    except requests.exceptions.RequestException as erro:
        return None, f"Erro na requisição: {erro}"


# ==========================================
# HISTÓRICO
# ==========================================

def mostrar_historico(dados):

    historico = dados.get("historicalDataPrice", [])

    if not historico:
        st.info("Não há dados históricos disponíveis.")
        return

    df = pd.DataFrame(historico)

    if "date" not in df.columns or "close" not in df.columns:
        st.info("Os dados históricos não possuem o formato esperado.")
        return

    df["Data"] = pd.to_datetime(
        df["date"],
        unit="s",
        utc=True
    ).dt.tz_convert("America/Sao_Paulo")

    df = df.sort_values("Data")

    df = df.set_index("Data")

    colunas = ["close"]

    if "adjustedClose" in df.columns:
        colunas.append("adjustedClose")

    grafico = df[colunas].rename(columns={
        "close": "Fechamento",
        "adjustedClose": "Fechamento ajustado"
    })

    st.line_chart(grafico)

    st.caption(
        f"Histórico com {len(df)} registros. "
        "Os valores representam os fechamentos disponíveis."
    )


# ==========================================
# CABEÇALHO
# ==========================================

st.title("📈 Painel de Análise de Ações")

st.markdown(
    "Consulte cotações e acompanhe a evolução histórica "
    "de empresas negociadas na bolsa brasileira."
)

st.divider()


# ==========================================
# FORMULÁRIO DE CONSULTA
# ==========================================

st.subheader("Consultar empresa")

with st.form("form_consulta"):

    col1, col2 = st.columns([2, 1])

    with col1:
        ticker = st.text_input(
            "Código da ação",
            value="WEGE3",
            placeholder="Exemplo: PETR4"
        )

    with col2:
        periodos = {
            "1 dia": "1d",
            "5 dias": "5d",
            "1 mês": "1mo",
            "3 meses": "3mo"
        }

        periodo_nome = st.selectbox(
            "Período histórico",
            options=list(periodos.keys()),
            index=2
        )

    st.caption(
        "Consulta básica de cotações. "
        "O intervalo histórico utilizado é diário."
    )

    consultar = st.form_submit_button(
        "🔎 Consultar ação",
        use_container_width=True
    )


# ==========================================
# RESULTADOS
# ==========================================

if consultar:

    ticker = ticker.strip().upper()

    if not ticker:
        st.warning("Digite o código de uma ação.")

    else:

        periodo = periodos[periodo_nome]

        with st.spinner(f"Consultando {ticker}..."):

            dados, erro = consultar_acao(
                ticker,
                periodo
            )

        if erro:
            st.error(erro)

        elif dados:

            st.success(
                f"Consulta de {dados.get('symbol', ticker)} realizada!"
            )

            nome_empresa = dados.get(
                "longName",
                dados.get("shortName", ticker)
            )

            st.subheader(nome_empresa)

            st.caption(
                f"Código: {dados.get('symbol', ticker)}"
            )

            # ----------------------------------
            # INDICADORES PRINCIPAIS
            # ----------------------------------

            preco = dados.get("regularMarketPrice")
            variacao = dados.get("regularMarketChangePercent")
            volume = dados.get("regularMarketVolume")
            maxima = dados.get("regularMarketDayHigh")
            minima = dados.get("regularMarketDayLow")
            fechamento = dados.get("regularMarketPreviousClose")
            abertura = dados.get("regularMarketOpen")
            market_cap = dados.get("marketCap")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Cotação atual",
                    formatar_moeda(preco)
                )

            with col2:
                delta = (
                    f"{float(variacao):.2f}%"
                    if variacao is not None
                    else None
                )

                st.metric(
                    "Variação",
                    delta if delta else "Não disponível"
                )

            with col3:
                st.metric(
                    "Máxima do dia",
                    formatar_moeda(maxima)
                )

            with col4:
                st.metric(
                    "Mínima do dia",
                    formatar_moeda(minima)
                )

            st.divider()

            # ----------------------------------
            # ABAS
            # ----------------------------------

            aba1, aba2, aba3 = st.tabs([
                "📊 Histórico",
                "📋 Informações",
                "🔧 Dados da API"
            ])

            # HISTÓRICO

            with aba1:

                st.subheader("Evolução da cotação")

                mostrar_historico(dados)

            # INFORMAÇÕES

            with aba2:

                st.subheader("Dados da negociação")

                col1, col2 = st.columns(2)

                with col1:

                    st.write("**Preço de abertura:**")
                    st.write(formatar_moeda(abertura))

                    st.write("**Fechamento anterior:**")
                    st.write(formatar_moeda(fechamento))

                    st.write("**Volume negociado:**")
                    st.write(formatar_numero(volume))

                with col2:

                    st.write("**Máxima do dia:**")
                    st.write(formatar_moeda(maxima))

                    st.write("**Mínima do dia:**")
                    st.write(formatar_moeda(minima))

                    st.write("**Valor de mercado:**")
                    st.write(formatar_moeda(market_cap))

            # JSON

            with aba3:

                st.subheader("Resposta completa da API")

                st.json(dados)

                arquivo = json.dumps(
                dados,
                indent=4,
                ensure_ascii=False
            )

                st.download_button(
                    "⬇️ Baixar dados JSON",
                    data=arquivo,
                    file_name=f"{ticker}_dados.json",
                    mime="application/json"
                )


# ==========================================
# EXEMPLOS
# ==========================================

st.divider()

st.subheader("Exemplos de ativos")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("PETR4 — Petrobras")

with col2:
    st.info("WEGE3 — WEG")

with col3:
    st.info("VALE3 — Vale")

with col4:
    st.info("ITUB4 — Itaú Unibanco")


# ==========================================
# RODAPÉ
# ==========================================

st.divider()

st.caption(
    "Dados fornecidos pela brapi.dev. "
    "As informações podem apresentar atraso e não representam "
    "recomendação de investimento."
)
