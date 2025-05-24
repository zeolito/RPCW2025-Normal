import json
import re
from rdflib import Graph, Namespace, RDF, OWL, URIRef, Literal, XSD, RDFS

n = Namespace("http://rpcw.di.uminho.pt/2025/sapientia#")
g = Graph()

g.bind("\n", n)
g.bind("owl", OWL)
g.bind("rdf", RDF)
g.bind("rdfs", RDFS)
g.bind("xsd", XSD)

g.parse("sapientia_base.ttl")

tconSet = set()
seculo = set()
apps = set()
conceitoSet = set()

## CONCEITOS -------------------------------------------------------------------------------
with open("conceitos.json","r",encoding="UTF-8") as file:
    data = json.load(file)
for i, value in enumerate(data["conceitos"]):
    conceitoURI = URIRef(n + value["nome"].replace(" ","_"))
    g.add((conceitoURI, RDF.type, OWL.NamedIndividual))
    g.add((conceitoURI, RDF.type, n.Conceito))
    g.add((conceitoURI, n.nome, Literal(value["nome"])))

    conceitoSet.add(value["nome"])

    for app in value["aplicações"]:
        appURI = URIRef(n + app.replace(" ","_"))
        g.add((conceitoURI, n.temAplicacaoEm, appURI))

        if app not in apps:
            apps.add(app)
            g.add((appURI, RDF.type, OWL.NamedIndividual))
            g.add((appURI, RDF.type, n.Aplicacao))
            g.add((appURI, n.nome, Literal(app)))

    periodoURI = URIRef(n + value["períodoHistórico"].replace(" ","_"))
    g.add((conceitoURI, n.surgeEm, periodoURI))

    if value["períodoHistórico"] not in seculo:
        seculo.add(value["períodoHistórico"])
        g.add((periodoURI, RDF.type, OWL.NamedIndividual))
        g.add((periodoURI, RDF.type, n.PeriodoHistorico))
        g.add((periodoURI, n.nome, Literal(value["períodoHistórico"])))

    for conceitosRelacionados in value["conceitosRelacionados"]:
        conceitoRelacionadoURI = URIRef(n + conceitosRelacionados.replace(" ","_"))
        g.add((conceitoURI, n.estaRelacionadoCom, conceitoRelacionadoURI))


## DISCIPLINAS -------------------------------------------------------------------------------
with open("disciplinas.json","r",encoding="UTF-8") as file:
    data = json.load(file)
for i, value in enumerate(data["disciplinas"]):
    disciplinaURI = URIRef(n + value["nome"].replace(" ","_"))
    g.add((disciplinaURI, RDF.type, OWL.NamedIndividual))
    g.add((disciplinaURI, RDF.type, n.Disciplina))
    g.add((disciplinaURI, n.nome, Literal(value["nome"])))

    for tcon in value["tiposDeConhecimento"]:
        tconURI = URIRef(n + tcon.replace(" ","_"))
        g.add((disciplinaURI, n.pertenceA, tconURI))
        if tcon not in tconSet:
            tconSet.add(tcon)
            g.add((tconURI, RDF.type, OWL.NamedIndividual))
            g.add((tconURI, RDF.type, n.TipoDeConhecimento))
            g.add((tconURI, n.nome, Literal(tcon)))

    if "conceitos" in value:
        for conceito in value["conceitos"]:
            conceitoURI = URIRef(n + conceito.replace(" ","_"))
            g.add((conceitoURI, n.eEstudadoEm, disciplinaURI))

            if conceito not in conceitoSet:
                conceitoSet.add(conceito)
                g.add((conceitoURI, RDF.type, OWL.NamedIndividual))
                g.add((conceitoURI, RDF.type, n.Conceito))
                g.add((conceitoURI, n.nome, Literal(conceito)))


## MESTRES -------------------------------------------------------------------------------
with open("mestres.json","r",encoding="UTF-8") as file:
    data = json.load(file)
for i, value in enumerate(data["mestres"]):
    mestreURI = URIRef(n + value["nome"].replace(" ","_"))
    g.add((mestreURI, RDF.type, OWL.NamedIndividual))
    g.add((mestreURI, RDF.type, n.Mestre))
    g.add((mestreURI, n.nome, Literal(value["nome"])))

    periodoURI = URIRef(n + value["períodoHistórico"].replace(" ","_"))
    g.add((mestreURI, n.daEpoca, periodoURI))

    if value["períodoHistórico"] not in seculo:
        seculo.add(value["períodoHistórico"])
        g.add((periodoURI, RDF.type, OWL.NamedIndividual))
        g.add((periodoURI, RDF.type, n.PeriodoHistorico))
        g.add((periodoURI, n.nome, Literal(value["períodoHistórico"])))

    for disciplina in value["disciplinas"]:
        disciplinaURI = URIRef(n + disciplina.replace(" ","_"))
        g.add((mestreURI,n.ensina, disciplinaURI))

## OBRAS -------------------------------------------------------------------------------
with open("obras.json","r",encoding="UTF-8") as file:
    data = json.load(file)
for i, value in enumerate(data["obras"]):
    obraURI = URIRef(n + value["titulo"].replace(" ","_"))
    g.add((obraURI, RDF.type, OWL.NamedIndividual))
    g.add((obraURI, RDF.type, n.Obra))
    g.add((obraURI, n.titulo, Literal(value["titulo"])))

    mestreURI = URIRef(n + value["autor"].replace(" ","_"))
    g.add((obraURI, n.foiEscritoPor, mestreURI))

    if "conceitos" in value:
        for conceito in value["conceitos"]:
            conceitoURI = URIRef(n + conceito.replace(" ","_"))
            g.add((obraURI, n.explica, conceitoURI))

            if conceito not in conceitoSet:
                conceitoSet.add(conceito)
                g.add((conceitoURI, RDF.type, OWL.NamedIndividual))
                g.add((conceitoURI, RDF.type, n.Conceito))
                g.add((conceitoURI, n.nome, Literal(conceito)))

## APRENDIZ -------------------------------------------------------------------------------
with open("pg47560.json","r",encoding="UTF-8") as file:
    data = json.load(file)

for i, value in enumerate(data):
    alunoURI = URIRef(n + value["nome"].replace(" ","_"))
    g.add((alunoURI, RDF.type, OWL.NamedIndividual))
    g.add((alunoURI, RDF.type, n.Aprendiz))
    g.add((alunoURI, n.nome, Literal(value["nome"])))
    g.add((alunoURI, n.idade, Literal(value["idade"],datatype=XSD.int)))

    for disciplina in value["disciplinas"]:
        disciplina = URIRef(n + disciplina.replace(" ","_"))
        g.add((alunoURI, n.aprende, disciplina))

g.serialize(format="turtle",destination="sapientia_ind.ttl")

# QUESTÃO 24 -----------------------------------------------

query="""
PREFIX h:    <http://rpcw.di.uminho.pt/2025/sapientia#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

INSERT DATA {
  :estudaCom  a owl:ObjectProperty ;
               rdfs:domain :Aprendiz ;
               rdfs:range  :Mestre .
}
"""

g.update(query)

# QUESTÃO 25 -----------------------------------------------

construct_q = """
PREFIX h: <http://rpcw.di.uminho.pt/2025/sapientia#>

CONSTRUCT {
  ?aluno h:estudaCom ?mestre .
}
WHERE {
  ?aluno a h:Aprendiz .
  ?aluno h:aprende ?disciplina .
  ?mestre h:ensina ?disciplina .
  ?mestre a h:Mestre .
}
"""

insert_q = """
PREFIX h: <http://rpcw.di.uminho.pt/2025/sapientia#>
INSERT {
  ?aluno h:estudaCom ?mestre .
}
WHERE {
  ?aluno a h:Aprendiz .
  ?aluno h:aprende ?disciplina .
  ?mestre h:ensina ?disciplina .
  ?mestre a h:Mestre .
}
"""

qres = g.query(construct_q)
g += qres

g.update(insert_q)


# QUESTÃO 26 -----------------------------------------------

query26="""
PREFIX h:    <http://rpcw.di.uminho.pt/2025/sapientia#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

INSERT DATA {
  :dáBasesPara  a owl:ObjectProperty ;
               rdfs:domain :Disciplina ;
               rdfs:range  :Aplicacao .
}
"""
g.update(query26)

# QUESTÃO 27 -----------------------------------------------

construct_q27 = """
PREFIX h: <http://rpcw.di.uminho.pt/2025/sapientia#>
CONSTRUCT {
  ?app h:dáBasesPara ?disciplina .
}
WHERE {
  ?disciplina a h:Disciplina .
  ?c h:eEstudadoEm ?disciplina .
  ?c h:temAplicacaoEm ?app .
  ?app a h:Aplicacao .
}
"""

insert_q27 = """
PREFIX h: <http://rpcw.di.uminho.pt/2025/sapientia#>
INSERT {
  ?app h:dáBasesPara ?disciplina .
}
WHERE {
  ?disciplina a h:Disciplina .
  ?c h:eEstudadoEm ?disciplina .
  ?c h:temAplicacaoEm ?app .
  ?app a h:Aplicacao .
}
"""
qres = g.query(construct_q27)
g += qres
g.update(insert_q27)


g.serialize(format="turtle",destination="sapientia_construct.ttl")