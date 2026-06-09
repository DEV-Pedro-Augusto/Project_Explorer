import json
from pathlib import Path
from supabase import create_client, Client

# =========================================================
# CONFIGURAÇÃO SUPABASE
# =========================================================

SUPABASE_URL = "https://ulgnemjbobycljlfuitc.supabase.co"
SUPABASE_KEY = "sb_publishable_BsXf3gfYCYCAz5LKlgHl_w_sGQjjMwd"

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# =========================================================
# CONFIGURAÇÕES DA MISSÃO
# =========================================================

ID_USUARIO = 1
ID_DISPOSITIVO = 1

DESCRICAO = "Importação automática via pipeline"

# =========================================================
# ARQUIVO GERADO PELO TEST.PY
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

ARQUIVO_JSON = BASE_DIR.parent / "saida_verticalizada.json"

# =========================================================
# CARREGA JSON
# =========================================================

with open(
    ARQUIVO_JSON,
    "r",
    encoding="utf-8"
) as f:

    dados = json.load(f)

print(f"Registros carregados: {len(dados)}")

# =========================================================
# DESCOBRE INÍCIO E FIM DA MISSÃO
# =========================================================

horarios = sorted(
    [registro["horario"] for registro in dados]
)

inicio_missao = horarios[0]
fim_missao = horarios[-1]

print("Início:", inicio_missao)
print("Fim:", fim_missao)

# =========================================================
# CRIA SESSÃO
# =========================================================

sessao = {
    "id_usuarios": ID_USUARIO,
    "id_dispositivos": ID_DISPOSITIVO,
    "inicio_missao": inicio_missao,
    "fim_missao": fim_missao,
    "descricao_livre": DESCRICAO
}

resultado = (
    supabase
    .table("sessoes_leituras")
    .insert(sessao)
    .execute()
)

if not resultado.data:
    raise Exception(
        "Não foi possível criar a sessão."
    )

id_sessao = resultado.data[0]["id_sessoes_leituras"]

print(
    f"Sessão criada com ID: {id_sessao}"
)

# =========================================================
# PREPARA LEITURAS
# =========================================================

leituras = []

for registro in dados:

    leituras.append({

        "id_sessoes_leituras": id_sessao,

        "id_etiquetas_sensores":
            registro["id_etiqueta"],

        "valores_lidos":
            registro["valor"],

        "data_hora":
            registro["horario"]

    })

print(
    f"Preparados {len(leituras)} inserts."
)

# =========================================================
# INSERT EM LOTES
# =========================================================

BATCH_SIZE = 500

for i in range(
    0,
    len(leituras),
    BATCH_SIZE
):

    lote = leituras[
        i:i + BATCH_SIZE
    ]

    (
        supabase
        .table("leituras")
        .insert(lote)
        .execute()
    )

    print(
        f"Lote enviado: "
        f"{i + len(lote)} / {len(leituras)}"
    )

print("\n✅ Importação concluída com sucesso!")
print(f"📌 Sessão criada: {id_sessao}")
print(f"📊 Leituras inseridas: {len(leituras)}")