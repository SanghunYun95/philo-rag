import os
import sys
import logging

# Ensure we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.database import get_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mapping metadata from update_metadata.sql
METADATA_MAPPING = {
    "Korean Translation of A Budget of Paradoxes Volume I": {"kr_title": "역설의 예산 1권", "thumbnail": "", "link": ""},
    "Korean Translation of A Pickle for the Knowing Ones": {"kr_title": "아는 자들을 위한 곤경", "thumbnail": "", "link": ""},
    "Korean Translation of A Treatise of Human Nature": {"kr_title": "인간 본성론", "thumbnail": "https://image.aladin.co.kr/product/435/90/coversum/8949705206_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=4359030"},
    "Korean Translation of A Vindication of the Rights of Woman": {"kr_title": "여권 옹호", "thumbnail": "https://image.aladin.co.kr/product/4569/0/coversum/8994054596_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=45690064"},
    "Korean Translation of Also sprach Zarathustra Ein Buch für Alle und Keinen German": {"kr_title": "차라투스트라는 이렇게 말했다", "thumbnail": "https://image.aladin.co.kr/product/45/40/coversum/s352934786_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=454014"},
    "Korean Translation of An Enquiry Concerning Human Understanding": {"kr_title": "인간 오성론", "thumbnail": "", "link": ""},
    "Korean Translation of An Essay Concerning Humane Understanding Volume 1": {"kr_title": "인간 오성론", "thumbnail": "https://image.aladin.co.kr/product/9059/21/coversum/k092535101_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=90592125"},
    "Korean Translation of Apology": {"kr_title": "소크라테스의 변명", "thumbnail": "https://image.aladin.co.kr/product/22/40/coversum/8931003714_3.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=224035"},
    "Korean Translation of Apology Crito and Phaedo of Socrates": {"kr_title": "소크라테스의 변론, 크리톤, 파이돈", "thumbnail": "https://image.aladin.co.kr/product/21679/27/coversum/k252636705_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=216792703"},
    "Korean Translation of As a man thinketh": {"kr_title": "생각하는 대로", "thumbnail": "https://image.aladin.co.kr/product/34558/80/coversum/k732933167_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=345588057"},
    "Korean Translation of Beyond Good and Evil": {"kr_title": "선악의 저편", "thumbnail": "https://image.aladin.co.kr/product/17492/31/coversum/8957336117_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=174923171"},
    "Korean Translation of Ciceros Tusculan Disputations": {"kr_title": "투스쿨룸 대화", "thumbnail": "https://image.aladin.co.kr/product/28633/67/coversum/8957337679_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=286336783"},
    "Korean Translation of De Officiis Latin": {"kr_title": "의무론", "thumbnail": "https://image.aladin.co.kr/product/85/24/coversum/8930606245_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=852420"},
    "Korean Translation of Democracy and Education An Introduction to the Philosophy of Education": {"kr_title": "민주주의와 교육", "thumbnail": "https://image.aladin.co.kr/product/92/29/coversum/8925400669_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=922961"},
    "Korean Translation of Discourse on the Method of Rightly Conducting Ones Reason and of Seeking Truth in the Sciences": {"kr_title": "방법서설", "thumbnail": "https://image.aladin.co.kr/product/34798/32/coversum/k152933225_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=347983217"},
    "Korean Translation of Ecce Homo": {"kr_title": "이 사람을 보라", "thumbnail": "https://image.aladin.co.kr/product/30235/68/coversum/8957338195_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=302356844"},
    "Korean Translation of Essays of Schopenhauer": {"kr_title": "인생론", "thumbnail": "https://image.aladin.co.kr/product/30866/59/coversum/8932440093_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=308665960"},
    "Korean Translation of Ethics": {"kr_title": "에티카", "thumbnail": "https://image.aladin.co.kr/product/99/33/coversum/8930625460_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=993377"},
    "Korean Translation of Euthyphro": {"kr_title": "에우티프론", "thumbnail": "https://image.aladin.co.kr/product/27217/11/coversum/8957337342_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=272171162"},
    "Korean Translation of Fundamental Principles of the Metaphysic of Morals": {"kr_title": "윤리 형이상학 정초", "thumbnail": "https://image.aladin.co.kr/product/16835/56/coversum/8957336036_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=168355651"},
    "Korean Translation of Gorgias": {"kr_title": "고르기아스", "thumbnail": "https://image.aladin.co.kr/product/26534/45/coversum/8957337210_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=265344583"},
    "Korean Translation of Human All Too Human A Book for Free Spirits": {"kr_title": "인간적인, 너무나 인간적인", "thumbnail": "https://image.aladin.co.kr/product/27/95/coversum/8970132619_3.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=279599"},
    "Korean Translation of Laws": {"kr_title": "법률", "thumbnail": "https://image.aladin.co.kr/product/464/64/coversum/8930606296_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=4646467"},
    "Korean Translation of Leviathan": {"kr_title": "리바이어던", "thumbnail": "https://image.aladin.co.kr/product/248/8/coversum/s392037901_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=2480851"},
    "Korean Translation of Meditations": {"kr_title": "명상록", "thumbnail": "https://image.aladin.co.kr/product/38459/20/coversum/k062135812_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=384592083"},
    "Korean Translation of Nature": {"kr_title": "자연", "thumbnail": "https://image.aladin.co.kr/product/3925/17/coversum/8956607648_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=39251790"},
    "Korean Translation of On Heroes Hero-Worship and the Heroic in History": {"kr_title": "영웅숭배론", "thumbnail": "https://image.aladin.co.kr/product/31353/18/coversum/8935678147_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=313531822"},
    "Korean Translation of On Liberty": {"kr_title": "자유론", "thumbnail": "https://image.aladin.co.kr/product/38193/81/coversum/k302034718_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=381938135"},
    "Korean Translation of On the Duty of Civil Disobedience": {"kr_title": "시민 불복종", "thumbnail": "https://image.aladin.co.kr/product/28419/44/coversum/k742835213_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=284194464"},
    "Korean Translation of On the Nature of Things": {"kr_title": "사물의 본성에 관하여", "thumbnail": "https://image.aladin.co.kr/product/1459/94/coversum/8957332227_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=14599483"},
    "Korean Translation of On War": {"kr_title": "전쟁론", "thumbnail": "https://image.aladin.co.kr/product/8652/41/coversum/8961951424_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=86524117"},
    "Korean Translation of Pascals Pensées": {"kr_title": "파스칼의 팡세", "thumbnail": "https://image.aladin.co.kr/product/36757/63/coversum/k952030294_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=367576319"},
    "Korean Translation of Perpetual Peace A Philosophical Essay": {"kr_title": "영구 평화론", "thumbnail": "https://image.aladin.co.kr/product/288/17/coversum/8930610439_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=2881780"},
    "Korean Translation of Phaedo": {"kr_title": "파이돈", "thumbnail": "https://image.aladin.co.kr/product/21679/27/coversum/k252636705_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=216792703"},
    "Korean Translation of Phaedrus": {"kr_title": "파이드로스", "thumbnail": "https://image.aladin.co.kr/product/182/6/coversum/8931005881_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=1820615"},
    "Korean Translation of Plutarchs Morals": {"kr_title": "플루타르코스 영웅전", "thumbnail": "https://image.aladin.co.kr/product/697/3/coversum/8991290337_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=6970308"},
    "Korean Translation of Politics A Treatise on Government": {"kr_title": "정치학", "thumbnail": "https://image.aladin.co.kr/product/439/98/coversum/8991290280_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=4399813"},
    "Korean Translation of Psychology of the Unconscious": {"kr_title": "무의식의 심리학", "thumbnail": "https://image.aladin.co.kr/product/30020/50/coversum/k222838355_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=300205010"},
    "Korean Translation of Reflections or Sentences and Moral Maxims": {"kr_title": "잠언과 도덕적 격언", "thumbnail": "", "link": ""},
    "Korean Translation of Second Treatise of Government": {"kr_title": "통치론", "thumbnail": "https://image.aladin.co.kr/product/30110/63/coversum/897291780x_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=301106377"},
    "Korean Translation of Siddhartha": {"kr_title": "싯다르타", "thumbnail": "https://image.aladin.co.kr/product/32/95/coversum/s062934786_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=329596"},
    "Korean Translation of Sun Tzŭ on the Art of War The Oldest Military Treatise in the World": {"kr_title": "손자병법", "thumbnail": "https://image.aladin.co.kr/product/37298/6/coversum/k292031545_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=372980631"},
    "Korean Translation of Symposium": {"kr_title": "향연", "thumbnail": "https://image.aladin.co.kr/product/21679/27/coversum/k252636705_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=216792703"},
    "Korean Translation of The Antichrist": {"kr_title": "안티크리스트", "thumbnail": "https://image.aladin.co.kr/product/3542/50/coversum/8957333444_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=35425033"},
    "Korean Translation of The Birth of Tragedy or Hellenism and Pessimism": {"kr_title": "비극의 탄생", "thumbnail": "https://image.aladin.co.kr/product/98/85/coversum/8957331077_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=988511"},
    "Korean Translation of The Communist Manifesto": {"kr_title": "공산당 선언", "thumbnail": "https://image.aladin.co.kr/product/14325/74/coversum/k172532941_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=143257420"},
    "Korean Translation of The Consolation of Philosophy": {"kr_title": "철학의 위안", "thumbnail": "https://image.aladin.co.kr/product/14712/19/coversum/k002532053_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=147121964"},
    "Korean Translation of The Critique of Pure Reason": {"kr_title": "순수이성비판", "thumbnail": "https://image.aladin.co.kr/product/66/97/coversum/8957330836_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=669748"},
    "Korean Translation of The Enchiridion": {"kr_title": "편람", "thumbnail": "https://image.aladin.co.kr/product/23132/6/coversum/k022637708_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=231320657"},
    "Korean Translation of The Ethics of Aristotle": {"kr_title": "니코마코스 윤리학", "thumbnail": "https://image.aladin.co.kr/product/3168/56/coversum/8991290523_3.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=31685631"},
    "Korean Translation of The Genealogy of Morals": {"kr_title": "도덕의 계보", "thumbnail": "https://image.aladin.co.kr/product/27464/78/coversum/8957337350_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=274647853"},
    "Korean Translation of The Marriage of Heaven and Hell": {"kr_title": "천국과 지옥의 결혼", "thumbnail": "https://image.aladin.co.kr/product/14/11/coversum/8937418460_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=141182"},
    "Korean Translation of The Poetics of Aristotle": {"kr_title": "시학", "thumbnail": "https://image.aladin.co.kr/product/26559/62/coversum/k392738937_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=265596201"},
    "Korean Translation of The Prince": {"kr_title": "군주론", "thumbnail": "https://image.aladin.co.kr/product/24943/22/coversum/k032632692_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=249432298"},
    "Korean Translation of The Principles of Psychology Volume 1 of 2": {"kr_title": "심리학의 원리 제1권", "thumbnail": "", "link": ""},
    "Korean Translation of The Problems of Philosophy": {"kr_title": "철학의 문제들", "thumbnail": "https://image.aladin.co.kr/product/38519/86/coversum/8961474928_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=385198660"},
    "Korean Translation of The Prophet": {"kr_title": "예언자", "thumbnail": "https://image.aladin.co.kr/product/12949/96/coversum/k672532485_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=129499645"},
    "Korean Translation of The Republic": {"kr_title": "국가", "thumbnail": "https://image.aladin.co.kr/product/1/68/coversum/8930606237_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=16812"},
    "Korean Translation of The Republic of Plato": {"kr_title": "국가", "thumbnail": "https://image.aladin.co.kr/product/1/68/coversum/8930606237_2.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=16812"},
    "Korean Translation of The social contract discourses": {"kr_title": "사회 계약론", "thumbnail": "https://image.aladin.co.kr/product/13917/20/coversum/8961672398_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=139172090"},
    "Korean Translation of Thus Spake Zarathustra A Book for All and None": {"kr_title": "차라투스트라는 이렇게 말했다", "thumbnail": "https://image.aladin.co.kr/product/45/40/coversum/s352934786_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=454014"},
    "Korean Translation of Utilitarianism": {"kr_title": "공리주의", "thumbnail": "https://image.aladin.co.kr/product/24304/80/coversum/k452630592_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=243048009"},
    "Korean Translation of Utopia": {"kr_title": "유토피아", "thumbnail": "https://image.aladin.co.kr/product/56/58/coversum/8974832534_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=565805"},
    "Korean Translation of Walden and On The Duty Of Civil Disobedience": {"kr_title": "월든", "thumbnail": "https://image.aladin.co.kr/product/1284/8/coversum/8956605416_3.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=12840843"},
    "Korean Translation of What Is Art": {"kr_title": "예술이란 무엇인가", "thumbnail": "https://image.aladin.co.kr/product/31976/76/coversum/k312834367_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=319767632"},
    "Korean Translation of 新序 Chinese": {"kr_title": "신서", "thumbnail": "https://image.aladin.co.kr/product/617/19/coversum/8949705818_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=6171917"},
    "Korean Translation of 日知錄 Chinese": {"kr_title": "일지록", "thumbnail": "https://image.aladin.co.kr/product/38390/55/coversum/k522135566_1.jpg", "link": "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=383905503"},
    "Korean Translation of 韓詩外傳 Complete Chinese": {"kr_title": "한시외전", "thumbnail": "", "link": ""},
}

def update_metadata():
    supabase = get_client()
    
    total = len(METADATA_MAPPING)
    logger.info(f"Starting update for {total} books...")
    
    for i, (title, meta) in enumerate(METADATA_MAPPING.items()):
        try:
            # Fetch all documents with this book title to update them individually
            # This preserves per-chunk metadata like chunk_index
            res = supabase.table("documents").select("id, metadata").eq("metadata->book_info->>title", title).execute()
            
            if not res.data:
                logger.warning(f"[{i+1}/{total}] Book not found in DB: {title}")
                continue
                
            # Update each document individually to preserve unique chunk_index
            for doc in res.data:
                update_data = {
                    "metadata": {
                        **doc["metadata"],
                        "kr_title": meta["kr_title"],
                        "thumbnail": meta["thumbnail"],
                        "link": meta["link"]
                    }
                }
                supabase.table("documents").update(update_data).eq("id", doc["id"]).execute()
            
            logger.info(f"[{i+1}/{total}] Successfully updated {len(res.data)} chunks: {meta['kr_title']}")
            
        except Exception as e:
            logger.error(f"[{i+1}/{total}] Error updating {title}: {e!r}")

if __name__ == "__main__":
    update_metadata()
