import os
import sqlite3

# Example: Add your full language/book mappings here
book_names = {
    'te': [  # Telugu
        "ఆదికాండము", "నిర్గమకాండము", "లేవీయకాండము", "సంఖ్యాకాండము", "ద్వితీయోపదేశకాండము",
        "యెహోషువ", "న్యాయాధిపతులు", "రూతు", "1 సమూయేలు", "2 సమూయేలు",
        "1 రాజులు", "2 రాజులు", "1 దినవృత్తాంతములు", "2 దినవృత్తాంతములు", "ఎజ్రా",
        "నెహెమ్యా", "ఎస్తేరు", "యోబు", "కీర్తనలు", "సామెతలు",
        "ప్రసంగి", "పరమగీతము", "యెషయా", "యిర్మియా", "విలాపవాక్యములు",
        "యెహెజ్కేలు", "దానియేలు", "హోషేయ", "యోవేలు", "ఆమోసు",
        "ఓబద్యా", "యోనా", "మీఖా", "నాహూము", "హబక్కూకు",
        "జెఫన్యా", "హగ్గయి", "జెకర్యా", "మలాకీ", "మత్తయి",
        "మార్కు", "లూకా", "యోహాను", "అపొస్తలుల కార్యములు", "రోమీయులకు",
        "1 కొరింథీయులకు", "2 కొరింథీయులకు", "గలతీయులకు", "ఎఫెసీయులకు", "ఫిలిప్పీయులకు",
        "కొలొస్సయులకు", "1 థెస్సలొనీకయులకు", "2 థెస్సలొనీకయులకు", "1 తిమోతికి", "2 తిమోతికి",
        "తీతుకు", "ఫిలేమోనుకు", "హెబ్రీయులకు", "యాకోబు", "1 పేతురు",
        "2 పేతురు", "1 యోహాను", "2 యోహాను", "3 యోహాను", "యూదా",
        "ప్రకటన గ్రంథము"
    ],
    'en': [  # English
        "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
        "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
        "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
        "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
        "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
        "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
        "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
        "Zephaniah", "Haggai", "Zechariah", "Malachi", "Matthew",
        "Mark", "Luke", "John", "Acts", "Romans",
        "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians",
        "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy",
        "Titus", "Philemon", "Hebrews", "James", "1 Peter",
        "2 Peter", "1 John", "2 John", "3 John", "Jude",
        "Revelation"
    ],
    'hi': [  # Hindi
        "उत्पत्ति", "निर्गमन", "लैव्यव्यवस्था", "गिनती", "व्यवस्थाविवरण",
        "यहोशू", "न्यायियों", "रूत", "1 शमूएल", "2 शमूएल",
        "1 राजा", "2 राजा", "1 इतिहास", "2 इतिहास", "एज्रा",
        "नहेमायाह", "एस्तेर", "अय्यूब", "भजन संहिता", "नीतिवचन",
        "सभोपदेशक", "श्रेष्ठगीत", "यशायाह", "यिर्मयाह", "विलापगीत",
        "यहेजकेल", "दानिय्येल", "होशे", "योएल", "आमोस",
        "ओबद्याह", "योना", "मीका", "नहूम", "हबक्कूक",
        "सपन्याह", "हाग्गै", "जकर्याह", "मलाकी", "मत्ती",
        "मरकुस", "लूका", "यूहन्ना", "प्रेरितों के काम", "रोमियों",
        "1 कुरिन्थियों", "2 कुरिन्थियों", "गलातियों", "इफिसियों", "फिलिप्पियों",
        "कुलुस्सियों", "1 थिस्सलुनीकियों", "2 थिस्सलुनीकियों", "1 तीमुथियुस", "2 तीमुथियुस",
        "तीतुस", "फिलेमोन", "इब्रानियों", "याकूब", "1 पतरस",
        "2 पतरस", "1 यूहन्ना", "2 यूहन्ना", "3 यूहन्ना", "यहूदा",
        "प्रकाशितवाक्य"
    ],
    'ta': [  # Tamil
        "ஆதியாகமம்", "விபவாகமம்", "லேவியராகமம்", "எண்ணாகமம்", "இயப்பாகமம்",
        "யோசுவா", "நியாயாதிபதிகள்", "ரூத்", "1 சாமுவேல்", "2 சாமுவேல்",
        "1 இராஜாக்கள்", "2 இராஜாக்கள்", "1 நாளாகமம்", "2 நாளாகமம்", "எஸ்றா",
        "நெகேமியா", "எஸ்தர்", "யோபு", "சங்கீதம்", "நீதிமொழிகள்",
        "பிரசங்கி", "உன்னதப்பாடல்", "ஏசாயா", "எரேமியா", "புலம்பல்",
        "எசேக்கியேல்", "தானியேல்", "ஓசியா", "யோவேல்", "ஆமோஸ்",
        "ஒபதியா", "யோனா", "மீக்கா", "நாகூம்", "ஆபக்கூக்",
        "செப்பனியா", "ஆக்காய்", "சகரியா", "மல்கியா", "மத்தேயு",
        "மாற்கு", "லூக்கா", "யோவான்", "அப்போஸ்தலர்", "ரோமர்",
        "1 கொரிந்தியர்", "2 கொரிந்தியர்", "கலாத்தியர்", "எபேசியர்", "பிலிப்பியர்",
        "கொலோசெயர்", "1 தெசலோனிகையர்", "2 தெசಲோನிகையர்", "1 தீமோத்தேயு", "2 தீமோத்தேயு",
        "தீத்து", "பிலேமோன்", "எபிரேயர்", "யாக்கோபு", "1 பேதுரு",
        "2 பேதురு", "1 யோவான்", "2 யோவான்", "3 யோவான்", "யூதா",
        "வெளிப்படுத்தின விசேஷம்"
    ],
    'kn': [  # Kannada
        "ಆದಿಕಾಂಡ", "ನಿರ್ಗಮಕಾಂಡ", "ಲೇವ್ಯಕಾಂಡ", "ಸಂಖ್ಯಾಕಾಂಡ", "ದ್ವಿತೀಯೋಪದೇಶಕಾಂಡ",
        "ಯೆಹೋಶುವ", "ನ್ಯಾಯಾಧಿಪತಿಗಳು", "ರೂತ್", "1 ಶಮೂವೇಲ", "2 ಶಮೂವೇಲ",
        "1 ರಾಜರು", "2 ರಾಜರು", "1 ದಿನಚರಿತ್ರೆ", "2 ದಿನಚರಿತ್ರೆ", "ಎಜ್ರಾ",
        "ನೆಹೆಮ್ಯಾ", "ಎಸ್ತೇರ್", "ಅಯೋಬು", "ಕೀರ್ತನೆಗಳು", "ಸಾಮೆತಿಗಳು",
        "ಪ್ರಸಂಗಿ", "ಪರಮಗೀತ", "ಯೆಶಾಯ", "ಯೆರೆಮಿಯಾ", "ವಿಲಾಪಗೀತೆಗಳು",
        "ಯೆಹೆಜ್ಕೇಲ್", "ದಾನಿಯೇಲ್", "ಹೋಶೇಯ", "ಯೋವೇಲ್", "ಆಮೋಸ್",
        "ಓಬದ್ಯಾ", "ಯೋನ", "ಮೀಖಾ", "ನಹೂಮ್", "ಹಬಕ್ಕೂಕ",
        "ಜೆಫನ್ಯಾ", "ಹಗ್ಗೈ", "ಜೆಕರ್ಯಾ", "ಮಲಾಕಿ", "ಮತ್ತಾಯ",
        "ಮಾರ್ಕ", "ಲೂಕ", "ಯೋಹಾನ", "ಪ್ರೇರಿತರು", "ರೋಮಾಪುರದವರಿಗೆ",
        "1 ಕೊರಿಂಥದವರಿಗೆ", "2 ಕೊರಿಂಥದವರಿಗೆ", "ಗಲಾತ್ಯದವರಿಗೆ", "ಎಫೆಸಿಯವರಿಗೆ", "ಫಿಲಿಪ್ಪಿಯವರಿಗೆ",
        "ಕೊಲೊಸ್ಸೆಯವರಿಗೆ", "1 ಥೆಸಲೋನಿಕದವರಿಗೆ", "2 ಥೆಸಲೋನಿಕದವರಿಗೆ", "1 ತಿಮೋಥಿಗೆ", "2 ತಿಮೋಥಿಗೆ",
        "ತೀತಿಗೆ", "ಫಿಲೇಮೋನಿಗೆ", "ಹೆಬ್ರೂಗಳಿಗೆ", "ಯಾಕೋಬ", "1 ಪೇತ್ರ",
        "2 ಪೇತ್ರ", "1 ಯೋಹಾನ", "2 ಯೋಹಾನ", "3 ಯೋಹಾನ", "ಯೂದ",
        "ಪ್ರಕಟನೆ"
    ],
    # Add more languages here, e.g. 'en': [...], 'hi': [...], etc.
}

# Map db filename patterns to language codes
db_lang_map = {
    'ACV': 'en',         # A Conservative Version
    'KJV': 'en',         # King James Version
    'AKJV': 'en',        # American King James Version
    'ASV': 'en',         # American Standard Version
    'Alb': 'sq',         # Albanian
    'BBE': 'en',         # Bible in Basic English
    'BSB': 'en',         # Berean Study Bible
    'BurJudson': 'my',   # Burmese
    'CSlElizabeth': 'cu',# Church Slavonic
    'CebPinadayag': 'ceb',# Cebuano
    'ChiSB': 'zh',       # Chinese (Simplified)
    'ChiUn': 'zh',       # Chinese
    'ChiUnL': 'zh',      # Chinese (Traditional)
    'CopSahBible2': 'cop',# Coptic
    'CroSaric': 'hr',    # Croatian
    'CzeBKR': 'cs',      # Czech
    'CzeCSP': 'cs',      # Czech
    'DRC': 'en',         # Douay-Rheims Challoner
    'DaOT1871NT1907': 'da',# Danish
    'Darby': 'en',       # Darby Bible
    'DutSVV': 'nl',      # Dutch
    'DutSVVA': 'nl',     # Dutch
    'Esperanto': 'eo',   # Esperanto
    'Est': 'et',         # Estonian
    'FinBiblia': 'fi',   # Finnish
    'FinPR': 'fi',       # Finnish
    'FinSTLK2017': 'fi', # Finnish
    'FreBBB': 'fr',      # French
    'FreBDM1744': 'fr',  # French
    'FreCrampon': 'fr',  # French
    'FreJND': 'fr',      # French
    'FreOltramare1874': 'fr', # French
    'FrePGR': 'fr',      # French
    'Geneva1599': 'en',  # Geneva Bible
    'GerBoLut': 'de',    # German
    'GerElb1871': 'de',  # German
    'GerElb1905': 'de',  # German
    'GerGruenewald': 'de',# German
    'GerMenge': 'de',    # German
    'GerSch': 'de',      # German
    'GerTextbibel': 'de',# German
    'GerZurcher': 'de',  # German
    'GreVamvas': 'el',   # Greek
    'Haitian': 'ht',     # Haitian Creole
    'HebModern': 'he',   # Hebrew
    'HunKar': 'hu',      # Hungarian
    'JPS': 'en',         # Jewish Publication Society
    'Afrikaans': 'af',   # Afrikaans
    'Bengali': 'bn',     # Bengali
    'Hindi': 'hi',       # Hindi
    'Gujarati': 'gu',    # Gujarati
    'Xhosa': 'xh',       # Xhosa
    'Zulu': 'zu',        # Zulu
    'Kannada': 'kn',     # Kannada
    'Marathi': 'mr',     # Marathi
    'Nepali': 'ne',      # Nepali
    'Oryia': 'or',       # Oryia
    'Punjabi': 'pa',     # Punjabi
    'Sapedi': 'nso',     # Sapedi
    'Tamil': 'ta',       # Tamil
    'JapBungo': 'ja',    # Japanese
    'JapKougo': 'ja',    # Japanese
    'Jubilee2000': 'en', # Jubilee Bible 2000
    'KJVA': 'en',        # King James Version with Apocrypha
    'KJVPCE': 'en',      # King James Version Pure Cambridge Edition
    'KLV': 'ko',         # Korean Living Bible
    'KorHKJV': 'ko',     # Korean HKJV
    'KorRV': 'ko',       # Korean Revised Version
    'LEB': 'en',         # Lexham English Bible
    'LvGluck8': 'lv',    # Latvian
    'MKJV': 'en',        # Modern King James Version
    'Mal1910': 'ml',     # Malayalam
    'ManxGaelic': 'gv',  # Manx Gaelic
    'Maori': 'mi',       # Maori
    'MapM': 'arn',       # Mapudungun
    'Mg1865': 'mg',      # Malagasy
    'NHEB': 'en',        # New Heart English Bible
    'NHEBJE': 'en',      # New Heart English Bible with Jehovah's Name
    'NHEBME': 'en',      # New Heart English Bible Messianic Edition
    'NlCanisius1939': 'nl',# Dutch
    'NorSMB': 'se',      # Sami
    'Norsk': 'no',       # Norwegian
    'PolGdanska': 'pl',  # Polish
    'PolUGdanska': 'pl', # Polish
    'PorBLivre': 'pt',   # Portuguese
    'PorBLivreTR': 'pt', # Portuguese
    'PorNVA': 'pt',      # Portuguese
    'RLT': 'en',         # Revised Literal Translation
    'RNKJV': 'en',       # Revised New King James Version
    'RWebster': 'en',    # Webster's Bible
    'Rotherham': 'en',   # Rotherham's Emphasized Bible
    'RusMakarij': 'ru',  # Russian
    'RusSynodal': 'ru',  # Russian
    'SloChraska': 'sl',  # Slovenian
    'SloKJV': 'sl',      # Slovenian
    'SpaRV': 'es',       # Spanish
    'SpaRV1865': 'es',   # Spanish
    'SrKDEkavski': 'sr', # Serbian
    'SrKDIjekav': 'sr',  # Serbian
    'Swe1917': 'sv',     # Swedish
    'SweKarlXII1873': 'sv',# Swedish
    'TagAngBiblia': 'tl',# Tagalog
    'Teb': 'te',         # Telugu
    'ThaiKJV': 'th',     # Thai
    'TpiKJPB': 'tpi',    # Tok Pisin
    'UKJV': 'en',        # Updated King James Version
    'Viet': 'vi',        # Vietnamese
    'Vulgate': 'la',     # Latin
    'WLC': 'he',         # Hebrew
    'Webster': 'en',     # Webster's Bible
    'Wycliffe': 'en',    # Wycliffe Bible
    'YLT': 'en',         # Young's Literal Translation
}

def get_language_from_filename(filename):
    for key in db_lang_map:
        if key.lower() in filename.lower():
            return db_lang_map[key]
    return None

def get_books_table_name(db_path):
    # Try to find the books table name from the db filename
    base = os.path.splitext(os.path.basename(db_path))[0]
    # Some tables are like Teb.db -> books, others like KJV.db -> KJV_books
    possible_names = [f"{base}_books", "books"]
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for name in possible_names:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (name,))
        if cursor.fetchone():
            conn.close()
            return name
    conn.close()
    return None

def update_books_table(db_path, lang_code):
    books = book_names[lang_code]
    table_name = get_books_table_name(db_path)
    if not table_name:
        print(f"Books table not found in {db_path}")
        return
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for i, name in enumerate(books, 1):
        cursor.execute(f"UPDATE {table_name} SET name=? WHERE id=?", (name, i))
    conn.commit()
    conn.close()
    print(f"Updated {db_path} ({table_name}) with {lang_code} book names.")

folder = r'd:\flutter projects\start.io\polylanguagebible\version dbs'
for file in os.listdir(folder):
    if file.endswith('.db'):
        lang = get_language_from_filename(file)
        if lang and lang in book_names:
            update_books_table(os.path.join(folder, file), lang)