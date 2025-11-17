"""
Deployment Script for Fraud Detection System
Provides options to deploy using FastAPI (API) or Streamlit (Web Interface)
"""
import subprocess
import sys
import time
from pathlib import Path
import argparse


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)


def check_requirements():
    """Check if required packages are installed"""
    print_header("Checking Dependencies")

    required_packages = [
        'fastapi', 'uvicorn', 'streamlit', 'pandas', 'numpy',
        'scikit-learn', 'xgboost', 'lightgbm', 'plotly'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - MISSING")

    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages, check=True)
        print("✅ Dependencies installed successfully")
    else:
        print("\n✅ All dependencies are installed")


def check_models():
    """Check if trained models exist"""
    print_header("Checking Models")

    model_paths = [
        Path("models/preprocessing/feature_engineer.pkl"),
        Path("models/predictive/ensemble"),
        Path("models/fraud_detection/fraud_detector.pkl")
    ]

    all_models_exist = True

    for model_path in model_paths:
        if model_path.exists():
            if model_path.is_dir():
                files = list(model_path.glob("*"))
                print(f"✅ {model_path}: {len(files)} files")
            else:
                size = model_path.stat().st_size / 1024
                print(f"✅ {model_path}: {size:.1f}KB")
        else:
            print(f"❌ {model_path}: NOT FOUND")
            all_models_exist = False

    if not all_models_exist:
        print("\n⚠️ Some models are missing. Please run the training pipeline first:")
        print("python run_all.py")
        return False

    return True


def start_fastapi(host="127.0.0.1", port=8000, reload=False):
    """Start FastAPI server"""
    print_header("Starting FastAPI Server")

    print("🚀 Starting FastAPI server...")
    print(f"📍 URL: http://{host}:{port}")
    print(f"📚 Docs: http://{host}:{port}/docs")
    print(f"🔄 ReDoc: http://{host}:{port}/redoc")
    print(f"🏥 Health: http://{host}:{port}/health")
    print(f"📊 Metrics: http://{host}:{port}/metrics")
    print("\n🔄 Press Ctrl+C to stop the server")

    try:
        cmd = [
            sys.executable, "-m", "uvicorn",
            "src.module4_deployment.api_server:app",
            "--host", host,
            "--port", str(port),
            "--log-level", "info"
        ]

        if reload:
            cmd.append("--reload")

        subprocess.run(cmd, check=True)

    except KeyboardInterrupt:
        print("\n👋 FastAPI server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting FastAPI server: {e}")


def start_streamlit(port=8501):
    """Start Streamlit web interface"""
    print_header("Starting Streamlit Web Interface")

    print("🚀 Starting Streamlit app...")
    print(f"📍 URL: http://localhost:{port}")
    print("\n🔄 Press Ctrl+C to stop the interface")

    try:
        cmd = [
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", str(port),
            "--server.address", "localhost",
            "--browser.serverAddress", "localhost"
        ]

        subprocess.run(cmd, check=True)

    except KeyboardInterrupt:
        print("\n👋 Streamlit interface stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting Streamlit: {e}")


def start_both(api_port=8000, streamlit_port=8501):
    """Start both FastAPI and Streamlit servers"""
    print_header("Starting Both Services")

    print("🚀 Starting FastAPI API server...")
    print(f"📍 API URL: http://localhost:{api_port}")
    print(f"📚 API Docs: http://localhost:{api_port}/docs")

    print(f"\n🚀 Starting Streamlit web interface...")
    print(f"📍 Web URL: http://localhost:{streamlit_port}")

    print("\n🔄 Both services will start in separate processes")
    print("🔄 Use Ctrl+C to stop both services")

    try:
        # Start FastAPI in background
        api_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn",
            "src.module4_deployment.api_server:app",
            "--host", "localhost",
            "--port", str(api_port),
            "--log-level", "warning"
        ])

        # Give API time to start
        time.sleep(3)

        # Start Streamlit
        streamlit_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", str(streamlit_port),
            "--server.address", "localhost"
        ])

        print(f"\n✅ Services started!")
        print(f"📊 API: http://localhost:{api_port}/docs")
        print(f"🖥️ Web Interface: http://localhost:{streamlit_port}")

        # Wait for both processes
        try:
            api_process.wait()
            streamlit_process.wait()
        except KeyboardInterrupt:
            print("\n👋 Stopping services...")
            api_process.terminate()
            streamlit_process.terminate()

    except Exception as e:
        print(f"❌ Error starting services: {e}")


def test_api_connection(host="localhost", port=8000):
    """Test API connection"""
    print_header("Testing API Connection")

    try:
        import requests

        # Test health endpoint
        response = requests.get(f"http://{host}:{port}/health", timeout=5)

        if response.status_code == 200:
            health_data = response.json()
            print("✅ API Connection Successful!")
            print(f"   Status: {health_data['status']}")
            print(f"   Model Loaded: {health_data['model_loaded']}")
            print(f"   Timestamp: {health_data['timestamp']}")
        else:
            print(f"❌ API returned status code: {response.status_code}")

        # Test fraud detection endpoint
        test_transaction = {
            "Transaction_Amount": 50000,
            "Transaction_Date": "2024-01-15",
            "Transaction_Time": "14:30:00",
            "Transaction_Location": "Mumbai",
            "Card_Type": "Visa",
            "Transaction_Currency": "INR",
            "Transaction_Status": "Completed",
            "Previous_Transaction_Count": 25,
            "Distance_Between_Transactions_km": 10.5,
            "Time_Since_Last_Transaction_min": 120,
            "Authentication_Method": "PIN",
            "Transaction_Velocity": 3,
            "Transaction_Category": "Shopping"
        }

        response = requests.post(f"http://{host}:{port}/detect/fraud", json=test_transaction, timeout=10)

        if response.status_code == 200:
            result = response.json()
            print("✅ Fraud Detection Test Successful!")
            print(f"   Risk Level: {result['risk_level']}")
            print(f"   Risk Score: {result['combined_risk_score']:.3f}")
            print(f"   Processing Time: {result['processing_time_ms']:.1f}ms")
        else:
            print(f"❌ Fraud detection test failed: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server")
        print(f"   Make sure the server is running at http://{host}:{port}")
    except requests.exceptions.Timeout:
        print("❌ API request timed out")
    except Exception as e:
        print(f"❌ Error testing API: {e}")


def main():
    """Main deployment function"""
    parser = argparse.ArgumentParser(description="Deploy Fraud Detection System")
    parser.add_argument("--mode", choices=["api", "web", "both", "test"],
                       default="both", help="Deployment mode")
    parser.add_argument("--api-port", type=int, default=8000, help="FastAPI port")
    parser.add_argument("--web-port", type=int, default=8501, help="Streamlit port")
    parser.add_argument("--host", default="localhost", help="Server host")

    args = parser.parse_args()

    print("\n" + "="*60)
    print(" 🛡️ FRAUD DETECTION SYSTEM - DEPLOYMENT")
    print("="*60)

    # Check prerequisites
    check_requirements()

    if not check_models():
        print("\n❌ Cannot deploy without trained models")
        print("Please run: python run_all.py")
        return

    # Deploy based on mode
    if args.mode == "test":
        test_api_connection(args.host, args.api_port)

    elif args.mode == "api":
        start_fastapi(args.host, args.api_port, reload=False)

    elif args.mode == "web":
        start_streamlit(args.web_port)

    elif args.mode == "both":
        start_both(args.api_port, args.web_port)


if __name__ == "__main__":
    main()
