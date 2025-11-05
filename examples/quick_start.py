#!/usr/bin/env python3
"""
Quick start script for Battalion RL system

This is the SIMPLEST way to get started - just run this script!
"""

import sys
from pathlib import Path

print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║           BATTALION RL SYSTEM - QUICK START              ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

This system will:
1. Evolve game mechanics automatically
2. Test each variant by running simulations
3. Find the best balance through reinforcement learning

First time? Let's start with a TINY test to make sure it works!
""")

def check_dependencies():
    """Make sure we have everything we need"""
    print("🔍 Checking dependencies...")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required")
        return False
    print("  ✅ Python version OK")
    
    # Check files exist
    required_files = [
        "battalion_simulator.py",
        "genetic_algorithm.py",
        "simulator_integration.py",
        "run_genetic_algorithm.py"
    ]
    
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Missing file: {file}")
            return False
    print("  ✅ All files present")
    
    return True


def run_tiny_test():
    """Run a tiny test to verify everything works"""
    print("\n🧪 Running tiny test (3 genomes, 1 generation, 50 games)...")
    print("   This will take ~5 minutes\n")
    
    from genetic_algorithm import GeneticAlgorithm, GameGenome
    from simulator_integration import SimulatorIntegration
    
    class TinyGA(GeneticAlgorithm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.integrator = SimulatorIntegration(self.simulator_path)
        
        def evaluate_genome(self, genome):
            return self.integrator.evaluate_genome(genome, games=self.games_per_test)
        
        def cleanup(self):
            self.integrator.cleanup()
    
    ga = TinyGA(
        population_size=3,
        games_per_test=50,
        mutation_rate=0.3,
        elite_count=1
    )
    
    try:
        ga.run(generations=1)
        ga.cleanup()
        
        print("\n✅ Test successful!")
        print(f"   Best fitness: {ga.best_fitness:.1f}/600")
        
        return True
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False


def run_real_evolution():
    """Run the full evolution"""
    print("\n🚀 Running REAL evolution...")
    print("   (8 genomes, 3 generations, 200 games each)")
    print("   This will take ~45 minutes")
    print("   Press Ctrl+C to stop early\n")
    
    import subprocess
    result = subprocess.run([sys.executable, "run_genetic_algorithm.py"])
    return result.returncode == 0


def main():
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Setup incomplete. Please check errors above.")
        return
    
    print("\n✅ All dependencies OK!\n")
    
    # Ask user what to do
    print("What do you want to do?")
    print("  1. Run tiny test (~5 min) - Verify system works")
    print("  2. Run real evolution (~45 min) - Find better balance")
    print("  3. Exit")
    
    choice = input("\nChoice (1-3): ").strip()
    
    if choice == "1":
        success = run_tiny_test()
        if success:
            print("\n🎉 System works! Ready for real evolution.")
            print("   Run again and choose option 2 to evolve for real.")
    elif choice == "2":
        success = run_real_evolution()
        if success:
            print("\n🎉 Evolution complete!")
            print("   Check genetic_algorithm_results.json for results.")
    elif choice == "3":
        print("\n👋 Goodbye!")
    else:
        print("\n❌ Invalid choice")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Goodbye!")
