# 生成假数据 v0.1.0
use openlib;

# 添加假数据，数据来源（河南理工大学图书馆）
INSERT INTO building (id, name, enabled)
VALUES (1, '南校区第一图书馆', 1);
INSERT INTO building (id, name, enabled)
VALUES (2, '北校区图书馆', 1);
INSERT INTO building (id, name, enabled)
VALUES (3, '南校区第二图书馆', 1);

# 添加房间数据，数据来源（河南理工大学图书馆）
INSERT INTO room (id, building_id, enabled, name)
VALUES (1, 1, 1, '五楼天井区');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (2, 1, 1, '五楼自习区');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (3, 1, 1, '三楼天井区');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (4, 1, 1, '四楼天井区');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (5, 1, 1, '六楼自习区');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (5, 1, 1, '六楼自习区');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (11, 1, 1, '朗读亭');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (12, 1, 1, '一层大厅');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (15, 3, 1, '4层工程技术类借阅区');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (17, 3, 1, '5层工程技术类借阅区');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (19, 3, 1, '5层自然科学借阅区');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (23, 3, 1, '6层社会科学借阅区（Ⅰ）');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (25, 3, 1, '7层社会科学类借阅区2');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (26, 3, 1, '7层社会科学类借阅区1');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (28, 3, 1, '7层自主学习空间（V）');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (29, 3, 1, '1层自主学习空间（Ⅰ）');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (30, 3, 1, '3层自主学习空间（Ⅱ）');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (31, 3, 1, '7层自主学习空间（Ⅳ）');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (32, 3, 1, '3层自主学习空间（Ⅲ）');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (33, 3, 1, '2层报刊阅览区');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (34, 3, 1, '4层计算机类借阅区');
INSERT INTO room (id, building_id, enabled, name)
VALUES (35, 3, 1, '6层社会科学类借阅区(Ⅱ)');
INSERT INTO room (id, building_id, enabled, name)
VALUES (7, 2, 1, '负一楼自习区');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (8, 2, 1, '一楼自习区');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (9, 2, 1, '三楼自习区A');
# INSERT INTO room (id, building_id, enabled, name)
# VALUES (10, 2, 1, '三楼自习区B');

# 将id=2的场馆关闭
UPDATE building t
SET t.enabled = 2
WHERE t.id = 2;
# 将id=2的场馆开放
UPDATE building t
SET t.enabled = 1
WHERE t.id = 2;