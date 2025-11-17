"""
Test API endpoints
"""
import requests
import json
from datetime import datetime
import time


class APITester:
    """Test Fraud Detection API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize API tester
        
        Args:
            base_url: Base URL of the API
        """
        self.base_url = base_url
    
    def test_health(self):
        """Test health endpoint"""
        print("\n" + "="*50)
        print("Testing Health Endpoint")
        print("="*50)
        
        try:
            response = requests.get(f"{self.base_url}/health")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def test_fraud_detection(self):
        """Test fraud detection endpoint"""
        print("\n" + "="*50)
        print("Testing Fraud Detection Endpoint")
        print("="*50)
        
        # Test transaction 1: Normal transaction
        transaction1 = {
            "Transaction_Amount": 25000,
            "Transaction_Date": "2024-01-15",
            "Transaction_Time": "14:30:00",
            "Transaction_Location": "Mumbai",
            "Card_Type": "Visa",
            "Transaction_Currency": "INR",
            "Transaction_Status": "Completed",
            "Previous_Transaction_Count": 25,
            "Distance_Between_Transactions_km": 5.0,
            "Time_Since_Last_Transaction_min": 120,
            "Authentication_Method": "PIN",
            "Transaction_Velocity": 2,
            "Transaction_Category": "Shopping"
        }
        
        print("\nTest 1: Normal Transaction")
        print(f"Amount: {transaction1['Transaction_Amount']}")
        
        try:
            response = requests.post(
                f"{self.base_url}/detect/fraud",
                json=transaction1
            )
            print(f"Status Code: {response.status_code}")
            result = response.json()
            print(f"Is Fraud: {result['is_fraud']}")
            print(f"Risk Level: {result['risk_level']}")
            print(f"Risk Score: {result['combined_risk_score']:.4f}")
            print(f"Recommendation: {result['recommendation']}")
            print(f"Processing Time: {result['processing_time_ms']:.2f}ms")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test transaction 2: Suspicious transaction
        transaction2 = {
            "Transaction_Amount": 95000000,  # Very high amount
            "Transaction_Date": "2024-01-15",
            "Transaction_Time": "02:30:00",  # Night time
            "Transaction_Location": "Unknown",
            "Card_Type": "Mastercard",
            "Transaction_Currency": "USD",
            "Transaction_Status": "Pending",
            "Previous_Transaction_Count": 2,
            "Distance_Between_Transactions_km": 800.0,  # Long distance
            "Time_Since_Last_Transaction_min": 1,  # Very quick
            "Authentication_Method": "Failed",
            "Transaction_Velocity": 15,  # High velocity
            "Transaction_Category": "Transfer"
        }
        
        print("\nTest 2: Suspicious Transaction")
        print(f"Amount: {transaction2['Transaction_Amount']}")
        
        try:
            response = requests.post(
                f"{self.base_url}/detect/fraud",
                json=transaction2
            )
            print(f"Status Code: {response.status_code}")
            result = response.json()
            print(f"Is Fraud: {result['is_fraud']}")
            print(f"Risk Level: {result['risk_level']}")
            print(f"Risk Score: {result['combined_risk_score']:.4f}")
            print(f"Triggered Rules: {', '.join(result['triggered_rules'])}")
            print(f"Recommendation: {result['recommendation']}")
            print(f"Processing Time: {result['processing_time_ms']:.2f}ms")
        except Exception as e:
            print(f"Error: {e}")
    
    def test_batch_detection(self):
        """Test batch fraud detection"""
        print("\n" + "="*50)
        print("Testing Batch Fraud Detection")
        print("="*50)
        
        transactions = [
            {
                "Transaction_Amount": 30000,
                "Transaction_Date": "2024-01-15",
                "Transaction_Time": "10:00:00",
                "Transaction_Location": "Delhi",
                "Card_Type": "Visa",
                "Transaction_Currency": "INR",
                "Transaction_Status": "Completed",
                "Previous_Transaction_Count": 50,
                "Distance_Between_Transactions_km": 3.0,
                "Time_Since_Last_Transaction_min": 180,
                "Authentication_Method": "PIN",
                "Transaction_Velocity": 1,
                "Transaction_Category": "Groceries"
            },
            {
                "Transaction_Amount": 85000000,
                "Transaction_Date": "2024-01-15",
                "Transaction_Time": "23:45:00",
                "Transaction_Location": "International",
                "Card_Type": "Amex",
                "Transaction_Currency": "USD",
                "Transaction_Status": "Pending",
                "Previous_Transaction_Count": 5,
                "Distance_Between_Transactions_km": 1200.0,
                "Time_Since_Last_Transaction_min": 2,
                "Authentication_Method": "None",
                "Transaction_Velocity": 20,
                "Transaction_Category": "Unknown"
            }
        ]
        
        try:
            response = requests.post(
                f"{self.base_url}/detect/batch",
                json={"transactions": transactions}
            )
            print(f"Status Code: {response.status_code}")
            result = response.json()
            print(f"Total Transactions: {result['total_transactions']}")
            print(f"Fraud Detected: {result['fraud_detected']}")
            print(f"Processing Time: {result['processing_time_ms']:.2f}ms")
            
            print("\nIndividual Results:")
            for i, res in enumerate(result['results'], 1):
                print(f"\nTransaction {i}:")
                print(f"  Risk Level: {res['risk_level']}")
                print(f"  Risk Score: {res['combined_risk_score']:.4f}")
                print(f"  Is Fraud: {res['is_fraud']}")
        except Exception as e:
            print(f"Error: {e}")
    
    def test_metrics(self):
        """Test metrics endpoint"""
        print("\n" + "="*50)
        print("Testing Metrics Endpoint")
        print("="*50)
        
        try:
            response = requests.get(f"{self.base_url}/metrics")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"Error: {e}")
    
    def run_all_tests(self):
        """Run all API tests"""
        print("\n" + "="*70)
        print("FRAUD DETECTION API - COMPREHENSIVE TESTING")
        print("="*70)
        
        # Wait for server to be ready
        print("\nWaiting for server to be ready...")
        for i in range(5):
            try:
                response = requests.get(f"{self.base_url}/health", timeout=2)
                if response.status_code == 200:
                    print("✓ Server is ready!")
                    break
            except:
                print(f"  Attempt {i+1}/5...")
                time.sleep(2)
        
        # Run tests
        self.test_health()
        self.test_fraud_detection()
        self.test_batch_detection()
        self.test_metrics()
        
        print("\n" + "="*70)
        print("TESTING COMPLETED")
        print("="*70)


def main():
    """Main execution"""
    tester = APITester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
