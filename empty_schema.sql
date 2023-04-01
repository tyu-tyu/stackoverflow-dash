-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.10.2-MariaDB-1:10.10.2+maria~ubu2204 - mariadb.org binary distribution
-- Server OS:                    debian-linux-gnu
-- HeidiSQL Version:             11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for dashboard_data
CREATE DATABASE IF NOT EXISTS `dashboard_data` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `dashboard_data`;

-- Dumping structure for table dashboard_data.answer
CREATE TABLE IF NOT EXISTS `answer` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `question_id` bigint(20) NOT NULL,
  `creation_date` date DEFAULT NULL,
  `score` int(11) NOT NULL DEFAULT 0,
  `sentiment` decimal(7,3) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `sentiment` (`sentiment`),
  KEY `answer_question_id` (`question_id`),
  KEY `answer_score` (`score`),
  KEY `FK_answer_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=72469192 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table dashboard_data.badges
CREATE TABLE IF NOT EXISTS `badges` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `badge_name` varchar(255) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `badge_name` (`badge_name`)
) ENGINE=InnoDB AUTO_INCREMENT=415 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table dashboard_data.badge_link
CREATE TABLE IF NOT EXISTS `badge_link` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL DEFAULT 0,
  `badge_id` varchar(256) NOT NULL DEFAULT '0',
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `badge_link_badge_id` (`badge_id`),
  KEY `FK_badge_link_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=134025 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table dashboard_data.comments
CREATE TABLE IF NOT EXISTS `comments` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `post_id` bigint(20) DEFAULT NULL,
  `score` int(11) DEFAULT 0,
  `sentiment` decimal(7,3) DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sentiment` (`sentiment`),
  KEY `comments` (`score`),
  KEY `comments_post` (`post_id`),
  KEY `FK_comments_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=128020272 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table dashboard_data.keyword
CREATE TABLE IF NOT EXISTS `keyword` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `keyword` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `keyword` (`keyword`)
) ENGINE=InnoDB AUTO_INCREMENT=462024 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table dashboard_data.keyword_link
CREATE TABLE IF NOT EXISTS `keyword_link` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `post_id` bigint(20) DEFAULT 0,
  `comment_id` bigint(20) DEFAULT 0,
  `user_id` bigint(20) DEFAULT NULL,
  `keyword_id` varchar(256) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `FK_keyword_link_keywords` (`keyword_id`) USING BTREE,
  KEY `keyword_link_post_id` (`post_id`),
  KEY `keyword_link_comment_id` (`comment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3604426 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table dashboard_data.question
CREATE TABLE IF NOT EXISTS `question` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `creation_date` date DEFAULT NULL,
  `score` int(11) NOT NULL DEFAULT 0,
  `view_count` int(11) NOT NULL DEFAULT 0,
  `title` text NOT NULL,
  `sentiment` decimal(7,3) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT 0,
  `accepted_answer_id` bigint(20) DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `creation_date` (`creation_date`),
  KEY `question_accepted_answer` (`accepted_answer_id`),
  KEY `sentiment` (`sentiment`) USING BTREE,
  KEY `question_score` (`score`),
  KEY `FK_question_user` (`user_id`),
  KEY `question_view_count` (`view_count`)
) ENGINE=InnoDB AUTO_INCREMENT=72469195 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table dashboard_data.tag
CREATE TABLE IF NOT EXISTS `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag` (`tag`)
) ENGINE=InnoDB AUTO_INCREMENT=158879 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table dashboard_data.tag_link
CREATE TABLE IF NOT EXISTS `tag_link` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `post_id` bigint(20) NOT NULL DEFAULT 0,
  `tag_id` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `tag_link_tag_id` (`tag_id`),
  KEY `FK_tag_link_question` (`post_id`)
) ENGINE=InnoDB AUTO_INCREMENT=451897 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table dashboard_data.user
CREATE TABLE IF NOT EXISTS `user` (
  `id` bigint(20) NOT NULL,
  `reputation` int(11) DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  `location` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_creation_date` (`creation_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- Data exporting was unselected.

-- Dumping structure for procedure dashboard_data.get_filtered_question_count
DELIMITER //
CREATE PROCEDURE `get_filtered_question_count`(
	IN `date_start` DATE,
	IN `date_end` DATE,
	IN `tag_list` VARCHAR(512)
)
BEGIN
  	DECLARE date_range VARCHAR(50);
  	DECLARE tag_list_len INT;
  	SET date_range = CONCAT("'", date_start, "' AND '", date_end, "'");
  	SET @sql = '
	SELECT COUNT(DISTINCT q.id) AS question_count FROM question AS q
		INNER JOIN tag_link AS tl ON tl.post_id = q.id';

	IF date_start IS NOT NULL AND date_end IS NOT NULL THEN
		SET @sql = CONCAT(@sql, ' WHERE (q.creation_date BETWEEN ', date_range, ')');
	ELSEIF date_start IS NOT NULL AND date_end IS NULL THEN
		SET @sql = CONCAT(@sql, ' WHERE (q.creation_date > "', date_start,'")');
	ELSEIF date_start IS NULL AND date_end IS NOT NULL THEN
		SET @SQL = CONCAT(@SQL, ' WHERE (q.creation_date < "', date_end, '")');
	ELSE
		SET @SQL = CONCAT(@SQL, ' WHERE (1 = 1)');
	END IF;
  	IF tag_list != '' THEN
  		SET tag_list_len = LENGTH(tag_list) - LENGTH(REPLACE(tag_list, ',', '')) + 1;
   	SET @sql = CONCAT(@sql, ' AND (q.id IN (SELECT post_id FROM tag_link WHERE tag_id IN(', tag_list, ') GROUP BY post_id HAVING COUNT(DISTINCT tag_id) >=', tag_list_len ,'))');
  	END IF;

  	PREPARE stmt FROM @sql;
  	EXECUTE stmt;
  	DEALLOCATE PREPARE stmt;
END//
DELIMITER ;

-- Dumping structure for procedure dashboard_data.get_filtered_question_details
DELIMITER //
CREATE PROCEDURE `get_filtered_question_details`(
	IN `date_start` DATE,
	IN `date_end` DATE,
	IN `tag_list` VARCHAR(512)
)
BEGIN
  	DECLARE date_range VARCHAR(50);
  	DECLARE tag_list_len INT;
  	SET date_range = CONCAT("'", date_start, "' AND '", date_end, "'");
  	SET @SQL = '(SELECT COUNT(DISTINCT q.id) FROM question AS q
		INNER JOIN tag_link AS tl ON tl.post_id = q.id';
	IF date_start IS NOT NULL AND date_end IS NOT NULL THEN
		SET @sql = CONCAT(@sql, ' WHERE (q.creation_date BETWEEN ', date_range, ')');
	ELSEIF date_start IS NOT NULL AND date_end IS NULL THEN
		SET @sql = CONCAT(@sql, ' WHERE (q.creation_date > "', date_start,'")');
	ELSEIF date_start IS NULL AND date_end IS NOT NULL THEN
		SET @SQL = CONCAT(@SQL, ' WHERE (q.creation_date < "', date_end, '")');
	ELSE
		SET @SQL = CONCAT(@SQL, ' WHERE (1 = 1)');
	END IF;
  	IF tag_list != '' THEN
  		SET tag_list_len = LENGTH(tag_list) - LENGTH(REPLACE(tag_list, ',', '')) + 1;
   	SET @sql = CONCAT(@sql, ' AND (tl.post_id IN (SELECT post_id FROM tag_link WHERE tag_id IN(', tag_list, ') GROUP BY post_id HAVING COUNT(DISTINCT tag_id) >=', tag_list_len ,'))');
  	END IF;

  	SET @sql = CONCAT(@sql, ' AND NOT EXISTS (SELECT NULL FROM answer WHERE answer.question_id = q.id)
		)
		UNION ALL 
		(
			SELECT COUNT(DISTINCT q.id) FROM question AS q
			INNER JOIN tag_link AS tl ON tl.post_id = q.id'
	);
	IF date_start IS NOT NULL AND date_end IS NOT NULL THEN
		SET @sql = CONCAT(@sql, ' WHERE (q.creation_date BETWEEN ', date_range, ')');
	ELSEIF date_start IS NOT NULL AND date_end IS NULL THEN
		SET @sql = CONCAT(@sql, ' WHERE (q.creation_date > "', date_start,'")');
	ELSEIF date_start IS NULL AND date_end IS NOT NULL THEN
		SET @SQL = CONCAT(@SQL, ' WHERE (q.creation_date < "', date_end, '")');
	ELSE
		SET @SQL = CONCAT(@SQL, ' WHERE (1 = 1)');
	END IF;
  	IF tag_list != '' THEN
   	SET @sql = CONCAT(@sql, ' AND (tl.post_id IN (SELECT post_id FROM tag_link WHERE tag_id IN(', tag_list, ') GROUP BY post_id HAVING COUNT(DISTINCT tag_id) >=', tag_list_len ,'))');
  	END IF;
  	SET @SQL = CONCAT(@SQL, ' AND q.accepted_answer_id IS NOT NULL);');
  	
  	PREPARE stmt FROM @sql;
  	EXECUTE stmt;
  	DEALLOCATE PREPARE stmt;
END//
DELIMITER ;

-- Dumping structure for procedure dashboard_data.get_filtered_tags
DELIMITER //
CREATE PROCEDURE `get_filtered_tags`(
	IN `date_start` DATE,
	IN `date_end` DATE,
	IN `tag_list` VARCHAR(512)
)
BEGIN
  	DECLARE date_range VARCHAR(50);
  	DECLARE tag_list_len INT;
  	SET date_range = CONCAT("'", date_start, "' AND '", date_end, "'");
  	SET @sql = '
	SELECT 
      t.tag, 
      COUNT(DISTINCT q.id) AS question_count,
      COUNT(DISTINCT a.id) AS answer_count,
      COUNT(DISTINCT c.id) + COUNT(DISTINCT d.id) AS comment_count,
      CAST((SUM(q.score) + SUM(a.score) + SUM(c.score) + SUM(d.score)) AS VARCHAR(10)) AS total_score,
      CAST((SUM(q.view_count)) AS INT) AS view_count,
      CAST((AVG(q.sentiment) + AVG(a.sentiment) + AVG(c.sentiment) + AVG(d.sentiment)) / 4 AS VARCHAR(6)) AS sentiment,
      CONCAT(''<a href="https://stackoverflow.com/tags/'', t.tag, ''/info" target="_blank" rel="noopener noreferrer"><i class="text-blue fa-solid fa-link"></i></a>'') AS link
   FROM question AS q
   INNER JOIN tag_link as tl ON tl.post_id = q.id
   INNER JOIN tag AS t ON t.id = tl.tag_id
   LEFT JOIN answer AS a ON a.question_id = q.id
   LEFT JOIN comments AS c ON c.post_id = q.id 
   LEFT JOIN comments AS d ON d.post_id = a.id';

	IF date_start IS NOT NULL AND date_end IS NOT NULL THEN
		SET @sql = CONCAT(@sql, ' WHERE (q.creation_date BETWEEN ', date_range, ')');
	ELSEIF date_start IS NOT NULL AND date_end IS NULL THEN
		SET @sql = CONCAT(@sql, ' WHERE (q.creation_date > "', date_start,'")');
	ELSEIF date_start IS NULL AND date_end IS NOT NULL THEN
		SET @SQL = CONCAT(@SQL, ' WHERE (q.creation_date < "', date_end, '")');
	ELSE
		SET @SQL = CONCAT(@SQL, ' WHERE (1 = 1)');
	END IF;
  	IF tag_list != '' THEN
  		SET tag_list_len = LENGTH(tag_list) - LENGTH(REPLACE(tag_list, ',', '')) + 1;
   	SET @sql = CONCAT(@sql, ' AND (tl.post_id IN (SELECT post_id FROM tag_link WHERE tag_id IN(', tag_list, ') GROUP BY post_id HAVING COUNT(DISTINCT tag_id) >=', tag_list_len ,'))');
	END IF;
	SET @sql = CONCAT(@sql, ' GROUP BY t.id ORDER BY question_count DESC LIMIT 250;');
  	PREPARE stmt FROM @sql;
  	EXECUTE stmt;
  	DEALLOCATE PREPARE stmt;
END//
DELIMITER ;

-- Dumping structure for procedure dashboard_data.get_filtered_top_badges
DELIMITER //
CREATE PROCEDURE `get_filtered_top_badges`(
	IN `date_start` DATE,
	IN `date_end` DATE,
	IN `tag_list` VARCHAR(512)
)
BEGIN
	DECLARE date_range VARCHAR(50);
  	DECLARE tag_list_len INT;
  	SET date_range = CONCAT("'", date_start, "' AND '", date_end, "'");
  	SET @sql = '
	SELECT b.badge_name, COUNT(DISTINCT bl.user_id) AS badge_count FROM badge_link AS bl
	INNER JOIN badges AS b ON b.id = bl.badge_id
	INNER JOIN user AS u ON u.id = bl.user_id
	LEFT JOIN question AS q ON q.user_id = u.id
	LEFT JOIN tag_link AS tl ON tl.post_id = q.id';

	IF date_start IS NOT NULL AND date_end IS NOT NULL THEN
		SET @sql = CONCAT(@sql, ' WHERE (q.creation_date BETWEEN ', date_range, ')');
	ELSEIF date_start IS NOT NULL AND date_end IS NULL THEN
		SET @sql = CONCAT(@sql, ' WHERE (q.creation_date > "', date_start,'")');
	ELSEIF date_start IS NULL AND date_end IS NOT NULL THEN
		SET @SQL = CONCAT(@SQL, ' WHERE (q.creation_date < "', date_end, '")');
	ELSE
		SET @SQL = CONCAT(@SQL, ' WHERE (1 = 1)');
	END IF;
  	IF tag_list != '' THEN
  		SET tag_list_len = LENGTH(tag_list) - LENGTH(REPLACE(tag_list, ',', '')) + 1;
   	SET @sql = CONCAT(@sql, ' AND (tl.post_id IN (SELECT post_id FROM tag_link WHERE tag_id IN(', tag_list, ') GROUP BY post_id HAVING COUNT(DISTINCT tag_id) >=', tag_list_len ,'))');
	END IF;
	SET @sql = CONCAT(@SQL, ' GROUP BY b.id ORDER BY badge_count DESC');
  	PREPARE stmt FROM @sql;
  	EXECUTE stmt;
  	DEALLOCATE PREPARE stmt;
END//
DELIMITER ;

-- Dumping structure for procedure dashboard_data.get_index_date_range
DELIMITER //
CREATE PROCEDURE `get_index_date_range`()
BEGIN
	(SELECT DATE_FORMAT(creation_date, "%d/%m/%Y") FROM question ORDER BY creation_date ASC LIMIT 1) UNION ALL 
	(SELECT DATE_FORMAT(creation_date, "%d/%m/%Y") FROM question ORDER BY creation_date DESC LIMIT 1) UNION ALL
	(SELECT DATE_FORMAT(creation_date, "%Y-%m-%d") FROM question ORDER BY creation_date ASC LIMIT 1) UNION ALL
	(SELECT DATE_FORMAT(creation_date, "%Y-%m-%d") FROM question ORDER BY creation_date DESC LIMIT 1);
END//
DELIMITER ;

-- Dumping structure for procedure dashboard_data.get_index_question_details
DELIMITER //
CREATE PROCEDURE `get_index_question_details`()
BEGIN
	(SELECT COUNT(*) FROM question WHERE NOT EXISTS (SELECT NULL FROM answer WHERE answer.question_id = question.id)) UNION ALL (SELECT COUNT(*) FROM question WHERE accepted_answer_id IS NOT NULL);
END//
DELIMITER ;

-- Dumping structure for procedure dashboard_data.get_location_scores
DELIMITER //
CREATE PROCEDURE `get_location_scores`(
	IN `date_start` DATE,
	IN `date_end` DATE,
	IN `tag_list` VARCHAR(512)
)
BEGIN
  	DECLARE date_range VARCHAR(50);
  	DECLARE tag_list_len INT;
  	SET date_range = CONCAT("'", date_start, "' AND '", date_end, "'");
  	SET @SQL = '
		SELECT u.location,
		COUNT(DISTINCT q.id) + COUNT(DISTINCT a.id) + COUNT(DISTINCT c.id) + COUNT(DISTINCT d.id) AS count,
		AVG(u.reputation) AS avg_rep,
		SUM(u.reputation) AS total_rep,
		COUNT(DISTINCT q.id) AS question_count,
		COUNT(DISTINCT a.id) AS answer_count,
		COUNT(DISTINCT c.id) + COUNT(DISTINCT d.id) AS comment_count,
		DATE_FORMAT(CAST(FROM_UNIXTIME(AVG(UNIX_TIMESTAMP(u.creation_date))) AS DATE),"%d/%m/%Y") AS avg_acc_age
		FROM user AS u
		INNER JOIN question AS q ON q.user_id = u.id
		LEFT JOIN answer AS a ON a.question_id = q.id
		LEFT JOIN comments AS c ON (c.post_id = q.id)
		LEFT JOIN comments AS d ON (d.post_id = a.id)
		WHERE';

	IF date_start IS NOT NULL AND date_end IS NOT NULL THEN
		SET @sql = CONCAT(@sql, ' (q.creation_date BETWEEN ', date_range, ')');
	ELSEIF date_start IS NOT NULL AND date_end IS NULL THEN
		SET @sql = CONCAT(@sql, ' (q.creation_date > "', date_start,'")');
	ELSEIF date_start IS NULL AND date_end IS NOT NULL THEN
		SET @SQL = CONCAT(@SQL, ' (q.creation_date < "', date_end, '")');
	ELSE
		SET @SQL = CONCAT(@SQL, ' (1=1)');
	END IF;
  	IF tag_list != '' THEN
  		SET tag_list_len = LENGTH(tag_list) - LENGTH(REPLACE(tag_list, ',', '')) + 1;
   	SET @sql = CONCAT(@sql, ' AND (q.id IN (SELECT post_id FROM tag_link WHERE tag_id IN(', tag_list, ') GROUP BY post_id HAVING COUNT(DISTINCT tag_id) >=', tag_list_len ,'))');
  	END IF;
  	
  	SET @sql = CONCAT(@sql, ' GROUP BY location ORDER BY COUNT(u.location) DESC LIMIT 100;');
  	PREPARE stmt FROM @sql;
  	EXECUTE stmt;
  	DEALLOCATE PREPARE stmt;
END//
DELIMITER ;

-- Dumping structure for procedure dashboard_data.get_post_keywords
DELIMITER //
CREATE PROCEDURE `get_post_keywords`(
	IN `date_start` DATE,
	IN `date_end` DATE,
	IN `tag_list` VARCHAR(512)
)
BEGIN
  	DECLARE date_range VARCHAR(50);
  	DECLARE tag_list_len INT;
  	SET date_range = CONCAT("'", date_start, "' AND '", date_end, "'");
  	SET @SQL = '
		SELECT k.keyword,
		COUNT(DISTINCT q.id) AS question_count,
		COUNT(DISTINCT a.id) AS answer_count,
		COUNT(DISTINCT c.id) + COUNT(DISTINCT d.id) AS comments_count,
		CAST((SUM(q.view_count)) AS INT) AS view_count,
		CAST((SUM(q.score) + SUM(a.score) + SUM(c.score) + SUM(d.score)) AS INT) AS total_score,
		CAST((AVG(q.sentiment)+AVG(a.sentiment)+AVG(c.sentiment)+AVG(d.sentiment))/4 AS VARCHAR(6)) AS sentiment
		FROM keyword_link AS kl
		INNER JOIN keyword AS k ON k.id = kl.keyword_id
		INNER JOIN question AS q ON q.id = kl.post_id
		LEFT JOIN answer AS a ON a.question_id = q.id
		LEFT JOIN comments AS c ON (c.post_id = q.id)
		LEFT JOIN comments AS d ON (d.post_id = a.id)
		WHERE (kl.user_id IS NULL)';

	IF date_start IS NOT NULL AND date_end IS NOT NULL THEN
		SET @sql = CONCAT(@sql, ' AND (q.creation_date BETWEEN ', date_range, ')');
	ELSEIF date_start IS NOT NULL AND date_end IS NULL THEN
		SET @sql = CONCAT(@sql, ' AND (q.creation_date > "', date_start,'")');
	ELSEIF date_start IS NULL AND date_end IS NOT NULL THEN
		SET @SQL = CONCAT(@SQL, ' AND (q.creation_date < "', date_end, '")');
	END IF;
  	IF tag_list != '' THEN
  		SET tag_list_len = LENGTH(tag_list) - LENGTH(REPLACE(tag_list, ',', '')) + 1;
   	SET @sql = CONCAT(@sql, ' AND (kl.post_id IN (SELECT post_id FROM tag_link WHERE tag_id IN(', tag_list, ') GROUP BY post_id HAVING COUNT(DISTINCT tag_id) >=', tag_list_len ,'))');
  	END IF;
  	
  	SET @sql = CONCAT(@sql, ' GROUP BY `keyword_id` ORDER BY COUNT(kl.keyword_id) DESC LIMIT 100;');
  	PREPARE stmt FROM @sql;
  	EXECUTE stmt;
  	DEALLOCATE PREPARE stmt;
END//
DELIMITER ;

-- Dumping structure for procedure dashboard_data.get_table_row_count
DELIMITER //
CREATE PROCEDURE `get_table_row_count`()
BEGIN
	(SELECT 'question',COUNT(*) FROM question)
	UNION ALL(SELECT 'answer',COUNT(*) FROM answer )
	UNION ALL(SELECT 'comments',COUNT(*) FROM comments )
	UNION ALL(SELECT 'tag_link',COUNT(*) FROM tag_link )
	UNION ALL(SELECT 'user',COUNT(*) FROM `user`)
	UNION ALL(SELECT 'badge_link',COUNT(*) FROM badge_link);
END//
DELIMITER ;

-- Dumping structure for procedure dashboard_data.get_tag_list
DELIMITER //
CREATE PROCEDURE `get_tag_list`()
BEGIN	
	SELECT * FROM tag WHERE EXISTS(SELECT * FROM tag_link WHERE tag_link.tag_id = tag.id) ORDER BY ID ASC;
END//
DELIMITER ;

-- Dumping structure for procedure dashboard_data.get_top_badges
DELIMITER //
CREATE PROCEDURE `get_top_badges`(
	IN `limit_no` INT
)
BEGIN
	SELECT b.badge_name, COUNT(*) AS total_count FROM badge_link AS bl
	INNER JOIN badges AS b ON b.id = bl.badge_id
	GROUP BY `badge_id` ORDER BY total_count DESC LIMIT limit_no;
END//
DELIMITER ;

-- Dumping structure for procedure dashboard_data.get_top_posts
DELIMITER //
CREATE PROCEDURE `get_top_posts`(
	IN `date_start` DATE,
	IN `date_end` DATE,
	IN `tag_list` VARCHAR(512)
)
BEGIN
	DECLARE date_range VARCHAR(50);
	DECLARE tag_list_len INT;
  	SET date_range = CONCAT("'", date_start, "' AND '", date_end, "'");
  	SET @SQL = '
		SELECT 
			title,
			score, 
			CONCAT(''https://stackoverflow.com/questions/'',q.id) AS link
		FROM question AS q
		INNER JOIN tag_link AS tl ON tl.post_id = q.id';

	IF date_start IS NOT NULL AND date_end IS NOT NULL THEN
		SET @sql = CONCAT(@sql, ' WHERE (q.creation_date BETWEEN ', date_range, ')');
	ELSEIF date_start IS NOT NULL AND date_end IS NULL THEN
		SET @sql = CONCAT(@sql, ' WHERE (q.creation_date > "', date_start,'")');
	ELSEIF date_start IS NULL AND date_end IS NOT NULL THEN
		SET @SQL = CONCAT(@SQL, ' WHERE (q.creation_date < "', date_end, '")');
	ELSE
		SET @SQL = CONCAT(@SQL, ' WHERE (1 = 1)');
	END IF;
  	IF tag_list != '' THEN
  		SET tag_list_len = LENGTH(tag_list) - LENGTH(REPLACE(tag_list, ',', '')) + 1;
   	SET @sql = CONCAT(@sql, ' AND (tl.post_id IN (SELECT post_id FROM tag_link WHERE tag_id IN(', tag_list, ') GROUP BY post_id HAVING COUNT(DISTINCT tag_id) >=', tag_list_len ,'))');
  	END IF;
	SET @sql = CONCAT(@sql, ' GROUP BY q.id ORDER BY score DESC LIMIT 50;');

  	PREPARE stmt FROM @sql;
  	EXECUTE stmt;
  	DEALLOCATE PREPARE stmt;
END//
DELIMITER ;

-- Dumping structure for procedure dashboard_data.get_top_tags
DELIMITER //
CREATE PROCEDURE `get_top_tags`(
	IN `limit_no` INT
)
BEGIN
	SELECT t.tag, COUNT(*) AS total_count FROM tag_link AS tl
	INNER JOIN tag AS t ON t.id = tl.tag_id
	GROUP BY `tag_id` ORDER BY total_count DESC LIMIT limit_no;
END//
DELIMITER ;

-- Dumping structure for procedure dashboard_data.get_user_keywords
DELIMITER //
CREATE PROCEDURE `get_user_keywords`(
	IN `date_start` DATE,
	IN `date_end` DATE,
	IN `tag_list` VARCHAR(512)
)
BEGIN
  	DECLARE date_range VARCHAR(50);
  	DECLARE tag_list_len INT;
  	SET date_range = CONCAT("'", date_start, "' AND '", date_end, "'");
  	SET @SQL = '
		SELECT k.keyword,
		CAST(COUNT(kl.keyword_id) AS INT) AS count,
		CAST(AVG(u.reputation) AS VARCHAR(10)) AS avg_rep,
		CAST(SUM(u.reputation) AS INT) AS total_rep,
		DATE_FORMAT(CAST(FROM_UNIXTIME(AVG(UNIX_TIMESTAMP(u.creation_date))) AS DATE),"%d/%m/%Y") AS avg_acc_age
		FROM keyword_link AS kl
		INNER JOIN keyword AS k ON k.id = kl.keyword_id
		INNER JOIN user AS u ON u.id = kl.user_id 
		INNER JOIN question AS q ON q.user_id = u.id
		LEFT JOIN answer AS a ON a.question_id = q.id
		LEFT JOIN comments AS c ON (c.post_id = q.id)
		LEFT JOIN comments AS d ON (d.post_id = a.id)
		WHERE (kl.user_id IS NOT NULL)';

	IF date_start IS NOT NULL AND date_end IS NOT NULL THEN
		SET @sql = CONCAT(@sql, ' AND (q.creation_date BETWEEN ', date_range, ')');
	ELSEIF date_start IS NOT NULL AND date_end IS NULL THEN
		SET @sql = CONCAT(@sql, ' AND (q.creation_date > "', date_start,'")');
	ELSEIF date_start IS NULL AND date_end IS NOT NULL THEN
		SET @SQL = CONCAT(@SQL, ' AND (q.creation_date < "', date_end, '")');
	END IF;
  	IF tag_list != '' THEN
  		SET tag_list_len = LENGTH(tag_list) - LENGTH(REPLACE(tag_list, ',', '')) + 1;
   	SET @sql = CONCAT(@sql, ' AND (q.id IN (SELECT post_id FROM tag_link WHERE tag_id IN(', tag_list, ') GROUP BY post_id HAVING COUNT(DISTINCT tag_id) >=', tag_list_len ,'))');
  	END IF;
  	
  	SET @sql = CONCAT(@sql, ' GROUP BY `keyword_id` ORDER BY COUNT(kl.keyword_id) DESC LIMIT 100;');
  	PREPARE stmt FROM @sql;
  	EXECUTE stmt;
  	DEALLOCATE PREPARE stmt;
END//
DELIMITER ;

-- Dumping structure for procedure dashboard_data.get_user_years
DELIMITER //
CREATE PROCEDURE `get_user_years`(
	IN `date_start` DATE,
	IN `date_end` DATE,
	IN `tag_list` VARCHAR(512)
)
BEGIN
	DECLARE date_range VARCHAR(50);
	DECLARE tag_list_len INT;
  	SET date_range = CONCAT("'", date_start, "' AND '", date_end, "'");
  	SET @SQL = 'SELECT
			CAST(YEAR(u.creation_date) AS VARCHAR(5)) AS creation_year,
			COUNT(DISTINCT u.id) AS year_count 
			FROM user AS u 
			LEFT JOIN question AS q ON q.user_id = u.id
			INNER JOIN tag_link AS tl ON tl.post_id = q.id
			WHERE YEAR(u.creation_date) IS NOT NULL';
	IF date_start IS NOT NULL AND date_end IS NOT NULL THEN
		SET @sql = CONCAT(@sql, ' AND (q.creation_date BETWEEN ', date_range, ')');
	ELSEIF date_start IS NOT NULL AND date_end IS NULL THEN
		SET @sql = CONCAT(@sql, ' AND (q.creation_date > "', date_start,'")');
	ELSEIF date_start IS NULL AND date_end IS NOT NULL THEN
		SET @SQL = CONCAT(@SQL, ' AND (q.creation_date < "', date_end, '")');
	END IF;
  	IF tag_list != '' THEN
  		SET tag_list_len = LENGTH(tag_list) - LENGTH(REPLACE(tag_list, ',', '')) + 1;
   	SET @sql = CONCAT(@sql, ' AND (tl.post_id IN (SELECT post_id FROM tag_link WHERE tag_id IN(', tag_list, ') GROUP BY post_id HAVING COUNT(DISTINCT tag_id) >=', tag_list_len ,'))');
  	END IF;
	SET @sql = CONCAT(@sql, ' GROUP BY YEAR(u.creation_date) ORDER BY YEAR(u.creation_date);');
	PREPARE stmt FROM @sql;
  	EXECUTE stmt;
  	DEALLOCATE PREPARE stmt;
END//
DELIMITER ;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
GRANT SELECT, PROCESS, SHOW DATABASES, EXECUTE, SHOW VIEW ON *.* TO `edgehill`@`%` IDENTIFIED BY PASSWORD '*96B98F206465F31434C8BF3B36975A64136B01A9';