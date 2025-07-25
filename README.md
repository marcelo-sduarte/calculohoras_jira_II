# Calculadora de Horas do Jira_II

# Visão Geral
A Calculadora de Horas do Jira é um projeto em Python projetado para otimizar o processo de rastreamento de horas de trabalho para funcionários em vários squads utilizando dados do Jira e arquivos de funcionários. Aproveitando o poder da biblioteca Pandas, esta ferramenta lê eficientemente arquivos Excel contendo dados do Jira e informações dos funcionários, realiza cálculos para determinar as horas trabalhadas por cada funcionário dentro de seus respectivos squads e entrega resultados abrangentes ao cliente.

# Estrutura de Pastas
    - env
    - input
    - output
        - files
        - logs
    - src
        -libs
        
# Instalação
Para usar a Calculadora de Horas do Jira, siga estes passos:

1.  Clone este repositório em sua máquina local:
bash
Copy code
git clone https://github.com/marcelo-sduarte/calculohoras_jira_II.git
Instale as dependências necessárias:

2. Configure o repositorio virtual.
bash
Copy code
python -m venv env

3. Instale as bibliotecas necessárias:
bash
Copy code
pip install -r requirements.txt

4. Certifique que seus arquivos Excel contendo dados do Jira e informações dos funcionários estejam na pasta [input] e garantindo que sigam o formato especificado.

5. Revise file [gvars.py] e ajustes os diretorios que serão utilizados no projeto.

6. Execute o script principal [src/main.py]:
bash
Copy code
python main.py

7. Todas as bibliotecas usadas no python constam no file [pieces.py]

8.  Salve as credentials no cofre do windows, usando a funcao save_credential no file e edite as variaves que constam no [gvars.py], Ex: TARGET_TOKEN_JIRA e EMAIL_TARGET

9. Pode usar as funções def save_credential e def get_credential que constam na [lib_process.py] para salvar as credentials no cofre do windows.

# Licença
Este projeto é licenciado sob a Licença MIT - consulte o arquivo LICENSE para obter mais detalhes.

Copyright © 2024 Cadmus by Marcelo Duarte. Todos os direitos reservados.