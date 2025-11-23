DROP DATABASE IF EXISTS onibusrjDB;

CREATE DATABASE onibusrjDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE onibusrjDB;

SET time_zone = '-03:00';

DROP TABLE IF EXISTS `Agencia`;
CREATE TABLE `Agencia` (
    `id_agencia` INTEGER,
    `nome` VARCHAR(32) NOT NULL,
    PRIMARY KEY (`id_agencia`)
);

DROP TABLE IF EXISTS `Rota`;
CREATE TABLE `Rota` (
    `id_rota` VARCHAR(10),
    `onibus` VARCHAR(10) NOT NULL,
    `nome` VARCHAR(50) NOT NULL,
    `modal_rota` BOOLEAN NOT NULL,
    `id_agencia` INTEGER,
    PRIMARY KEY (`id_rota`),
    CONSTRAINT `fk_rota_agencia` FOREIGN KEY (`id_agencia`) REFERENCES `Agencia` (`id_agencia`)
);

DROP TABLE IF EXISTS `Shape`;
CREATE TABLE `Shape` (
    `id_shape` VARCHAR(40) NOT NULL,
    `indice_ponto` INTEGER NOT NULL,
    `ponto_lat` DECIMAL(10, 8) NOT NULL,
    `ponto_long` DECIMAL (11, 8) NOT NULL,
    `ponto_dist` DECIMAL (10, 2),
    PRIMARY KEY (`id_shape`, `indice_ponto`)
);

DROP TABLE IF EXISTS `Parada`;
CREATE TABLE `Parada` (
    `id_parada` VARCHAR(30) NOT NULL,
    `nome` VARCHAR(100) NOT NULL,
    `lat_parada` DECIMAL(10, 8) NOT NULL,
    `long_parada` DECIMAL (11, 8) NOT NULL,
    PRIMARY KEY (`id_parada`)
);

DROP TABLE IF EXISTS `Viagem`;
CREATE TABLE `Viagem` (
    `id_viagem` CHAR(36) NOT NULL,
    `destino` VARCHAR(100) NOT NULL,
    `tipo` BOOLEAN,
    `id_rota` VARCHAR(10) NOT NULL,
    `id_shape` VARCHAR(40) NOT NULL,
    PRIMARY KEY (`id_viagem`),
    CONSTRAINT `fk_viagem_rota` FOREIGN KEY (`id_rota`) REFERENCES Rota (`id_rota`),
    CONSTRAINT `fk_viagem_shape` FOREIGN KEY (`id_shape`) REFERENCES Shape (`id_shape`)
);

DROP TABLE IF EXISTS `Passa_por`;
CREATE TABLE `Passa_por` (
    `horario_saida` TIME,
    `horario_entrada` TIME,
    `indice_parada` INTEGER NOT NULL, 
    `id_viagem` CHAR(36) NOT NULL,
    `id_parada` varchar(30) NOT NULL,
    CONSTRAINT `pk_passa_por` PRIMARY KEY (`id_viagem`, `indice_parada`),
    CONSTRAINT `fk_passapor_viagem` FOREIGN KEY (`id_viagem`) REFERENCES Viagem (`id_viagem`),
    CONSTRAINT `fk_passapor_parada` FOREIGN KEY (`id_parada`) REFERENCES Parada (`id_parada`)
);
