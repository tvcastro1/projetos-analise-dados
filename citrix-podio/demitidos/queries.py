# Queries

QUERY_TABLETS = """SELECT
    app_item_id,  
    imei,
    [patrimonio-novo],
    modeloDesc,
    serie,
    [tipo-de-dispositivoDesc],
    [nome-colaborador],
    [sistema-utilizadoDesc],
    statusDesc,
    last_event_on
FROM
    [Podio].[ListarTabletsNovos] a
WHERE
    [last_event_on] = (
        SELECT
        MAX(last_event_on)
        FROM
        [Podio].[ListarTabletsNovos]
        WHERE
        app_item_id = a.app_item_id
    )
ORDER BY
    [nome-colaborador] ASC"""