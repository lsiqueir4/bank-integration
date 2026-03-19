# Stark Integration API

## Features:
- API Desenvolvida em Flask
- Banco de dados postgres, ORM Sqlalchemy
- Validaçao de schemas e documentaçao automatizada com Flask Smorest + Marshmellow (acesse a documentaçao em: http://13.58.112.146:5000/docs)
- API e banco de dados rodando em máquina EC2 na AWS(http://13.58.112.146:5000)
- Script de geraçao automatica de invoice utilizando Lambda + Amazon EventBridge
- Integraçao com Stark Bank feita via API utilizando requests e cryptography
- Redirecionamento de webhooks utilizando Ngrok

## Executar testes localmente:

chmod +x start.sh
./start.sh test # subir api em ambiente de testes localmente(nao utilizar a flag 'test' vai subir a api em ambiente sandbox)
 docker compose exec api_tests bash # acessar container
pytest # executar testes

## Para parar a execucao:

chmod +x stop.sh
./stop.sh

## Diagrama do banco de dados:
https://dbdiagram.io/d/69bc1876fb2db18e3bbeb7da

## TO DO:
- Processamento de webhook assincrono
- Logs e alertas para monitoramento
- Tabelas de eventos de entidades
- Autenticaçao de requests e verificaçao de assinatura dos webhooks
- Remover chave de autenticaçao da API, utilizar secret
