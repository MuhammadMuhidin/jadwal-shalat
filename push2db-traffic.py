import os, random, psycopg2
from faker import Faker

class TrafficDataGenerator:
    def __init__(self):
        self.db = os.getenv('NEONDB_URI')
        self.num_records = random.randint(1, 25) # Random number of records to insert
        self.fake = Faker()

    def insert_fake_data(self):
        try:
            conn = psycopg2.connect(self.db)
            cursor = conn.cursor()

            for _ in range(self.num_records):
                cursor.execute("""
                    INSERT INTO realtime_traffic_sensor (
                        sensor_id, location, plate_number, latitude, longitude, traffic_flow, speed_avg
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    self.fake.uuid4(),
                    self.fake.address(),
                    self.fake.license_plate(),
                    float(self.fake.latitude()),
                    float(self.fake.longitude()),
                    random.randint(0, 100),
                    random.randint(0, 120)
                ))

            conn.commit()
            cursor.close()
            conn.close()
            print(f"✅ Inserted {self.num_records} fake traffic records.")
        
        except Exception as e:
            print(f"❌ Error inserting data: {e}")

if __name__ == '__main__':
    generator = TrafficDataGenerator()
    generator.insert_fake_data()
