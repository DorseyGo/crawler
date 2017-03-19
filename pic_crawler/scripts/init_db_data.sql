-- ---------
-- VALUE should be initialized
-- --------

INSERT INTO PIC_DOMAINS(
	`DOMAIN`,
	`ABBREVIATION`,
	`RULE_4_NAVI_IMG`,
	`RULE_4_NAVI_2_NEXT_PAGE`,
	`PATTERN_EXTRACT_PAGINATION`,
	`RULE_4_LOCATE_DETAIL_IMG`,
	`ENABLE`
) VALUES(
	'www.jiinstyle.com',
	'JiinStyle',
	'//img[@class=\'thumb\']',
	'//a[@class=\'this\']',
	'r\'[pP][aA][gG][eE]=\d+',
	'//img[contains(@src, \'jk\') and contains(@src, \'upload\')]',
	1
), (
	'www.attrangs.co.kr',
	'AttRangs',
	'//div[@class=\'thumb\']/a/img',
	'',
	'',
	'//img[contains(@src, \'goodsm\')]',
	1
), (
	'www.marlangrouge.com',
	'MarLangRouge',
	'//div[@class=\'-image\']/a/img',
	'//a[@class=\'this\']',
	'r\'[pP][aA][gG][eE]=\d+',
	'//img[contains(@src, \'(\'), contains(@src, \')\')]',
	1
), (
	'www.styleonme.com',
	'StyleOnMe',
	'//img[@class=\'prdImg\']',
	'',
	'',
	'//img[@name=\'detail_images\']',
	1
), (
	'www.vividnco.com',
	'ViviDnco',
	'//div[@class=\'thumbnail\']/a/img',
	'//a[@class=\'this\']',
	'r\'[pP][aA][gG][eE]=\d+',
	'//img[contains(@src, \'aaa_\')]',
	1
), (
	'www.shescoming.co.kr',
	'ShesComing',
	'//img[@class=\'MS_prod_img_s\']',
	'//a[@class=\'now\']',
	'r\'[pP][aA][gG][eE]=\d+',
	'//img[contains(@src, \'i_\')]',
	1
), (
	'www.esther-st.co.kr',
	'Esther-ST',
	'//img[@class=\'thumb\']',
	'//a[@class=\'this\']',
	'r\'[pP][aA][gG][eE]=\d+',
	'//img[contains(@src, \'cafe\') and contains(@src, \'-product\')]',
	1
), (
	'',
	'',
	'//img[contains(@id, \'eListPrdImage\')]',
	'//a[@class=\'this\']',
	'r\'[pP][aA][gG][eE]=\d+',
	'//img[contains(@src, \'swellsee\')]',
	1
)
