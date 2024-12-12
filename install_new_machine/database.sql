
CREATE DATABASE IF NOT EXISTS estoque;
USE estoque;
CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL,
                    email varchar(255) NOT NULL,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    flag_admin boolean null 
);


CREATE TABLE IF NOT EXISTS produtos (
    id int AUTO_INCREMENT NOT NULL,
    nome VARCHAR(255) NOT NULL,        -- Nome do produto
    quantidade INT NOT NULL,           -- Quantidade disponível no estoque
    quant_minima INT NOT NULL,         -- Quantidade mínima para reabastecimento
    preco FLOAT NOT NULL,              -- Preço do produto
    validade DATETIME NOT NULL,        -- Data e hora de validade do produto
    PRIMARY KEY (id)                 -- Define a coluna `nome` como chave primária
);

CREATE TABLE IF NOT EXISTS saida (
    id INT AUTO_INCREMENT PRIMARY KEY,     -- id será auto incremento
    nome VARCHAR(255) NOT NULL,            -- Nome do produto ou item
    quantidadeSaida INT NOT NULL,          -- Quantidade de saída do produto
    valorEntrada DECIMAL(10, 2) NOT NULL,  -- Valor de entrada (custo de aquisição)
    valorSaida DECIMAL(10, 2) NOT NULL,    -- Valor de saída (preço de venda)
    lucro DECIMAL(10, 2) NOT NULL,         -- Lucro calculado (valorSaida - valorEntrada)
    validade DATETIME NOT NULL             -- Data e hora de validade
);

INSERT INTO users (nome, email, username, password, flag_admin) 
VALUES ('Admin User', 'admin@example.com', 'admin', 'senha123', 1);

