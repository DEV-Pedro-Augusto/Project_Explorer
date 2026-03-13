# Projeto Explorer: Integração Desktop e Monitoramento Ambiental 🚀

Este repositório contém a **Aplicação Desktop** desenvolvida para o projeto final de curso técnico. O objetivo central é atuar como a ponte de dados de um carrinho robótico equipado com sensores de ambiente.

## 🛠️ O Papel da Aplicação
Nossa aplicação é responsável por processar as informações coletadas pelo hardware (Arduino) e garantir que esses dados se tornem informações úteis e acessíveis para tomada de decisão.

### Principais Funcionalidades:
* **Processamento de Dados:** Leitura e conversão de arquivos armazenados via módulo SD (Backup de segurança).
* **Integração em Nuvem:** Envio automático dos dados convertidos para um banco de dados SQL online.
* **Geração de Relatórios:** Criação de visões detalhadas sobre os níveis de gases, umidade e temperatura coletados em locais de difícil acesso.
* **Sincronização Web:** Garante que a interface Web do projeto tenha dados atualizados para exibição pública através do banco de dados compartilhado.

## ⚙️ Tecnologias Utilizadas
* **Linguagem:** Python
* **Banco de Dados:** SQL (A definir provedor: MySQL/PostgreSQL/SQL Server)
* **Formato de Dados:** CSV / JSON (Provenientes dos sensores do Arduino)
* **Arquitetura:** MVC (Model-View-Controller)

## 📊 Dados Monitorados
A aplicação está preparada para tratar dados de:
* Sensores de Gás (Qualidade do ar)
* Sensores de Umidade e Temperatura
* Logs de telemetria do carrinho

## 👥 Membros do Grupo (Aplicação Desktop)
* Daniel Maxx Silva Soares
* Gabriel Henrique da Silva
* Pedro Augusto Domingos Pereira da Silva
* Thales Frederico Fagundes de Noronha

# Window Ambiente virtual 
.... Instalacao  do  ambiente virtual  

    pip install flask # Instalando o virtualizador  
    python -m venv Project_Explorer # Criando o ambiente virtual 
    Project_Explorer/Scripts/activate # Iniciando o ambiente virtual 

    #pip freeze > requirements.txt 
    pip install -r requirements.txt # Instalando as dependencias 
    
# Lixux  Ambiente virtual 
.... Instalacao  do  ambiente virtual Linux

    pip install flask # Instalando o virtualizador  
    python3 -m venv Project_Explorer
    source Project_Explorer/bin/activate
    pip install -r requirements.txt