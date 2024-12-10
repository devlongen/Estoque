-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 10/12/2024 às 23:33
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `estoque`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `produtos`
--

CREATE TABLE `produtos` (
  `id` int(11) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `quantidade` int(11) NOT NULL,
  `quant_minima` int(11) NOT NULL,
  `preco` float NOT NULL,
  `validade` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `produtos`
--

INSERT INTO `produtos` (`id`, `nome`, `quantidade`, `quant_minima`, `preco`, `validade`) VALUES
(4, 'queijo', 50, 20, 50, '2024-12-02 00:00:00'),
(5, 'maça', 150, 50, 5, '2024-12-17 00:00:00'),
(6, 'banana', 200, 70, 15, '2024-12-02 00:00:00'),
(7, 'manteiga', 200, 20, 15, '2024-12-24 00:00:00'),
(8, 'pessego', 100, 50, 10, '2024-12-31 00:00:00'),
(9, 'amendoim', 300, 40, 2, '2024-12-25 00:00:00'),
(10, 'Abacate', 100, 20, 30, '2024-12-24 00:00:00'),
(11, 'Abacaxi', 100, 50, 20, '2024-12-25 00:00:00'),
(12, 'Açaí', 300, 30, 20, '2024-12-30 00:00:00'),
(13, 'Acerola', 90, 10, 5, '2024-12-25 00:00:00');

-- --------------------------------------------------------

--
-- Estrutura para tabela `saida`
--

CREATE TABLE `saida` (
  `id` int(11) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `quantidadeSaida` int(11) NOT NULL,
  `valorEntrada` decimal(10,2) NOT NULL,
  `valorSaida` decimal(10,2) NOT NULL,
  `lucro` decimal(10,2) NOT NULL,
  `validade` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `saida`
--

INSERT INTO `saida` (`id`, `nome`, `quantidadeSaida`, `valorEntrada`, `valorSaida`, `lucro`, `validade`) VALUES
(1, 'queijo', 50, 20.00, 50.00, 50.00, '2024-12-10 00:00:00');

-- --------------------------------------------------------

--
-- Estrutura para tabela `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `users`
--

INSERT INTO `users` (`id`, `nome`, `email`, `username`, `password`) VALUES
(1, 'UserIago', '12345678@gmail.com', 'iago', '12345678'),
(2, 'Alisson Vargas', 'alissonvargas@gmail.com', 'alissonv', 'Esqueçatudo1#');

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `produtos`
--
ALTER TABLE `produtos`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `saida`
--
ALTER TABLE `saida`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `produtos`
--
ALTER TABLE `produtos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de tabela `saida`
--
ALTER TABLE `saida`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
