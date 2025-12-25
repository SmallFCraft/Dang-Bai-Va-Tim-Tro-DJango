-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 25, 2025 at 07:40 AM
-- Server version: 8.0.30
-- PHP Version: 8.3.24

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tro_django`
--

-- --------------------------------------------------------

--
-- Table structure for table `account_emailaddress`
--

CREATE TABLE `account_emailaddress` (
  `id` int NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `account_emailaddress`
--

INSERT INTO `account_emailaddress` (`id`, `email`, `verified`, `primary`, `user_id`) VALUES
(2, 'huytqd@gmail.com', 0, 1, 4);

-- --------------------------------------------------------

--
-- Table structure for table `account_emailconfirmation`
--

CREATE TABLE `account_emailconfirmation` (
  `id` int NOT NULL,
  `created` datetime(6) NOT NULL,
  `sent` datetime(6) DEFAULT NULL,
  `key` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email_address_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int NOT NULL,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add site', 6, 'add_site'),
(22, 'Can change site', 6, 'change_site'),
(23, 'Can delete site', 6, 'delete_site'),
(24, 'Can view site', 6, 'view_site'),
(25, 'Can add email address', 7, 'add_emailaddress'),
(26, 'Can change email address', 7, 'change_emailaddress'),
(27, 'Can delete email address', 7, 'delete_emailaddress'),
(28, 'Can view email address', 7, 'view_emailaddress'),
(29, 'Can add email confirmation', 8, 'add_emailconfirmation'),
(30, 'Can change email confirmation', 8, 'change_emailconfirmation'),
(31, 'Can delete email confirmation', 8, 'delete_emailconfirmation'),
(32, 'Can view email confirmation', 8, 'view_emailconfirmation'),
(33, 'Can add social account', 9, 'add_socialaccount'),
(34, 'Can change social account', 9, 'change_socialaccount'),
(35, 'Can delete social account', 9, 'delete_socialaccount'),
(36, 'Can view social account', 9, 'view_socialaccount'),
(37, 'Can add social application', 10, 'add_socialapp'),
(38, 'Can change social application', 10, 'change_socialapp'),
(39, 'Can delete social application', 10, 'delete_socialapp'),
(40, 'Can view social application', 10, 'view_socialapp'),
(41, 'Can add social application token', 11, 'add_socialtoken'),
(42, 'Can change social application token', 11, 'change_socialtoken'),
(43, 'Can delete social application token', 11, 'delete_socialtoken'),
(44, 'Can view social application token', 11, 'view_socialtoken'),
(45, 'Can add Danh mục', 12, 'add_category'),
(46, 'Can change Danh mục', 12, 'change_category'),
(47, 'Can delete Danh mục', 12, 'delete_category'),
(48, 'Can view Danh mục', 12, 'view_category'),
(49, 'Can add Quận/Huyện', 13, 'add_district'),
(50, 'Can change Quận/Huyện', 13, 'change_district'),
(51, 'Can delete Quận/Huyện', 13, 'delete_district'),
(52, 'Can view Quận/Huyện', 13, 'view_district'),
(53, 'Can add Tiện ích', 14, 'add_utility'),
(54, 'Can change Tiện ích', 14, 'change_utility'),
(55, 'Can delete Tiện ích', 14, 'delete_utility'),
(56, 'Can view Tiện ích', 14, 'view_utility'),
(57, 'Can add Người dùng', 15, 'add_user'),
(58, 'Can change Người dùng', 15, 'change_user'),
(59, 'Can delete Người dùng', 15, 'delete_user'),
(60, 'Can view Người dùng', 15, 'view_user'),
(61, 'Can add Phòng trọ', 16, 'add_motelroom'),
(62, 'Can change Phòng trọ', 16, 'change_motelroom'),
(63, 'Can delete Phòng trọ', 16, 'delete_motelroom'),
(64, 'Can view Phòng trọ', 16, 'view_motelroom'),
(65, 'Can add Hình ảnh phòng trọ', 17, 'add_motelimage'),
(66, 'Can change Hình ảnh phòng trọ', 17, 'change_motelimage'),
(67, 'Can delete Hình ảnh phòng trọ', 17, 'delete_motelimage'),
(68, 'Can view Hình ảnh phòng trọ', 17, 'view_motelimage'),
(69, 'Can add Báo cáo', 18, 'add_report'),
(70, 'Can change Báo cáo', 18, 'change_report'),
(71, 'Can delete Báo cáo', 18, 'delete_report'),
(72, 'Can view Báo cáo', 18, 'view_report'),
(73, 'Can add Đánh giá', 19, 'add_review'),
(74, 'Can change Đánh giá', 19, 'change_review'),
(75, 'Can delete Đánh giá', 19, 'delete_review'),
(76, 'Can view Đánh giá', 19, 'view_review'),
(77, 'Can add Yêu thích', 20, 'add_favorite'),
(78, 'Can change Yêu thích', 20, 'change_favorite'),
(79, 'Can delete Yêu thích', 20, 'delete_favorite'),
(80, 'Can view Yêu thích', 20, 'view_favorite');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL
) ;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-11-17 00:30:10.898379', '6', 'Phòng trọ Cẩm Lệ giá sinh viên', 2, '[{\"changed\": {\"fields\": [\"Ng\\u01b0\\u1eddi \\u0111\\u0103ng\"]}}]', 16, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int NOT NULL,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(7, 'account', 'emailaddress'),
(8, 'account', 'emailconfirmation'),
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session'),
(6, 'sites', 'site'),
(9, 'socialaccount', 'socialaccount'),
(10, 'socialaccount', 'socialapp'),
(11, 'socialaccount', 'socialtoken'),
(12, 'tro_site', 'category'),
(13, 'tro_site', 'district'),
(20, 'tro_site', 'favorite'),
(17, 'tro_site', 'motelimage'),
(16, 'tro_site', 'motelroom'),
(18, 'tro_site', 'report'),
(19, 'tro_site', 'review'),
(15, 'tro_site', 'user'),
(14, 'tro_site', 'utility');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-11-16 16:26:52.860662'),
(2, 'contenttypes', '0002_remove_content_type_name', '2025-11-16 16:26:52.900509'),
(3, 'auth', '0001_initial', '2025-11-16 16:26:53.051413'),
(4, 'auth', '0002_alter_permission_name_max_length', '2025-11-16 16:26:53.096098'),
(5, 'auth', '0003_alter_user_email_max_length', '2025-11-16 16:26:53.102830'),
(6, 'auth', '0004_alter_user_username_opts', '2025-11-16 16:26:53.108854'),
(7, 'auth', '0005_alter_user_last_login_null', '2025-11-16 16:26:53.111640'),
(8, 'auth', '0006_require_contenttypes_0002', '2025-11-16 16:26:53.113099'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2025-11-16 16:26:53.113099'),
(10, 'auth', '0008_alter_user_username_max_length', '2025-11-16 16:26:53.119689'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2025-11-16 16:26:53.122721'),
(12, 'auth', '0010_alter_group_name_max_length', '2025-11-16 16:26:53.131498'),
(13, 'auth', '0011_update_proxy_permissions', '2025-11-16 16:26:53.138295'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2025-11-16 16:26:53.141764'),
(15, 'tro_site', '0001_initial', '2025-11-16 16:26:53.880562'),
(16, 'account', '0001_initial', '2025-11-16 16:26:54.006275'),
(17, 'account', '0002_email_max_length', '2025-11-16 16:26:54.022570'),
(18, 'account', '0003_alter_emailaddress_create_unique_verified_email', '2025-11-16 16:26:54.045256'),
(19, 'account', '0004_alter_emailaddress_drop_unique_email', '2025-11-16 16:26:54.068788'),
(20, 'account', '0005_emailaddress_idx_upper_email', '2025-11-16 16:26:54.085454'),
(21, 'account', '0006_emailaddress_lower', '2025-11-16 16:26:54.096776'),
(22, 'account', '0007_emailaddress_idx_email', '2025-11-16 16:26:54.124605'),
(23, 'account', '0008_emailaddress_unique_primary_email_fixup', '2025-11-16 16:26:54.137541'),
(24, 'account', '0009_emailaddress_unique_primary_email', '2025-11-16 16:26:54.140541'),
(25, 'admin', '0001_initial', '2025-11-16 16:26:54.229722'),
(26, 'admin', '0002_logentry_remove_auto_add', '2025-11-16 16:26:54.229722'),
(27, 'admin', '0003_logentry_add_action_flag_choices', '2025-11-16 16:26:54.247298'),
(28, 'sessions', '0001_initial', '2025-11-16 16:26:54.269791'),
(29, 'sites', '0001_initial', '2025-11-16 16:26:54.276830'),
(30, 'sites', '0002_alter_domain_unique', '2025-11-16 16:26:54.294887'),
(31, 'socialaccount', '0001_initial', '2025-11-16 16:26:54.561307'),
(32, 'socialaccount', '0002_token_max_lengths', '2025-11-16 16:26:54.620850'),
(33, 'socialaccount', '0003_extra_data_default_dict', '2025-11-16 16:26:54.623810'),
(34, 'socialaccount', '0004_app_provider_id_settings', '2025-11-16 16:26:54.742655'),
(35, 'socialaccount', '0005_socialtoken_nullable_app', '2025-11-16 16:26:54.865620'),
(36, 'socialaccount', '0006_alter_socialaccount_extra_data', '2025-11-16 16:26:54.916223'),
(37, 'tro_site', '0002_favorite_review', '2025-11-17 01:32:48.075157');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('1bza6usj5e1qr4l2wadskcy1rwosyg6u', '.eJxVj8tuwyAQAP9lzxYC8zD2sfd-QVVZC4tr2hoig9VEUf69oc0lt9XO7Eh7BfQ-H6nOeNQ1pBo91pjTvIW6ZiowvV3hf4YJTljKT94JOsAKkxiMlFpIq5jiWkojOjhK2BNu4W4jbTHB7b2Dv_jc0BxbR8DTzqH_CqkB-sT0kZnPqe7RsaawBy3sNVP4fnm4T4EVy3q_XlAZNSg-9nbU_UgoFjksordE1vSSey-98Ua6xZCxGJxF7bRyVhAna3WLllBK-z-cT3G_wMRvvyCoX_E:1vKqFM:K_-bl3s66lTh4lXmOkNFneAwlV3sm1cFYG589ihgW74', '2025-12-01 03:49:44.517335'),
('1l8mm9x3m0eohaxs89wzni76r3xulmsp', '.eJxVj0FuwyAQRe8ya8sCJgbjZfc5QVVZYxhq2hoig9VWUe7e0maT3ei_pyfNFci5fKQ601FXTjU6qjGneeO6Zl9ger7C_w0TXKiUz7x76IAqTNJoRImDUr3G0yi07eAovCfa-Ncmv8UEt5cO_uJzQ3NsHQkP20LunVMD_o3Sa-5dTnWPS9-U_k5Lf86eP57u7kNgpbK2LOolnAJ6P6pRBemVsbwEwsEiWS0EIzs3uCEIFVA4w4GtQiNHK7TQpkULl9L-569L3L9hErcfQahf8Q:1vKgOg:Horp73mFbS0-Mj9NeiLkuWC2pIwR04YLvIzJp_2VFRA', '2025-11-30 17:18:42.669518'),
('6zlsd5ubemi29kernwp1u4mrw9h2qllu', '.eJxtkM9qwzAMxt9F5xBiJ_GfnMbue4JRgmwrjbfG7mKHrpS---Ktl8IOAknfT5-EboDWxi3kEbc8U8jeYvYxjAvlOboEw_sN_nIY4IwpXeLqoALMMDAphOgUY00tG6E6pSugBf1pR-ftmr_cy7GUtY3LPrIlWgMu9J96P1Twe8JYqNGXbR089QzaTwpFcB8YjnGfC3n1pi5I_VBT_RYdnV4f7JPBjGkutqSE6S1Drs0kWztxK1vBpG0Fas7EHowm0h3TxvRT08uO80YJEkw76_pimiil8iX6Pvv1CkNz_wFOm206:1vYfsM:dbarrLgI7B_W_7_R7tGOtN6nJ1gBb-4EzjarB4lEXSc', '2026-01-08 07:35:10.720624'),
('9r2vvc9xc329pyir2mrjudxj2bguofdm', '.eJxVj7tuwzAMAP-Fs2FI1Cv22D1fUBQGLbG12loKLBlJEeTfG7VZshG84wG8Anmf91Qn2uvCqUZPNeY0rVyXHAqMr1f4n2GEE5VyzluADqjCKJ1VSqI82B6VNEbqDvbCW6KV73bgNcPtrYO_9tTIFFsG4Wk3k__i1ED4pPSRe59T3eLcN6V_0NIfc-Dvl4f7FFioLPdrUqznAa0WJLVB66wVpNEelHTGsCSvaUbhBusHRwGN8hrDgMKQM2jeW7RwKe19vpzi9gOjuP0CdgxeSw:1vKg38:Iu6bzObCeEffkCuKH-IT4Av0aLGRukDHv8k33K5mNv8', '2025-11-30 16:56:26.282610'),
('bzg9yjua152vzk9pxbh78kdufybehah0', '.eJxVj8tuwyAQAP9lzxbiZYx97L1fUFXWwuKatobIYDVRlH9vaHPJbbUzO9JeAb3PR6ozHnUNqUaPNeY0b6GumQpMb1f4n2GCE5byk3eCDrDCJAajlFZGSCaN5Ep0cJSwJ9zCXUbaYoLbewd_7bmhObaMgKedQ_8VUgP0iekjM59T3aNjTWEPWthrpvD98nCfAiuW9X69oDZ60HyUduzlSCgWNSxCWiJrpOLeK2-8UW4xZCwGZ7F3vXZWECdr-xYtoZT2fjif4n6Bid9-AdPFX7Q:1vKoE0:h_y28HO0sYiCpl1uC1mgAemj7HIAqX9sGE9pGsR3vrQ', '2025-12-01 01:40:12.339715'),
('ew5y8bymlrft49mojwi8vgxd2brtsjue', '.eJxVj8tuwyAQAP9lz5YFBvPwsfd-QVVZC4tr2hoig9VEUf69oc0lt9XO7Eh7BfQ-H6nOeNQ1pBo91pjTvIW6ZiowvV3hf4YJTljKT94JOsAKE9dKCMWsZL21g9bKdnCUsCfcwt1G2mKC23sHf_G5oTm2DoennUP_FVID9InpI_c-p7pH1zelf9DSv2YK3y8P9ymwYlnv1wtKJbVkdjB2HCwhX4Re-GCIjBoE81545ZVwiyJlMDiDoxulM5wYGTO2aAmltP_D-RT3C0zs9gs1wWAK:1vKsjV:AI_2cxM6sp2pSH05J49K-M3Z8tZhqL4qFDr7ZbWYj3s', '2025-12-01 06:29:01.048766'),
('mg9ip8zx431df9w9a8g17x5rkcc3qw2d', '.eJxVj0FOxDAMRe_idRU1TZq6XbLnBAhVTpzSAE1GTSpAo7k7Dcxmdpbf95P_Fci5dMQy01FWH0twVEKK8-bLmjjD9HKF_xkmuFDOX2lnaIAKTHIwSnfYDig0Sj122MCR_R5p82eaeAsRbq8N_MnniuZQPRIedpbch48V8DvFtyRcimUPVtSIuNMsnhP7z6d79kGwUl7P64W00YNuz0fGvhuZ5KKGRXbIjKZTrXPKGWeUXQwbJG-Rettri5JbRuyrNPuca3__fQn7D0zt7RcwyWAE:1vLACM:eAj6_tyJv0p8AOKId7VVlcLAn_sQjM8AlQMdzH9SqS0', '2025-12-02 01:07:58.619639'),
('n0wjtyhmpngcfxt0bk2srzfsjaf78146', '.eJxVj8FuwyAMQP_F5wglEByS4-77gmmKDCYL2wJVIFqrqv--svXSm-X3_CRfgZxLRywzHWX1sQRHJaQ4b76siTNMb1f4n2GCE-X8k3aGBqjA1A2IalSIKGSrNGps4Mh-j7T5u028hQi39wb-4nNFc6idDp52ltyXjxXwJ8WPJFyKZQ9WVEU8aBavif33y8N9CqyU1_v1Qj32Q9-O0oxajkzdooalk4bZoFStc8qhQ2UXZDTkrSFtdW9Nxy0bo2s0-5zr__58CvsFpvb2Cy9QYAI:1vXbgQ:MCyW8eSYkNs490cipXRKIXov-ktNPO7xr74RGL5hfYI', '2026-01-05 08:54:26.402005'),
('p5p1fmhphjdka6v2v4orpxxcbe4gzsnj', '.eJxVj0FuwyAQRe8yawuBwYC97L4nqCprYHBNW0NksJooyt0b2myyG8378zT_Cuh9PlKd8ahrSDV6rDGneQt1zVRgervC_wwTnLCUn7wTdIAVJmG0lEoaw5lQfOy56uAoYU-4hXsaaYsJbu8d_MnnhubYPAKedg79V0gN0Cemj8x8TnWPjrUIe9DCXjOF75dH9kmwYlnv1wsqrUz7xI5DPxKKRZpF9JbI6l5y76XXXku3aNIWg7M4uEE5K4iTtUOTllBK6x_Op7hfYOK3Xx7_X-8:1vKoGY:tD_L3uuPmu1nKeLQlP1fMNcEzLqTLPVuo78HzKAGwQs', '2025-12-01 01:42:50.174750'),
('zven0f38uiivhg22o86w6zfrbq4ycjgz', '.eJxVj8FuwyAMQP_F5wiFkBCT4-77gmmKDCYL2wJVIFqrqv--svXSm-X3_CRfgZxLRywzHWX1sQRHJaQ4b76siTNMb1f4n2GCE-X8k3aGBqjAJEetlEIjUaCWxpgGjuz3SJu_y8RbiHB7b-CvPVc0h5qR8LSz5L58rIA_KX4k4VIse7CiKuJBs3hN7L9fHu5TYKW83q8X6nU_9q3p0AydYZKLGhfZITPqTrXOKaedVnbRrJG8RRrs0FuU3DLiUKPZ51zf9-dT2C8wtbdf9oFf3Q:1vKn0I:BppkOha38wNJ4isZHe9GHkRRKOsLAFUuWEKje3P-zhE', '2025-12-01 00:21:58.907441');

-- --------------------------------------------------------

--
-- Table structure for table `django_site`
--

CREATE TABLE `django_site` (
  `id` int NOT NULL,
  `domain` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_site`
--

INSERT INTO `django_site` (`id`, `domain`, `name`) VALUES
(1, 'example.com', 'example.com');

-- --------------------------------------------------------

--
-- Table structure for table `socialaccount_socialaccount`
--

CREATE TABLE `socialaccount_socialaccount` (
  `id` int NOT NULL,
  `provider` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uid` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` json NOT NULL,
  `user_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `socialaccount_socialapp`
--

CREATE TABLE `socialaccount_socialapp` (
  `id` int NOT NULL,
  `provider` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `client_id` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `secret` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `key` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `provider_id` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `settings` json NOT NULL DEFAULT (_utf8mb3'{}')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `socialaccount_socialapp_sites`
--

CREATE TABLE `socialaccount_socialapp_sites` (
  `id` bigint NOT NULL,
  `socialapp_id` int NOT NULL,
  `site_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `socialaccount_socialtoken`
--

CREATE TABLE `socialaccount_socialtoken` (
  `id` int NOT NULL,
  `token` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `token_secret` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `account_id` int NOT NULL,
  `app_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tro_site_category`
--

CREATE TABLE `tro_site_category` (
  `id` bigint NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `icon` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tro_site_category`
--

INSERT INTO `tro_site_category` (`id`, `name`, `slug`, `description`, `icon`, `created_at`) VALUES
(6, 'Phòng trọ', 'phong-tro', NULL, 'fa-home', '2025-11-16 16:49:55.580943'),
(7, 'Chung cư mini', 'chung-cu-mini', NULL, 'fa-building', '2025-11-16 16:49:55.582338'),
(8, 'Nhà nguyên căn', 'nha-nguyen-can', NULL, 'fa-house', '2025-11-16 16:49:55.583358'),
(9, 'Căn hộ dịch vụ', 'can-ho-dich-vu', NULL, 'fa-hotel', '2025-11-16 16:49:55.584282'),
(10, 'Ký túc xá', 'ky-tuc-xa', NULL, 'fa-bed', '2025-11-16 16:49:55.585062');

-- --------------------------------------------------------

--
-- Table structure for table `tro_site_district`
--

CREATE TABLE `tro_site_district` (
  `id` bigint NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tro_site_district`
--

INSERT INTO `tro_site_district` (`id`, `name`, `slug`, `description`, `created_at`) VALUES
(24, 'Quận Hải Châu', 'quan-hai-chau', NULL, '2025-11-16 16:49:55.570050'),
(25, 'Quận Thanh Khê', 'quan-thanh-khe', NULL, '2025-11-16 16:49:55.573210'),
(26, 'Quận Sơn Trà', 'quan-son-tra', NULL, '2025-11-16 16:49:55.574147'),
(27, 'Quận Ngũ Hành Sơn', 'quan-ngu-hanh-son', NULL, '2025-11-16 16:49:55.574147'),
(28, 'Quận Liên Chiểu', 'quan-lien-chieu', NULL, '2025-11-16 16:49:55.574147'),
(29, 'Quận Cẩm Lệ', 'quan-cam-le', NULL, '2025-11-16 16:49:55.574147');

-- --------------------------------------------------------

--
-- Table structure for table `tro_site_favorite`
--

CREATE TABLE `tro_site_favorite` (
  `id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `motel_room_id` bigint NOT NULL,
  `user_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tro_site_favorite`
--

INSERT INTO `tro_site_favorite` (`id`, `created_at`, `motel_room_id`, `user_id`) VALUES
(33, '2025-11-17 07:15:19.943929', 2, 1),
(35, '2025-12-22 08:55:29.142835', 1, 1),
(43, '2025-12-25 05:10:44.091908', 5, 4);

-- --------------------------------------------------------

--
-- Table structure for table `tro_site_motelimage`
--

CREATE TABLE `tro_site_motelimage` (
  `id` bigint NOT NULL,
  `image` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `caption` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_primary` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `motel_room_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tro_site_motelimage`
--

INSERT INTO `tro_site_motelimage` (`id`, `image`, `caption`, `is_primary`, `created_at`, `motel_room_id`) VALUES
(1, 'motel_rooms/70_kenh_nuoc_den_hinh_1_3.jpg', NULL, 0, '2025-11-17 01:33:28.428989', 6),
(2, 'motel_rooms/70_kenh_nuoc_den_hinh_1_9.jpg', NULL, 0, '2025-11-17 01:33:28.657095', 6),
(3, 'motel_rooms/70_kenh_nuoc_den_hinh_1_15.jpg', NULL, 0, '2025-11-17 01:33:28.892191', 6);

-- --------------------------------------------------------

--
-- Table structure for table `tro_site_motelroom`
--

CREATE TABLE `tro_site_motelroom` (
  `id` bigint NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(12,0) NOT NULL,
  `area` decimal(6,2) NOT NULL,
  `address` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  `contact_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact_phone` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact_email` varchar(254) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` int NOT NULL,
  `views` int UNSIGNED NOT NULL,
  `is_featured` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `approved_at` datetime(6) DEFAULT NULL,
  `category_id` bigint DEFAULT NULL,
  `district_id` bigint DEFAULT NULL,
  `owner_id` bigint NOT NULL
) ;

--
-- Dumping data for table `tro_site_motelroom`
--

INSERT INTO `tro_site_motelroom` (`id`, `title`, `slug`, `description`, `price`, `area`, `address`, `latitude`, `longitude`, `contact_name`, `contact_phone`, `contact_email`, `status`, `views`, `is_featured`, `created_at`, `updated_at`, `approved_at`, `category_id`, `district_id`, `owner_id`) VALUES
(1, 'Phòng trọ giá rẻ gần ĐH Bách Khoa Đà Nẵng', 'phong-tro-gia-re-gan-dh-bach-khoa-da-nang', 'Phòng trọ sạch sẽ, thoáng mát, gần trường ĐH Bách Khoa, ĐH Kinh Tế. Đầy đủ tiện nghi: giường, tủ, điều hòa, nóng lạnh. An ninh 24/7.', '1500000', '20.00', '123 Nguyễn Lương Bằng', NULL, NULL, 'Chị Hoa', '0905111222', 'contact@timtro.vn', 1, 1, 1, '2025-11-16 16:49:55.976719', '2025-11-16 16:49:55.976719', NULL, 6, 28, 2),
(2, 'Chung cư mini cao cấp Hải Châu', 'chung-cu-mini-cao-cap-hai-chau', 'Chung cư mini mới xây, full nội thất cao cấp. Gần biển Mỹ Khê, trung tâm thành phố. Thang máy, bảo vệ 24/7.', '3500000', '35.00', '456 Lê Duẩn', NULL, NULL, 'Anh Tuấn', '0905222333', 'contact@timtro.vn', 1, 23, 1, '2025-11-16 16:49:55.989359', '2025-11-16 16:49:55.989359', NULL, 7, 24, 2),
(3, 'Phòng trọ sinh viên Thanh Khê', 'phong-tro-sinh-vien-thanh-khe', 'Phòng trọ dành cho sinh viên, giá rẻ, gần các trường ĐH. Có chỗ để xe, wifi miễn phí.', '1200000', '18.00', '789 Điện Biên Phủ', NULL, NULL, 'Chị Lan', '0905333444', 'contact@timtro.vn', 1, 14, 1, '2025-11-16 16:49:56.003500', '2025-11-16 16:49:56.003500', NULL, 6, 25, 2),
(4, 'Căn hộ dịch vụ view biển Sơn Trà', 'can-ho-dich-vu-view-bien-son-tra', 'Căn hộ dịch vụ cao cấp, view biển tuyệt đẹp. Full nội thất 5 sao, có hồ bơi, gym.', '8000000', '50.00', '321 Võ Nguyên Giáp', NULL, NULL, 'Anh Minh', '0905444555', 'contact@timtro.vn', 1, 0, 0, '2025-11-16 16:49:56.012931', '2025-11-16 16:49:56.012931', NULL, 9, 26, 2),
(5, 'Nhà nguyên căn Ngũ Hành Sơn', 'nha-nguyen-can-ngu-hanh-son', 'Nhà nguyên căn 2 tầng, gần biển Non Nước, khu du lịch. Thích hợp gia đình hoặc nhóm bạn.', '6000000', '80.00', '555 Nguyễn Tất Thành', NULL, NULL, 'Chị Mai', '0905555666', 'contact@timtro.vn', 1, 5, 0, '2025-11-16 16:49:56.026098', '2025-11-16 16:49:56.026098', NULL, 8, 27, 2),
(6, 'Phòng trọ Cẩm Lệ giá sinh viên', 'phong-tro-cam-le-gia-sinh-vien', 'Phòng trọ mới xây, sạch sẽ, an ninh tốt. Gần chợ, siêu thị, thuận tiện đi lại.', '1300000', '22.00', '888 Nguyễn Hữu Thọ', NULL, NULL, 'Anh Hùng', '0905666777', 'contact@timtro.vn', 1, 21, 0, '2025-11-16 16:49:56.041670', '2025-11-17 01:33:28.012541', NULL, 6, 29, 1);

-- --------------------------------------------------------

--
-- Table structure for table `tro_site_motelroom_utilities`
--

CREATE TABLE `tro_site_motelroom_utilities` (
  `id` bigint NOT NULL,
  `motelroom_id` bigint NOT NULL,
  `utility_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tro_site_motelroom_utilities`
--

INSERT INTO `tro_site_motelroom_utilities` (`id`, `motelroom_id`, `utility_id`) VALUES
(1, 1, 13),
(2, 1, 14),
(3, 1, 17),
(4, 1, 19),
(5, 1, 20),
(6, 2, 13),
(7, 2, 14),
(8, 2, 15),
(9, 2, 16),
(10, 2, 18),
(11, 2, 22),
(12, 2, 23),
(13, 3, 13),
(14, 3, 19),
(15, 3, 20),
(16, 3, 24),
(17, 4, 13),
(18, 4, 14),
(19, 4, 15),
(20, 4, 16),
(21, 4, 18),
(22, 4, 21),
(23, 4, 22),
(24, 4, 23),
(25, 5, 13),
(26, 5, 14),
(27, 5, 15),
(28, 5, 16),
(29, 5, 18),
(30, 5, 21),
(31, 5, 24),
(32, 6, 13),
(33, 6, 14),
(34, 6, 17),
(35, 6, 19),
(36, 6, 24);

-- --------------------------------------------------------

--
-- Table structure for table `tro_site_report`
--

CREATE TABLE `tro_site_report` (
  `id` bigint NOT NULL,
  `reason` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` int NOT NULL,
  `admin_note` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `motel_room_id` bigint NOT NULL,
  `reporter_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tro_site_report`
--

INSERT INTO `tro_site_report` (`id`, `reason`, `description`, `status`, `admin_note`, `created_at`, `updated_at`, `motel_room_id`, `reporter_id`) VALUES
(1, 'spam', 'test', 0, NULL, '2025-11-17 01:38:56.539578', '2025-11-17 01:38:56.539578', 3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `tro_site_review`
--

CREATE TABLE `tro_site_review` (
  `id` bigint NOT NULL,
  `rating` int NOT NULL,
  `comment` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `motel_room_id` bigint NOT NULL,
  `user_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tro_site_review`
--

INSERT INTO `tro_site_review` (`id`, `rating`, `comment`, `created_at`, `updated_at`, `motel_room_id`, `user_id`) VALUES
(1, 1, 's', '2025-11-17 01:52:04.368196', '2025-11-17 01:55:02.368569', 2, 1),
(2, 5, 'test nhan xet', '2025-11-17 03:41:52.014304', '2025-11-17 03:42:09.791280', 3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `tro_site_user`
--

CREATE TABLE `tro_site_user` (
  `id` bigint NOT NULL,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` int NOT NULL,
  `phone` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `avatar` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `bio` longtext COLLATE utf8mb4_unicode_ci,
  `address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tro_site_user`
--

INSERT INTO `tro_site_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `role`, `phone`, `avatar`, `bio`, `address`, `created_at`, `updated_at`) VALUES
(1, 'pbkdf2_sha256$870000$qbnlwYuyC8rBB4GOtmcWEm$Gj5g+KVVLfqvDMcKhaOHilL93ObPIlUP1YBToBXyVXY=', '2025-12-22 08:54:26.324453', 1, 'admin', 'Pham', 'Huy', 'admin@gmail.com', 1, 1, '2025-11-16 16:42:12.594273', 0, '0387368890', 'avatars/download.jpg', '', NULL, '2025-11-16 16:42:12.946804', '2025-11-17 07:12:20.331766'),
(2, 'pbkdf2_sha256$870000$qtKuSBGV7XzPsBc6t7ODmB$Wre04U7Mf0yNAJ8Kzjqin8dm6vviAxwyGQmfWIbZhOw=', '2025-11-16 16:56:26.244195', 0, 'demo', 'Nguyễn', 'Văn A', 'demo@timtro.vn', 0, 1, '2025-11-16 16:49:55.602843', 0, '0905123456', '', NULL, NULL, '2025-11-16 16:49:55.969692', '2025-11-16 16:49:55.969692'),
(4, 'pbkdf2_sha256$870000$p3uoTwDPvBplIXi4MfP2DK$IEyGqzlOQjquhQl71LtUJCXqaN+3ZtRri2fqPStV6tI=', '2025-12-25 07:35:10.717115', 1, 'huytqd@gmail.com', '', '', 'huytqd@gmail.com', 1, 1, '2025-12-25 04:40:59.587427', 0, NULL, '', NULL, NULL, '2025-12-25 04:40:59.991629', '2025-12-25 04:40:59.991629');

-- --------------------------------------------------------

--
-- Table structure for table `tro_site_user_groups`
--

CREATE TABLE `tro_site_user_groups` (
  `id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tro_site_user_user_permissions`
--

CREATE TABLE `tro_site_user_user_permissions` (
  `id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tro_site_utility`
--

CREATE TABLE `tro_site_utility` (
  `id` bigint NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `icon` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tro_site_utility`
--

INSERT INTO `tro_site_utility` (`id`, `name`, `icon`, `created_at`) VALUES
(13, 'Wifi miễn phí', 'fa-wifi', '2025-11-16 16:49:55.586990'),
(14, 'Điều hòa', 'fa-snowflake', '2025-11-16 16:49:55.588994'),
(15, 'Máy giặt', 'fa-soap', '2025-11-16 16:49:55.589996'),
(16, 'Tủ lạnh', 'fa-temperature-low', '2025-11-16 16:49:55.591994'),
(17, 'Nóng lạnh', 'fa-shower', '2025-11-16 16:49:55.592950'),
(18, 'Bếp', 'fa-fire-burner', '2025-11-16 16:49:55.593357'),
(19, 'Giường', 'fa-bed', '2025-11-16 16:49:55.595465'),
(20, 'Tủ quần áo', 'fa-door-closed', '2025-11-16 16:49:55.596466'),
(21, 'Ban công', 'fa-window-maximize', '2025-11-16 16:49:55.597752'),
(22, 'Thang máy', 'fa-elevator', '2025-11-16 16:49:55.598924'),
(23, 'Bảo vệ 24/7', 'fa-shield', '2025-11-16 16:49:55.599799'),
(24, 'Gửi xe miễn phí', 'fa-motorcycle', '2025-11-16 16:49:55.600840');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account_emailaddress`
--
ALTER TABLE `account_emailaddress`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `account_emailaddress_user_id_email_987c8728_uniq` (`user_id`,`email`),
  ADD KEY `account_emailaddress_email_03be32b2` (`email`);

--
-- Indexes for table `account_emailconfirmation`
--
ALTER TABLE `account_emailconfirmation`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `key` (`key`),
  ADD KEY `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` (`email_address_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_tro_site_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `django_site`
--
ALTER TABLE `django_site`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`);

--
-- Indexes for table `socialaccount_socialaccount`
--
ALTER TABLE `socialaccount_socialaccount`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`),
  ADD KEY `socialaccount_socialaccount_user_id_8146e70c_fk_tro_site_user_id` (`user_id`);

--
-- Indexes for table `socialaccount_socialapp`
--
ALTER TABLE `socialaccount_socialapp`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `socialaccount_socialapp_sites`
--
ALTER TABLE `socialaccount_socialapp_sites`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `socialaccount_socialapp_sites_socialapp_id_site_id_71a9a768_uniq` (`socialapp_id`,`site_id`),
  ADD KEY `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` (`site_id`);

--
-- Indexes for table `socialaccount_socialtoken`
--
ALTER TABLE `socialaccount_socialtoken`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  ADD KEY `socialaccount_social_account_id_951f210e_fk_socialacc` (`account_id`);

--
-- Indexes for table `tro_site_category`
--
ALTER TABLE `tro_site_category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `slug` (`slug`);

--
-- Indexes for table `tro_site_district`
--
ALTER TABLE `tro_site_district`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `slug` (`slug`);

--
-- Indexes for table `tro_site_favorite`
--
ALTER TABLE `tro_site_favorite`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tro_site_favorite_user_id_motel_room_id_eea08665_uniq` (`user_id`,`motel_room_id`),
  ADD KEY `tro_site_favorite_motel_room_id_b9e0b625_fk_tro_site_` (`motel_room_id`),
  ADD KEY `tro_site_fa_user_id_ef5125_idx` (`user_id`,`created_at` DESC);

--
-- Indexes for table `tro_site_motelimage`
--
ALTER TABLE `tro_site_motelimage`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tro_site_motelimage_motel_room_id_a37bc74c_fk_tro_site_` (`motel_room_id`);

--
-- Indexes for table `tro_site_motelroom`
--
ALTER TABLE `tro_site_motelroom`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `tro_site_mo_status_a4ebed_idx` (`status`,`created_at` DESC),
  ADD KEY `tro_site_mo_distric_c662e7_idx` (`district_id`,`status`),
  ADD KEY `tro_site_mo_categor_e754c9_idx` (`category_id`,`status`),
  ADD KEY `tro_site_motelroom_owner_id_bc0132ff_fk_tro_site_user_id` (`owner_id`);

--
-- Indexes for table `tro_site_motelroom_utilities`
--
ALTER TABLE `tro_site_motelroom_utilities`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tro_site_motelroom_utili_motelroom_id_utility_id_edae0f7a_uniq` (`motelroom_id`,`utility_id`),
  ADD KEY `tro_site_motelroom_u_utility_id_f3cfc885_fk_tro_site_` (`utility_id`);

--
-- Indexes for table `tro_site_report`
--
ALTER TABLE `tro_site_report`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tro_site_report_motel_room_id_45df1a90_fk_tro_site_motelroom_id` (`motel_room_id`),
  ADD KEY `tro_site_report_reporter_id_2a1a4384_fk_tro_site_user_id` (`reporter_id`);

--
-- Indexes for table `tro_site_review`
--
ALTER TABLE `tro_site_review`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tro_site_review_user_id_motel_room_id_7f7091ee_uniq` (`user_id`,`motel_room_id`),
  ADD KEY `tro_site_re_motel_r_261743_idx` (`motel_room_id`,`created_at` DESC);

--
-- Indexes for table `tro_site_user`
--
ALTER TABLE `tro_site_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `tro_site_user_groups`
--
ALTER TABLE `tro_site_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tro_site_user_groups_user_id_group_id_db00fa2c_uniq` (`user_id`,`group_id`),
  ADD KEY `tro_site_user_groups_group_id_5a54acb0_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `tro_site_user_user_permissions`
--
ALTER TABLE `tro_site_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tro_site_user_user_permi_user_id_permission_id_f4164e53_uniq` (`user_id`,`permission_id`),
  ADD KEY `tro_site_user_user_p_permission_id_bb05311e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `tro_site_utility`
--
ALTER TABLE `tro_site_utility`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account_emailaddress`
--
ALTER TABLE `account_emailaddress`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `account_emailconfirmation`
--
ALTER TABLE `account_emailconfirmation`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=81;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `django_site`
--
ALTER TABLE `django_site`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `socialaccount_socialaccount`
--
ALTER TABLE `socialaccount_socialaccount`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `socialaccount_socialapp`
--
ALTER TABLE `socialaccount_socialapp`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `socialaccount_socialapp_sites`
--
ALTER TABLE `socialaccount_socialapp_sites`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `socialaccount_socialtoken`
--
ALTER TABLE `socialaccount_socialtoken`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tro_site_category`
--
ALTER TABLE `tro_site_category`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `tro_site_district`
--
ALTER TABLE `tro_site_district`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `tro_site_favorite`
--
ALTER TABLE `tro_site_favorite`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT for table `tro_site_motelimage`
--
ALTER TABLE `tro_site_motelimage`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tro_site_motelroom`
--
ALTER TABLE `tro_site_motelroom`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tro_site_motelroom_utilities`
--
ALTER TABLE `tro_site_motelroom_utilities`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `tro_site_report`
--
ALTER TABLE `tro_site_report`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `tro_site_review`
--
ALTER TABLE `tro_site_review`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `tro_site_user`
--
ALTER TABLE `tro_site_user`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `tro_site_user_groups`
--
ALTER TABLE `tro_site_user_groups`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tro_site_user_user_permissions`
--
ALTER TABLE `tro_site_user_user_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tro_site_utility`
--
ALTER TABLE `tro_site_utility`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `account_emailaddress`
--
ALTER TABLE `account_emailaddress`
  ADD CONSTRAINT `account_emailaddress_user_id_2c513194_fk_tro_site_user_id` FOREIGN KEY (`user_id`) REFERENCES `tro_site_user` (`id`);

--
-- Constraints for table `account_emailconfirmation`
--
ALTER TABLE `account_emailconfirmation`
  ADD CONSTRAINT `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_tro_site_user_id` FOREIGN KEY (`user_id`) REFERENCES `tro_site_user` (`id`);

--
-- Constraints for table `socialaccount_socialaccount`
--
ALTER TABLE `socialaccount_socialaccount`
  ADD CONSTRAINT `socialaccount_socialaccount_user_id_8146e70c_fk_tro_site_user_id` FOREIGN KEY (`user_id`) REFERENCES `tro_site_user` (`id`);

--
-- Constraints for table `socialaccount_socialapp_sites`
--
ALTER TABLE `socialaccount_socialapp_sites`
  ADD CONSTRAINT `socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc` FOREIGN KEY (`socialapp_id`) REFERENCES `socialaccount_socialapp` (`id`),
  ADD CONSTRAINT `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`);

--
-- Constraints for table `socialaccount_socialtoken`
--
ALTER TABLE `socialaccount_socialtoken`
  ADD CONSTRAINT `socialaccount_social_account_id_951f210e_fk_socialacc` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  ADD CONSTRAINT `socialaccount_social_app_id_636a42d7_fk_socialacc` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`);

--
-- Constraints for table `tro_site_favorite`
--
ALTER TABLE `tro_site_favorite`
  ADD CONSTRAINT `tro_site_favorite_motel_room_id_b9e0b625_fk_tro_site_` FOREIGN KEY (`motel_room_id`) REFERENCES `tro_site_motelroom` (`id`),
  ADD CONSTRAINT `tro_site_favorite_user_id_8da0f5f1_fk_tro_site_user_id` FOREIGN KEY (`user_id`) REFERENCES `tro_site_user` (`id`);

--
-- Constraints for table `tro_site_motelimage`
--
ALTER TABLE `tro_site_motelimage`
  ADD CONSTRAINT `tro_site_motelimage_motel_room_id_a37bc74c_fk_tro_site_` FOREIGN KEY (`motel_room_id`) REFERENCES `tro_site_motelroom` (`id`);

--
-- Constraints for table `tro_site_motelroom`
--
ALTER TABLE `tro_site_motelroom`
  ADD CONSTRAINT `tro_site_motelroom_category_id_b7cc51eb_fk_tro_site_category_id` FOREIGN KEY (`category_id`) REFERENCES `tro_site_category` (`id`),
  ADD CONSTRAINT `tro_site_motelroom_district_id_0342c74a_fk_tro_site_district_id` FOREIGN KEY (`district_id`) REFERENCES `tro_site_district` (`id`),
  ADD CONSTRAINT `tro_site_motelroom_owner_id_bc0132ff_fk_tro_site_user_id` FOREIGN KEY (`owner_id`) REFERENCES `tro_site_user` (`id`);

--
-- Constraints for table `tro_site_motelroom_utilities`
--
ALTER TABLE `tro_site_motelroom_utilities`
  ADD CONSTRAINT `tro_site_motelroom_u_motelroom_id_6695acf4_fk_tro_site_` FOREIGN KEY (`motelroom_id`) REFERENCES `tro_site_motelroom` (`id`),
  ADD CONSTRAINT `tro_site_motelroom_u_utility_id_f3cfc885_fk_tro_site_` FOREIGN KEY (`utility_id`) REFERENCES `tro_site_utility` (`id`);

--
-- Constraints for table `tro_site_report`
--
ALTER TABLE `tro_site_report`
  ADD CONSTRAINT `tro_site_report_motel_room_id_45df1a90_fk_tro_site_motelroom_id` FOREIGN KEY (`motel_room_id`) REFERENCES `tro_site_motelroom` (`id`),
  ADD CONSTRAINT `tro_site_report_reporter_id_2a1a4384_fk_tro_site_user_id` FOREIGN KEY (`reporter_id`) REFERENCES `tro_site_user` (`id`);

--
-- Constraints for table `tro_site_review`
--
ALTER TABLE `tro_site_review`
  ADD CONSTRAINT `tro_site_review_motel_room_id_66e72853_fk_tro_site_motelroom_id` FOREIGN KEY (`motel_room_id`) REFERENCES `tro_site_motelroom` (`id`),
  ADD CONSTRAINT `tro_site_review_user_id_132c8dc9_fk_tro_site_user_id` FOREIGN KEY (`user_id`) REFERENCES `tro_site_user` (`id`);

--
-- Constraints for table `tro_site_user_groups`
--
ALTER TABLE `tro_site_user_groups`
  ADD CONSTRAINT `tro_site_user_groups_group_id_5a54acb0_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `tro_site_user_groups_user_id_19852393_fk_tro_site_user_id` FOREIGN KEY (`user_id`) REFERENCES `tro_site_user` (`id`);

--
-- Constraints for table `tro_site_user_user_permissions`
--
ALTER TABLE `tro_site_user_user_permissions`
  ADD CONSTRAINT `tro_site_user_user_p_permission_id_bb05311e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `tro_site_user_user_p_user_id_3ec3d0a6_fk_tro_site_` FOREIGN KEY (`user_id`) REFERENCES `tro_site_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
