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
    # Add more languages here, e.g. 'en': [...], 'hi': [...], etc.
}

# Map db filename patterns to language codes
db_lang_map = {
    'Teb': 'te',  # Telugu
    # Add more mappings as needed, e.g. 'KJV': 'en'
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