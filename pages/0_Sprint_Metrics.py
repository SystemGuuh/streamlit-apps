import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Sprint Metrics", page_icon="🤡", layout="wide")
st.markdown("# Current Sprint")


with st.sidebar:
    st.sidebar.header("Sprint metrics")
    uploaded_file2 = st.file_uploader("Sprint Tasks")
    uploaded_file1 = st.file_uploader("Sprint Metrics")
    if (uploaded_file1 is None) or (uploaded_file2 is None):
            st.info('Suba os arquivos na ordem certa!', icon="ℹ️")
    

if uploaded_file2 is not None:
    df2 = pd.read_csv(uploaded_file2)
    with st.sidebar:
        distinct_sprint = df2["Sprint"].unique().tolist()
        sprint_selected = st.selectbox("Sprint cicle:", distinct_sprint)

    if sprint_selected:
        df2 = df2[df2["Sprint"] == sprint_selected]
        st.write("### Dados das tarefas da Sprint ", sprint_selected)

        #calculando fim da sprint
        start_date = datetime.strptime(df2["Start Date"].unique().tolist()[0], "%d/%m/%y")
        end_date = start_date + timedelta(days=7)

        col1, col2 = st.columns(2)
        col1.text("Início da sprint: \U0001F4C5 {}".format(df2["Start Date"].unique().tolist()[0]))
        col2.text("Fim da sprint: \U0001F4C5 {}".format(end_date.strftime("%d/%m/%y")))
        
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
        

        
        df2_view = df2.drop(columns=['Sprint', 'Leadtime','Estimation Date','Estimate Leadtime','Weight to Burndown' ,'Leadtime * Weight', 'Notes/Comments'])
        df2_view.columns = ['Tarefa', 'Responsável','Prioridade','Peso','Início','Termino','Status','Dependência']
        
        if not Task:
            df2_view.drop(columns=['Tarefa'], inplace=True)

        if not Assignee:
            df2_view.drop(columns=['Responsável'], inplace=True)

        if not Priority:
            df2_view.drop(columns=['Prioridade'], inplace=True)

        if not Task_Weight:
            df2_view.drop(columns=['Peso'], inplace=True)

        if not Start_Date:
            df2_view.drop(columns=['Início'], inplace=True)

        if not End_Date:
            df2_view.drop(columns=['Termino'], inplace=True)

        if not Status:
            df2_view.drop(columns=['Status'], inplace=True)

        if not Dependence:
            df2_view.drop(columns=['Dependência'], inplace=True)

        
        st.dataframe(
            df2_view,
            hide_index=True,
        )

st.divider()

if uploaded_file1 is not None:
    df = pd.read_csv(uploaded_file1)

    if sprint_selected:
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
