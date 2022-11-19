CREATE TABLE IF NOT EXISTS `notes` (
    `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    `pfp` varchar(255),
    `email_confirmation` varchar(255)
)

CREATE TABLE IF NOT EXISTS `editor` (
    `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` varchar(255) NOT NULL,
    `editor_data` varchar(max)
)