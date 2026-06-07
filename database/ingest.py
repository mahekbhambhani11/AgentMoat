import os
import json
import chromadb
from sentence_transformers import SentenceTransformer

def seed_vector_db():
    print("🚀 Initializing AgentMoat Threat Intelligence Loader...")
    
    # 1. Establish persistent local storage for your vector database
    db_path = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_or_create_collection(name="malicious_vectors")
    
    # 2. Boot up your local semantic embedding AI model
    print("🧠 Loading local text-embedding engine (all-MiniLM-L6-v2)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # 3. Locate your JSON/JSONL dataset file automatically
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    target_file = None
    
    if os.path.exists(data_dir):
        for file in os.listdir(data_dir):
            if file.endswith('.json') or file.endswith('.jsonl'):
                target_file = os.path.join(data_dir, file)
                break
                
    if not target_file:
        print(f"❌ Error: Place your dataset inside the '{data_dir}/' folder first.")
        return

    print(f"📂 Found dataset target: {os.path.basename(target_file)}")
    toxic_prompts = []
    
    # 4. Read the entire file content cleanly to strip hidden characters
    try:
        with open(target_file, 'r', encoding='utf-8-sig') as f:
            content = f.read().strip()
            
        # Detect format: Standard JSON Array vs JSON Lines
        if content.startswith('['):
            # It's a standard JSON Array
            try:
                records = json.loads(content)
                for item in records:
                    if isinstance(item, dict) and item.get('label') == 'malicious' and item.get('prompt'):
                        toxic_prompts.append(item['prompt'])
            except json.JSONDecodeError as e:
                print(f"❌ JSON Array format error: {e}")
                return
        else:
            # It's JSON Lines (one JSON object per line)
            lines = content.splitlines()
            for line in lines:
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                    if isinstance(item, dict) and item.get('label') == 'malicious' and item.get('prompt'):
                        toxic_prompts.append(item['prompt'])
                except json.JSONDecodeError:
                    # Silently skip any malformed lines
                    continue
                            
    except Exception as e:
        print(f"❌ Error reading file structure: {e}")
        return

    # Remove duplicates to optimize database performance
    toxic_prompts = list(set(toxic_prompts))
    
    # Take a highly effective 2,000 sample batch for the prototype
    sample_size = min(2000, len(toxic_prompts))
    toxic_prompts = toxic_prompts[:sample_size]
    
    if not toxic_prompts:
        print("❌ Verification Failed: No records matched 'label' == 'malicious'. Check JSON schema.")
        return
        
    print(f"📦 Vectorizing {sample_size} injection attack payloads. Please wait...")
    
    # 5. Convert text phrases into numeric vectors and save them
    embeddings = model.encode(toxic_prompts, show_progress_bar=True).tolist()
    ids = [f"threat_id_{i}" for i in range(len(toxic_prompts))]
    
    collection.add(
        embeddings=embeddings,
        documents=toxic_prompts,
        ids=ids
    )
    
    print("✅ Ingestion Success! Local ChromaDB threat vectors are armed.")

if __name__ == "__main__":
    seed_vector_db()