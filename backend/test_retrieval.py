from backend.vector_store import retrieve

results = retrieve("what is frs", k=3)
for r in results:
    print(r["title"], "|", r["topic"])
