/*
 Navicat Premium Data Transfer

 Source Server         : test
 Source Server Type    : MySQL
 Source Server Version : 100421
 Source Host           : localhost:3306
 Source Schema         : player

 Target Server Type    : MySQL
 Target Server Version : 100421
 File Encoding         : 65001
 AUTHOR                : blackdragonx61 / Mali

 Date: 15/09/2021 11:03:50
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for mailbox_log
-- ----------------------------
DROP TABLE IF EXISTS `mailbox_log`;
CREATE TABLE `mailbox_log`  (
  `name` varchar(24) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '',
  `who` varchar(24) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '',
  `title` varchar(25) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '',
  `message` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '',
  `gm` tinyint NOT NULL DEFAULT 0,
  `gold` int NOT NULL DEFAULT 0,
  `won` int NOT NULL DEFAULT 0,
  `ivnum` int UNSIGNED NOT NULL DEFAULT 0,
  `icount` tinyint UNSIGNED NOT NULL DEFAULT 0,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = MyISAM CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
