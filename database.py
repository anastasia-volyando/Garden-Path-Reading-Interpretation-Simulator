import sqlite3

DB_NAME = "garden_path.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sentences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sentence TEXT NOT NULL,
            disambiguating_word TEXT NOT NULL,
            trap_explanation TEXT NOT NULL,
            correct_meaning TEXT NOT NULL,
            wrong_keywords TEXT NOT NULL,
            correct_keywords TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sentence_id INTEGER,
            user_interpretation TEXT,
            longest_pause_word TEXT,
            longest_pause_time REAL,
            interpretation_result TEXT,
            FOREIGN KEY(sentence_id) REFERENCES sentences(id)
        )
    """)

    conn.commit()
    conn.close()


def insert_sample_sentences():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM sentences")
    count = cursor.fetchone()[0]

    if count == 0:
        sample_sentences = [
            (
                "The old man the boat",
                "boat",
                "The reader may first interpret 'old' as an adjective and 'man' as a noun.",
                "Old people operate the boat.",
                "old man,old men,man is old",
                "old people,operate,man the boat"
            ),
            (
                "The man whistling tunes pianos",
                "pianos",
                "The reader may first interpret 'tunes' as a noun, but it is actually a verb.",
                "The man who is whistling also tunes pianos.",
                "whistling tunes,songs,melodies",
                "tunes pianos,fixes pianos,adjusts pianos"
            ),
            (
                "The horse raced past the barn fell",
                "fell",
                "The reader may first interpret 'raced' as the main verb, but 'fell' forces reanalysis.",
                "The horse that was raced past the barn fell.",
                "horse ran,raced past,ran past",
                "was raced,that was raced,fell"
            ),
            (
                "While Anna dressed the baby played in the crib",
                "played",
                "The reader may first think Anna dressed the baby, but 'played' shows that the baby is the subject of a new clause.",
                "While Anna dressed herself, the baby played in the crib.",
                "dressed the baby,anna dressed baby",
                "dressed herself,baby played,played in the crib"
            ),
            (
                "The government plans to raise taxes were defeated",
                "were",
                "The reader may first interpret 'plans' as a verb, but 'were defeated' shows that 'plans' is a noun.",
                "The government's plans to raise taxes were defeated.",
                "government plans,making plans,plans to raise",
                "plans were defeated,government's plans,were defeated"
            ),
            (
                "The author wrote the novel was likely to be a best-seller",
                "was",
                "The reader may first think 'wrote' is the main verb of the sentence, but 'was' forces reanalysis.",
                "The novel that the author wrote was likely to be a best-seller.",
                "author wrote novel,wrote the novel",
                "novel was likely,that the author wrote,best-seller"
            ),
            (
                "The man returned to his house was happy",
                "was",
                "The reader may first think 'returned' is the main verb, but 'was' shows that the main predicate is 'was happy'.",
                "The man who was returned to his house was happy.",
                "man returned,came back,returned home",
                "was returned,was happy,man was happy"
            ),
            (
                "The tomcat curled up on the cushion seemed friendly",
                "seemed",
                "The reader may first think the tomcat curled itself up, but 'seemed' shows that the curled-up phrase describes the tomcat.",
                "The tomcat that was curled up on the cushion seemed friendly.",
                "cat curled,tomcat curled,curled up",
                "was curled,seemed friendly,tomcat seemed"
            )
        ]

        cursor.executemany("""
            INSERT INTO sentences
            (sentence, disambiguating_word, trap_explanation, correct_meaning, wrong_keywords, correct_keywords)
            VALUES (?, ?, ?, ?, ?, ?)
        """, sample_sentences)

    conn.commit()
    conn.close()


def get_sentences():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sentences")
    rows = cursor.fetchall()

    conn.close()
    return rows


def save_result(sentence_id, user_interpretation, longest_pause_word, longest_pause_time, interpretation_result):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO results
        (sentence_id, user_interpretation, longest_pause_word, longest_pause_time, interpretation_result)
        VALUES (?, ?, ?, ?, ?)
    """, (sentence_id, user_interpretation, longest_pause_word, longest_pause_time, interpretation_result))

    conn.commit()
    conn.close()