import os, random, psycopg2
from faker import Faker


class FakerDataGenerator:
    def __init__(self, db_uri, num_records):
        self.db_uri = db_uri
        self.num_records = num_records
        self.fake = Faker()

    def run(self):
        conn = psycopg2.connect(self.db_uri)
        cursor = conn.cursor()
        for _ in range(self.total):
            cur.execute("""
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
                random.uniform(0, 120)
            ))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Inserted {self.num_records} fake traffic records into the database.")

if __name__ == "__main__":
    db_uri = os.getenv('NEONDB_URI')
    num_records = random.randint(1, 1000)  # Random number of records between 1 to 1000
    generator = FakerDataGenerator(db_uri, num_records)
    generator.run()