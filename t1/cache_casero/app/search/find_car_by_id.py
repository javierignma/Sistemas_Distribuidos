import json

def find_car_by_id(target_id, file_path="./cars.json"):
    with open(file_path, 'r') as f:
        f.seek(0, 2)
        total_size = f.tell()
        
        low = 0
        high = total_size
        
        while low <= high:
            mid = (low + high) // 2
            f.seek(mid)
            
            while f.read(1) != "{":
                f.seek(f.tell() - 2)
                
            obj_str = "{"
            
            while True:
                char = f.read(1)
                obj_str += char
                if char == "}":
                    break
            
            obj = json.loads(obj_str)
            
            if obj["id"] == target_id:
                return obj
            elif obj["id"] < target_id:
                low = mid + 1
            else:
                high = mid - 1

    return None

'''
result = find_car_by_id(99)
if result:
    print(f"Car found: {result}")
else:
    print("Car not found")
'''