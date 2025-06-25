import pieces
from gvars import *

"""
Obj: Realizar Todos os calculos para montagem do dataframe para exportacao com resultados
"""
       
def coleta_indicadores(dataframe):
    try:
        
        pieces.lib_logging.logger.info("> INICIO coleta_indicadores()")            

        # pega todos coloboradores do dataframe
        lista_colaboradores = dataframe['Nome'].unique()

        for item in lista_colaboradores:
            dados_filtrados = dataframe.loc[dataframe['Nome'] == item]
            total_titulos = dados_filtrados['Título'].nunique()
            pieces.lib_logging.logger.info(f"total de itens do {item} foi: {total_titulos}")
                                
    except Exception as error:
        pieces.lib_logging.logger.error(f"ERRO no coleta_indicadores: message: {error}")

    finally:
        pieces.lib_logging.logger.info("> FIM coleta_indicadores()")
        
def export_to_excel(dataframes, filenames):
    try:
        pieces.lib_logging.logger.info(">[INICIO] export_to_excel()")
        for df, file_name in zip(dataframes, filenames):
            file_name = PATH_FILES + pieces.os.sep +f"{file_name}.xlsx"  # Adicionando a extensão .xlsx
            df.to_excel(file_name, index=False)
            print(f"DataFrame exportado para '{file_name}' com sucesso.")
    except Exception as error:
        pieces.lib_logging.logger.error(f"> ERRO create_base: message: {error}")
    finally:
        pieces.lib_logging.logger.info(">[FIM] export_to_excel()")

def mapear_qtd_funcionarios_projeto(file_path,sheet_name):
    try:
        pieces.lib_logging.logger.info(">[INICIO] mapear_qtd_funcionarios_projeto() ")
        df_funcionarios = pieces.pd.read_excel(file_path, sheet_name=sheet_name)

        contagens_por_projeto = {}
        # Agrupando as funcionario por projeto
        funcao_por_projeto = df_funcionarios.groupby(f'{COLUNA_PROJETO_FUNC}')[f'{COLUNA_FUNCAO}'].apply(list) 
        
        for projeto, funcoes in funcao_por_projeto.items():            
            # Filtrar funcionários por  projeto
            filter_projeto = df_funcionarios[(df_funcionarios[f'{COLUNA_PROJETO_FUNC}'] == projeto)]
            # Filtrando valores nulos na coluna 'Nome'
            filter_projeto_sem_nulos = filter_projeto[(filter_projeto[f'{COLUNA_NOME_FUNC}'].notna()) & (filter_projeto[f'{COLUNA_HORAS}'].notna())]            
            # Filtrar funcionários por projeto
            funcionarios_projeto = filter_projeto_sem_nulos[(filter_projeto_sem_nulos[f'{COLUNA_PROJETO_FUNC}'] == projeto)]  

            # Agrupar os dados pela coluna 'Funcao' e contar o número de ocorrências de cada função
            contagem_funcoes = funcionarios_projeto[f'{COLUNA_FUNCAO}'].value_counts()

            # Adicionar a contagem de funcionários por função ao dicionário
            contagens_por_projeto[projeto] = contagem_funcoes.to_dict()        

        pieces.lib_logging.logger.info(f"contagens_por_projeto: {contagens_por_projeto}")
        
        return contagens_por_projeto

    except Exception as error:
        pieces.lib_logging.logger.error(f">[ERRO] mapear_qtd_funcionarios_squad(): message: {error}")
    finally:
        pieces.lib_logging.logger.info(">[FIM] mapear_qtd_funcionarios_projeto() ")

def get_qtd_funcao(dictionary,projeto, funcao):
    try:
        total = dictionary[f'{projeto}'][f'{funcao}']
        pieces.lib_logging.logger.info(f"[INICIO]get_qtd_funcao")
        pieces.lib_logging.logger.info(f" > total: {total} na funcao: {funcao}")
        return total
    except Exception as error:
        pieces.lib_logging.logger.error(f"ERRO get_qtd_funcao, menssage: {error}")
    finally:
        pieces.lib_logging.logger.info(f"[FIM]get_qtd_funcao")             

def distribuir_numero(numero, partes):
    quociente, resto = divmod(numero, partes)
    partes_distribuidas = [quociente] * partes
    # Adiciona o resto à primeira parte
    partes_distribuidas[0] += resto
     # se o numero for que a parte retorna sempre o indice 0
    if numero < partes:
        return partes_distribuidas
 
    return partes_distribuidas

def create_plan_modelo(dias_uteis,mes,ano):
    try:  
        lista_erros = []
        #recupera dados do excel JIRA
        df_jira_geral = pieces.pd.read_excel(PATH_EXCEL_2, sheet_name=SHEET_2)
        #selecionando somente duas colunas do Jira
        colunas_selecionadas = [f'{COLUNA_KEY}',f'{COLUNA_WORK_ITEM}', f'{COLUNA_PROJETO}']
        df_jira_selecao = df_jira_geral[colunas_selecionadas]
        #formata campo projeto para trocar de sigla para campo texto inteiro
        df_jira = formata_df(df=df_jira_selecao)
        #recupera dados do excel com horas, projeto e funcionarios
        df_funcionarios = pieces.pd.read_excel(PATH_EXCEL_3, sheet_name=SHEET_3)
        # Chama funcao para calcular total funcionario em todas do projeto
        #dic_funcionarios = pieces.lib_spreadsheet.mapear_qtd_funcionarios_projeto(file_path=PATH_EXCEL_3, sheet_name=SHEET_3)
        # Cria o modelo dataframe que sera entregue        
        df_modelo = pieces.pd.DataFrame(columns=COLUMNS_PLAN_MODELO)
        #Agrupando projeto e Nome dos funcionarios planilha variavel
        funcionario_por_projeto = df_funcionarios.groupby(f'{COLUNA_PROJETO_FUNC}')[f'{COLUNA_NOME_FUNC}'].apply(list)
        # Iterar sobre cada projeto e suas work item
        for projeto, nome in funcionario_por_projeto.items():
            # Filtrar funcionários por projeto
            funcionarios_projeto = df_funcionarios[(df_funcionarios[f'{COLUNA_PROJETO_FUNC}'] == projeto)]
            # Filtrando valores nulos na coluna 'Nome'            
            filter_projeto_sem_nulos = funcionarios_projeto[(funcionarios_projeto[f'{COLUNA_NOME_FUNC}'].notna()) & (funcionarios_projeto[f'{COLUNA_HORAS}'].notna())]
            #filtrar projeto de acordo com resumo jira
            work_filter = df_jira[(df_jira[f'{COLUNA_PROJETO}'] == projeto)]
            #totalizar itens
            #total_work_item = work_filter[f'{COLUNA_WORK_ITEM}'].count()
            try:                                                
                if work_filter.empty:
                    pieces.lib_logging.logger.error(f"> Ver projeto: {projeto} esta divergente entre Jira e Base de Funcionários")
                    continue
            except Exception as error:
                pieces.lib_logging.logger.error(f"> ERRO new_create_plan_modelo: message: {error}")
            # Se tiver vazio significa que nao tem funcionario para este projeto pula para prox
            if filter_projeto_sem_nulos.empty:
                continue
        
            for _, row in filter_projeto_sem_nulos.iterrows():                
                horas = row[f'{COLUNA_HORAS}']
                nome = row[f'{COLUNA_NOME_FUNC}']
                funcao = row[f'{COLUNA_FUNCAO}']
                squad = row[f'{COLUNA_SQUAD}']
                dt_inicio_ferias = row[f'{COLUNA_INICIO}']
                dt_fim_ferias = row[f'{COLUNA_FIM}']      
                dt_inicio_ferias= pieces.lib_calendar.valida_data_dataframe(dt_inicio_ferias)
                dt_fim_ferias= pieces.lib_calendar.valida_data_dataframe(dt_fim_ferias)
                # valida se tem horas para distribuir
                if horas == 0:
                    pieces.lib_logging.logger.info(f"> Funcionario {nome} do projeto  não tem horas para distribuir")
                    continue
                # valida ferias
                if not pieces.pd.isnull(dt_inicio_ferias) and not pieces.pd.isnull(horas):
                    ferias = True
                else:
                    ferias = False
                # Valida Horas file funcionarios
                result_validation = pieces.lib_spreadsheet.valida_dias_uteis_file_func(
                    dias_uteis=dias_uteis, 
                    horas=horas, 
                    ferias=ferias,
                    nome= nome)
                
                if len(result_validation) > 0:
                    lista_erros += result_validation
                    falha = True
                    continue
                else:
                    falha = False

                ### NOVA DISTRIBUICAO DE HORAS POR CARD E DIAS UPDATE 25/06/2025 ###
                df_modelo = distribuir_horas_card(
                    df_modelo=df_modelo,
                    num_work_items=len(work_filter['Key']),
                    work_item_df=work_filter,
                    total_horas=horas,
                    dias_uteis=dias_uteis,
                    ferias=ferias,
                    inicio_ferias=dt_inicio_ferias,
                    fim_ferias=dt_fim_ferias,
                    projeto=projeto,
                    squad=squad,
                    funcao=funcao,
                    nome=nome,
                    mes = mes,
                    ano = ano
                    )  
        # EXPORTA DATAFRAME PARA EXCEL
        if not falha:            
            df_modelo.to_excel(PATH_REPORT, index=False) 
            pieces.lib_logging.logger.info(f">Relatório exportado com sucesso para o diretório: {PATH_REPORT}")
            continuar = True 
            msg = "Sucesso"
    except Exception as error:
        pieces.lib_logging.logger.error(f"> ERRO create_plan_modelo: message: {error}")
        pieces.traceback.print_exc()
        continuar = False
        msg = error
    finally:
        return continuar, msg 
    
def valida_dias_uteis_file_func(dias_uteis, horas, ferias,nome):
    try:
        erros = []
        total_dias_uteis = len(dias_uteis)
        total_horas_possiveis = total_dias_uteis * 8
        if ferias:
            if horas == total_horas_possiveis:
                msg = f"» Funcionario: {nome} - Não foi descontado horas de ferias na tab funcionarios: {horas}"
                pieces.lib_logging.logger.error(msg) 
                erros.append(msg)                       
        if horas >  total_horas_possiveis:
            msg = f"» Funcionario: {nome} - Divergencia entre horas possiveis: {total_horas_possiveis} e horas na tabela funcionario: {horas} em dias uteis: {total_dias_uteis}"
            pieces.lib_logging.logger.error(msg)
            erros.append(msg)  
        return erros 
        
    except Exception as error:
        pieces.lib_logging.logger.error(f"> ERRO valida_dias_uteis_file_func: message: {error}")
        pieces.traceback.print_exc()

    
def formata_df(df):
    df = df.copy()  # Garante uma cópia interna e evita SettingWithCopyWarning
    try:
        for palavra, substituicao in zip(COL_JIRA_API, PROJECTS):
            df["Project"] = df["Project"].str.replace(palavra, substituicao, regex=False)
    except Exception as error:
        pieces.lib_logging.logger.error(error) 
    finally:
        return df


def distribuir_horas_card(df_modelo,total_horas, num_work_items, work_item_df,squad, projeto, funcao, nome,ferias,inicio_ferias,fim_ferias,dias_uteis,mes,ano):
    if ferias:
        dias_uteis_mes = pieces.lib_calendar.dias_fora_do_intervalo_ferias(dia_inicial= int(inicio_ferias), dia_final= int(fim_ferias),lista_dias_uteis= dias_uteis) 
    else:
        dias_uteis_mes = dias_uteis
    num_dias = dias_uteis_mes
    
    if total_horas != len(num_dias) * 8:
        raise ValueError("Total de horas não bate com dias úteis * 8h")
    work_item_summaries = dict(work_item_df[['Key','Summary']].values)
    work_keys = list(work_item_df['Key'])
    num_work_items = len(work_keys)
    dia_horas = [[] for _ in num_dias]
    horas_por_item = [0] * num_work_items

    for i in range(num_work_items):
        horas_por_item[i] = 1
    restante = total_horas - num_work_items
    index = 0

    while restante > 0:
        if restante > 0:
            horas_por_item[index] += 1
            restante -= 1
        index = (index + 1) % num_work_items

    item_index = 0
    registros = []
    for dia in num_dias:
        dia_total = 0
        while dia_total < 8 and item_index < num_work_items:
            alocar = min(horas_por_item[item_index], 8 - dia_total)
            # Calcula o incremento de dias para o 'Fim'            
            data_inicio = pieces.date(ano, mes, dia)
            dias_extra = (alocar - 1) // 8
            data_fim = data_inicio + pieces.timedelta(days=dias_extra)

            registros.append({
                'Squad': squad,
                'Projeto': projeto,
                'Título': work_item_summaries.get(work_keys[item_index], str(work_keys[item_index])),
                'Função': funcao,
                'Nome': nome,
                'Inicio': data_inicio.strftime("%d/%m/%Y"),
                'Fim': data_fim.strftime("%d/%m/%Y"),
                'Qtd Horas': alocar
            })
            dia_total += alocar
            horas_por_item[item_index] -= alocar
            if horas_por_item[item_index] == 0:
                item_index += 1
    df_novo = pieces.pd.DataFrame(registros)
    pieces.lib_logging.logger.info(f"SUCESSO ao adicionar {total_horas} Horas do funcionario: {nome} ao Dataframe!")
    if df_modelo is not None:
        return pieces.pd.concat([df_modelo, df_novo], ignore_index=True)

    return pieces.df_novo
    

    
    
