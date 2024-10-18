CREATE DATABASE IF NOT EXISTS league_data;
USE league_data;

CREATE TABLE IF NOT EXISTS players (
    id INT AUTO_INCREMENT PRIMARY KEY,
    game_name VARCHAR(50) NOT NULL,
    tag_line VARCHAR(10) NOT NULL,
    riot_id VARCHAR(100) NOT NULL,
    puuid VARCHAR(78) UNIQUE NOT NULL,
    region VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS matches (
    match_id VARCHAR(50) PRIMARY KEY,
    puuid VARCHAR(78),
    game_duration INT,
    game_creation BIGINT,
    game_mode VARCHAR(50),
    champion_id INT,
    kills INT,
    deaths INT,
    assists INT,
    win BOOLEAN,
    FOREIGN KEY (puuid) REFERENCES players(puuid) ON DELETE CASCADE
);