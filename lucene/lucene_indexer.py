import os
import sys
import lucene
import json
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField, StoredField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from java.nio.file import Paths

### initialize lucene jvm
lucene.initVM()

### define index directory
index_dir = "stackoverflow_index"
if not os.path.exists(index_dir):
    os.mkdir(index_dir)

### setup lucene index writer (appends to existing index)
store = SimpleFSDirectory(Paths.get(index_dir))
analyzer = StandardAnalyzer()
config = IndexWriterConfig(analyzer)
config.setOpenMode(IndexWriterConfig.OpenMode.CREATE_OR_APPEND)
writer = IndexWriter(store, config)

def safe_value(value, default=""):
    """returns a safe non-null value"""
    return value if value and isinstance(value, str) else default

def index_stackoverflow_data(json_file):
    """indexes a single json file into the existing index"""
    if not os.path.exists(json_file):
        print(f"error: file '{json_file}' not found")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"indexing {json_file} ({len(data)} entries)...")

    skipped_entries = 0  ### count entries skipped due to missing data

    for entry in data:
        ### skip documents missing required fields
        if "title" not in entry or not entry["title"]:
            skipped_entries += 1
            continue

        doc = Document()
        doc.add(TextField("title", safe_value(entry.get("title")), Field.Store.YES))
        doc.add(TextField("body", safe_value(entry.get("body")), Field.Store.YES))
        doc.add(StoredField("link", safe_value(entry.get("link"))))
        doc.add(StoredField("score", safe_value(entry.get("score"))))
        doc.add(StoredField("creation_date", safe_value(entry.get("creation_date"))))
        doc.add(TextField("tags", safe_value(", ".join(set(entry.get("tags", [])))), Field.Store.YES))
        doc.add(TextField("comments", safe_value(" | ".join(entry.get("comments", []))), Field.Store.YES))

        answers_text = " | ".join([ans["body"] for ans in entry.get("answers", []) if "body" in ans])
        doc.add(TextField("answers", safe_value(answers_text), Field.Store.YES))

        writer.addDocument(doc)

    writer.commit()
    print(f"finished indexing {json_file}! (skipped {skipped_entries} invalid entries)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        index_stackoverflow_data('/home/cs242/group_6/stackoverflow_data_set_5.json')
        index_stackoverflow_data('/home/cs242/group_6/stackoverflow_data_set_3.json')
        index_stackoverflow_data('/home/cs242/group_6/stackoverflow_data_set_41.json')
        index_stackoverflow_data('/home/cs242/group_6/stackoverflow_data_set_42.json')
        index_stackoverflow_data('/home/cs242/group_6/stackoverflow_data_set_31.json')
        index_stackoverflow_data('/home/cs242/group_6/stackoverflow_data_set_2.json')
    else:
        index_stackoverflow_data(sys.argv[1])

    writer.close()
