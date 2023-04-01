/* -------------------------------------------------------------------------- */
/*                  Backup Queries if the parser insert fails 				  */
/*		don't forget to replace the filenames with your file path in ''       */
/* -------------------------------------------------------------------------- */

--Tags
LOAD DATA LOCAL INFILE /*myFile*/ REPLACE INTO TABLE tag FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' (`id`, `tag`)

--TagLink
CREATE TEMPORARY TABLE temp_tag_link (id BIGINT, post_id BIGINT, tag_name VARCHAR(256))
LOAD DATA LOCAL INFILE /*myFile*/ REPLACE INTO TABLE temp_tag_link FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' (`id`, `post_id`, `tag_name`)
UPDATE temp_tag_link tl INNER JOIN tag AS t ON tl.tag_name = t.tag SET tl.`tag_name` = t.`id` WHERE tl.`tag_name` = t.`tag`;
INSERT INTO tag_link (post_id,tag_id) SELECT post_id, tag_name FROM temp_tag_link WHERE `tag_name` REGEXP '^[0-9]+$';
DROP TABLE temp_tag_link;

--Question
CREATE TEMPORARY TABLE temp_question like question;
LOAD DATA LOCAL INFILE /*myFile*/ REPLACE INTO TABLE temp_question FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' (`id`, `creation_date`, `score`, `view_count`, `title`, `sentiment`, `user_id`, `accepted_answer_id`)
INSERT IGNORE INTO question SELECT * FROM temp_question;
INSERT INTO `user` (id) SELECT user_id FROM temp_question WHERE user_id <> 'NULL' ON DUPLICATE KEY UPDATE user.id=user.id;
DROP TABLE temp_question;

--Answer
CREATE TEMPORARY TABLE temp_answer LIKE answer;
LOAD DATA LOCAL INFILE /*myFile*/ REPLACE INTO TABLE temp_answer FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' (`id`, `question_id`, `creation_date`, `score`, `sentiment`,`user_id`);
INSERT IGNORE INTO answer SELECT * FROM temp_answer WHERE EXISTS (SELECT * FROM `question` where `id` = `question_id` LIMIT 1);
INSERT INTO `user` (id) SELECT user_id FROM temp_answer WHERE user_id <> 'NULL' ON DUPLICATE KEY UPDATE user.id=user.id;
DROP TABLE temp_answer;

--Comments
CREATE TEMPORARY TABLE temp_comments LIKE comments;
LOAD DATA LOCAL INFILE /*myFile*/ REPLACE INTO TABLE temp_comments FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' (`id`, `post_id`, `score`, `sentiment`,`creation_date`, `user_id`);
INSERT INTO comments SELECT * FROM temp_comments as tc WHERE EXISTS (SELECT * FROM question WHERE tc.`post_id` = question.`id` LIMIT 1) OR EXISTS (SELECT * FROM answer WHERE tc.`post_id` = answer.`id` LIMIT 1);
INSERT INTO `user` (id) SELECT user_id FROM temp_comments WHERE user_id <> 'NULL' ON DUPLICATE KEY UPDATE user.id=user.id;
DROP TABLE temp_comments;

--Users
CREATE TEMPORARY TABLE temp_user LIKE user;
LOAD DATA LOCAL INFILE /*myFile*/ REPLACE INTO TABLE temp_user FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' (`id`, `reputation`, `creation_date`, `location`);
UPDATE user AS u, temp_user AS tu SET u.reputation = tu.reputation, u.creation_date = tu.creation_date, u.location = tu.location WHERE u.id = tu.id;
DROP TABLE temp_user;

--Badge Link
CREATE TEMPORARY TABLE temp_badge_link (`user_id` BIGINT, `badge` VARCHAR(256), `date` DATE);
LOAD DATA LOCAL INFILE /*myFile*/ REPLACE INTO TABLE temp_badge_link FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' (`user_id`, `badge`, `date`);
DELETE FROM temp_badge_link WHERE NOT EXISTS (SELECT * FROM user u WHERE u.id = temp_badge_link.user_id);
ALTER TABLE `badge_link` CHANGE COLUMN `badge_id` `badge_id` VARCHAR(256) NOT NULL DEFAULT '0' AFTER `user_id`;
INSERT INTO badge_link (user_id, badge_id, date) SELECT * FROM temp_badge_link;
DROP TABLE temp_badge_link;

--Keyword Link
CREATE TEMPORARY TABLE temp_keyword_link (`post_id` BIGINT, `comment_id` BIGINT, `user_id` BIGINT, `keyword_id` VARCHAR(256));
LOAD DATA LOCAL INFILE /*myFile*/ REPLACE INTO TABLE temp_keyword_link CHARACTER SET UTF8 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' (`post_id`, `comment_id`, `user_id`, `keyword_id`);
INSERT INTO keyword_link (post_id,comment_id,user_id,keyword_id) SELECT * FROM temp_keyword_link;
DROP TABLE temp_keyword_link;

--Badges Normalization
INSERT INTO badges (`badge_name`) SELECT DISTINCT `badge_id` FROM badge_link;
UPDATE badge_link bl INNER JOIN badges AS b ON bl.badge_id = b.badge_name SET bl.`badge_id` = b.`id`;

--Keyword Normalization
INSERT INTO keyword (`keyword`) SELECT DISTINCT `keyword_id` FROM keyword_link;
UPDATE keyword_link kl INNER JOIN keyword as k ON kl.keyword_id = k.keyword SET kl.`keyword_id` = k.`id`;
