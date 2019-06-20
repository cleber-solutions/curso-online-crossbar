# Curso online: Crossbar

# Componentes

## crossbar-django

Uma aplicação simples usando Django. Poderia ser qualquer framework, já
que só precisaremos criar algumas tabelas no banco de dados.

O Django é uma boa escolha porque já tem um "admin" disponível, de forma
que não precisaremos nos preocupar com a criação de uma interface para
o usuário.

## crossbar-notifier

Componente que ouve notificações geradas pelo Postgres e traduz em
mensagens enviadas via roteador WAMP.

## crossbar-tester

Pequena aplicação para linha de comando que servirá para nos ajudar
a "ver" as coisas acontecendo no sistema e efetuar alguns testes.

## router

As configurações básicas do Crossbar, nosso roteador WAMP.


# Requisitos para executar os exemplos

* Docker
* Python>=3.6
* Postgresql>=9.5
