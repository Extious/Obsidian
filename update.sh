git add .
git commit -m "update"
git push
python update_knowledge_graph.py
scp /home/zhaozhan/Project/Obsidian/knowledge_graph.json zhaozhan@zhaozhan.site:/home/zhaozhan/Index/knowledge_graph.json