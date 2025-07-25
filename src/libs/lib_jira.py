import pieces
from gvars import JIRA_ENDPOINT, PROJECTS, PATH_INPUT, TARGET_TOKEN_JIRA

"""
Funcoes de conexao a API do Jira
"""

def connect_api_jira():
    try:
        # recupera user e token
        jira_user, jira_token = pieces.lib_process.get_credential(target_name=TARGET_TOKEN_JIRA)
        # Conecta-se ao Jira
        jira = pieces.JIRA(JIRA_ENDPOINT, basic_auth=(jira_user, jira_token))

        # Define a data de início do mês anterior e o início deste mês
        #primeiro_dia = pieces.datetime.datetime(ano, mes, 1).strftime("%Y-%m-%d")
        #ultimo_dia = pieces.datetime.datetime(ano, mes, pieces.calendar.monthrange(ano, mes)[1]).strftime("%Y-%m-%d") 

        # Define a query JQL
        ''' Exemplo passado pelo Fabio
        query = ('project in (BANK, COR, CS, FBACK, FIDC, FLIQ, INV, "Fundos Backoffice Cadmus",Banking FrontOffice, Escrituracao,CAAS,Corporate Back,Fundos 175 - Cadmus) '
                'and issuetype in ("Automação", "Debito Tecnico", Story) '
                'and resolutiondate >= "{}" '
                'and resolutiondate <= "{}" '
                'and status = Done').format(primeiro_dia, ultimo_dia)
        
                query = (f'project in ({project_str}) '
                'and issuetype in ( "Debito Tecnico", Story) '
                'and resolutiondate >= startOfMonth(-1) '
                'and resolutiondate < startOfMonth() and status = Done')  
        
        '''
        #Montando a String JQL
        project_str = ', '.join(f'"{project}"' for project in PROJECTS)

        query = ('issuetype in ( "Debito Tecnico", Story) '
                'and resolutiondate >= startOfMonth(-1) '
                'and resolutiondate < startOfMonth() and status = Done')                                            

        # Paginacao pela limitacao de 50 da api Jira
        start_at = 0
        max_results = 500
        issues = []
        
        while True:
            batch = jira.search_issues(query, startAt=start_at, maxResults=max_results)
            if not batch:
                break
            issues.extend(batch)
            start_at += max_results
        # Extrai os dados relevantes das issues
        data = []
        for issue in issues:
            data.append({
            'Key': issue.key,
            'Project': issue.fields.project,
            'Summary': issue.fields.summary,
            'Created': issue.fields.created,
            'Resolution Date': issue.fields.resolutiondate
            })
        # Cria um DataFrame a partir dos dados
        df = pieces.pd.DataFrame(data)
        # Salva o DataFrame como um arquivo Excel
        df.to_excel(PATH_INPUT +'/jira_api.xlsx', index=False, )
        continuar = True
        msg = "Sucesso"
    except Exception as error:
        pieces.lib_logging.logger.error(f" > message error connect_api_jira: {error}")
        continuar = False
        msg = error
        return continuar, msg



