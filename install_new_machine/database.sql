CREATE DATABASE IF NOT EXISTS estoque;


CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL
                );


CREATE TABLE IF NOT EXISTS produto (
    id int NOT NULL,
    nome VARCHAR(255) NOT NULL,        -- Nome do produto
    quantidade INT NOT NULL,           -- Quantidade disponível no estoque
    quant_minima INT NOT NULL,         -- Quantidade mínima para reabastecimento
    preco FLOAT NOT NULL,              -- Preço do produto
    validade DATETIME NOT NULL,        -- Data e hora de validade do produto
    PRIMARY KEY (id)                 -- Define a coluna `nome` como chave primária
);

