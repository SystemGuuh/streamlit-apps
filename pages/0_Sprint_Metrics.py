import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.sheets import *

# Variável global para armazenar o resultado da primeira chamada da função getGSheet, se não teremos erro de requisição excessiva
first_execution_result = None #pensar numa logica para nao dar erro de requisicao
def getGSheet(sheet):
    global first_execution_result
    if first_execution_result is None:
        # Pegando planilha do google sheets
        gsheets_reader = GSheetsReader()
        first_execution_result = 1
        if(sheet==1): #retorna planilha de task
            taskControl = gsheets_reader.taskControl()
            taskControl = taskControl.drop(columns=[col for col in taskControl.columns if 'Unnamed' in col])
            return taskControl
        else: #retorna planilha de metricas
            sprintMetrics = gsheets_reader.sprintMetrics()
            sprintMetrics = sprintMetrics.drop(columns=[col for col in sprintMetrics.columns if 'Unnamed' in col])
            return sprintMetrics

sprint_selected = None
def showTaskData(taskControl):
    global sprint_selected
    if taskControl is not None:
        with st.sidebar:
            distinct_sprint = taskControl["Sprint"].unique().tolist()
            sprint_selected = st.selectbox("Sprint cicle:", distinct_sprint)
            
        if sprint_selected:
            taskControl = taskControl[taskControl["Sprint"] == sprint_selected]
            st.write("### Dados das tarefas da Sprint ", sprint_selected)

            #calculando fim da sprint
            start_date = datetime.strptime(taskControl["Start Date"].unique().tolist()[0], "%d/%m/%y")
            end_date = start_date + timedelta(days=7)

            #imprime inicio e fim da sprint em colunas diferentes
            col1, col2 = st.columns(2)
            col1.text("Início da sprint: \U0001F4C5 {}".format(taskControl["Start Date"].unique().tolist()[0]))
            col2.text("Fim da sprint: \U0001F4C5 {}".format(end_date.strftime("%d/%m/%y")))
            
            #cria checkbox para colunas da tabela
            col3, col4, col5, col6 = st.columns(4)
            Task = col3.checkbox('Tarefa', value=True)
            Assignee = col4.checkbox('Responsável', value=True)
            Priority = col5.checkbox('Prioridade', value=True)
            Task_Weight = col6.checkbox('Peso da Tarefa', value=True)

            col7, col8, col9, col10 = st.columns(4)
            Status = col7.checkbox('Estatus', value=True)
            Dependence = col8.checkbox('Dependência')
            Start_Date = col9.checkbox('Data de Início', value=True)
            End_Date = col10.checkbox('Data de Término')
        

        #tira colunas que não estamos usando e renomeia as colunas que ficaram
        taskControl_view = taskControl.drop(columns=['Sprint', 'Leadtime','Estimation Date','Estimate Leadtime','Weight to Burndown' ,'Leadtime * Weight', 'Notes/Comments'])
        taskControl_view.columns = ['Tarefa', 'Responsável','Prioridade','Peso','Início','Termino','Status','Dependência']
        
        # se checkbox nao ativa, dropa coluna, seão, coloca de volta
        if not Task:
            taskControl_view.drop(columns=['Tarefa'], inplace=True)
        else:
            taskControl_view['Tarefa'] = taskControl['Task']

        if not Assignee:
            taskControl_view.drop(columns=['Responsável'], inplace=True)
        else:
            taskControl_view['Responsável'] = taskControl['Assignee']

        if not Priority:
            taskControl_view.drop(columns=['Prioridade'], inplace=True)
        else:
            taskControl_view['Prioridade'] = taskControl['Priority']

        if not Task_Weight:
            taskControl_view.drop(columns=['Peso'], inplace=True)
        else:
            taskControl_view['Peso'] = taskControl['Task Weight']

        if not Start_Date:
            taskControl_view.drop(columns=['Início'], inplace=True)
        else:
            taskControl_view['Início'] = taskControl['Start Date']

        if not End_Date:
            taskControl_view.drop(columns=['Termino'], inplace=True)
        else:
            taskControl_view['Termino'] = taskControl['End Date']

        if not Status:
            taskControl_view.drop(columns=['Status'], inplace=True)
        else:
            taskControl_view['Status'] = taskControl['Status']

        if not Dependence:
            taskControl_view.drop(columns=['Dependência'], inplace=True)
        else:
            taskControl_view['Dependência'] = taskControl['Dependencies']

        st.dataframe(taskControl_view, hide_index=True)


st.set_page_config(page_title="Sprint Metrics", page_icon="🤡", layout="wide")
st.markdown("# Current Sprint")
st.sidebar.header("Sprint metrics")

showTaskData(getGSheet(1))
st.divider()

#nao ta pegando valor sprint_selected
if sprint_selected:
    df = getGSheet(2)
    df = df[df["Sprint"] == sprint_selected]
    st.write("### Métricas da sprint ", sprint_selected, ":")

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Pontos totais", value=int(df[" Total Story Points"]), delta=int(df["Total Sprint Effort"] - df[" Total Story Points"]), delta_color="inverse")
    col2.metric(label="Velocidade média", value=int(df["Burndown Speed"]), delta=int(df["Required Burndown Speed"]), delta_color="inverse")
    try:
        col3.metric(label="Porcentagem", value=df["Weighted Cycle Time"].astype(str).iloc[0])
    except IndexError:
        st.error("A coluna 'Weighted Cycle Time' está vazia. Não há valores para exibir.")
    except Exception as e:
        st.error("Ocorreu um erro ao processar os dados da coluna 'Weighted Cycle Time': {}".format(str(e)))

    if uploaded_file2 is None:
        st.warning('Se quiser ver mais dados, mande o arquivo SprintTasks.csv', icon="⚠️")
    else:
        if(df["Weighted Cycle Time"].astype(str).iloc[0] != '100%'):
            col11, col12 = st.columns([1, 2]) #seta o espaço de cada coluna
            col11.write("### Tarefas não terminadas:")

            df2_view = df2.drop(columns=['Sprint', 'Leadtime','Estimation Date','Estimate Leadtime','Weight to Burndown' ,'Leadtime * Weight', 'Notes/Comments'])
            df2_view.columns = ['Tarefa', 'Responsável','Prioridade','Peso','Início','Termino','Status','Dependência']
            
            df2_nextTask = df2_view[df2_view["Status"] == 'Next']
            col12.dataframe(df2_nextTask[["Tarefa","Responsável", "Prioridade", "Peso"]], hide_index=True)
    
    df2_grouped = df2[df2["Status"] == "Finished"].groupby("Assignee")["Task Weight"].sum().reset_index()
    df2_grouped2 = df2[df2["Status"] == "Next"].groupby("Assignee")["Task Weight"].sum().reset_index()
    df2_grouped.rename(columns={"Task Weight": "Pontos da Sprint", "Assignee": "Nome"}, inplace=True)
    df2_grouped2.rename(columns={"Task Weight": "Pontos perdidos", "Assignee": "Nome"}, inplace=True)
    df2_merged = pd.merge(df2_grouped, df2_grouped2, on="Nome", how="outer")
    
    
    mid_index = len(df2_merged) // 2
    col1, col2, col3 = st.columns(3)

    # Exibir os dados na primeira coluna
    for i in range(mid_index):
        nome = df2_merged["Nome"].iloc[i]
        pontos_sprint = int(df2_merged["Pontos da Sprint"].iloc[i]) if not pd.isna(df2_merged["Pontos da Sprint"].iloc[i]) else 0
        pontos_perdidos = int(df2_merged["Pontos perdidos"].iloc[i]) if not pd.isna(df2_merged["Pontos perdidos"].iloc[i]) else 0
        col1.metric(label=nome, value=pontos_sprint, delta=pontos_perdidos, delta_color="inverse")

    # Exibir os dados na segunda coluna
    for i in range(mid_index, len(df2_merged)):
        nome = df2_merged["Nome"].iloc[i]
        pontos_sprint = int(df2_merged["Pontos da Sprint"].iloc[i]) if not pd.isna(df2_merged["Pontos da Sprint"].iloc[i]) else 0
        pontos_perdidos = int(df2_merged["Pontos perdidos"].iloc[i]) if not pd.isna(df2_merged["Pontos perdidos"].iloc[i]) else 0
        col2.metric(label=nome, value=pontos_sprint, delta=pontos_perdidos, delta_color="inverse")

    col3.dataframe(df2_merged[["Nome","Pontos da Sprint", "Pontos perdidos"]],  hide_index=True)
