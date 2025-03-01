from enum import Enum



class TestTuri(str, Enum):
    ASOSIY = 'asosiy'
    BLOK = 'blok'
    
    
class UmumiyButtons(str, Enum):
    ORTGA = "◀️Ortga"
    YOPISH = "❌Yopish"
    TESTNI_BOSHLASH = "🟢Testni boshlash"
    QOLLANMANI_OCHISH = "Qo'llanmani ochish 📖"
    YUBORISH = "Yuborish ✈️"
    ISMNI_TAHRIRLASH = "♻️Ismni tahrirlash"
    JAVOB_YUBORISHNI_BOSHLASH = "⚡️Javob yuborishni boshlash⚡️"
    

class TestTuriButtons(str, Enum):
    ASOSIY_FANLAR = "📕Asosiy fanlar"
    MAJBURIY_FANLAR = "📗Majburiy fanlar"
    BLOK_TEST = "📚Blok test"


class UserMenuButtons(str, Enum):
    TEST_ISHLASH = "👨‍💻Test ishlash"
    JAVOBLARNI_TEKSHIRISH = "🏁Javoblarni tekshirish"
    SOZLAMALAR = "🛠Sozlamalar"
    DOST_TAKLIF = "👥Do'stlarni taklif qilish"
    QOLLANMA = "📓Qo'llanma"
    UMUMIY_STATISTIKA = "🧮Umumiy statistika"


class AdminMenu(str, Enum):
    FILE_ID = "📥Fayl ID olish"
    XABAR_YUBORISH = 'Foydalanuvchilarga xabar yuborish 📤'
    XABAR_YUBORISHNI_TOXTATISH = 'Xabar yuborishni to\'xtatish ❌'
    

class MessageType(str, Enum):
    TEXT = 'text'
    PHOTO = 'photo'
    DOCUMENT = 'document'
    VIDEO = 'video'
    ANIMATION = 'animation'
    AUDIO = 'audio'
    STICKER = 'sticker'
    LOCATION = 'location'
    
    
KITOBLAR = [
    '📕',
    '📗',
    '📘',
    '📙'
]

STICKERS = [
    '❌',
    '✅'
]

MAQTOV = [
    "Natijangiz yaxshi, o'z ustingizda ishlashda savom eting 😊", # 0-60
    "Natijangiz juda yaxshi, tabriklayman 👍", # 61 - 80
    "Qoyilmaqom natija 👏, kelgusi ishlaringizda doimo omad tilayman 😊" # 81 - 100
]
