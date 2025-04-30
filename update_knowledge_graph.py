import os
import json

# --- Configuration ---
DOCS_DIR = '/home/zhaozhan/Project/Obsidian/docs'
JSON_FILE = '/home/zhaozhan/Project/Obsidian/knowledge_graph.json'
URL_PREFIX = 'https://note.zhaozhan.site/'
EXCLUDE_DIRS = ['.obsidian'] # Directories to exclude
# --- End Configuration ---

def generate_nodes(docs_dir, url_prefix, exclude_dirs):
    """Generates node data by scanning the docs directory."""
    nodes = []
    node_id_counter = 1
    abs_docs_dir = os.path.abspath(docs_dir)

    for root, dirs, files in os.walk(abs_docs_dir, topdown=True):
        # Modify dirs in-place to skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for filename in files:
            # Skip index.md in the root docs directory for URL generation consistency
            if root == abs_docs_dir and filename.lower() == 'index.md':
                continue
            # Skip CNAME file
            if filename == 'CNAME':
                continue

            if filename.lower().endswith('.md'):
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, abs_docs_dir)

                # Generate name (remove .md extension)
                name = os.path.splitext(filename)[0]

                # Generate URL
                # Replace backslashes with forward slashes for URL
                url_path = os.path.splitext(relative_path)[0].replace(os.sep, '/')
                # Ensure trailing slash
                url = f"{url_prefix}{url_path}/"

                # Create node entry
                nodes.append({
                    "id": node_id_counter,
                    "name": name,
                    "description": name, # Use filename as initial description
                    "url": url
                })
                node_id_counter += 1
    return nodes

def update_knowledge_graph(json_file, new_nodes):
    """Reads the existing JSON, updates the nodes, and writes back."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is invalid, start with a default structure
        data = {"nodes": [], "links": [], "layout": {}}
        print(f"Warning: Could not read {json_file}. Starting with a new structure.")


    # Preserve existing links and layout if they exist
    existing_links = data.get("links", [])
    existing_layout = data.get("layout", {}) # Keep existing layout or use empty dict

    # Update the nodes list
    data["nodes"] = new_nodes
    data["links"] = existing_links # Keep existing links
    data["layout"] = existing_layout # Keep existing layout

    # Write the updated data back to the file
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Successfully updated {json_file} with {len(new_nodes)} nodes.")
    except IOError as e:
        print(f"Error writing to {json_file}: {e}")

if __name__ == "__main__":
    print(f"Scanning directory: {DOCS_DIR}")
    generated_nodes = generate_nodes(DOCS_DIR, URL_PREFIX, EXCLUDE_DIRS)
    if generated_nodes:
        print(f"Found {len(generated_nodes)} markdown files.")
        update_knowledge_graph(JSON_FILE, generated_nodes)
    else:
        print("No markdown files found.")
