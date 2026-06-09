import pandas as pd
import json
import logging
import math
from typing import List, Dict, Any
from datetime import datetime
import os
from pathlib import Path

print("SCRIPT:", os.path.abspath(__file__))
print("PASTA ATUAL:", os.getcwd())

# Configuração de Logging para auditoria e rastreabilidade
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class PipelineTelemetria:
    """
    Orquestrador de processamento de dados telemétricos.
    Sincroniza sensores de frequências distintas baseando-se em proximidade temporal.
    """

    # Mapeamento Oficial Exigido
    MAPEAMENTO_ETIQUETAS = {
        "mq2_ppm": 1,
        "mq2_lel_pct": 2,
        "mq3_ppm": 3,
        "mq3_mgl": 4,
        "mq7_ppm": 5,
        "mq7_cohb_pct": 6,
        "tempo_volta_s": 7,
        "dist_total_m": 8,
        "frente_cm": 9,
        "direita_cm": 10,
        "esquerda_cm": 11,
        "traseira_cm": 12
    }

    def __init__(self, path_gases: str, path_movimento: str):
        self.path_gases = path_gases
        self.path_movimento = path_movimento

        self.df_gases: pd.DataFrame = pd.DataFrame()
        self.df_movimento: pd.DataFrame = pd.DataFrame()
        self.df_sync: pd.DataFrame = pd.DataFrame()

        self.lista_unificada: List[Dict[str, Any]] = []
        self.lista_verticalizada: List[Dict[str, Any]] = []

        # Variáveis para estatísticas
        self.stats_gases_orig = 0
        self.stats_mov_orig = 0
        self.stats_removidos_limpeza = 0

    def carregar_arquivos(self) -> None:
        """Lê os arquivos CSV ignorando linhas de comentário com '#'."""
        logging.info("Carregando arquivos de telemetria...")

        try:
            self.df_gases = pd.read_csv(
                self.path_gases,
                comment='#'
            )

            self.df_movimento = pd.read_csv(
                self.path_movimento,
                comment='#'
            )

            self.stats_gases_orig = len(self.df_gases)
            self.stats_mov_orig = len(self.df_movimento)

            logging.info(
                f"Arquivos carregados: "
                f"Gases ({self.stats_gases_orig} linhas), "
                f"Movimento ({self.stats_mov_orig} linhas)."
            )

        except FileNotFoundError as e:
            logging.error(f"Erro ao encontrar arquivo: {e}")
            raise

        except pd.errors.EmptyDataError:
            logging.error(
                "O arquivo CSV está vazio ou contém apenas comentários."
            )
            raise

    def limpar_gases(self) -> None:
        """Converte a coluna de horário para datetime."""
        logging.info("Limpando dados de gases...")

        self.df_gases['horario'] = pd.to_datetime(
            self.df_gases['horario'],
            errors='coerce'
        )

        self.df_gases.sort_values(
            'horario',
            inplace=True
        )

    def limpar_movimento(self) -> None:
        """
        Limpa os dados de movimento.

        REGRA DE NEGÓCIO:
        - 'Sem leitura' NÃO deve remover registros.
        - Os valores numéricos já vêm preenchidos (geralmente 0).
        - Nenhuma linha será descartada.
        """

        logging.info("Limpando dados de movimento...")

        self.df_movimento['horario'] = pd.to_datetime(
            self.df_movimento['horario'],
            errors='coerce'
        )

        colunas_numericas = [
            'tempo_volta_s',
            'dist_total_m',
            'frente_cm',
            'direita_cm',
            'esquerda_cm',
            'traseira_cm'
        ]

        for coluna in colunas_numericas:
            if coluna in self.df_movimento.columns:
                self.df_movimento[coluna] = pd.to_numeric(
                    self.df_movimento[coluna],
                    errors='coerce'
                ).fillna(0)

        self.df_movimento.sort_values(
            'horario',
            inplace=True
        )

        self.stats_removidos_limpeza = 0

        logging.info(
            f"Movimento carregado com "
            f"{len(self.df_movimento)} registros. "
            f"Nenhuma linha removida."
        )

    def sincronizar_tabelas(self) -> None:
        """Mescla os DataFrames usando o df_gases como âncora temporal."""

        logging.info(
            "Sincronizando registros por proximidade temporal..."
        )

        self.df_sync = pd.merge_asof(
            left=self.df_gases,
            right=self.df_movimento,
            on='horario',
            direction='nearest',
            tolerance=pd.Timedelta(seconds=5),
            suffixes=('_gases', '_mov')
        )

        self.df_sync = self.df_sync.where(
            pd.notnull(self.df_sync),
            None
        )

    def gerar_lista_unificada(self) -> None:
        """Gera uma lista única com todos os dados sincronizados."""

        logging.info("Gerando Lista Unificada...")

        self.lista_unificada = []

        for _, row in self.df_sync.iterrows():

            linha_unificada = {
                "horario": row["horario"].isoformat(),

                "mq2_ppm": row.get("mq2_ppm"),
                "mq2_lel_pct": row.get("mq2_lel_pct"),

                "mq3_ppm": row.get("mq3_ppm"),
                "mq3_mgl": row.get("mq3_mgl"),

                "mq7_ppm": row.get("mq7_ppm"),
                "mq7_cohb_pct": row.get("mq7_cohb_pct"),

                "tempo_volta_s": (
                    row.get("tempo_volta_s_mov")
                    if row.get("tempo_volta_s_mov") is not None
                    else row.get("tempo_volta_s_gases")
                ),

                "dist_total_m": row.get("dist_total_m"),

                "frente_cm": row.get("frente_cm"),
                "direita_cm": row.get("direita_cm"),
                "esquerda_cm": row.get("esquerda_cm"),
                "traseira_cm": row.get("traseira_cm")
            }

            self.lista_unificada.append(
                linha_unificada
            )

    def gerar_lista_verticalizada(self) -> None:
        """
        Converte a lista horizontalizada
        para modelo EAV.
        """

        logging.info(
            "Gerando Lista Verticalizada "
            "(preparação para Banco de Dados)..."
        )

        self.lista_verticalizada = []

        for registro in self.lista_unificada:

            horario = registro["horario"]

            for chave, id_tag in self.MAPEAMENTO_ETIQUETAS.items():

                valor = registro.get(chave)

                if (
                    valor is not None
                    and not (
                        isinstance(valor, float)
                        and math.isnan(valor)
                    )
                ):
                    self.lista_verticalizada.append(
                        {
                            "horario": horario,
                            "id_etiqueta": id_tag,
                            "valor": float(valor)
                        }
                    )

    def exportar_json(self) -> None:
        """Exporta os JSONs de saída."""

        logging.info(
            "Exportando artefatos JSON..."
        )

        with open(
            "saida_unificada.json",
            "w",
            encoding="utf-8"
        ) as file_uni:
            json.dump(
                self.lista_unificada,
                file_uni,
                indent=4,
                ensure_ascii=False
            )

        with open(
            "saida_verticalizada.json",
            "w",
            encoding="utf-8"
        ) as file_vert:
            json.dump(
                self.lista_verticalizada,
                file_vert,
                indent=4,
                ensure_ascii=False
            )

    def executar_pipeline(self) -> None:

        try:
            self.carregar_arquivos()
            self.limpar_gases()
            self.limpar_movimento()
            self.sincronizar_tabelas()
            self.gerar_lista_unificada()
            self.gerar_lista_verticalizada()
            self.exportar_json()

            print("\n" + "=" * 50)
            print("📊 ESTATÍSTICAS DO PIPELINE")
            print("=" * 50)
            print(
                f"🔸 Registros originais (Gases):      "
                f"{self.stats_gases_orig}"
            )
            print(
                f"🔸 Registros originais (Movimento):  "
                f"{self.stats_mov_orig}"
            )
            print(
                f"🧹 Registros removidos:             "
                f"{self.stats_removidos_limpeza}"
            )
            print(
                f"🔀 Registros resultantes da fusão:   "
                f"{len(self.df_sync)}"
            )
            print(
                f"📄 Tamanho da Lista Unificada:       "
                f"{len(self.lista_unificada)}"
            )
            print(
                f"📑 Tamanho da Lista Verticalizada:   "
                f"{len(self.lista_verticalizada)}"
            )
            print("=" * 50)
            print(
                "✅ Artefatos "
                "'saida_unificada.json' "
                "e 'saida_verticalizada.json' gerados."
            )

        except Exception as e:
            logging.error(
                f"A execução do pipeline falhou: {e}"
            )


# =========================================================
# BLOCO DE EXECUÇÃO
# =========================================================

if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent

    ARQUIVO_GASES = BASE_DIR / "volta_20260602_205723.csv"
    ARQUIVO_MOVIMENTO = BASE_DIR / "volta_20260602_205803.csv"

    print("CSV GASES:", ARQUIVO_GASES)
    print("CSV MOVIMENTO:", ARQUIVO_MOVIMENTO)

    pipeline = PipelineTelemetria(
        str(ARQUIVO_GASES),
        str(ARQUIVO_MOVIMENTO)
    )

    pipeline.executar_pipeline()