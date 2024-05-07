# Quantidade de projetos por estilo musical
GET_ESTILOS_POR_PROJETO = """
SELECT EM.DESCRICAO AS Estilo, COUNT(A.FK_ESTILO_PRINCIPAL) AS Quantidade
FROM T_ATRACOES A
INNER JOIN T_ESTILOS_MUSICAIS EM ON A.FK_ESTILO_PRINCIPAL = EM.ID
GROUP BY EM.DESCRICAO;
"""

# Quantidade de usuário por local
GET_USER_POR_LOCAL = """
SELECT AUD.UF AS UF, COUNT(AUD.ID) AS Quantidade 
FROM T_ADMIN_USERS_DADOS AUD 
WHERE AUD.UF IS NOT NULL AND AUD.UF != '' GROUP BY AUD.UF;
"""

# Quantidade de propostas por estilo musical
GET_ESTILOS_POR_PROPOSTA = """
SELECT Estilo, SUM(Quantidade) AS Total
FROM (
    SELECT EM.DESCRICAO AS Estilo, COUNT(O.FK_ESTILO_INTERESSE_1) AS Quantidade
    FROM T_OPORTUNIDADES O
    INNER JOIN T_ESTILOS_MUSICAIS EM ON O.FK_ESTILO_INTERESSE_1 = EM.ID
    GROUP BY EM.DESCRICAO

    UNION ALL

    SELECT EM.DESCRICAO AS Estilo, COUNT(O.FK_ESTILO_INTERESSE_2) AS Quantidade
    FROM T_OPORTUNIDADES O
    INNER JOIN T_ESTILOS_MUSICAIS EM ON O.FK_ESTILO_INTERESSE_2 = EM.ID
    GROUP BY EM.DESCRICAO

    UNION ALL

    SELECT EM.DESCRICAO AS Estilo, COUNT(O.FK_ESTILO_INTERESSE_3) AS Quantidade
    FROM T_OPORTUNIDADES O
    INNER JOIN T_ESTILOS_MUSICAIS EM ON O.FK_ESTILO_INTERESSE_3 = EM.ID
    GROUP BY EM.DESCRICAO
) AS subconsulta
GROUP BY Estilo;
"""

# Media valor bruto de oportunidade por UF
GET_CACHE_MEDIO_OPORTUNIDADES = """
SELECT O.UF AS UF, ROUND(AVG(O.VALOR_BRUTO), 2) AS Media_Valor
FROM T_OPORTUNIDADES O
WHERE O.UF IS NOT NULL AND O.UF != '' AND O.UF != 'x'
GROUP BY O.UF;
"""
