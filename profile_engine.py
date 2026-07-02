import time
import cProfile
import pstats
from backend.app.engine.core import EnginePipeline
from backend.app.engine.models import Heir

pipeline = EnginePipeline()

heirs = [
    Heir(relation="Father", relation_type="Father", count=1, gender="M", generation_level=1, lineage="Paternal"),
    Heir(relation="Mother", relation_type="Mother", count=1, gender="F", generation_level=1, lineage="Maternal"),
    Heir(relation="Son", relation_type="Son", count=2, gender="M", generation_level=1, lineage="Direct"),
    Heir(relation="Daughter", relation_type="Daughter", count=1, gender="F", generation_level=1, lineage="Direct"),
]

def run_lots():
    for _ in range(1000):
        pipeline.calculate(heirs, estate_value=1000)

start = time.time()
run_lots()
print("Execution time without optimization:", time.time() - start)

cProfile.run("run_lots()", "profile_stats")
p = pstats.Stats("profile_stats")
p.strip_dirs().sort_stats("tottime").print_stats(10)
