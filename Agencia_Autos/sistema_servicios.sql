-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 25-04-2026 a las 03:49:24
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `sistema_servicios`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administradores`
--

CREATE TABLE `administradores` (
  `id` int(11) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `administradores`
--

INSERT INTO `administradores` (`id`, `usuario`, `contrasena`, `nombre`, `created_at`) VALUES
(1, 'admin', 'admin123', 'Administrador', '2026-04-23 22:42:08');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `anos`
--

CREATE TABLE `anos` (
  `id` int(11) NOT NULL,
  `año` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `anos`
--

INSERT INTO `anos` (`id`, `año`) VALUES
(15, 2015),
(14, 2016),
(13, 2017),
(12, 2018),
(11, 2019),
(1, 2020),
(2, 2021),
(3, 2022),
(7, 2023),
(6, 2024),
(5, 2025),
(4, 2026);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id`, `nombre`, `telefono`, `direccion`, `created_at`) VALUES
(1, 'Juan Pérez', '8441234567', 'Zona centro', '2026-04-23 22:50:22'),
(2, 'María López', '8449876543', 'arteaga', '2026-04-23 22:50:22'),
(3, 'Dulce', '8443692321', 'fghjkilokiujhyg', '2026-04-23 23:01:15'),
(4, 'Ramiro', '3456789', 'carlos pacheco', '2026-04-23 23:09:25'),
(5, 'Alberto', '456789', 'dfghj', '2026-04-23 23:20:34');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `marcas`
--

CREATE TABLE `marcas` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `marcas`
--

INSERT INTO `marcas` (`id`, `nombre`, `created_at`) VALUES
(1, 'Toyota', '2026-04-23 22:51:31'),
(2, 'Nissan', '2026-04-23 22:51:31'),
(3, 'Ford', '2026-04-23 22:51:31'),
(4, 'Toyota', '2026-04-23 22:58:11'),
(5, 'Nissan', '2026-04-23 22:58:11'),
(6, 'Ford', '2026-04-23 22:58:11'),
(7, 'Nissan', '2026-04-23 22:59:50'),
(8, 'Toyota', '2026-04-23 22:59:50'),
(9, 'Honda', '2026-04-23 22:59:50'),
(10, 'Ford', '2026-04-23 22:59:50'),
(11, 'Mazda', '2026-04-23 22:59:50'),
(12, 'Nissan', '2026-04-23 23:28:58'),
(13, 'Toyota', '2026-04-23 23:28:58'),
(14, 'Honda', '2026-04-23 23:28:58'),
(15, 'Ford', '2026-04-23 23:28:58'),
(16, 'Mazda', '2026-04-23 23:28:58');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modelos`
--

CREATE TABLE `modelos` (
  `id` int(11) NOT NULL,
  `marca_id` int(11) DEFAULT NULL,
  `nombre` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `modelos`
--

INSERT INTO `modelos` (`id`, `marca_id`, `nombre`, `created_at`) VALUES
(19, 1, 'Corolla', '2026-04-23 22:58:11'),
(20, 2, 'Sentra', '2026-04-23 22:58:11'),
(21, 3, 'Mustang', '2026-04-23 22:58:11'),
(22, 2, 'Versa', '2026-04-23 22:59:50'),
(23, 1, 'Hilux', '2026-04-23 22:59:50'),
(24, 9, 'Civic', '2026-04-23 22:59:50'),
(25, 9, 'Accord', '2026-04-23 22:59:50'),
(26, 3, 'Focus', '2026-04-23 22:59:50'),
(27, 3, 'Ranger', '2026-04-23 22:59:50'),
(28, 11, 'Mazda 3', '2026-04-23 22:59:50');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `refacciones`
--

CREATE TABLE `refacciones` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `stock` int(11) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `refacciones`
--

INSERT INTO `refacciones` (`id`, `nombre`, `precio`, `stock`, `created_at`) VALUES
(1, 'Filtro de aceite', 180.00, 11, '2026-04-17 22:25:40'),
(2, 'Balatas', 950.00, 8, '2026-04-17 22:25:40'),
(3, 'Bujías', 420.00, 18, '2026-04-17 22:25:40'),
(4, 'Aceite', 150.00, 0, '2026-04-17 23:07:44');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fallos`
--

CREATE TABLE `fallos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `costo` decimal(10,2) NOT NULL DEFAULT 0.00,
  `descripcion` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `fallos`
--

INSERT INTO `fallos` (`id`, `nombre`, `costo`, `descripcion`, `created_at`) VALUES
(1, 'Fuga de aceite', 350.00, 'Revisión de empaques, retenes y nivelación', '2026-05-25 00:00:00'),
(2, 'Sistema de frenos desgastado', 480.00, 'Inspección de balatas, discos y líquido', '2026-05-25 00:00:00'),
(3, 'Batería descargada', 220.00, 'Diagnóstico del sistema eléctrico', '2026-05-25 00:00:00'),
(4, 'Sobrecalentamiento', 520.00, 'Revisión de radiador, bomba de agua y anticongelante', '2026-05-25 00:00:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios`
--

CREATE TABLE `servicios` (
  `id` int(11) NOT NULL,
  `folio` varchar(20) NOT NULL,
  `vehiculo_id` int(11) DEFAULT NULL,
  `cliente_id` int(11) DEFAULT NULL,
  `fecha_registro` date DEFAULT NULL,
  `fecha_proximo_servicio` date DEFAULT NULL,
  `estatus` enum('En espera','En proceso','Finalizado') DEFAULT 'En espera',
  `quien_llevo` varchar(100) NOT NULL,
  `observaciones` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `servicios`
--

INSERT INTO `servicios` (`id`, `folio`, `vehiculo_id`, `cliente_id`, `fecha_registro`, `fecha_proximo_servicio`, `estatus`, `quien_llevo`, `observaciones`, `created_at`) VALUES
(1, 'SERV-20260423170115', 3, 3, '2026-04-23', '2026-04-30', 'En proceso', 'DULCE', 'TIRA ACEITE', '2026-04-23 23:01:15'),
(2, 'SERV-20260423170925', 4, 4, '2026-04-23', '2026-05-07', 'En espera', 'Roberto', 'Fuga de agua', '2026-04-23 23:09:25'),
(4, 'SERV-20260423172035', 5, 5, '2026-04-23', '2026-04-29', 'Finalizado', 'CHUY', '', '2026-04-23 23:20:35');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicio_refaccion`
--

CREATE TABLE `servicio_refaccion` (
  `id` int(11) NOT NULL,
  `servicio_id` int(11) DEFAULT NULL,
  `refaccion_id` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicio_refacciones`
--

CREATE TABLE `servicio_refacciones` (
  `id` int(11) NOT NULL,
  `servicio_folio` varchar(30) NOT NULL,
  `refaccion_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicio_fallos`
--

CREATE TABLE `servicio_fallos` (
  `id` int(11) NOT NULL,
  `servicio_folio` varchar(30) NOT NULL,
  `fallo_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE `servicio_fallos`
  ADD CONSTRAINT `servicio_fallos_ibfk_1` FOREIGN KEY (`servicio_folio`) REFERENCES `servicios` (`folio`) ON DELETE CASCADE,
  ADD CONSTRAINT `servicio_fallos_ibfk_2` FOREIGN KEY (`fallo_id`) REFERENCES `fallos` (`id`);

--
-- Volcado de datos para la tabla `servicio_refacciones`
--

INSERT INTO `servicio_refacciones` (`id`, `servicio_folio`, `refaccion_id`, `cantidad`) VALUES
(1, 'SERV-20260423170115', 3, 1),
(2, 'SERV-20260423170115', 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vehiculos`
--

CREATE TABLE `vehiculos` (
  `id` int(11) NOT NULL,
  `cliente_id` int(11) DEFAULT NULL,
  `marca_id` int(11) DEFAULT NULL,
  `modelo_id` int(11) DEFAULT NULL,
  `año_id` int(11) DEFAULT NULL,
  `placas` varchar(20) DEFAULT NULL,
  `color` varchar(30) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `vehiculos`
--

INSERT INTO `vehiculos` (`id`, `cliente_id`, `marca_id`, `modelo_id`, `año_id`, `placas`, `color`, `created_at`) VALUES
(3, 3, 5, 28, 2, '76543ERFT', 'rojo', '2026-04-23 23:01:15'),
(4, 4, 9, 24, 3, 'RTYU678', 'azul', '2026-04-23 23:09:25'),
(5, 5, 8, 19, 11, 'DFGHBJNKL6789', 'verde', '2026-04-23 23:20:34');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administradores`
--
ALTER TABLE `administradores`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario` (`usuario`);

--
-- Indices de la tabla `anos`
--
ALTER TABLE `anos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `año` (`año`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `marcas`
--
ALTER TABLE `marcas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `modelos`
--
ALTER TABLE `modelos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `marca_id` (`marca_id`);

--
-- Indices de la tabla `refacciones`
--
ALTER TABLE `refacciones`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `servicios`
--
ALTER TABLE `servicios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `folio` (`folio`),
  ADD KEY `vehiculo_id` (`vehiculo_id`),
  ADD KEY `cliente_id` (`cliente_id`);

--
-- Indices de la tabla `servicio_refaccion`
--
ALTER TABLE `servicio_refaccion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `servicio_id` (`servicio_id`),
  ADD KEY `refaccion_id` (`refaccion_id`);

--
-- Indices de la tabla `servicio_refacciones`
--
ALTER TABLE `servicio_refacciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `servicio_folio` (`servicio_folio`),
  ADD KEY `refaccion_id` (`refaccion_id`);

--
-- Indices de la tabla `vehiculos`
--
ALTER TABLE `vehiculos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `placas` (`placas`),
  ADD KEY `cliente_id` (`cliente_id`),
  ADD KEY `marca_id` (`marca_id`),
  ADD KEY `modelo_id` (`modelo_id`),
  ADD KEY `año_id` (`año_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `administradores`
--
ALTER TABLE `administradores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `anos`
--
ALTER TABLE `anos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `marcas`
--
ALTER TABLE `marcas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `modelos`
--
ALTER TABLE `modelos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT de la tabla `refacciones`
--
ALTER TABLE `refacciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `servicios`
--
ALTER TABLE `servicios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `servicio_refaccion`
--
ALTER TABLE `servicio_refaccion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `servicio_refacciones`
--
ALTER TABLE `servicio_refacciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `vehiculos`
--
ALTER TABLE `vehiculos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `modelos`
--
ALTER TABLE `modelos`
  ADD CONSTRAINT `modelos_ibfk_1` FOREIGN KEY (`marca_id`) REFERENCES `marcas` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `servicios`
--
ALTER TABLE `servicios`
  ADD CONSTRAINT `servicios_ibfk_1` FOREIGN KEY (`vehiculo_id`) REFERENCES `vehiculos` (`id`),
  ADD CONSTRAINT `servicios_ibfk_2` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`);

--
-- Filtros para la tabla `servicio_refaccion`
--
ALTER TABLE `servicio_refaccion`
  ADD CONSTRAINT `servicio_refaccion_ibfk_1` FOREIGN KEY (`servicio_id`) REFERENCES `servicios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `servicio_refaccion_ibfk_2` FOREIGN KEY (`refaccion_id`) REFERENCES `refacciones` (`id`);

--
-- Filtros para la tabla `servicio_refacciones`
--
ALTER TABLE `servicio_refacciones`
  ADD CONSTRAINT `servicio_refacciones_ibfk_1` FOREIGN KEY (`servicio_folio`) REFERENCES `servicios` (`folio`) ON DELETE CASCADE,
  ADD CONSTRAINT `servicio_refacciones_ibfk_2` FOREIGN KEY (`refaccion_id`) REFERENCES `refacciones` (`id`);

--
-- Filtros para la tabla `vehiculos`
--
ALTER TABLE `vehiculos`
  ADD CONSTRAINT `vehiculos_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`),
  ADD CONSTRAINT `vehiculos_ibfk_2` FOREIGN KEY (`marca_id`) REFERENCES `marcas` (`id`),
  ADD CONSTRAINT `vehiculos_ibfk_3` FOREIGN KEY (`modelo_id`) REFERENCES `modelos` (`id`),
  ADD CONSTRAINT `vehiculos_ibfk_4` FOREIGN KEY (`año_id`) REFERENCES `anos` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
