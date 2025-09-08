"""
Concurrency test utility for Advocate Diary application
"""
import threading
import time
import random
from models.database import get_connection

def simulate_concurrent_case_addition(num_users=5, cases_per_user=3):
    """
    Simulate multiple users adding cases concurrently
    """
    print(f"🧪 Starting concurrency test with {num_users} users, {cases_per_user} cases each")
    
    results = []
    threads = []
    
    def add_cases_for_user(user_id):
        """Add cases for a specific user"""
        user_results = []
        sheets_service = get_connection()
        
        for case_num in range(cases_per_user):
            try:
                # Simulate some processing time
                time.sleep(random.uniform(0.1, 0.5))
                
                case_data = {
                    "Case Number": f"TEST-{user_id}-{case_num}",
                    "Case Title": f"Test Case {user_id}-{case_num}",
                    "Case Type": "Civil",
                    "Location": "Test Location",
                    "Company Name": f"Test Company {user_id}",
                    "Upcoming Date": "2024-12-31",
                    "Stage": "Initial",
                    "Remarks": f"Test case from user {user_id}",
                    "Status": "Active",
                    "Claimant Advocate Name": f"Test Advocate {user_id}",
                    "Claimant Advocate Mobile Number": f"123456789{user_id}"
                }
                
                # Add the case
                result = sheets_service.add_case(case_data)
                user_results.append({
                    'user_id': user_id,
                    'case_num': case_num,
                    'success': result,
                    'case_number': case_data['Case Number']
                })
                
                print(f"👤 User {user_id}: Case {case_num} - {'✅ Success' if result else '❌ Failed'}")
                
            except Exception as e:
                print(f"❌ User {user_id}: Case {case_num} - Error: {e}")
                user_results.append({
                    'user_id': user_id,
                    'case_num': case_num,
                    'success': False,
                    'error': str(e)
                })
        
        results.extend(user_results)
    
    # Start all threads
    for user_id in range(num_users):
        thread = threading.Thread(target=add_cases_for_user, args=(user_id,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Analyze results
    print(f"\n📊 Concurrency Test Results:")
    print(f"Total operations: {len(results)}")
    print(f"Successful: {sum(1 for r in results if r.get('success', False))}")
    print(f"Failed: {sum(1 for r in results if not r.get('success', False))}")
    
    # Check for duplicate IDs
    sheets_service = get_connection()
    all_records = sheets_service._get_all_records()
    ids = [r.get('ID') for r in all_records if r.get('ID')]
    unique_ids = set(ids)
    
    print(f"\n🔍 ID Analysis:")
    print(f"Total records: {len(ids)}")
    print(f"Unique IDs: {len(unique_ids)}")
    print(f"Duplicate IDs: {len(ids) - len(unique_ids)}")
    
    if len(ids) != len(unique_ids):
        print("⚠️ WARNING: Duplicate IDs found!")
        duplicates = [id for id in ids if ids.count(id) > 1]
        print(f"Duplicate IDs: {set(duplicates)}")
    else:
        print("✅ No duplicate IDs found - concurrency handling working correctly!")
    
    return results

def test_concurrent_updates():
    """
    Test concurrent updates to the same record
    """
    print(f"\n🧪 Testing concurrent updates...")
    
    sheets_service = get_connection()
    
    # First, add a test case
    test_case = {
        "Case Number": "UPDATE-TEST-001",
        "Case Title": "Concurrent Update Test",
        "Case Type": "Civil",
        "Location": "Test Location",
        "Company Name": "Test Company",
        "Upcoming Date": "2024-12-31",
        "Stage": "Initial",
        "Remarks": "Test case for concurrent updates",
        "Status": "Active",
        "Claimant Advocate Name": "Test Advocate",
        "Claimant Advocate Mobile Number": "1234567890"
    }
    
    # Add the test case
    result = sheets_service.add_case(test_case)
    if not result:
        print("❌ Failed to add test case for update test")
        return
    
    # Get the case ID
    records = sheets_service._get_all_records()
    test_record = next((r for r in records if r.get('Case Number') == 'UPDATE-TEST-001'), None)
    if not test_record:
        print("❌ Test case not found after creation")
        return
    
    case_id = test_record['ID']
    print(f"✅ Test case created with ID: {case_id}")
    
    # Now test concurrent updates
    update_results = []
    threads = []
    
    def update_case_worker(worker_id):
        """Worker function for concurrent updates"""
        try:
            time.sleep(random.uniform(0.1, 0.3))  # Random delay
            
            update_data = {
                "Case Title": f"Updated by Worker {worker_id}",
                "Remarks": f"Updated at {time.time()} by worker {worker_id}",
                "Status": f"Status-{worker_id}"
            }
            
            result = sheets_service.update_case(case_id, update_data)
            update_results.append({
                'worker_id': worker_id,
                'success': result,
                'timestamp': time.time()
            })
            
            print(f"👷 Worker {worker_id}: Update {'✅ Success' if result else '❌ Failed'}")
            
        except Exception as e:
            print(f"❌ Worker {worker_id}: Error - {e}")
            update_results.append({
                'worker_id': worker_id,
                'success': False,
                'error': str(e)
            })
    
    # Start multiple update threads
    for worker_id in range(5):
        thread = threading.Thread(target=update_case_worker, args=(worker_id,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads
    for thread in threads:
        thread.join()
    
    # Check final state
    final_records = sheets_service._get_all_records()
    final_record = next((r for r in final_records if r.get('ID') == case_id), None)
    
    print(f"\n📊 Update Test Results:")
    print(f"Total update attempts: {len(update_results)}")
    print(f"Successful updates: {sum(1 for r in update_results if r.get('success', False))}")
    print(f"Final record state: {final_record}")

if __name__ == "__main__":
    print("🚀 Starting Advocate Diary Concurrency Tests")
    print("=" * 50)
    
    # Test concurrent additions
    addition_results = simulate_concurrent_case_addition(num_users=3, cases_per_user=2)
    
    # Test concurrent updates
    test_concurrent_updates()
    
    print("\n✅ Concurrency tests completed!")
