CREATE TABLE IF NOT EXISTS `notes` (
    `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    `pfp` varchar(255),
    `email_confirmation` varchar(255)
)

CREATE TABLE IF NOT EXISTS `editor` (
    `id`INTERGER PRIMARY KEY,
    `email` TEXT NOT NULL,
    `filename` TEXT NOT NULL,
    `editor_data` TEXT
)

CREATE TABLE IF NOT EXISTS `use_media`(
    `id` INTERGER PRIMARY KEY,
    `email` TEXT NOT NULL,
    `email_to_use` TEXT NOT NULL,
    `status` TEXT
)
