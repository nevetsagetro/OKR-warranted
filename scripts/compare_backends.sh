#!/bin/bash
set -e

# compare_backends.sh
# Runs indexing and evaluation across local, ChromaDB, and Qdrant backends
# to compare retrieval quality and operational behavior.

WORK_DIR="data/compare_work"
BENCHMARK="benchmarks/real_corpus_expanded.json"
# Fall back to a smaller benchmark if expanded doesn't exist
if [ ! -f "$BENCHMARK" ]; then
    BENCHMARK="benchmarks/real_corpus_smoke.json"
fi

if [ ! -f "$BENCHMARK" ]; then
    echo "Error: No benchmark found at $BENCHMARK"
    exit 1
fi

echo "=========================================================="
echo "Comparing vector backends using benchmark: $BENCHMARK"
echo "=========================================================="
echo ""

for BACKEND in local chromadb qdrant; do
    echo "----------------------------------------------------------"
    echo "Backend: $BACKEND"
    echo "----------------------------------------------------------"
    
    export OKR_VECTOR_BACKEND="$BACKEND"
    
    echo "Building index..."
    okr build-index --work-dir "$WORK_DIR"
    
    echo "Evaluating..."
    okr evaluate --work-dir "$WORK_DIR" --benchmark-path "$BENCHMARK"
    echo ""
done

echo "=========================================================="
echo "Comparison complete."
echo "=========================================================="
