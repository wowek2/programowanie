import timeit
from vector import Vector as OptimizedVector
from naive_vector import Vector as NaiveVector

VECTOR_SIZE = 1000
REPETITIONS = 1000

#CProfile

def test_performance(cls):
    results = {}
    
    # Test vector creation
    def create_vector():
        return cls.random(size=VECTOR_SIZE)
    results['Creation'] = timeit.timeit(create_vector, number=REPETITIONS)
    
    v1 = cls.random(size=VECTOR_SIZE)
    v2 = cls.random(size=VECTOR_SIZE)

    # Test vector addition
    results['Addition'] = timeit.timeit(lambda: v1 + v2, number=REPETITIONS)
    
    # Test in-place addition
    results['In-place Add'] = timeit.timeit(lambda: v1.__iadd__(v2), number=REPETITIONS)
    2
    scalar = 4391413

    # Test in-place multiplication
    results['In-place Multiplicaton'] = timeit.timeit(lambda: v1.__imul__(scalar), number=REPETITIONS)
    
    # Test dot product
    results['Dot Product'] = timeit.timeit(lambda: v1.dot(v2), number=REPETITIONS)
    
    return results



# Run tests for both implementations
print("Testing Optimized Vector...")
optimized_results = test_performance(OptimizedVector)

print("\nTesting Naive Vector...")
naive_results = test_performance(NaiveVector)


print("\nPerformance Comparison (seconds):")
print(f"{'Operation':<30} {'Optimized':<10} {'Naive':<10} {'Difference':<10}")
for op in optimized_results:
    opt = optimized_results[op]
    naive = naive_results[op]
    diff = naive / opt if opt != 0 else 0
    print(f"{op:<30} {opt:.5f}     {naive:.5f}     {diff:.1f}x")