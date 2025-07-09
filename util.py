def extrair_membros(grupo, estadosAntigos):
    return grupo.split('_')

def agruparEstadosComuns(lista_de_listas):
    grupos = []

    for sublista in lista_de_listas:
        sublista_set = set(sublista)
        grupo_atual = []

        for grupo in grupos:
            if sublista_set & grupo:  # interseção não vazia
                sublista_set |= grupo  # união
            else:
                grupo_atual.append(grupo)

        grupo_atual.append(sublista_set)
        grupos = grupo_atual

    # Converter para listas ordenadas
    return [sorted(list(grupo)) for grupo in grupos]