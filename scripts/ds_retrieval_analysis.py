import sys
from pathlib import Path

# Add src to sys.path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from own_knowledge_rag.config import Settings
from own_knowledge_rag.pipeline import KnowledgePipeline
from own_knowledge_rag.analytics import KnowledgeAnalytics

def run_experiment():
    settings = Settings()
    work_dir = Path("data/work")
    if not work_dir.exists():
        print(f"Error: Work directory {work_dir} not found.")
        return

    pipeline = KnowledgePipeline(settings)
    analytics = KnowledgeAnalytics(work_dir)
    retriever = pipeline._load_retriever(work_dir)
    
    # Sample queries representing different retrieval challenges
    queries = [
        "Sender in Spain?",
        "Does Sri Lanka support two-way SMS?",
        "What is the dialing code for Nepal?",
        "Compare sender provisioning and two-way support in Spain.",
        "Alphanumeric vs Long Code in Albania"
    ]
    
    print("--- Data Science Retrieval Analysis ---")
    analysis = analytics.analyze_retrieval_baseline(retriever, queries)
    
    boost = analysis["avg_score_boost"]
    print(f"Hybrid vs Lexical Boost: {boost['hybrid_vs_lexical']*100:+.1f}%")
    print(f"Hybrid vs Vector Boost: {boost['hybrid_vs_vector']*100:+.1f}%")
    
    print("\nDetailed Sample Scores:")
    for i, q in enumerate(queries):
        lex = analysis["raw_samples"]["lexical_only"][i]
        vec = analysis["raw_samples"]["vector_only"][i]
        hyb = analysis["raw_samples"]["hybrid"][i]
        print(f"Q: {q}")
        print(f"  Lexical: {lex:.4f}")
        print(f"  Vector:  {vec:.4f}")
        print(f"  Hybrid:  {hyb:.4f}")

if __name__ == "__main__":
    run_experiment()
