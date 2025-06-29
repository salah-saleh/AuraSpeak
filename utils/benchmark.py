import time  # For timing operations
import functools  # For decorators
from contextlib import contextmanager  # For context managers

# Global benchmark data storage
benchmark_data = {}

def benchmark_function(func_name=None):
    """
    Decorator to benchmark function execution time.
    Usage: @benchmark_function("my_function")
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            name = func_name or func.__name__
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            
            if name not in benchmark_data:
                benchmark_data[name] = []
            benchmark_data[name].append(duration)
            
            print(f"[Benchmark] {name}: {duration:.3f}s")
            return result
        return wrapper
    return decorator

@contextmanager
def benchmark_block(block_name):
    """
    Context manager to benchmark code blocks.
    Usage: with benchmark_block("my_block"):
    """
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        duration = end_time - start_time
        
        if block_name not in benchmark_data:
            benchmark_data[block_name] = []
        benchmark_data[block_name].append(duration)
        
        print(f"[Benchmark] {block_name}: {duration:.3f}s")

def print_benchmark_summary():
    """
    Print a summary of all benchmark data collected.
    """
    if not benchmark_data:
        print("[Benchmark] No data collected.")
        return
    
    print("\n" + "="*50)
    print("BENCHMARK SUMMARY")
    print("="*50)
    
    for name, times in benchmark_data.items():
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            total_time = sum(times)
            count = len(times)
            
            print(f"{name}:")
            print(f"  Count: {count}")
            print(f"  Average: {avg_time:.3f}s")
            print(f"  Min: {min_time:.3f}s")
            print(f"  Max: {max_time:.3f}s")
            print(f"  Total: {total_time:.3f}s")
            print()

def clear_benchmark_data():
    """
    Clear all collected benchmark data.
    """
    global benchmark_data
    benchmark_data.clear()
    print("[Benchmark] Data cleared.") 