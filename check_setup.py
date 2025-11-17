"""
Setup Checker - Verify project setup and dependencies
"""
import sys
from pathlib import Path
import importlib


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)


def check_python_version():
    """Check Python version"""
    print_header("Python Version Check")
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible (3.8+)")
        return True
    else:
        print("❌ Python version is too old. Please upgrade to 3.8+")
        return False


def check_dependencies():
    """Check if required packages are installed"""
    print_header("Dependency Check")
    
    required_packages = [
        'pandas',
        'numpy',
        'sklearn',
        'xgboost',
        'lightgbm',
        'fastapi',
        'uvicorn',
        'pydantic',
        'joblib',
        'matplotlib',
        'seaborn'
    ]
    
    optional_packages = [
        'torch',
        'transformers'
    ]
    
    all_ok = True
    
    print("\nRequired Packages:")
    for package in required_packages:
        try:
            mod = importlib.import_module(package)
            version = getattr(mod, '__version__', 'unknown')
            print(f"  ✅ {package:20s} {version}")
        except ImportError:
            print(f"  ❌ {package:20s} NOT INSTALLED")
            all_ok = False
    
    print("\nOptional Packages (for LLM features):")
    for package in optional_packages:
        try:
            mod = importlib.import_module(package)
            version = getattr(mod, '__version__', 'unknown')
            print(f"  ✅ {package:20s} {version}")
        except ImportError:
            print(f"  ⚠️  {package:20s} NOT INSTALLED (optional)")
    
    return all_ok


def check_project_structure():
    """Check if project structure is correct"""
    print_header("Project Structure Check")
    
    required_dirs = [
        'src/module1_preprocessing',
        'src/module2_predictive',
        'src/module3_fraud_detection',
        'src/module4_deployment',
        'config',
        'tests'
    ]
    
    required_files = [
        'requirements.txt',
        'README.md',
        'config/config.py',
        'src/module1_preprocessing/preprocess_data.py',
        'src/module2_predictive/train_model.py',
        'src/module3_fraud_detection/train_fraud_detector.py',
        'src/module4_deployment/api_server.py'
    ]
    
    all_ok = True
    
    print("\nDirectories:")
    for dir_path in required_dirs:
        full_path = Path(dir_path)
        if full_path.exists():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path} NOT FOUND")
            all_ok = False
    
    print("\nKey Files:")
    for file_path in required_files:
        full_path = Path(file_path)
        if full_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} NOT FOUND")
            all_ok = False
    
    return all_ok


def check_data_file():
    """Check if data file exists"""
    print_header("Data File Check")
    
    data_file = Path("card_fraud.csv_processed.csv")
    
    if data_file.exists():
        size_mb = data_file.stat().st_size / (1024 * 1024)
        print(f"✅ Data file found: {data_file}")
        print(f"   Size: {size_mb:.2f} MB")
        return True
    else:
        print(f"❌ Data file not found: {data_file}")
        print("   Please ensure the data file is in the project root directory")
        return False


def check_models():
    """Check if models directory exists"""
    print_header("Models Directory Check")
    
    models_dir = Path("models")
    
    if models_dir.exists():
        print(f"✅ Models directory exists")
        
        # Check for trained models
        subdirs = ['preprocessing', 'predictive', 'fraud_detection']
        for subdir in subdirs:
            subdir_path = models_dir / subdir
            if subdir_path.exists():
                files = list(subdir_path.glob('*'))
                if files:
                    print(f"   ✅ {subdir}: {len(files)} file(s)")
                else:
                    print(f"   ⚠️  {subdir}: No models yet (run training)")
            else:
                print(f"   ⚠️  {subdir}: Directory will be created during training")
        return True
    else:
        print(f"⚠️  Models directory doesn't exist yet")
        print("   It will be created when you run the training scripts")
        return True


def provide_recommendations(checks):
    """Provide recommendations based on checks"""
    print_header("Recommendations")
    
    if all(checks.values()):
        print("\n✅ All checks passed! Your setup is ready.")
        print("\nNext steps:")
        print("  1. Run the complete pipeline: python run_all.py")
        print("  2. Or run individual modules:")
        print("     - python src/module1_preprocessing/preprocess_data.py")
        print("     - python src/module2_predictive/train_model.py")
        print("     - python src/module3_fraud_detection/train_fraud_detector.py")
        print("  3. Start API server: python src/module4_deployment/api_server.py")
        print("  4. Test API: python src/module4_deployment/test_api.py")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        
        if not checks['dependencies']:
            print("\n📦 To install dependencies:")
            print("   pip install -r requirements.txt")
        
        if not checks['data']:
            print("\n📁 Data file issue:")
            print("   Ensure 'card_fraud.csv_processed.csv' is in the project root")
        
        if not checks['structure']:
            print("\n📂 Project structure issue:")
            print("   Some files or directories are missing")
            print("   Please ensure you have the complete project")


def main():
    """Main execution"""
    print("\n" + "="*60)
    print(" FRAUD DETECTION SYSTEM - SETUP CHECKER")
    print("="*60)
    
    checks = {
        'python': check_python_version(),
        'dependencies': check_dependencies(),
        'structure': check_project_structure(),
        'data': check_data_file(),
        'models': check_models()
    }
    
    provide_recommendations(checks)
    
    print("\n" + "="*60)
    print(" Setup check completed")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
