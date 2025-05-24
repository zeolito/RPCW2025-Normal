# RPCW2025-Normal

O povoadorJSON.py é responsável por povoar a ontologia e "inserir contructs", abrindo sequencialmente cada json e abstraindo os valores para o povoamento, foi usado rdflib.
Os comentários com # QUESTÃO X na segunda metade do código indicam as queries de construção no código para cada pergunta.

Corre com: python3 povoadorJSON.py 

sapientia_base.ttl é a ontologia base antes da povoação
sapientia_ind.ttl é a ontologia depois da povoação
sapientia_construct é a ontologia com as queries de construção

sparql.txt contem as queries sparql requisitadas