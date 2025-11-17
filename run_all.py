"""
Master Script to Run All Modules
Executes the complete fraud detection pipeline
"""
import sys
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70 + "\n")


def run_module_1():
    """Run Module 1: Data Preprocessing"""
    print_header("MODULE 1: DATA PREPROCESSING")
    
    try:
        from src.module1_preprocessing.preprocess_data import main
        main()
        logger.info("✓ Module 1 completed successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Module 1 failed: {e}")
        return False


def run_module_2():
    """Run Module 2: Predictive Transaction Modeling"""
    print_header("MODULE 2: PREDICTIVE TRANSACTION MODELING")
    
    try:
        from src.module2_predictive.train_model import main
        main()
        logger.info("✓ Module 2 completed successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Module 2 failed: {e}")
        return False


def run_module_3():
    """Run Module 3: Fraud Detection Engine"""
    print_header("MODULE 3: FRAUD DETECTION ENGINE")
    
    try:
        from src.module3_fraud_detection.train_fraud_detector import main
        main()
        logger.info("✓ Module 3 completed successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Module 3 failed: {e}")
        return False


def run_eda():
    """Run Exploratory Data Analysis"""
    print_header("EXPLORATORY DATA ANALYSIS")
    
    try:
        import runpy
        from pathlib import Path
        eda_path = Path(__file__).parent / "notebooks" / "01_exploratory_analysis.py"
        runpy.run_path(str(eda_path), run_name="__main__")
        logger.info("✓ EDA completed successfully")
        return True
    except Exception as e:
        logger.error(f"✗ EDA failed: {e}")
        return False


def main():
    """Main execution function"""
    start_time = datetime.now()
    
    print("\n" + "="*70)
    print(" PREDICTIVE TRANSACTION INTELLIGENCE FOR BFSI")
    print(" Complete Pipeline Execution")
    print("="*70)
    print(f"\nStart Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'Module 1 - Data Preprocessing': False,
        'Module 2 - Predictive Modeling': False,
        'Module 3 - Fraud Detection': False,
        'Exploratory Analysis': False
    }
    
    # Run all modules
    print("\n" + "="*70)
    print(" EXECUTION PLAN")
    print("="*70)
    print("\n1. Data Preprocessing")
    print("2. Predictive Transaction Modeling")
    print("3. Fraud Detection Engine Training")
    print("4. Exploratory Data Analysis")
    
    input("\nPress Enter to start execution...")
    
    # Module 1
    results['Module 1 - Data Preprocessing'] = run_module_1()
    
    # Module 2 (only if Module 1 succeeded)
    if results['Module 1 - Data Preprocessing']:
        results['Module 2 - Predictive Modeling'] = run_module_2()
    else:
        logger.warning("Skipping Module 2 due to Module 1 failure")
    
    # Module 3 (only if Module 2 succeeded)
    if results['Module 2 - Predictive Modeling']:
        results['Module 3 - Fraud Detection'] = run_module_3()
    else:
        logger.warning("Skipping Module 3 due to Module 2 failure")
    
    # EDA (can run independently)
    results['Exploratory Analysis'] = run_eda()
    
    # Summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    print_header("EXECUTION SUMMARY")
    
    print("Module Status:")
    for module, status in results.items():
        status_icon = "✓" if status else "✗"
        status_text = "SUCCESS" if status else "FAILED"
        print(f"  {status_icon} {module}: {status_text}")
    
    print(f"\nStart Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Duration: {duration}")
    
    success_count = sum(results.values())
    total_count = len(results)
    
    print(f"\nOverall: {success_count}/{total_count} modules completed successfully")
    
    if success_count == total_count:
        print("\n🎉 All modules completed successfully!")
        print("\nNext Steps:")
        print("1. Review the generated models in the 'models/' directory")
        print("2. Check visualizations in 'notebooks/figures/'")
        print("3. Start the API server: python src/module4_deployment/api_server.py")
        print("4. Test the API: python src/module4_deployment/test_api.py")
    else:
        print("\n⚠ Some modules failed. Please check the logs above.")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
