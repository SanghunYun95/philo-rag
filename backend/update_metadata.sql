CREATE INDEX IF NOT EXISTS idx_documents_book_title ON documents ((metadata->'book_info'->>'title'));


SET statement_timeout = '120s'; -- Increase timeout to be safe

BEGIN;

UPDATE documents
SET metadata = metadata || '{"kr_title": "역설의 예산 1권", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of A Budget of Paradoxes Volume I';

UPDATE documents
SET metadata = metadata || '{"kr_title": "아는 자들을 위한 곤경", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of A Pickle for the Knowing Ones';

UPDATE documents
SET metadata = metadata || '{"kr_title": "인간 본성론", "thumbnail": "https://image.aladin.co.kr/product/435/90/coversum/8949705206_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=4359030&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of A Treatise of Human Nature';

UPDATE documents
SET metadata = metadata || '{"kr_title": "여권 옹호", "thumbnail": "https://image.aladin.co.kr/product/4569/0/coversum/8994054596_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=45690064&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of A Vindication of the Rights of Woman';

UPDATE documents
SET metadata = metadata || '{"kr_title": "차라투스트라는 이렇게 말했다", "thumbnail": "https://image.aladin.co.kr/product/45/40/coversum/s352934786_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=454014&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Also sprach Zarathustra Ein Buch für Alle und Keinen German';

UPDATE documents
SET metadata = metadata || '{"kr_title": "인간 오성론", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of An Enquiry Concerning Human Understanding';

UPDATE documents
SET metadata = metadata || '{"kr_title": "인간 오성론", "thumbnail": "https://image.aladin.co.kr/product/9059/21/coversum/k092535101_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=90592125&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of An Essay Concerning Humane Understanding Volume 1';

UPDATE documents
SET metadata = metadata || '{"kr_title": "소크라테스의 변명", "thumbnail": "https://image.aladin.co.kr/product/22/40/coversum/8931003714_3.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=224035&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Apology';

UPDATE documents
SET metadata = metadata || '{"kr_title": "소크라테스의 변론, 크리톤, 파이돈", "thumbnail": "https://image.aladin.co.kr/product/21679/27/coversum/k252636705_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=216792703&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Apology Crito and Phaedo of Socrates';

UPDATE documents
SET metadata = metadata || '{"kr_title": "생각하는 대로", "thumbnail": "https://image.aladin.co.kr/product/34558/80/coversum/k732933167_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=345588057&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of As a man thinketh';

UPDATE documents
SET metadata = metadata || '{"kr_title": "베이컨 수상록; 고대인의 지혜", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Bacons Essays and Wisdom of the Ancients';

UPDATE documents
SET metadata = metadata || '{"kr_title": "선악의 저편", "thumbnail": "https://image.aladin.co.kr/product/17492/31/coversum/8957336117_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=174923171&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Beyond Good and Evil';

UPDATE documents
SET metadata = metadata || '{"kr_title": "투스쿨룸 대화", "thumbnail": "https://image.aladin.co.kr/product/28633/67/coversum/8957337679_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=286336783&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Ciceros Tusculan Disputations';

UPDATE documents
SET metadata = metadata || '{"kr_title": "의무론", "thumbnail": "https://image.aladin.co.kr/product/85/24/coversum/8930606245_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=852420&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of De Officiis Latin';

UPDATE documents
SET metadata = metadata || '{"kr_title": "민주주의와 교육", "thumbnail": "https://image.aladin.co.kr/product/92/29/coversum/8925400669_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=922961&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Democracy and Education An Introduction to the Philosophy of Education';

UPDATE documents
SET metadata = metadata || '{"kr_title": "미국의 민주주의 2권", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Democracy in America Volume 2';

UPDATE documents
SET metadata = metadata || '{"kr_title": "악마학 및 악마 전승", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Demonology and Devil-lore';

UPDATE documents
SET metadata = metadata || '{"kr_title": "방법서설", "thumbnail": "https://image.aladin.co.kr/product/34798/32/coversum/k152933225_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=347983217&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Discourse on the Method of Rightly Conducting Ones Reason and of Seeking Truth in the Sciences';

UPDATE documents
SET metadata = metadata || '{"kr_title": "이 사람을 보라", "thumbnail": "https://image.aladin.co.kr/product/30235/68/coversum/8957338195_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=302356844&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Ecce Homo';

UPDATE documents
SET metadata = metadata || '{"kr_title": "에머슨 수상록", "thumbnail": "https://image.aladin.co.kr/product/10/4/coversum/8972432954_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=100408&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Essays by Ralph Waldo Emerson';

UPDATE documents
SET metadata = metadata || '{"kr_title": "인생론", "thumbnail": "https://image.aladin.co.kr/product/30866/59/coversum/8932440093_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=308665960&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Essays of Schopenhauer';

UPDATE documents
SET metadata = metadata || '{"kr_title": "에티카", "thumbnail": "https://image.aladin.co.kr/product/99/33/coversum/8930625460_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=993377&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Ethics';

UPDATE documents
SET metadata = metadata || '{"kr_title": "에밀리 포스트의 에티켓", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Etiquette';

UPDATE documents
SET metadata = metadata || '{"kr_title": "에우티프론", "thumbnail": "https://image.aladin.co.kr/product/27217/11/coversum/8957337342_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=272171162&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Euthyphro';

UPDATE documents
SET metadata = metadata || '{"kr_title": "윤리 형이상학 정초", "thumbnail": "https://image.aladin.co.kr/product/16835/56/coversum/8957336036_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=168355651&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Fundamental Principles of the Metaphysic of Morals';

UPDATE documents
SET metadata = metadata || '{"kr_title": "괴테의 색채론", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Goethes Theory of Colours';

UPDATE documents
SET metadata = metadata || '{"kr_title": "고르기아스", "thumbnail": "https://image.aladin.co.kr/product/26534/45/coversum/8957337210_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=265344583&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Gorgias';

UPDATE documents
SET metadata = metadata || '{"kr_title": "우리는 어떻게 생각하는가", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of How We Think';

UPDATE documents
SET metadata = metadata || '{"kr_title": "인간적인, 너무나 인간적인", "thumbnail": "https://image.aladin.co.kr/product/27/95/coversum/8970132619_3.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=279599&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Human All Too Human A Book for Free Spirits';

UPDATE documents
SET metadata = metadata || '{"kr_title": "베일 벗은 이시스", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Isis unveiled Volume 1 of 2 Science A master-key to mysteries of ancient and modern science and theology';

UPDATE documents
SET metadata = metadata || '{"kr_title": "법률", "thumbnail": "https://image.aladin.co.kr/product/464/64/coversum/8930606296_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=4646467&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Laws';

UPDATE documents
SET metadata = metadata || '{"kr_title": "리바이어던", "thumbnail": "https://image.aladin.co.kr/product/248/8/coversum/s392037901_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=2480851&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Leviathan';

UPDATE documents
SET metadata = metadata || '{"kr_title": "명상록", "thumbnail": "https://image.aladin.co.kr/product/38459/20/coversum/k062135812_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=384592083&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Meditations';

UPDATE documents
SET metadata = metadata || '{"kr_title": "자연", "thumbnail": "https://image.aladin.co.kr/product/3925/17/coversum/8956607648_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=39251790&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Nature';

UPDATE documents
SET metadata = metadata || '{"kr_title": "영웅숭배론", "thumbnail": "https://image.aladin.co.kr/product/31353/18/coversum/8935678147_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=313531822&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of On Heroes Hero-Worship and the Heroic in History';

UPDATE documents
SET metadata = metadata || '{"kr_title": "자유론", "thumbnail": "https://image.aladin.co.kr/product/38193/81/coversum/k302034718_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=381938135&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of On Liberty';

UPDATE documents
SET metadata = metadata || '{"kr_title": "시민 불복종", "thumbnail": "https://image.aladin.co.kr/product/28419/44/coversum/k742835213_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=284194464&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of On the Duty of Civil Disobedience';

UPDATE documents
SET metadata = metadata || '{"kr_title": "사물의 본성에 관하여", "thumbnail": "https://image.aladin.co.kr/product/1459/94/coversum/8957332227_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=14599483&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of On the Nature of Things';

UPDATE documents
SET metadata = metadata || '{"kr_title": "전쟁론", "thumbnail": "https://image.aladin.co.kr/product/8652/41/coversum/8961951424_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=86524117&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of On War';

UPDATE documents
SET metadata = metadata || '{"kr_title": "파스칼의 팡세", "thumbnail": "https://image.aladin.co.kr/product/36757/63/coversum/k952030294_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=367576319&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Pascals Pensées';

UPDATE documents
SET metadata = metadata || '{"kr_title": "영구 평화론", "thumbnail": "https://image.aladin.co.kr/product/288/17/coversum/8930610439_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=2881780&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Perpetual Peace A Philosophical Essay';

UPDATE documents
SET metadata = metadata || '{"kr_title": "파이돈", "thumbnail": "https://image.aladin.co.kr/product/21679/27/coversum/k252636705_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=216792703&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Phaedo';

UPDATE documents
SET metadata = metadata || '{"kr_title": "파이드로스", "thumbnail": "https://image.aladin.co.kr/product/182/6/coversum/8931005881_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=1820615&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Phaedrus';

UPDATE documents
SET metadata = metadata || '{"kr_title": "플라톤과 소크라테스의 동반자들", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Plato and the Other Companions of Sokrates 3rd ed Volume 1';

UPDATE documents
SET metadata = metadata || '{"kr_title": "플루타르코스 영웅전", "thumbnail": "https://image.aladin.co.kr/product/697/3/coversum/8991290337_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=6970308&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Plutarchs Morals';

UPDATE documents
SET metadata = metadata || '{"kr_title": "정치학", "thumbnail": "https://image.aladin.co.kr/product/439/98/coversum/8991290280_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=4399813&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Politics A Treatise on Government';

UPDATE documents
SET metadata = metadata || '{"kr_title": "실용주의: 어떤 오래된 사고방식에 대한 새로운 이름", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Pragmatism A New Name for Some Old Ways of Thinking';

UPDATE documents
SET metadata = metadata || '{"kr_title": "그리스 정신사: 영혼 숭배와 불멸에 대한 신념", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Psyche The Cult of Souls and Belief in Immortality among the Greeks';

UPDATE documents
SET metadata = metadata || '{"kr_title": "무의식의 심리학", "thumbnail": "https://image.aladin.co.kr/product/30020/50/coversum/k222838355_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=300205010&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Psychology of the Unconscious';

UPDATE documents
SET metadata = metadata || '{"kr_title": "잠언과 도덕적 격언", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Reflections or Sentences and Moral Maxims';

UPDATE documents
SET metadata = metadata || '{"kr_title": "신의 사랑에 대한 계시", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Revelations of Divine Love';

UPDATE documents
SET metadata = metadata || '{"kr_title": "로마 스토아주의", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Roman Stoicism';

UPDATE documents
SET metadata = metadata || '{"kr_title": "통치론", "thumbnail": "https://image.aladin.co.kr/product/30110/63/coversum/897291780x_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=301106377&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Second Treatise of Government';

UPDATE documents
SET metadata = metadata || '{"kr_title": "싯다르타", "thumbnail": "https://image.aladin.co.kr/product/32/95/coversum/s062934786_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=329596&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Siddhartha';

UPDATE documents
SET metadata = metadata || '{"kr_title": "손자병법", "thumbnail": "https://image.aladin.co.kr/product/37298/6/coversum/k292031545_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=372980631&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Sun Tzŭ on the Art of War The Oldest Military Treatise in the World';

UPDATE documents
SET metadata = metadata || '{"kr_title": "향연", "thumbnail": "https://image.aladin.co.kr/product/21679/27/coversum/k252636705_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=216792703&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Symposium';

UPDATE documents
SET metadata = metadata || '{"kr_title": "우울의 해부", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Anatomy of Melancholy';

UPDATE documents
SET metadata = metadata || '{"kr_title": "안티크리스트", "thumbnail": "https://image.aladin.co.kr/product/3542/50/coversum/8957333444_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=35425033&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Antichrist';

UPDATE documents
SET metadata = metadata || '{"kr_title": "비극의 탄생", "thumbnail": "https://image.aladin.co.kr/product/98/85/coversum/8957331077_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=988511&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Birth of Tragedy or Hellenism and Pessimism';

UPDATE documents
SET metadata = metadata || '{"kr_title": "우상의 황혼", "thumbnail": "https://image.aladin.co.kr/product/6419/39/coversum/8957334513_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=64193963&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Case of Wagner Nietzsche Contra Wagner and Selected Aphorisms';

UPDATE documents
SET metadata = metadata || '{"kr_title": "신의 도시 1", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The City of God Volume I';

UPDATE documents
SET metadata = metadata || '{"kr_title": "신의 도성 2", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The City of God Volume II';

UPDATE documents
SET metadata = metadata || '{"kr_title": "공산당 선언", "thumbnail": "https://image.aladin.co.kr/product/14325/74/coversum/k172532941_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=143257420&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Communist Manifesto';

UPDATE documents
SET metadata = metadata || '{"kr_title": "고백록", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Confessions of St Augustine';

UPDATE documents
SET metadata = metadata || '{"kr_title": "철학의 위안", "thumbnail": "https://image.aladin.co.kr/product/14712/19/coversum/k002532053_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=147121964&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Consolation of Philosophy';

UPDATE documents
SET metadata = metadata || '{"kr_title": "순수이성비판", "thumbnail": "https://image.aladin.co.kr/product/66/97/coversum/8957330836_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=669748&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Critique of Pure Reason';

UPDATE documents
SET metadata = metadata || '{"kr_title": "편람", "thumbnail": "https://image.aladin.co.kr/product/23132/6/coversum/k022637708_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=231320657&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Enchiridion';

UPDATE documents
SET metadata = metadata || '{"kr_title": "쇼펜하우어 철학 에세이: 비관주의 연구", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Essays of Arthur Schopenhauer Studies in Pessimism';

UPDATE documents
SET metadata = metadata || '{"kr_title": "행복론", "thumbnail": "https://image.aladin.co.kr/product/30866/59/coversum/8932440093_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=308665960&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Essays of Arthur Schopenhauer the Wisdom of Life';

UPDATE documents
SET metadata = metadata || '{"kr_title": "니코마코스 윤리학", "thumbnail": "https://image.aladin.co.kr/product/3168/56/coversum/8991290523_3.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=31685631&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Ethics of Aristotle';

UPDATE documents
SET metadata = metadata || '{"kr_title": "도덕의 계보", "thumbnail": "https://image.aladin.co.kr/product/27464/78/coversum/8957337350_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=274647853&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Genealogy of Morals';

UPDATE documents
SET metadata = metadata || '{"kr_title": "대심문관", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Grand Inquisitor';

UPDATE documents
SET metadata = metadata || '{"kr_title": "마법의 역사", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The history of magic including a clear and precise exposition of its procedure its rites and its mysteries';

UPDATE documents
SET metadata = metadata || '{"kr_title": "카마수트라", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Kama Sutra of Vatsyayana';

UPDATE documents
SET metadata = metadata || '{"kr_title": "위대한 철학자들의 생애와 사상", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Lives and Opinions of Eminent Philosophers';

UPDATE documents
SET metadata = metadata || '{"kr_title": "목요일의 사나이", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Man Who Was Thursday A Nightmare';

UPDATE documents
SET metadata = metadata || '{"kr_title": "천국과 지옥의 결혼", "thumbnail": "https://image.aladin.co.kr/product/14/11/coversum/8937418460_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=141182&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Marriage of Heaven and Hell';

UPDATE documents
SET metadata = metadata || '{"kr_title": "마르쿠스 아우렐리우스 황제의 명상록", "thumbnail": "https://image.aladin.co.kr/product/38459/20/coversum/k062135812_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=384592083&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Meditations of the Emperor Marcus Aurelius Antoninus';

UPDATE documents
SET metadata = metadata || '{"kr_title": "시학", "thumbnail": "https://image.aladin.co.kr/product/26559/62/coversum/k392738937_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=265596201&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Poetics of Aristotle';

UPDATE documents
SET metadata = metadata || '{"kr_title": "군주론", "thumbnail": "https://image.aladin.co.kr/product/24943/22/coversum/k032632692_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=249432298&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Prince';

UPDATE documents
SET metadata = metadata || '{"kr_title": "심리학의 원리 제1권", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Principles of Psychology Volume 1 of 2';

UPDATE documents
SET metadata = metadata || '{"kr_title": "철학의 문제들", "thumbnail": "https://image.aladin.co.kr/product/38519/86/coversum/8961474928_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=385198660&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Problems of Philosophy';

UPDATE documents
SET metadata = metadata || '{"kr_title": "예언자", "thumbnail": "https://image.aladin.co.kr/product/12949/96/coversum/k672532485_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=129499645&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Prophet';

UPDATE documents
SET metadata = metadata || '{"kr_title": "국가", "thumbnail": "https://image.aladin.co.kr/product/1/68/coversum/8930606237_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=16812&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Republic';

UPDATE documents
SET metadata = metadata || '{"kr_title": "국가", "thumbnail": "https://image.aladin.co.kr/product/1/68/coversum/8930606237_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=16812&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Republic of Plato';

UPDATE documents
SET metadata = metadata || '{"kr_title": "비밀 교리 1권", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Secret Doctrine Vol 1 of 4';

UPDATE documents
SET metadata = metadata || '{"kr_title": "비밀 교리 제2권", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Secret Doctrine Vol 2 of 4';

UPDATE documents
SET metadata = metadata || '{"kr_title": "사회 계약론", "thumbnail": "https://image.aladin.co.kr/product/13917/20/coversum/8961672398_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=139172090&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The social contract discourses';

UPDATE documents
SET metadata = metadata || '{"kr_title": "신성한 노래", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Song Celestial Or Bhagavad-Gîtâ from the Mahâbhârata';

UPDATE documents
SET metadata = metadata || '{"kr_title": "프리메이슨 상징학", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The symbolism of Freemasonry Illustrating and explaining its science and philosophy its legends myths and symbols';

UPDATE documents
SET metadata = metadata || '{"kr_title": "우상의 황혼, 혹은 망치로 철학하기 : 안티크리스트", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Twilight of the Idols or How to Philosophize with the Hammer The Antichrist';

UPDATE documents
SET metadata = metadata || '{"kr_title": "의지의 힘", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The Will to Believe and Other Essays in Popular Philosophy';

UPDATE documents
SET metadata = metadata || '{"kr_title": "의지와 표상으로서의 세계 1", "thumbnail": "https://image.aladin.co.kr/product/9560/70/coversum/8949714221_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=95607072&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of The World as Will and Idea Vol 1 of 3';

UPDATE documents
SET metadata = metadata || '{"kr_title": "차라투스트라는 이렇게 말했다", "thumbnail": "https://image.aladin.co.kr/product/45/40/coversum/s352934786_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=454014&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Thus Spake Zarathustra A Book for All and None';

UPDATE documents
SET metadata = metadata || '{"kr_title": "공리주의", "thumbnail": "https://image.aladin.co.kr/product/24304/80/coversum/k452630592_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=243048009&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Utilitarianism';

UPDATE documents
SET metadata = metadata || '{"kr_title": "유토피아", "thumbnail": "https://image.aladin.co.kr/product/56/58/coversum/8974832534_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=565805&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Utopia';

UPDATE documents
SET metadata = metadata || '{"kr_title": "월든", "thumbnail": "https://image.aladin.co.kr/product/1284/8/coversum/8956605416_3.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=12840843&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of Walden and On The Duty Of Civil Disobedience';

UPDATE documents
SET metadata = metadata || '{"kr_title": "예술이란 무엇인가", "thumbnail": "https://image.aladin.co.kr/product/31976/76/coversum/k312834367_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=319767632&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of What Is Art';

UPDATE documents
SET metadata = metadata || '{"kr_title": "신서", "thumbnail": "https://image.aladin.co.kr/product/617/19/coversum/8949705818_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=6171917&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of 新序 Chinese';

UPDATE documents
SET metadata = metadata || '{"kr_title": "일지록", "thumbnail": "https://image.aladin.co.kr/product/38390/55/coversum/k522135566_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=383905503&amp;partner=openAPI&amp;start=api"}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of 日知錄 Chinese';

UPDATE documents
SET metadata = metadata || '{"kr_title": "한시외전", "thumbnail": "", "link": ""}'::jsonb
WHERE metadata->'book_info'->>'title' = 'Korean Translation of 韓詩外傳 Complete Chinese';

COMMIT;